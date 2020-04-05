import requests
import numpy

response = requests.get("https://covidtracking.com/api/states/daily?state=NY&date=20200316")
print(response.status_code)
print(response.json())