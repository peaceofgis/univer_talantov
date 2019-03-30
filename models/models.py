from datetime import datetime

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class CarBrand(Base):
    __tablename__ = 'car_brands'
    id = Column(Integer, primary_key=True, unique=True)
    name = Column(String)
    dromru_url = Column(String)
    autoru_url = Column(String)
    avitoru_url = Column(String)

    def __init__(self, name, dromru_url=None, autoru_url=None, avitoru_url=None):
        self.name = name
        if dromru_url is not None:
            self.dromru_url = dromru_url
        else:
            self.dromru_url = ""
        if autoru_url is not None:
            self.autoru_url = autoru_url
        else:
            self.autoru_url = ""
        if avitoru_url is not None:
            self.avitoru_url = avitoru_url
        else:
            self.avitoru_url = ""

    def __repr__(self):
        return "<CarBrand('%s')>" % (self.name,)


class CarModel(Base):
    __tablename__ = 'car_models'
    id = Column(Integer, primary_key=True, unique=True)
    brand_id = Column(Integer, ForeignKey("car_brands.id"), nullable=False)
    name = Column(String)
    dromru_url = Column(String)
    autoru_url = Column(String)
    avitoru_url = Column(String)

    def __init__(self, name, brand_id, dromru_url=None, autoru_url=None, avitoru_url=None):
        self.name = name
        self.brand_id = brand_id
        if dromru_url is not None:
            self.dromru_url = dromru_url
        else:
            self.dromru_url = ""
        if autoru_url is not None:
            self.autoru_url = autoru_url
        else:
            self.autoru_url = ""
        if avitoru_url is not None:
            self.avitoru_url = avitoru_url
        else:
            self.avitoru_url = ""

    def __repr__(self):
        return "<CarModel('%s')>" % (self.name, )


class CarAdv(Base):
    __tablename__ = 'car_advs'
    id = Column(Integer, primary_key=True, unique=True)
    brand_id = Column(Integer, ForeignKey("car_brands.id"), nullable=False)
    model_id = Column(Integer, ForeignKey("car_models.id"), nullable=False)
    name = Column(String)
    year = Column(Integer)
    odometer = Column(Integer)
    fueltype = Column(String)
    transmission = Column(String)
    privod = Column(String)
    dromru_url = Column(String)
    dromru_price = Column(Integer)
    autoru_url = Column(String)
    autoru_price = Column(Integer)
    avitoru_url = Column(String)
    avitoru_price = Column(Integer)
    created = Column(DateTime(), default=datetime.utcnow)
    updated = Column(DateTime(), default=datetime.utcnow)

    def __init__(self, name, brand_id, model_id, year, fueltype, transmission, mileage, privod,  dromru_url=None, dromru_price=None,autoru_url=None, autoru_price=None, avitoru_url=None, avitoru_pricee=None):
        self.name = name
        self.brand_id = brand_id
        self.model_id = model_id
        self.year = year
        self.fueltype = fueltype
        self.transmission = transmission
        self.odometer = mileage
        self.privod = privod
        if dromru_url is not None:
            self.dromru_url = dromru_url
        else:
            self.dromru_url = ""
        if dromru_price is not None:
            self.dromru_price = dromru_price
        if autoru_url is not None:
            self.autoru_url = autoru_url
        else:
            self.autoru_url = ""
        if autoru_price is not None:
            self.autoru_price = autoru_price
        if avitoru_url is not None:
            self.avitoru_url = avitoru_url
        else:
            self.avitoru_url = ""
        if avitoru_pricee is not None:
            self.avitoru_price = avitoru_pricee

    def __repr__(self):
        return "<CarAdv('%s')>" % (self.name, )


def init_database(engine):
    Base.metadata.create_all(engine)
