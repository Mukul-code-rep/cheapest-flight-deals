import requests
from flight_data import FlightData
import os

TEQUILA_ENDPOINT = os.environ.get("url")
TEQUILA_KEY = os.environ.get("key")


class FlightSearch:
    #This class is responsible for talking to the Flight Search API.
    def check_flights(self, origin, dest, from_date, to_date):
        header = {
            'apikey': TEQUILA_KEY
        }
        parameters = {
            'fly_from': origin,
            'fly_to': dest,
            'date_from': from_date.strftime("%d/%m/%Y"),
            'date_to': to_date.strftime("%d/%m/%Y"),
            'nights_in_dst_from': 7,
            'nights_in_dst_to': 28,
            'flight_type': 'round',
            'one_for_city': 1,
            'curr': 'GBP',
            'max_stopovers': 0
        }

        response = requests.get(url=f"{TEQUILA_ENDPOINT}/v2/search", params=parameters, headers=header)
        response.raise_for_status()

        try:
            data = response.json()['data'][0]
        except IndexError:
            parameters['max_stopovers'] = 1
            response = requests.get(url=f"{TEQUILA_ENDPOINT}/v2/search", params=parameters, headers=header)
            response.raise_for_status()
            data = response.json()['data'][0]
            flight_data = FlightData(
                price=data['price'],
                origin_city=data['route'][0]['cityFrom'],
                destination_city=data['route'][0]['cityTo'],
                origin_airport=data['route'][0]['flyFrom'],
                destination_airport=data['route'][0]['flyTo'],
                out_date=data["route"][0]["local_departure"].split("T")[0],
                return_date=data["route"][1]["local_departure"].split("T")[0],
                stopovers=1,
                via_city=data["route"][0]["cityTo"]
            )

            return flight_data

        else:
            flight_data = FlightData(
                price=data['price'],
                origin_city=data['route'][0]['cityFrom'],
                destination_city=data['route'][0]['cityTo'],
                origin_airport=data['route'][0]['flyFrom'],
                destination_airport=data['route'][0]['flyTo'],
                out_date=data["route"][0]["local_departure"].split("T")[0],
                return_date=data["route"][1]["local_departure"].split("T")[0]
            )

            return flight_data

