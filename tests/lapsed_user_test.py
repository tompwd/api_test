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

    def test_lapsed_count(self):
        response = requests.get(
            "http://127.0.0.1:5000/api/v1/resources/policy/lapsed/count?month=%272021-02%27"
            )
        assert json.loads(response.text) == 10

    # def test_lapsed_count_underwriter(self):
    #     response = requests.get(
    #         "http://127.0.0.1:5000/api/v1/resources/policy/lapsed/count?month=%272021-02%27&underwriter='red'"
    #         )
    #     assert json.loads(response.text) == 60
