import pytest
import time
import json
from app import app


@pytest.fixture
def client():
    with app.test_client() as client:
        yield client


def test_get_flights_no_params(client):
    # Test endpoint without parameters
    response = client.get('/flights')
    assert response.status_code == 200


def test_get_flights_with_destination(client):
    response = client.get('/flights?destination=MUC')
    assert response.status_code == 200
    data = json.loads(response.data)
    # Check if the returned flights have correct destination
    if data:
        assert all(flight['destination'] == 'MUC' for flight in data)


def test_get_flights_with_airlines(client):
    # testing with airlines parameter
    response = client.get('/flights?airlines=OS,TK')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert isinstance(data, list)
    # Check if the returned flights are from specified airlines
    if data:
        assert all(flight['airline'] in ['OS', 'TK'] for flight in data)


def test_get_flights_with_destination_and_airlines(client):
    # testing with both destination and airlines parameters
    response = client.get('/flights?destination=MUC&airlines=OS,TK')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert isinstance(data, list)
    # Check if the returned flights have the correct destination and are from the specified airlines
    if data:
        assert all(flight['destination'] == 'MUC' and flight['airline'] in ['OS', 'TK'] for flight in data)


def test_get_flights_with_empty_result(client):
    # Test endpoint to get an empty list
    response = client.get('/flights?destination=XYZ&airlines=NO')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert isinstance(data, list)
    assert len(data) == 0


def test_get_flights_with_empty_strings(client):
    response = client.get('/flights?destination=&airlines=')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert isinstance(data, list)
    assert len(data) == 0


def test_get_flights_with_long_strings(client):
    # testing filterings with a long string
    long_string = 'A' * 1000
    response = client.get(f'/flights?destination={long_string}&airlines={long_string}')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert isinstance(data, list)
    assert len(data) == 0


def test_get_flights_response_format(client):
    # testing if the response contains all required fields
    # and 'delays' is a list
    response = client.get('/flights')
    assert response.status_code == 200
    data = json.loads(response.data)
    if data:
        for flight in data:
            assert 'flight_number' in flight
            assert 'airline' in flight
            assert 'origin' in flight
            assert 'destination' in flight
            assert 'scheduled_departure_at' in flight
            assert 'actual_departure_at' in flight
            assert 'delays' in flight
            assert 'time_status' in flight
            assert 'flight_status' in flight
            assert isinstance(flight['delays'], list)


def test_get_flights_performance(client):
    start_time = time.time()
    response = client.get('/flights')
    end_time = time.time()
    assert response.status_code == 200
    assert (end_time - start_time) < 1
