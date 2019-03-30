from datetime import datetime
import re
import requests
import sqlalchemy as sa
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.models import CarBrand, CarModel, CarAdv, init_database
import config

try:
    from BeautifulSoup import BeautifulSoup
except ImportError:
    from bs4 import BeautifulSoup

engine = create_engine(config.DevelopmentConfig.SQLALCHEMY_DATABASE_URI, echo=False)
Session = sessionmaker(bind=engine)
session = Session()

if len(sa.inspect(engine).get_table_names()) < 1:
    init_database(engine)

url = "https://kazan.drom.ru/auto/"

headers = {
    'Referer': 'https://kazan.drom.ru/auto/',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.75 Safari/537.36'
}

brands_page = requests.get(url, headers=headers)

parsed_brands_page = BeautifulSoup(brands_page.text, features="lxml")
brands_mark_cols = parsed_brands_page.body.find_all('div', attrs={'class': 'b-selectCars__col'})

for brands_col in brands_mark_cols:
    for brand in brands_col.find_all('a'):
        brand_link = brand.get('href')
        brand_name = brand.text
        print(brand_name)
        new_brand = session.query(CarBrand).filter_by(name=brand_name).first()

        if not new_brand:
            new_brand = CarBrand(name=brand_name, dromru_url=brand_link)
            session.add(new_brand)
            session.commit()
            print("Add new brand {0} at {1}".format(brand_name, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
            session.refresh(new_brand)

        brand_page = requests.get(brand_link, headers=headers)
        parsed_brand_page = BeautifulSoup(brand_page.text, features="lxml")

        models_mark_cols = parsed_brand_page.body.find_all('div', attrs={'class': 'b-selectCars__col'})

        for models_col in models_mark_cols:
            for model in models_col.find_all('a'):
                model_link = model.get('href')
                model_name = model.text
                print(model_name)
                new_model = session.query(CarModel).filter_by(name=model_name).first()

                if not new_model:
                    new_model = CarModel(name=model_name, brand_id=new_brand.id, dromru_url=model_link)
                    session.add(new_model)
                    session.commit()
                    print("Add new model {0} at {1}".format(model_name, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
                    session.refresh(new_model)

                #sleep(random.randint(3, 8))

                model_page = requests.get(model_link, headers=headers)
                parsed_model_page = BeautifulSoup(model_page.text, features="lxml")
                advs = parsed_model_page.body.find_all('a', attrs={'class': 'b-advItem'})

                for adv in advs:
                    car_name, car_year = adv.find('div', attrs={'class': 'b-advItem__section_type_main'}).div.text.split(',')
                    car_fueltype_parsed = adv.find_all('div', attrs={'data-ftid': 'sales__bulls-item_fueltype'})
                    car_transmission_parsed = adv.find_all('div', attrs={'data-ftid': 'sales__bulls-item_transmission'})
                    car_privod_parsed = adv.find_all('div', attrs={'data-ftid': 'sales__bulls-item_privod'})
                    car_mileage_parsed = adv.find_all('div', attrs={'data-ftid': 'sales__bulls-item_mileage'})

                    car_price_parsed = adv.find_all('div', attrs={'data-ftid': 'sales__bulls-item_price'})

                    if len(car_fueltype_parsed) < 1:
                        car_fueltype = ""
                    else:
                        car_fueltype = car_fueltype_parsed[0].text

                    if len(car_transmission_parsed) < 1:
                        car_transmission = ""
                    else:
                        car_transmission = car_transmission_parsed[0].text

                    if len(car_privod_parsed) < 1:
                        car_privod = ""
                    else:
                        car_privod = car_privod_parsed[0].text

                    if len(car_mileage_parsed) < 1:
                        car_mileage = ""
                    else:
                        car_mileage_tmp = re.findall('\d+', car_mileage_parsed[0].text)
                        if len(car_mileage_tmp) < 1:
                            car_mileage = ""
                        else:
                            car_mileage = car_mileage_tmp[0]

                    if len(car_price_parsed) < 1:
                        car_price = 0
                    else:
                        car_price_tmp = car_price_parsed[0].text
                        car_price_tmp_re = re.findall('\d+', car_price_tmp)
                        if len(car_price_tmp_re) == 3:
                            car_price = int(car_price_tmp_re[0]) * 1000000 + int(car_price_tmp_re[1]) * 1000 + int(car_price_tmp_re[2])
                        elif len(car_price_tmp_re) == 2:
                            car_price = int(car_price_tmp_re[0]) * 1000 + int(car_price_tmp_re[1])
                        elif len(car_price_tmp_re) == 1:
                            car_price = int(car_price_tmp_re[0]) * 1000

                    adv_link = adv.get('href')

                    new_car = session.query(CarAdv).filter_by(dromru_url=adv_link).first()
                    if not new_car:
                        new_car = CarAdv(brand_id=new_brand.id,
                                         model_id=new_model.id,
                                         year=car_year,
                                         name=car_name,
                                         mileage=car_mileage,
                                         transmission=car_transmission,
                                         fueltype=car_fueltype,
                                         privod=car_privod,
                                         dromru_url=adv_link,
                                         dromru_price=car_price
                                         )

                        session.add(new_car)
                        session.commit()
                        print("Add new car adv {0} at {1}".format(car_name, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))

session.close_all()
