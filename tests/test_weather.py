import json
import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from unittest.mock import patch, MagicMock
from weatherAPI import app


def test_get_weather_by_name_missing_city_returns_400():
    client = app.test_client()
    response = client.get('/get_weather_by_name')
    assert response.status_code == 400
    data = response.get_json()
    assert data['error']


def test_get_weather_by_name_success_with_mocking():
    with patch('weatherAPI.geolocator.geocode') as geocode_mock, \
         patch('weatherAPI.requests.get') as requests_get:
        geocode_mock.return_value = MagicMock(latitude=52.52, longitude=13.405)
        mock_resp = MagicMock(status_code=200)
        mock_resp.json.return_value = {
            'current_weather': {
                'temperature': 20,
                'humidity': 60,
                'windspeed': 5,
                'winddirection': 90
            }
        }
        requests_get.return_value = mock_resp

        client = app.test_client()
        response = client.get('/get_weather_by_name?city=Berlin')
        assert response.status_code == 200
        data = response.get_json()
        assert data['city'] == 'Berlin'
        assert data['temperature'] == 20
        assert data['humidity'] == 60
        assert data['windspeed'] == 5
        assert data['winddirection'] == 90
