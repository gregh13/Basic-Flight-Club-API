from urllib.error import HTTPError
import requests
from datetime import datetime, timedelta


class FlightSearcher:

    def __init__(self, flying_from, destination, API):
        self.FLIGHT_FROM = flying_from
        self.city_name = destination
        self.FLIGHT_DESTINATION = ""

        today = datetime.now()
        self.today_date = today.strftime("%d/%m/%Y")
        self.new_date = (today + timedelta(days=180)).strftime("%d/%m/%Y")

        self.LOCATION_ENDPOINT = "https://tequila-api.kiwi.com/locations/query"
        self.FLIGHT_ENDPOINT = "https://tequila-api.kiwi.com/v2/search"
        self.API_KEY = API
        self.header = {
            "apikey": self.API_KEY
        }
        self.currency = "USD"
        self.flight_type = "round"
        self.min_nights = "2"
        self.max_nights = "14"
        self.passengers = "1"
        self.search_limit = "300"
        self.max_flight_time = "?"
        self.only_one_city = 1

    def get_iata_code(self):
        query = {
            "term": self.city_name,
            "location_types": "city",
            "limit": 1,
            "active_only": "true",
        }
        response = requests.get(url=self.LOCATION_ENDPOINT, headers=self.header, params=query)
        code_data = response.json()
        try:
            iata_code = code_data["locations"][0]["code"]
        except IndexError:
            print(f"ERROR! {self.city_name} didn't get any results. Check spelling?")
            iata_code = ""
            self.FLIGHT_DESTINATION = iata_code
            return iata_code
        else:
            self.FLIGHT_DESTINATION = iata_code
            return iata_code

    def look_for_flights(self):
        parameters = {
            "fly_from": self.FLIGHT_FROM,
            "fly_to": self.FLIGHT_DESTINATION,
            "date_from": self.today_date,
            "date_to": self.new_date,
            "nights_in_dst_from": self.min_nights,
            "nights_in_dst_to": self.max_nights,
            "flight_type": self.flight_type,
            "adults": self.passengers,
            "curr": self.currency,
            "limit": self.search_limit,
        }
        try:
            search_response = requests.get(url=self.FLIGHT_ENDPOINT, headers=self.header, params=parameters)
            # search_response.raise_for_status()
        except HTTPError:
            print("Home airport code is wrong")
        else:
            self.flight_data = search_response.json()
            return self.flight_data


