# Flight Delay API

## Project Links
**You can test the API via Swagger Documentation**
- **Swagger UI**: [Swagger Documentation](https://cosmos-task-b0ea2d2d1d46.herokuapp.com/apidocs)
- **Flights API**: [Flights Endpoint](https://cosmos-task-b0ea2d2d1d46.herokuapp.com/flights)

## Prerequisites
- Python 3.10.5
- pip 22.0.4

## Installation

1. **Clone the repository**:
    ```sh
    git clone https://github.com/rashadgsml/cosmos-task.git
    ```

2. **Create a virtual environment**:
    ```sh
    cd <project_path>
    python -m venv venv
    ```

3. **Activate the virtual environment**:
    - On Windows:
        ```sh
        venv\Scripts\activate
        ```
    - On macOS/Linux:
        ```sh
        source venv/bin/activate
        ```

4. **Install the dependencies**:
    ```sh
    pip install -r requirements.txt
    ```

## Running the API

1. **Start the Flask application**:
    ```sh
    python app.py
    ```

2. **The API will be accessible at**:
    ```sh
    http://127.0.0.1:5000/flights

3. **The Swagger URL**:
    ```sh
    http://127.0.0.1:5000/apidocs
    ```

## Running Tests

1. **Run the tests**:
    ```sh
    pytest
    ```

## API Endpoints

- **GET /flights**
  - **Description**: Retrieve a list of flights with optional filters.
  - **Query Parameters**:
    - `destination`: (optional) Destination airport IATA code.
    - `airlines`: (optional) Comma-separated list of airline IATA codes.
  - **Example Request**:
    ```sh
    curl "https://cosmos-task-b0ea2d2d1d46.herokuapp.com/flights?destination=MUC&airlines=LH,OS"
    ```

## Example Response

```json
[
  {
    "actual_departure_at": "2024-06-19T07:39Z",
    "airline": "LH",
    "delays": [
      {
        "code": "1",
        "description": "Aircraft Problem",
        "time_minutes": 20
      },
      {
        "code": "2",
        "description": "Slow baggage handling",
        "time_minutes": 10
      },
      {
        "code": "3",
        "description": "Weather",
        "time_minutes": 4
      }
    ],
    "destination": "MUC",
    "flight_number": "2325",
    "flight_status": "Flight Landed",
    "origin": "VIE",
    "scheduled_departure_at": "2024-06-19T07:05Z",
    "time_status": "Flight Delayed",
    "total_delay_minutes": 34
  }
]
```