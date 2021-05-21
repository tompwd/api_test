from flask import Flask
from flask_testing import TestCase
import requests
import json


class MyTests(TestCase):

    def create_app(self):

        app = Flask(__name__)
        app.config['TESTING'] = True
        return app

    def test_server_is_up_and_running(self):
        response = requests.get('http://127.0.0.1:5000/')
        self.assertEqual(response.status_code, 200)

    def test_new_policy_count(self):
        response = requests.get(
            "http://127.0.0.1:5000/api/v1/resources/policy/new/count?date=%272020-03-04%27"
            )
        response2 = requests.get(
            "http://127.0.0.1:5000/api/v1/resources/policy/new/count?date=%272020-03-05%27"
            )

        assert json.loads(response.text) == 1 and json.loads(response2.text) == 0
