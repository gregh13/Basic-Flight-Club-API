import os
from flight_search import FlightSearcher
from flight_info import FlightInfo
from sheety_handler import SheetyHandler
from notification_manager import EmailSender, NotifySMS
# import json
import datetime

# Use os.environ variables to store this info
# Necessary for the core functionality of the program
EMAIL = "EMAIL TO SEND OUT SMTP"
PASS = "PASSWORD FOR EMAIL"
API = 'KIWI FLIGHT SEARCH API TOKEN'


# SMS is to alert the dev of any issues; optional
SID = "YOUR TWILIO SID"
TOKEN = "YOUR TWILIO TOKEN"
NUM_FROM = 'YOUR TWILIO ACCOUNT NUMBER'
NUM_TO = "PHONE NUMBER TO RECEIVE SMS (DEV PURPOSES)"


day_of_week = datetime.datetime.today().weekday()

# If using a daily auto-run program, the day_of_week condition will make it run weekly
if day_of_week == 5:
    # Gets the user_info from the Googlesheet through Sheety. Only 200 requests per month, so save to json file
    sheety = SheetyHandler()
    user_data_all = sheety.get_user_info()
    # with open("flight_club_user_data.json") as user_data:
    #     user_data_all = json.load(user_data)

    # Runs through each user's data and then searches for each city in the user's data
    for user in user_data_all:
        notify_dev = False
        flight_deal_message_list = []
        user_name = user["firstName"]
        print(user_name)
        user_email = user["email"]
        flying_from = user["flyingFrom"]
        destination_list = [user[f"city{x}"] for x in range(1, 6)]
        price_ceiling_dict = {destination_list[x-1]: user[f"price{x}"] for x in range(1, 6)}
        print(price_ceiling_dict)
        for destination in destination_list:
            print(destination)
            tequila = FlightSearcher(flying_from, destination, API)
            city_code = tequila.get_iata_code()
            print(city_code)
            flight_data = tequila.look_for_flights()
            if "error" in flight_data:
                notify_dev = True
                continue
            elif len(flight_data["data"]) == 0:
                continue
            else:
                flight_info = FlightInfo(flight_data, destination)
                user_price_ceiling = price_ceiling_dict[destination]
                if flight_info.price <= user_price_ceiling:
                    print(f"The price is right for {flying_from}-{city_code}")
                    email_message = flight_info.deal_info_to_message()
                    flight_deal_message_list += email_message
        if len(flight_deal_message_list) != 0:
            print(f"Number of deals: {round(len(flight_deal_message_list)/422)}")
            email_sender = EmailSender(user_name, user_email, flight_deal_message_list, EMAIL, PASS)
            email_sender.send_email()
        if notify_dev:
            sender = NotifySMS(SID, TOKEN, NUM_FROM, NUM_TO)
            sender.send_sms(user_name)
else:
    print("It's not time yet!")