#app.py
from flask import Flask, request, jsonify
from flask_expects_json import expects_json

#This module is for the schedule task runing in backgroud
from apscheduler.schedulers.background import BackgroundScheduler
from flask_sqlalchemy import SQLAlchemy
from config import configParser
import logging

#Configuring the logging

logging.basicConfig(filename=configParser.get('Logging','log_file'),
                level=logging.getLevelName(configParser.get('Logging','log_level')), format=configParser.get('Logging','log_format'))

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
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{configParser.get('Database','db_location')}"

#Initialize the database
db = SQLAlchemy(app)

#Create db model for Country
class Country(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256), nullable=False)
    capital = db.Column(db.String(256), nullable=False)
    area = db.Column(db.Integer)

    #Function to return a string when we add a country
    def __repr__(self):
        return "{0} with {1} mk2".format(self.name, self.area)

def initializeDBData():
    app.logger.info("Adding test data to database")
    thailand = Country(name="Thailand", capital = "Bangkok", area = 513120)
    australia = Country(name="Australia", capital = "Canberra", area = 7617930)
    egypt = Country(name="Egypt", capital = "Cairo", area = 1010408)
    cuba = Country(name="Cuba", capital ="Habana", area = 110860)
    for country in (thailand, australia, egypt, cuba):
        db.session.add(country) 
    db.session.commit()

    app.logger.info("Test data added successfully to the database")

initializeDBData()

def biggest_area():
    """Query the database to get the country with the biggest area

    Logs the country found in the database
    """
    biggest_country =  db.session.query(Country).order_by(Country.area.desc()).first() 
    msg= f"The country with the biggest area in the collection is {biggest_country}"
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

#Defining the Country schema used by expects_json decorator to validate the data posted to /countries
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
        #country["id"] = _find_next_id()
        #countries.append(country)
        new_country=Country(name=country["name"], capital=country["capital"], area=country["area"])
        #Push to database
        try:
            db.session.add(new_country)
            db.session.commit()
            app.logger.info("Added new country {0} succesfully".format(country))
            return country, 201
        except:
            app.logger.info("There was an error adding {0}".format(country))
            return {"error": "Error while adding country"}, 500
    return {"error": "Request must be JSON"}, 415
