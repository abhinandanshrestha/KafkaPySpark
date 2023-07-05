from confluent_kafka import Producer
from time import sleep
import json
import random
from flask import Flask, request, jsonify

# Create a Kafka producer configuration
conf = {
    'bootstrap.servers': 'localhost:9092',
    'default.topic.config': {'acks': 'all'}
}

# Create a Kafka producer instance
producer = Producer(conf)

# Kafka topic
kafka_topic = 'iot'

app = Flask(__name__)

@app.route('/data', methods=['POST'])
def process_data():
    data = request.json # Get JSON data from the request

    # Prettify the data and print it to the console
    # prettified_data = json.dumps(data, indent=4)
    # print(prettified_data)

    producer.produce(kafka_topic, value=json.dumps(data).encode('utf-8'))
    # print(json.dumps(data).encode('utf-8'))
    # Flush the producer buffer
    producer.flush()

    # Sleep for 1 second
    # sleep(1)

    return ''

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000,debug=True)
