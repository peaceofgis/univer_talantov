from flask import Flask, render_template, url_for, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.models import CarBrand, CarModel, CarAdv
import config

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
            data = [{"name": cm.name, "id": cm.id} for cm in session.query(CarModel).filter(CarModel.name.like('%' + brand + '%')).all()]
        except Exception:
            return jsonify({"status": "error", "message": "Something goes wrong"}), 500
    session.close()
    return jsonify(data), 200


if __name__ == "__main__":
    app.run()
