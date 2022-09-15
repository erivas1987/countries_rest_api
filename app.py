#app.py
from flask import Flask, request, jsonify
from flask_expects_json import expects_json
#This module is for the schedule task runing in backgroud
from apscheduler.schedulers.background import BackgroundScheduler
from flask_sqlalchemy import SQLAlchemy

import logging
#Configuring the logging
logging.basicConfig(filename='record.log',
                level=logging.DEBUG, format='%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')

"""
Collection of test data in memory
"""
countries = [
    {"id": 1, "name": "Thailand", "capital": "Bangkok", "area": 513120},
    {"id": 2, "name": "Australia", "capital": "Canberra", "area": 7617930},
    {"id": 3, "name": "Egypt", "capital": "Cairo", "area": 1010408},
    {"id": 4, "name": "Cuba", "capital": "Habana", "area": 110860 },
]

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///countries.db'

#Initialize the database
db = SQLAlchemy(app)

#Create db model
class Country(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256), nullable=False)
    capital = db.Column(db.String(256), nullable=False)
    area = db.Column(db.Integer)

#Create function to return a string when we add a country
def __repr__(self):
    return "{0}".format(self.name)




def biggest_area():
    country_biggest_area_pos = 0
    for pos in range(1,len(countries)):
        if countries[pos]["area"] > countries[country_biggest_area_pos]["area"]:
            country_biggest_area_pos = pos
    msg= "The country with the biggest area in the collection is {0} with {1} km2".\
    format(countries[country_biggest_area_pos]["name"], countries[country_biggest_area_pos]["area"] )
    app.logger.info(msg)

scheduler = BackgroundScheduler()
job = scheduler.add_job(biggest_area, 'interval', seconds=10)
scheduler.start()

def _find_next_id():
    """_summary_
        Finds the next id for assings to a newly created country
        Search the max used id in the countries list and add one
    Returns:
        int: A unique Id in the set of countries 
    """
    return max(country["id"] for country in countries) + 1

@app.get("/countries")
def get_countries():
    return jsonify(countries)

schema = {
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://example.com/product.schema.json",
  "title": "Country",
  "description": "A country",
   "type": "object",
    "properties": {
        "name": {"description": "The name of the country", "type": "string"},
        "capital": {"description": "The name of the country capital","type": "string"},
        "area": {"description": "The  country surface area in square kilometers", "type": "integer"}
    },
     "required": [ "name", "capital" ]
}

@app.post("/countries")
@expects_json(schema)
def add_country():
    if request.is_json:
        country = request.get_json()
        country["id"] = _find_next_id()
        countries.append(country)
        app.logger.info("Added new country {0} succesfully".format(country))
        return country, 201
    return {"error": "Request must be JSON"}, 415
