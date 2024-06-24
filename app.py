from flask import Flask, request, jsonify
from flasgger import Swagger, swag_from
import pandas as pd
import uuid

from swagger_params import get_flights_params
from utils import convert_delays_type, get_total_delay_minutes, process_schedule_data, process_delay_data


app = Flask(__name__)
swagger = Swagger(app)


@app.route('/flights', methods=['GET'])
@swag_from(get_flights_params)
def get_flights():
    destination = request.args.get('destination')
    airlines = request.args.getlist('airlines')

    # in case the link is broken
    try:
        schedules_df = process_schedule_data()
    except:
        return bad_request("Couldn't fetch the schedules data")

    try:
        delays_df = process_delay_data()
    except:
        return bad_request("Couldn't fetch the delays data")

    # merging schedule and delay
    merged_df = pd.merge(schedules_df, delays_df, on='flight_number', how='left')

    # assigning id for each flight
    # merged_df['id'] = [str(uuid.uuid4()) for _ in range(len(merged_df))]

    # filtering based on the destination
    if destination:
        merged_df = merged_df[merged_df['destination'] == destination]
        if not merged_df.to_dict(orient='records'):
            return []

    # filtering based on the list of airlines
    if airlines:
        airlines = airlines[0].split(',')
        merged_df = merged_df[merged_df['airline'].isin(airlines)]
        if not merged_df.to_dict(orient='records'):
            return []

    # converting 'delays' from dictionary to list of dictionaries
    merged_df['delays'] = merged_df['delays'].apply(convert_delays_type)

    # adding total_delay_minutes to the dataset
    merged_df['total_delay_minutes'] = merged_df.apply(
        lambda row: get_total_delay_minutes(row['scheduled_departure_at'], row['actual_departure_at']), axis=1
    )

    return jsonify(merged_df.to_dict(orient='records'))


@app.errorhandler(400)
def bad_request(error):
    return jsonify({'error': 'Bad Request', 'message': str(error)}), 400


@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not Found', 'message': str(error)}), 404


@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal Server Error', 'message': str(error)}), 500


if __name__ == '__main__':
    app.run(debug=True)
