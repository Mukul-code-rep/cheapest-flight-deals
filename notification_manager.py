from twilio.rest import Client
import smtplib
import os


class NotificationManager:
    #This class is responsible for sending notifications with the deal flight details.
    def send_notification(self, flight_price: int, our_price: int, dept_city, dept_code, arr_city, arr_code, out_date,
                          in_date, stopover, via_city):
        if flight_price < our_price:
            acc_sid = 'AC788f8c0ba31921fbcaa5f7789a4aafc6'
            auth_token = '1424b597a4e0f009683bc18caaa85f5e'
            client = Client(acc_sid, auth_token)
            if stopover == 0:
                message = client.messages.create(
                    body=f'Low price alert! Only £{flight_price} to fly from {dept_city}-{dept_code} to '
                         f'{arr_city}-{arr_code}, from {out_date} to {in_date}',
                    from_='+14352721610',
                    to=os.environ.get("my_number")
                )
            else:
                message = client.messages.create(
                    body=f'Low price alert! Only £{flight_price} to fly from {dept_city}-{dept_code} to '
                         f'{arr_city}-{arr_code}, from {out_date} to {in_date}\n\nFlight has {stopover} stopover,'
                         f' via {via_city}',
                    from_='+14352721610',
                    to=os.environ.get("my_number")
                )

            print(message.status)

    def send_emails(self, flight_price: int, our_price: int, dept_city, dept_code, arr_city, arr_code, out_date,
                    in_date, stopover, via_city):
        my_email = os.environ.get("email")
        password = os.environ.get("password")

        if flight_price < our_price:
            if stopover == 0:
                with smtplib.SMTP('smtp.mail.yahoo.com', 587) as connection:
                    connection.starttls()
                    connection.login(user=my_email, password=password)
                    connection.sendmail(from_addr=my_email,
                                        to_addrs=my_email,
                                        msg=f'Subject:Flight Deal!\n\nLow price alert! Only {u"\u00A3"}{flight_price} to '
                                            f'fly from'
                                            f' {dept_city}-{dept_code} to {arr_city}-{arr_code}, from {out_date} to '
                                            f'{in_date}\n'
                                            f'https://www.google.co.uk/flights?hl=en#flt={dept_code}.{arr_code}.'
                                            f'{out_date}*{arr_code}.{dept_code}.{in_date}'
                                        )
            else:
                with smtplib.SMTP('smtp.mail.yahoo.com', 587) as connection:
                    connection.login(user=my_email, password=password)
                    connection.sendmail(from_addr=my_email,
                                        to_addrs=my_email,
                                        msg=f'Subject:Flight Deal!\n\nLow price alert! Only {u"\u00A3"}{flight_price} '
                                            f'to fly from'
                                            f' {dept_city}-{dept_code} to {arr_city}-{arr_code}, from {out_date} to '
                                            f'{in_date} with {stopover} stopover(s) at {via_city}.\n'
                                            f'https://www.google.co.uk/flights?hl=en#flt={dept_code}.{arr_code}.'
                                            f'{out_date}*{arr_code}.{dept_code}.{in_date}'
                                        )
