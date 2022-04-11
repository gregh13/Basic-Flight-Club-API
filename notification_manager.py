from twilio.rest import Client
import smtplib


class EmailSender:

    def __init__(self, user_name, user_email, flight_deal_message_list, EMAIL, PASSWORD):
        self.user_name = user_name
        self.user_email = user_email
        self.message_list = flight_deal_message_list
        self.MY_EMAIL = EMAIL
        self.MY_PASSWORD = PASSWORD
        self.my_message = ""
        for item in self.message_list:
            self.my_message += item
        self.my_message = self.my_message

    def send_email(self):
        with smtplib.SMTP("smtp.gmail.com") as connection:
            connection.starttls()
            connection.login(self.MY_EMAIL, self.MY_PASSWORD)
            connection.sendmail(from_addr=self.MY_EMAIL, to_addrs=self.user_email,
                                msg=f"Subject:Hello {self.user_name}! It's Flight Deal Time :)\n\n{self.my_message}"
                                )


class NotifySMS:

    def __init__(self, SID, TOKEN, NUM_FROM, NUM_TO):
        self.TWILIO_ACC_SID = SID
        self.TWILIO_TOKEN = TOKEN
        self.PHONE_NUM1 = NUM_FROM
        self.PHONE_NUM2 = NUM_TO

    def send_sms(self, user_name):
        client = Client(self.TWILIO_ACC_SID, self.TWILIO_TOKEN)
        client.messages \
            .create(
            body=f"Problem with the 'home' airport of {user_name}. Fix it!",
            from_=self.PHONE_NUM1,
            to=self.PHONE_NUM2
        )