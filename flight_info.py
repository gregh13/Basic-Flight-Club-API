class FlightInfo:

    def __init__(self, flight_data, destination):
        data = flight_data["data"][0]
        self.city_from = data['cityFrom']
        self.city_from_code = data['cityCodeFrom']
        self.city_to = destination
        self.city_to_code = data['cityCodeTo']
        self.departure = data['local_departure'].split("T")[0]
        self.leave_destination_date = data["route"][-1]['local_departure'].split("T")[0]
        self.arrival = data["route"][-1]['local_arrival'].split("T")[0]
        self.nights_at_destination = data['nightsInDest']
        self.price = data['price']

    def deal_info_to_message(self):
        email_message = f"Great deals!\n\nOnly ${self.price} for a roundtrip ticket from " \
                        f"{self.city_from}-{self.city_from_code} " \
                        f"to {self.city_to}-{self.city_to_code} leaving {self.city_from_code} on {self.departure} " \
                        f"and returning from {self.city_to_code} " \
                        f"on {self.leave_destination_date}.\n" \
                        f"That's {self.nights_at_destination} nights in {self.city_to}, could be fun!" \
                        f"\n\nHere is a link with the flight details all setup to see this deal on Kayak.com." \
                        f"\nhttps://www.kayak.com/flights/{self.city_from_code}-{self.city_to_code}/{self.departure}/{self.leave_destination_date}?sort=price_a" \
                        f"\n----------------------------------------------------\n\n"
        return email_message
