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

    def test_user_days_active(self):
        response = requests.get(
            "http://127.0.0.1:5000/api/v1/resources/user/days_active/count?user_id='user_000000C4wvsbftmmdew81vUDGDwjx'"
            )
        assert json.loads(response.text) == 91

    def test_user_days_active_underwriter(self):
        response = requests.get(
            "http://127.0.0.1:5000/api/v1/resources/user/days_active/count"
            "?user_id='user_000000C4wvsbftmmdew81vUDGDwjx'&underwriter='red'"
            )
        assert json.loads(response.text) == 91

    def test_user_days_active_month(self):
        response = requests.get(
            "http://127.0.0.1:5000/api/v1/resources/user/days_active/count"
            "?user_id='user_000000C4wvsbftmmdew81vUDGDwjx'&month='2020-04'"
            )
        assert json.loads(response.text) == 60
