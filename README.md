# Weather API Documentation

This Flask app provides various endpoints for weather-related operations.

## 1. Get Weather by City Name
Endpoint: /get_weather_by_name  
Method: GET  
Parameters:  
city (required): The name of the city.
Description: This endpoint retrieves current weather information based on the provided city name.

Example Request:

```bash
GET /get_weather_by_name?city=Berlin
```

Example Response:
```json
{
  "city": "Berlin",
  "latitude": 52.5200,
  "longitude": 13.4050,
  "temperature": 31.3,
  "humidity": 56,
  "windspeed": 3.2,
  "winddirection": 240
}
```

**How to Run**
To run the Flask app, use the following command:

```bash
python weatherAPI.py
```
The app will be accessible at http://localhost:8000/.

**CORS**  
Cross-Origin Resource Sharing (CORS) is enabled for the entire app to allow requests from different origins. This ensures that frontend applications can make requests to this API.

**Dependencies**  
Flask: Used for creating the API.  
Geopy: Used for geocoding and reverse geocoding.  
Requests: Used for making HTTP requests to external APIs.  
Flask-CORS: Used to enable CORS.  

**Author**  
This Flask app was created by Gaurav Aryal.

**License**  
This app is open-source and available under the MIT license.