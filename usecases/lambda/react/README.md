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
    columns:
    connection: !Ref flights_conn

  - name: flights
    table_name: flights
    columns:
    connection: !Ref flights_conn

  - name: ticket_flights
    table_name: ticket_flights
    columns:
    connection: !Ref flights_conn

  - name: airports
    table_name: airports
    columns:
    connection: !Ref flights_conn

  - name: airports_flights_schema
    table_name: airports
    columns:
    schema: flights_schema
    connection: !Ref flights_conn

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

## Available Scripts

In the project directory, you can run:

### `yarn start`

Runs the app in the development mode.\
Open [http://localhost:3000](http://localhost:3000) to view it in your browser.

The page will reload when you make changes.\
You may also see any lint errors in the console.