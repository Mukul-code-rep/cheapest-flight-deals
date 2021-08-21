from datetime import datetime, timedelta
from data_manager import DataManager
from flight_search import FlightSearch
from notification_manager import NotificationManager

ORIGIN = "LON"

data_manager = DataManager()

dest_codes, dest_name = data_manager.get_destination()
our_budget = data_manager.get_destination_lowest_price()
print(dest_codes, dest_name, our_budget)

tomorrow = datetime.today() + timedelta(days=1)
six_month_from_today = datetime.today() + timedelta(days=6*30)

flightSearch = FlightSearch()
flights = []
for dest in dest_codes:
    flight_data = flightSearch.check_flights(origin=ORIGIN, dest=dest, from_date=tomorrow,
                                             to_date=six_month_from_today)
    flights.append(flight_data)

notification_manager = NotificationManager()
for flight in flights:
    notification_manager.send_notification(flight_price=flight.price,
                                           our_price=our_budget[dest_name.index(flight.destination_city)],
                                           dept_city=flight.origin_city,
                                           dept_code=flight.origin_airport,
                                           arr_city=flight.destination_city,
                                           arr_code=flight.destination_airport,
                                           out_date=flight.out_date,
                                           in_date=flight.return_date)
