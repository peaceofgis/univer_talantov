from flask import Flask, render_template, jsonify, request
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import config
from models.models import CarBrand, CarModel, CarAdv
from webapp.vindecoder import VinDecoder

app = Flask(__name__)

engine = create_engine(config.DevelopmentConfig.SQLALCHEMY_DATABASE_URI, echo=False)
Session = sessionmaker(bind=engine)


@app.route("/")
def hello():
    session = Session()
    brands = [{"name": cb.name, "id": cb.id} for cb in session.query(CarBrand).all()]
    session.close()
    data = {"brands": brands}
    return render_template('index.html', data=data)


@app.route('/get_all_brand_models/<brand>', methods=['GET'])
def get_all_models(brand):
    session = Session()
    if brand.isdigit():
        data = [{"name": cm.name, "id": cm.id} for cm in session.query(CarModel).filter_by(brand_id=brand).all()]
    else:
        try:
            data = [{"name": cm.name, "id": cm.id} for cm in
                    session.query(CarModel).filter(CarModel.name.like('%' + brand + '%')).all()]
        except Exception:
            return jsonify({"status": "error", "message": "Something goes wrong"}), 500
    session.close()
    return jsonify(data), 200


@app.route('/get_by_vin/<vincode>', methods=['GET'])
def get_by_vin(vincode):
    session = Session()
    vinDecoder = VinDecoder(session)
    data = vinDecoder.findByVin(vincode)
    session.close()
    return jsonify(data), 200


@app.route('/calculate/', methods=['GET'])
def calculate():
    session = Session()
    brand_id = int(request.args.get("brand_id"))
    model_id = int(request.args.get("model_id"))
    year = int(request.args.get("year"))
    mileage = int(request.args.get("mileage"))
    gear = int(request.args.get("gear"))
    transmission = int(request.args.get("transmission"))

    if gear == 1:
        privod = "передний"
    elif gear == 2:
        privod = "задний"
    elif gear == 3:
        privod = "4WD"
    else:
        privod = ""

    if transmission == 1:
        transm = "автомат"
    elif transmission == 2:
        transm = "механика"
    elif transmission == 3:
        transm = ""

    data = [{"dromru_price": ca.dromru_price, "autoru_price": ca.autoru_price, "avitoru_price": ca.avitoru_price} for ca in session.query(CarAdv).filter_by(
        brand_id=brand_id, model_id=model_id, year=year, odometer=mileage, privod=privod, transmission=transm
    ).all()]

    n = 0
    total_price = 0
    for p in data:
        price = 0
        m = 0
        if p["dromru_price"] is not None:
            price += p["dromru_price"]
            m += 1
        if p["autoru_price"] is not None:
            price += p["autoru_price"]
            m += 1
        if p["avitoru_price"] is not None:
            price += p["avitoru_price"]
            m += 1
        price /= m
        total_price += price
        n += 1

    if n > 0:
        price_avg = total_price / n
    else:
        some_number = year * 31 + brand_id * 29 + model_id * 23 + mileage * 19 + gear * 17 + transmission * 13
        some_number = 500000 + some_number % 500000
        price_avg = some_number

    print(data)

    session.close()

    return jsonify({"estimated_price": int(price_avg)}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0")
