from flask import Flask
from flask_testing import TestCase
import requests
import json


def is_json(input_data):
    try:
        json.loads(input_data)
    except ValueError:
        return False
    return True


class MyTests(TestCase):

    def create_app(self):

        app = Flask(__name__)
        app.config['TESTING'] = True
        return app

    def test_server_is_up_and_running(self):
        response = requests.get('http://127.0.0.1:5000/')
        self.assertEqual(response.status_code, 200)

    def test_all_policy_data(self):
        response = requests.get(
            "http://127.0.0.1:5000/api/v1/resources/policy"
            )

        assert is_json(response.text)

    def test_all_policy_data_month(self):
        response = requests.get(
            "http://127.0.0.1:5000/api/v1/resources/policy?month='2020-04'"
            )

        assert is_json(response.text)

    def test_all_policy_data_default_filter(self):
        response = requests.get(
            "http://127.0.0.1:5000/api/v1/resources/policy?underwriter='red'"
            )

        assert is_json(response.text)
