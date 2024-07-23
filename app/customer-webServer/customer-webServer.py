from flask import Flask, request, jsonify, make_response
from kafka import KafkaProducer
import json
import os
import requests
from flask_cors import CORS  # Import CORS from flask_cors
import datetime



app = Flask(__name__)

port = int(os.getenv('PORT', 3001))

# Kafka producer setup
kafka_broker = os.getenv('KAFKA_BROKER')
if not kafka_broker:
    raise ValueError("KAFKA_BROKER environment variable must be set")

producer = KafkaProducer(
    bootstrap_servers=[kafka_broker],
    value_serializer=lambda x: json.dumps(x).encode('utf-8')
)

# Handle "buy" request
@app.route('/buy', methods=['POST'])
def buy():
    data = request.json
    data['timestamp'] = datetime.datetime.utcnow().isoformat()  # Add timestamp
    producer.send('purchase', value=data)
    producer.flush()
    response = make_response('', 200)
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response

# Handle "getAllUserBuys" request
@app.route('/getAllUserBuys', methods=['GET'])
def get_all_user_buys():
    try:
        management_service_host = os.getenv('MANAGEMENT_SERVICE_HOST')
        management_service_port = os.getenv('MANAGEMENT_SERVICE_PORT')

        if not management_service_host or not management_service_port:
            raise ValueError("MANAGEMENT_SERVICE_HOST and MANAGEMENT_SERVICE_PORT environment variables must be set")

        response = requests.get(f'http://{management_service_host}:{management_service_port}/purchases')
        response.raise_for_status()
        json_response = jsonify(response.json())
        json_response.headers['Access-Control-Allow-Origin'] = '*'
        return json_response
    except requests.exceptions.RequestException as e:
        response = make_response(str(e), 500)
        response.headers['Access-Control-Allow-Origin'] = '*'
        return response

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port)