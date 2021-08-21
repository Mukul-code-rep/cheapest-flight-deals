import requests
import os

SHEETY_PRICES_ENDPOINT = os.environ.get("sheety_url")


class DataManager:
    #This class is responsible for talking to the Google Sheet.
    def __init__(self):
        self.destination_data = {}
        self.get_destination_data()
        self.destination_code = []
        self.destination_name = []
        self.destination_lowest_price = []

    def get_destination_data(self):
        response = requests.get(url=SHEETY_PRICES_ENDPOINT)
        data = response.json()
        self.destination_data = data["prices"]
        return self.destination_data

    def get_destination(self):
        for dic in self.destination_data:
            self.destination_code.append(dic['iataCode'])
            self.destination_name.append(dic['city'])
        return self.destination_code, self.destination_name

    def get_destination_lowest_price(self):
        for dic in self.destination_data:
            self.destination_lowest_price.append(dic['lowestPrice'])
        return self.destination_lowest_price
