# Dozer Clickstream App with Redpanda

This project demonstrates how to use Dozer and Redpanda to capture and process clickstream data from a web application and display real-time analytics on a web page.

## Prerequisites

- Docker and Docker Compose
- Python 3.7 or later
- Flask
- Kafka Python client
- Dozer

## Steps to Run the Project

1. **Start Redpanda:**

   Use the provided `docker-compose.yml` file to start a Redpanda instance:

   ```bash
   docker-compose up -d
   ```

2. **Create a Topic:**

   Create a Kafka topic named "clickstream" using the following command:

   ```bash
   docker exec -it redpanda-0 rpk topic create clickstream
   ```

3. **Register the Schema:**

   Register the clickstream schema with the Redpanda schema registry:
```bash
curl -X POST -H "Content-Type: application/vnd.schemaregistry.v1+json" \
        --data '{"schema": "{\"type\":\"record\",\"name\":\"clickstream\",\"namespace\":\"dozer.samples\",\"fields\":[{\"name\":\"timestamp\",\"type\":\"int\"},{\"name\":\"type\",\"type\":\"string\"}]}"}' \
        http://localhost:18081/subjects/clickstream-value/versions

curl -X POST -H "Content-Type: application/vnd.schemaregistry.v1+json" \
        --data '{"schema": "{\"type\":\"string\"}"}' \
        http://localhost:18081/subjects/clickstream-key/versions
```

4. **Start the Flask Server:**

   Run the Flask server which serves the web page and handles click events:

   ```bash
   python server_and_producer.py
   ```

   The web application is now accessible at `http://localhost:3000`.

5. **Start Dozer:**

   Run Dozer with the provided configuration to consume clickstream events from Kafka and process them.
   start the Dozer app with the following command:

   ```bash
   dozer
   ```

6. **Interact with the Web Application:**

   Open the web application in a browser and interact with it. Click events are sent to the Flask server, which publishes them to a Kafka topic. Dozer consumes these events and processes them according to its configuration.

7. **View Real-Time Analytics:**

   Open the analytics page in a browser to view real-time analytics. The page is accessible at `http://localhost:3000/analytics`.
## Notes

- The Flask server uses the Kafka Python client to produce clickstream events to Kafka.
- The web application uses JavaScript to send click events to the Flask server when the user interacts with various elements.
- Dozer is configured to consume from the Kafka topic and process the clickstream events.
- The Redpanda instance includes a schema registry, which is used to register the clickstream event schema.

## Troubleshooting

If you encounter issues with the schema registry, ensure that the schema is correctly defined and that the Redpanda instance is running and accessible.

If you encounter issues with Dozer, check the Dozer logs for error messages and ensure that it is correctly configured to consume from the Kafka topic.

## Conclusion

This project demonstrates a basic setup for capturing and processing clickstream data using Dozer and Redpanda. It can be extended and customized to suit more complex use cases. The real-time analytics page provides a live view of the processed data, enabling you to gain immediate insights into user behavior.
