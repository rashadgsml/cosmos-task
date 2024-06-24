import requests
import pandas as pd
from datetime import datetime
from flask import jsonify


FLIGHT_SCHEDULES_URL = "https://challange.usecosmos.cloud/flight_schedules.json"
FLIGHT_DELAYS_URL = "https://challange.usecosmos.cloud/flight_delays.json"


def convert_delays_type(delays_dict):
    if not delays_dict or str(delays_dict) == "nan":
        return []

    delays_list = [
        {
            "code": delay_info["Code"],
            "time_minutes": delay_info["DelayTime"],
            "description": delay_info["Description"]
        }
        for key, delay_info in delays_dict.items() if delay_info is not None
    ]

    return delays_list


def get_total_delay_minutes(scheduled_departure_at, actual_departure_at):
    datetime_format = "%Y-%m-%dT%H:%MZ"

    scheduled_departure_at = datetime.strptime(scheduled_departure_at, datetime_format)
    actual_departure_at = datetime.strptime(actual_departure_at, datetime_format)

    time_difference = actual_departure_at - scheduled_departure_at

    difference_in_minutes = time_difference.total_seconds() / 60

    return difference_in_minutes


def fetch_flight_schedules():
    response = requests.get(FLIGHT_SCHEDULES_URL)
    return response.json()


def fetch_flight_delays():
    response = requests.get(FLIGHT_DELAYS_URL)
    return response.json()


def process_schedule_data():
    schedules = fetch_flight_schedules()["FlightStatusResource"]["Flights"]["Flight"]

    schedules_df = pd.json_normalize(schedules)
    schedules_df = pd.DataFrame(schedules_df)

    selected_columns = ['Arrival.AirportCode', 'Departure.AirportCode', 'Departure.TimeStatus.Definition',
                        'Departure.ScheduledTimeUTC.DateTime', 'Departure.ActualTimeUTC.DateTime', 
                        'MarketingCarrier.FlightNumber', 'MarketingCarrier.AirlineID', 'FlightStatus.Definition']
    schedules_df = schedules_df[selected_columns]

    selected_columns = {
        'MarketingCarrier.FlightNumber': 'flight_number',
        'MarketingCarrier.AirlineID': 'airline',
        'Departure.AirportCode': 'origin',
        'Departure.TimeStatus.Definition': 'time_status',
        'Arrival.AirportCode': 'destination',
        'Departure.ScheduledTimeUTC.DateTime': 'scheduled_departure_at',
        'Departure.ActualTimeUTC.DateTime': 'actual_departure_at',
        'FlightStatus.Definition': 'flight_status',
    }
    schedules_df.rename(columns=selected_columns, inplace=True)

    return schedules_df


def process_delay_data():
    delays = fetch_flight_delays()

    delays_df = pd.json_normalize(delays, record_path="FlightLegs", 
                                  meta=[["Flight", "OperatingFlight", "Number"]], 
                                  sep='_', max_level=1)

    delays_df = pd.DataFrame(delays_df)

    selected_columns = ['Flight_OperatingFlight_Number', 'Departure_Delay']
    delays_df = delays_df[selected_columns]

    selected_columns = {
        'Flight_OperatingFlight_Number': 'flight_number',
        'Departure_Delay': 'delays',
    }
    delays_df.rename(columns=selected_columns, inplace=True)

    return delays_df


