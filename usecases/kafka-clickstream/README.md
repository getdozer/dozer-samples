### WIP ...

# Dozer Clickstream App with Redpanda

This project demonstrates how to use Dozer and Redpanda to capture and process clickstream data from a web application.

## Prerequisites

- Docker and Docker Compose
- Python 3.7 or later
- Flask
- Kafka Python client

## Steps to Run the Project

1. **Start Redpanda:**

   Use the provided `docker-compose.yml` file to start a Redpanda instance:

   ```bash
   docker-compose up -d
   ```

2. **Register the Schema:**

   Register the clickstream schema with the Redpanda schema registry:

   ```bash
   curl -X POST -H "Content-Type: application/vnd.schemaregistry.v1+json" \
        --data '{"schema": "{\"type\":\"record\",\"name\":\"clickstream\",\"namespace\":\"dozer.samples\",\"fields\":[{\"name\":\"timestamp\",\"type\":\"int\"},{\"name\":\"type\",\"type\":\"string\"}]}"}' \
        http://localhost:18081/subjects/clickstream-value/versions

  curl -X POST -H "Content-Type: application/vnd.schemaregistry.v1+json" \
        --data '{"schema": "{\"type\":\"string\"}"}' \
        http://localhost:18081/subjects/clickstream-key/versions

   ```

3. **Start the Flask Server:**

   Run the Flask server which serves the web page and handles click events:

   ```bash
   python server.py
   ```

   The web application is now accessible at `http://localhost:3000`.

4. **Start Dozer:**

   Run Dozer with the provided configuration to consume clickstream events from Kafka and process them.

5. **Interact with the Web Application:**

   Open the web application in a browser and interact with it. Click events are sent to the Flask server, which publishes them to a Kafka topic. Dozer consumes these events and processes them according to its configuration.

6. **Query the dozer API endpoints:**

## Notes

- The Flask server uses the Kafka Python client to produce clickstream events to Kafka.
- The web application uses JavaScript to send click events to the Flask server when the user interacts with various elements.
- Dozer is configured to consume from the Kafka topic and process the clickstream events.
- The Redpanda instance includes a schema registry, which is used to register the clickstream event schema.

## Troubleshooting

If you encounter issues with the schema registry, ensure that the schema is correctly defined and that the Redpanda instance is running and accessible.

If you encounter issues with Dozer, check the Dozer logs for error messages and ensure that it is correctly configured to consume from the Kafka topic.

## Conclusion

This project demonstrates a basic setup for capturing and processing clickstream data using Dozer and Redpanda. It can be extended and customized to suit more complex use cases.
