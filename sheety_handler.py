import requests

class SheetyHandler:

    def __init__(self):
        self.SHEETY_ENDPOINT = \
            "YOUR SHEETY ENDPOINT"

    def get_user_info(self):
        sheety_response = requests.get(url=self.SHEETY_ENDPOINT).json()["YOUR SHEET NAME"]
        return sheety_response