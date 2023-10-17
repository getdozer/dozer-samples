import json
import random
from kafka import KafkaProducer
from faker import Faker

faker = Faker()

# Set the bootstrap servers and topic for the Kafka producer
kafka_bootstrap_servers = 'localhost:19092'
kafka_topic = 'transactions'

# Create a Kafka producer instance
producer = KafkaProducer(bootstrap_servers=kafka_bootstrap_servers)

# Generate mock transaction data and send it to the Kafka topic
for index in range(10):
    # Generate mock transaction data using the Faker library
    transaction_data = {
        'id': index,
        'customer_id': faker.random_int(min=1000, max=9999),
        'timestamp': faker.date_time_this_decade().isoformat(),
        'amount': round(random.uniform(1, 1000), 2),
        'location': faker.random_element(elements=('New York', 'London', 'Tokyo', 'Sydney')),
        'provider': faker.random_element(elements=('AT&T', 'Verizon', 'Vodafone', 'Telstra')),
    }

    # Set the key for the Kafka message
    key_value = {
        'id': index
    }

    # Encode the transaction data and key as JSON
    transaction_bytes = json.dumps(transaction_data).encode()
    transaction_key_bytes = json.dumps(key_value).encode()

    # Send the transaction data to the Kafka topic
    result = producer.send(kafka_topic, value=transaction_bytes, key=transaction_key_bytes)

    # Print the sent record
    print(f"Sent record: {transaction_data}")

# Flush and close the Kafka producer
producer.flush()
producer.close()
