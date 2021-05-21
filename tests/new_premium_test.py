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

    def test_new_premium_total(self):
        response = requests.get(
            "http://127.0.0.1:5000/api/v1/resources/policy/new/premium?underwriter=%27red%27"
            )
        assert json.loads(response.text) == json.loads("""[
                                                [
                                                    "2020-02-26",
                                                    94
                                                ],
                                                [
                                                    "2020-03-13",
                                                    86
                                                ],
                                                [
                                                    "2020-03-17",
                                                    49
                                                ],
                                                [
                                                    "2020-03-25",
                                                    89
                                                ],
                                                [
                                                    "2020-03-29",
                                                    21
                                                ]
                                                ]""")

    def test_new_premium_total_month(self):
        response = requests.get(
            "http://127.0.0.1:5000/api/v1/resources/policy/new/premium?underwriter='red'&month='2020-03'"
            )
        assert json.loads(response.text) == json.loads("""[
                                                [
                                                    "2020-03-13",
                                                    86
                                                ],
                                                [
                                                    "2020-03-17",
                                                    49
                                                ],
                                                [
                                                    "2020-03-25",
                                                    89
                                                ],
                                                [
                                                    "2020-03-29",
                                                    21
                                                ]
                                                ]""")
