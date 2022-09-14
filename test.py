import requests

api_url = "http://127.0.0.1:5000/countries"
country={"name":"Germany", "capital": "Berlin", "area": 357022}
response = requests.post(api_url, json=country)


