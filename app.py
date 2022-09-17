#app.py
from distutils.command.config import config
from flask import Flask, request, jsonify
from flask_expects_json import expects_json
from models import Country, db
from config import configParser, configScheduler


#Initialize the app

def create_app():
    app = Flask(__name__)
    db.init_app(app)
    return app

#app = Flask(__name__)
app = create_app()

app.config['SQLALCHEMY_DATABASE_URI'] = configParser.get('Database','db_connection')
db.init_app(app)

def biggest_area(logger):
    """Query the database to get the country with the biggest area
    Logs the country found in the database
    Return: None
    """
    try:
        with app.app_context():
            biggest_country =  db.session.query(Country).order_by(Country.area.desc()).first() 
            msg= f"The country with the biggest area in the collection is {biggest_country}"
    except Exception as e:
        msg = f"An exception was thrown querying the database. The error was: {e}"
    logger.info(msg)


configScheduler(biggest_area,[app.logger],1)
#initializeDBData(app.logger)

@app.get("/countries")
def get_countries():
    countries = db.session.query(Country).all()
    return jsonify(jsonlist =[c.serialize for c in countries])

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
