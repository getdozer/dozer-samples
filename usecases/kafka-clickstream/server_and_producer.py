import json
from flask import Flask, request, render_template
from kafka import KafkaProducer

app = Flask(__name__)

kafka_bootstrap_servers = 'localhost:19092'
kafka_topic = 'clickstream'

producer = KafkaProducer(
    bootstrap_servers=kafka_bootstrap_servers,
    key_serializer=lambda k: json.dumps(k).encode('utf-8'),
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/click', methods=['POST'])
def click():
    data = request.get_json()
    timestamp = data['timestamp']
    click_type = data['type']

    key = {
        'timestamp': timestamp,
        'type': click_type
    }

    value = {
        'timestamp': timestamp,
        'type': click_type
    }

    producer.send(kafka_topic, key=key, value=value)
    producer.flush()

    return '', 200

if __name__ == '__main__':
    app.run(port=3000)
