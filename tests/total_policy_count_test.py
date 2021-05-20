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

    def test_policy_count(self):
        response = requests.get(
            "http://127.0.0.1:5000/api/v1/resources/user/policy/count?user_id='user_000000BcyxC7NwL6OnB9boEXLUNBw'"
            )
        print(response.text)
        assert json.loads(response.text) == 5

    def test_policy_count_month(self):
        response = requests.get(
            "http://127.0.0.1:5000/api/v1/resources/user/policy/count?user_id='user_000000BcyxC7NwL6OnB9boEXLUNBw'&month='2020-05'"
            )

        assert json.loads(response.text) == 1
