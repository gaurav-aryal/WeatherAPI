from flask import Flask, request, jsonify
from geopy.geocoders import Nominatim
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)  # Enable CORS for your entire app

# Create an instance of the Nominatim geocoder
geolocator = Nominatim(user_agent="geoapiExercises")


def _extract_current_humidity(api_data):
    """Return humidity value matching current weather time if available."""
    hourly = api_data.get("hourly", {})
    times = hourly.get("time", [])
    humidity_values = hourly.get("relativehumidity_2m", [])
    current_time = api_data.get("current_weather", {}).get("time")
    if current_time and current_time in times:
        idx = times.index(current_time)
        if idx < len(humidity_values):
            return humidity_values[idx]
    return None

@app.route('/weather', methods=['GET'])
def get_weather():
    # Get latitude and longitude from query parameters
    latitude = request.args.get('latitude')
    longitude = request.args.get('longitude')

    if not latitude or not longitude:
        return jsonify({'error': 'Latitude and longitude parameters are required.'}), 400

    # Define the URL for the weather API
    url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current_weather=true&hourly=temperature_2m,relativehumidity_2m,windspeed_10m"

    # Make a GET request to the weather API
    response = requests.get(url)

    if response.status_code == 200:
        # Parse the JSON response
        data = response.json()
        current_weather = data.get('current_weather', {})

        # Extract weather data
        temperature = current_weather.get('temperature')
        windspeed = current_weather.get('windspeed')
        winddirection = current_weather.get('winddirection')
        humidity = _extract_current_humidity(data)

        weather_data = {
            'latitude': latitude,
            'longitude': longitude,
            'temperature': temperature,
            'humidity': humidity,
            'windspeed': windspeed,
            'winddirection': winddirection
        }

        return jsonify(weather_data), 200
    else:
        return jsonify({'error': 'Unable to fetch weather data.'}), 500
    

@app.route('/reverse_geocode', methods=['GET'])
def reverse_geocode():
    # Get latitude and longitude from query parameters
    latitude = request.args.get('latitude')
    longitude = request.args.get('longitude')

    if not latitude or not longitude:
        return jsonify({'error': 'Latitude and longitude parameters are required.'}), 400

    try:
        # Initialize the geolocator
        geolocator = Nominatim(user_agent="reverse_geocoding_api")

        # Perform reverse geocoding
        location = geolocator.reverse((latitude, longitude), exactly_one=True)

        if location:
            location_data = {
                'latitude': latitude,
                'longitude': longitude,
                'address': location.address
            }
            return jsonify(location_data), 200
        else:
            return jsonify({'error': 'Location not found.'}), 404
    except Exception as e:
        return jsonify({'error': f'An error occurred: {str(e)}'}), 500
    

@app.route('/get_coordinates', methods=['GET'])
def get_coordinates():
    city = request.args.get('city')

    if not city:
        return jsonify({'error': 'City parameter is missing.'}), 400

    # Find the latitude and longitude of the provided city
    location = geolocator.geocode(city)

    if location:
        latitude = location.latitude
        longitude = location.longitude
        response = {
            'city': city,
            'latitude': latitude,
            'longitude': longitude
        }
        return jsonify(response), 200
    else:
        return jsonify({'error': 'Location not found.'}), 404


@app.route('/get_weather_by_name', methods=['GET'])
def get_weather_by_name():
    city = request.args.get('city')

    if not city:
        return jsonify({'error': 'City parameter is missing.'}), 400

    # Find the latitude and longitude of the provided city
    location = geolocator.geocode(city)

    if location:
        latitude = location.latitude
        longitude = location.longitude
    else:
        return jsonify({'error': 'Location not found.'}), 404

    # Define the URL for the weather API
    url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current_weather=true&hourly=temperature_2m,relativehumidity_2m,windspeed_10m"

    # Make a GET request to the weather API
    response = requests.get(url)

    if response.status_code == 200:
        # Parse the JSON response
        data = response.json()
        current_weather = data.get('current_weather', {})

        # Extract weather data
        temperature = current_weather.get('temperature')
        windspeed = current_weather.get('windspeed')
        winddirection = current_weather.get('winddirection')
        humidity = _extract_current_humidity(data)

        weather_data = {
            'city': city,
            'latitude': latitude,
            'longitude': longitude,
            'temperature': temperature,
            'humidity': humidity,
            'windspeed': windspeed,
            'winddirection': winddirection
        }

        return jsonify(weather_data), 200
    else:
        return jsonify({'error': 'Unable to fetch weather data.'}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
