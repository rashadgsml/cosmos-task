get_flights_params = {
    "parameters": [
        {
            "name": "destination",
            "in": "query",
            "type": "string",
            "required": False,
            "description": "Destination airport IATA code"
        },
        {
            "name": "airlines",
            "in": "query",
            "type": "array",
            "items": {
                "type": "string"
            },
            "required": False,
            "description": "List of airline IATA codes"
        }
    ],
    "responses": {
        200: {
            "description": "A list of flights",
            "schema": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "id": {
                            "type": "string"
                        },
                        "flight_number": {
                            "type": "string"
                        },
                        "airline": {
                            "type": "string"
                        },
                        "origin": {
                            "type": "string"
                        },
                        "destination": {
                            "type": "string"
                        },
                        "scheduled_departure_at": {
                            "type": "string"
                        },
                        "actual_departure_at": {
                            "type": "string"
                        },
                        "delays": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "code": {
                                        "type": "string"
                                    },
                                    "time_minutes": {
                                        "type": "integer"
                                    },
                                    "description": {
                                        "type": "string"
                                    }
                                }
                            }
                        },
                        "total_delay_minutes": {
                            "type": "number"
                        }
                    }
                }
            }
        }
    }
}