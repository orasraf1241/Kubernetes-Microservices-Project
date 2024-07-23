import os
import json
import threading
from kafka import KafkaConsumer
from pymongo import MongoClient
from flask import Flask, jsonify, make_response
from flask_cors import CORS  # Import CORS from flask_cors

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Environment variable setup
port = int(os.getenv('PORT', 3000))
mongo_host = os.getenv('MONGO_HOST', 'mongo')
mongo_port = int(os.getenv('MONGO_PORT', 27017))
kafka_broker = os.getenv('KAFKA_BROKER', 'my-cluster-kafka-bootstrap:9092')
kafka_group_id = os.getenv('KAFKA_GROUP_ID', 'my-group')
mongo_database = os.getenv('MONGO_DATABASE', 'mydatabase')
mongo_collection = os.getenv('MONGO_COLLECTION', 'purchases')

# MongoDB setup
client = MongoClient(f'mongodb://{mongo_host}:{mongo_port}/')
db = client[mongo_database]
collection = db[mongo_collection]

# Kafka consumer setup
consumer = KafkaConsumer(
    'purchase',
    bootstrap_servers=[kafka_broker],
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    group_id=kafka_group_id,
    value_deserializer=lambda x: x.decode('utf-8')  # Deserialize as string
)

@app.route('/consume', methods=['GET'])
def consume_messages():
    def consume():
        print("Starting consumer...")
        for message in consumer:
            raw_message = message.value
            print(f"Received raw message: {raw_message}")
            try:
                deserialized_message = json.loads(raw_message)
                collection.insert_one(deserialized_message)
                print(f"Inserted message into MongoDB: {deserialized_message}")
            except json.JSONDecodeError as e:
                print(f"Failed to decode JSON: {e}")
            except Exception as e:
                print(f"An error occurred: {e}")

    if not hasattr(consume_messages, "thread") or not consume_messages.thread.is_alive():
        consume_messages.thread = threading.Thread(target=consume)
        consume_messages.thread.start()
        response = make_response("Consumer thread has started")
    else:
        response = make_response("Consumer is already running")
    
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response

@app.route('/purchases', methods=['GET'])
def get_purchases():
    purchases = list(collection.find({}, {'_id': 0}))
    response = jsonify(purchases)
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port)
