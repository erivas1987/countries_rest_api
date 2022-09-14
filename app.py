#app.py
from flask import Flask, request, jsonify
from flask_expects_json import expects_json
#This module is for the schedule task runing in backgroud
from apscheduler.schedulers.background import BackgroundScheduler
import logging

#Configuring the logging
logging.basicConfig(filename='used_ids.log', level=logging.DEBUG, format=f'%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')

app = Flask(__name__)

"""
Collection of data in memory
"""
countries = [
    {"id": 1, "name": "Thailand", "capital": "Bangkok", "area": 513120},
    {"id": 2, "name": "Australia", "capital": "Canberra", "area": 7617930},
    {"id": 3, "name": "Egypt", "capital": "Cairo", "area": 1010408},
    {"id": 4, "name": "Cuba", "capital": "Habana", "area": 110860 },
]

def _find_next_id():
    return max(country["id"] for country in countries) + 1

@app.get("/countries")
def get_countries():
    return jsonify(countries)

schema = {
    'type': 'object',
    'properties': {
        'name': {'type': 'string'},
        'capital': {'type': 'string'},
        'area': {'type': 'int'}
    },
}

@app.post("/countries")
def add_country():
    if request.is_json:
        country = request.get_json()
        country["id"] = _find_next_id()
        countries.append(country)
        return country, 201
    return {"error": "Request must be JSON"}, 415

def biggest_area():
    country_biggest_area_pos = 0
    for pos in range(1,len(countries)-1):
        if countries[pos]["area"] > countries[country_biggest_area_pos]["area"]:
            country_biggest_area_pos = pos
    print("The country with the biggest area in the collection is {0} with {1} km2".format(countries[country_biggest_area_pos]["name"], countries[country_biggest_area_pos]["area"] ))
    app.logger.info("The country with the biggest area in the collection is {0} with {1} km2".\
    format(countries[country_biggest_area_pos]["name"], countries[country_biggest_area_pos]["area"] ))


if __name__ == '__main__':
    #app.debug = False

    #applogger = app.logger

    #file_handler = logging.FileHandler("error.log")
    #file_handler.setLevel(logging.DEBUG)

    #applogger.setLevel(logging.DEBUG)
    #applogger.addHandler(file_handler)

    scheduler = BackgroundScheduler()
    job = scheduler.add_job(biggest_area, 'interval', minutes=1)
    scheduler.start()

    app.run(host='127.0.0.0', port="5000")




