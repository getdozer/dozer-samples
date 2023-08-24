# Getting Started with Dozer react example

```yaml
app_name: flight-microservices
connections:
  - name: flights_conn
    config: !Postgres
      user: postgres
      password: postgres
      host: 0.0.0.0
      port: 5437
      database: flights

sql: |
  select f.arrival_airport as airport, a.coordinates as coordinates, COUNT(t.ticket_no) as tickets
  INTO airports_count
  from tickets t
  join ticket_flights tf on t.ticket_no = tf.ticket_no
  join flights f on tf.flight_id = f.flight_id
  join airports a on f.arrival_airport = a.airport_code
  group by f.arrival_airport, a.coordinates;

  select extract(HOUR FROM f.window_start) as start, count(f.window_start) as dep_count
  INTO departures_count
  from TUMBLE(flights, scheduled_departure, '4 HOURS') f
  group by extract(HOUR FROM f.window_start)

sources:
  - name: tickets
    table_name: tickets
    connection: flights_conn

  - name: flights
    table_name: flights
    connection: flights_conn

  - name: ticket_flights
    table_name: ticket_flights
    connection: flights_conn

  - name: airports
    table_name: airports
    connection: flights_conn

  - name: airports_flights_schema
    table_name: airports
    schema: flights_schema
    connection: flights_conn

endpoints:

  - name: tickets
    path: /bookings/tickets
    table_name: tickets
    index:
      primary_key:
        - ticket_no

  - name: flights
    path: /bookings/flights
    table_name: flights
    index:
      primary_key:
        - flight_id

  - name: airports
    path: /bookings/airports
    table_name: airports
    index:
      primary_key:
        - airport_code


  - name: airports_flights_schema
    path: /bookings/airports_flights_schema
    table_name: airports_flights_schema
    index:
      primary_key:
        - id

  - name: ticket_flights
    path: /bookings/ticket_flights
    table_name: ticket_flights
    index:
      primary_key:
        - ticket_no
        - flight_id

  - name: airports_count
    path: /airports_count
    table_name: airports_count
    index:
      primary_key:
        - airport
        - coordinates

  - name: departures_count
    path: /departures_count
    table_name: departures_count
    index:
      primary_key:
        - start
```

## Setup and Running the Project

1. Navigate to the `usecases/pg-flights` directory in your terminal:

    ```bash
    cd ../pg-flights
    ```

2. Run the following command to execute Dozer with the provided `dozer-config.yaml` configuration:

    ```bash
    dozer -c dozer-config.yaml
    ```

3. Once the Dozer process is running successfully, you can proceed to start the React app.

4. Navigate back to this directory

5. Run the following command to start the React app in development mode:

    ```bash
    yarn start
    ```

6. Open your browser and visit [http://localhost:3000](http://localhost:3000) to view the React app.

7. As you make changes to the project code, the page will automatically reload to reflect those changes. Any lint errors will also be displayed in the console.

## Data Sources and Endpoints

The project utilizes various data sources and endpoints defined in the `dozer-config.yaml` file. These include:

- `tickets`: Endpoint for booking tickets.
- `flights`: Endpoint for flight information.
- `airports`: Endpoint for airport details.
- `airports_flights_schema`: Endpoint for airport and flight schema.
- `ticket_flights`: Endpoint for ticket-flight associations.
- `airports_count`: Endpoint for counting airports and their coordinates.
- `departures_count`: Endpoint for counting flight departures.

You can access these endpoints in your React app to display relevant information.

Remember to keep the `dozer-config.yaml` file and the project directory structure consistent to ensure proper functionality.
