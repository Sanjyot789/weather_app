from flask import Flask, render_template, request
import requests
import json

app = Flask(__name__)

# Get your API key from https://developer.accuweather.com/
api_key = "dV677UnRDLJWF7CpY4mcjpUXn7PKzQgV"

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        location = request.form['location']

        # Retrieve weather data for the selected location
        weather_data = get_weather_data(location)

        if weather_data:
            return render_template('index.html', weather_data=weather_data)
        else:
            error_message = "Failed to retrieve weather data."
            return render_template('index.html', error_message=error_message)

    return render_template('index.html')




# ... existing code ...

def get_weather_data(location):
    # Get the location key
    location_key = get_location_key(location)

    if location_key:
        # Make a GET request to the AccuWeather API
        url = f"http://dataservice.accuweather.com/currentconditions/v1/{location_key}?apikey={api_key}"
        response = requests.get(url)
        data = json.loads(response.text)

        # Extract the relevant weather information
        weather_text = data[0]['WeatherText']
        temperature = data[0]['Temperature']['Metric']['Value']

        # Create the AccuWeather URL
        accuweather_url = f"https://www.accuweather.com/en/in/{location_key}/current-weather/{location_key}"

        weather_data = {
            'location': location,
            'weather_text': weather_text,
            'temperature': temperature,
            'accuweather_url': accuweather_url
        }

        # Save the weather data to a JSON file
        save_weather_data(weather_data)

        return weather_data

    return None

def save_weather_data(weather_data):
    with open('weather_data.json', 'w') as file:
        json.dump(weather_data, file)

# ... remaining code ...



def get_location_key(location):
    url = f"http://dataservice.accuweather.com/locations/v1/search?q={location}&apikey={api_key}"
    response = requests.get(url)
    data = json.loads(response.text)

    if data:
        if len(data) > 0:
            location_key = data[0]['Key']
            return location_key

    return None

if __name__ == '__main__':
    app.run(debug=True)
