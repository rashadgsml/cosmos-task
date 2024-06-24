import unittest
from flask import Flask
from app import app
import json


class FlaskTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True


    def test_get_flights_no_params(self):
        # Test endpoint without parameters
        response = self.app.get('/flights')
        self.assertEqual(response.status_code, 200)


    def test_get_flights_with_destination(self):
        response = self.app.get('/flights?destination=MUC')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        # Check if the returned flights have correct destination
        if data:
            self.assertTrue(all(flight['destination'] == 'MUC' for flight in data))


    def test_get_flights_with_airlines(self):
        # Test endpoint with airlines parameter
        response = self.app.get('/flights?airlines=OS,TK')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIsInstance(data, list)
        # Check if the returned flights are from specified airlines
        if data:
            self.assertTrue(all(flight['airline'] in ['OS', 'TK'] for flight in data))


    def test_get_flights_with_destination_and_airlines(self):
        # Test endpoint with both destination and airlines parameters
        response = self.app.get('/flights?destination=MUC&airlines=OS,TK')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIsInstance(data, list)
        # Check if the returned flights have the correct destination and are from the specified airlines
        if data:
            self.assertTrue(all(flight['destination'] == 'MUC' and flight['airline'] in ['OS', 'TK'] for flight in data))


if __name__ == '__main__':
    unittest.main()
