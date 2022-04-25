from pip._vendor import requests
import os
from datetime import datetime
from logo import logo
from dotenv import load_dotenv
load_dotenv()

ENDPOINT = "https://trackapi.nutritionix.com/v2/natural/exercise"

HEADERS = {
    "x-app-id": os.environ.get('APP_ID'),
    "x-app-key": os.environ.get('API_KEY'),
}

print(logo)
exercise_info = input("What exercise(s) did you complete: ")

PARAMETERS = {
    "query": exercise_info,
    "gender": os.environ.get('GENDER'),
    "weight_kg": os.environ.get('WEIGHT_KG'),
    "height_cm": os.environ.get('HEIGHT_CM'),
    "age": os.environ.get('AGE')
}

response = requests.post(ENDPOINT, json=PARAMETERS, headers=HEADERS)
exercise_data = response.json()

# Get the current date and time
current_datetime = datetime.now()
date = current_datetime.strftime("%x")
time = current_datetime.strftime("%X")

SHEETY_ENDPOINT = os.environ.get('SHEETY_ENDPOINT')

SHEETY_HEADERS = {
    "Authorization": os.environ.get('SHEETY_AUTH')
}

# Add the data into google sheets using sheety api endpoint
for exercise in exercise_data['exercise']:
    sheety_inputs = {
        "workout": {
            "date": date,
            "time": time,
            "exercise": exercise["name"].title(),
            "duration": exercise["duration_min"],
            "calories": exercise["nf_calories"]
        }
    }

    sheety_response = requests.post(SHEETY_ENDPOINT, json=sheety_inputs, headers=SHEETY_HEADERS)

    print(sheety_response.text)

