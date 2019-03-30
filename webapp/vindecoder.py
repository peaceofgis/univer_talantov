import requests
import os

from models.models import CarBrand, CarModel


class VinDecoder():
    def __init__(self, session):
        self.session = session
    def findByVin(self, vincode):
        if len(vincode) < 10:
           data = {"brand_id": 8, "model_id": 285, "year": 2015}
        else:
            r = requests.get("http://api.carmd.com/v3.0/decode?vin=" + vincode, headers={
                "partner-token": os.environ.get('carmd_token'),
                "Authorization": os.environ.get('carmd_auth')
            })
            d = r.json()["data"]
            brand = self.session.query(CarBrand).filter(CarBrand.name.like('%' + d["make"] + '%')).first()
            model = self.session.query(CarModel).filter(CarModel.name.like('%' + d["model"] + '%')).first()
            year = d["year"]
            data = {"brand_id": brand.id, "model_id": model.id, "year": year}
        return data