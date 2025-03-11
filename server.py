import requests
import json
from flask import Flask, jsonify, request

app = Flask(__name__)

def get_weather(lat, long):
    url = f"https://api.open-meteo.com/v1/forecast"
    response = requests.get(url, params={
        "latitude": lat,
        "longitude": long,
        "current": "temperature_2m,wind_speed_10m",
        "hourly": "temperature_2m,relative_humidity_2m,wind_speed_10m",
    })
    json_response = response.json()
    celsius_temp = json_response['current']['temperature_2m']
    kmh_wind_speed = json_response['current']['wind_speed_10m']
    fahrenheit_temp = 1.8 * celsius_temp + 32
    mph_wind_speed = 0.621371 * kmh_wind_speed
    return {"temperature": {"units": "fahrenheit", "value": fahrenheit_temp}, "wind_speed": {"units": "miles/hour", "value": mph_wind_speed}}

@app.route("/weather", methods=["GET"])
def weather():
    latitude = request.args.get("lat")
    longitude = request.args.get("long")
    return jsonify(get_weather(latitude, longitude))

if __name__ == "__main__":
    print(get_weather("39.768192", "-94.848167"))
    app.run(debug=True, port=4002)
