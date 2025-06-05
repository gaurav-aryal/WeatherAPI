import json
from weatherAPI import app, geolocator
from unittest.mock import patch, MagicMock
import pytest

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_get_weather_success(client):
    with patch('weatherAPI.requests.get') as mock_get:
        mock_resp = MagicMock()
        mock_resp.status_code = 200
        mock_resp.json.return_value = {
            'current_weather': {
                'temperature_2m': 20.5,
                'relativehumidity_2m': 60,
                'windspeed_10m': 5.1
            }
        }
        mock_get.return_value = mock_resp

        resp = client.get('/weather?latitude=52.52&longitude=13.4050')
        assert resp.status_code == 200
        data = resp.get_json()
        assert data['temperature'] == 20.5
        assert data['humidity'] == 60
        assert data['windspeed'] == 5.1

def test_weather_missing_parameters(client):
    resp = client.get('/weather')
    assert resp.status_code == 400

def test_get_coordinates_success(client):
    mock_location = type('loc', (object,), {'latitude': 52.52, 'longitude': 13.405})()
    with patch.object(geolocator, 'geocode', return_value=mock_location):
        resp = client.get('/get_coordinates?city=Berlin')
        assert resp.status_code == 200
        data = resp.get_json()
        assert data == {'city': 'Berlin', 'latitude': 52.52, 'longitude': 13.405}

def test_reverse_geocode_success(client):
    mock_location = type('loc', (object,), {'address': 'Berlin, Germany'})()
    with patch.object(geolocator, 'reverse', return_value=mock_location):
        resp = client.get('/reverse_geocode?latitude=52.52&longitude=13.405')
        assert resp.status_code == 200
        data = resp.get_json()
        assert data['address'] == 'Berlin, Germany'

def test_get_weather_by_name_success(client):
    mock_location = type('loc', (object,), {'latitude': 52.52, 'longitude': 13.405})()
    with patch.object(geolocator, 'geocode', return_value=mock_location), \
         patch('weatherAPI.requests.get') as mock_get:
        mock_resp = MagicMock()
        mock_resp.status_code = 200
        mock_resp.json.return_value = {
            'current_weather': {
                'temperature': 22.1,
                'humidity': 65,
                'windspeed': 4.0,
                'winddirection': 240
            }
        }
        mock_get.return_value = mock_resp

        resp = client.get('/get_weather_by_name?city=Berlin')
        assert resp.status_code == 200
        data = resp.get_json()
        assert data['city'] == 'Berlin'
        assert data['temperature'] == 22.1
        assert data['humidity'] == 65
        assert data['windspeed'] == 4.0
        assert data['winddirection'] == 240
