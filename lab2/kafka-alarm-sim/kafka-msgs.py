#!/usr/bin/env python3

# kafka-msgs.py --bootstrap-servers kafka:9092

import json
import argparse
from confluent_kafka import Consumer, KafkaError

def parse_args():
    parser = argparse.ArgumentParser(description="Kafka Consumer with optional SSL support.")
    parser.add_argument("--bootstrap-servers", required=True, help="Kafka bootstrap server (e.g., 127.0.0.1:9092)")
    parser.add_argument("--ssl-certificate", help="Path to SSL certificate for secure connection (optional)")
    return parser.parse_args()

def create_consumer_config(bootstrap_servers, ssl_certificate):
    config = {
        "bootstrap.servers": bootstrap_servers,
        "group.id": "test-group",
        "auto.offset.reset": "earliest"
    }

    if ssl_certificate:
        config.update({
            "security.protocol": "SSL",
            "ssl.ca.location": ssl_certificate
        })
    else:
        config["security.protocol"] = "PLAINTEXT"

    return config

def consume_messages(consumer, topics):
    print(f"Listening for messages on topics: {topics}")

    try:
        while True:
            msg = consumer.poll(1.0)  # Wait for messages
            if msg is None:
                continue
            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    continue  # End of partition (normal)
                else:
                    print(f"Error: {msg.error()}")
                    break

            # Print message in JSON format
            message_value = msg.value().decode("utf-8")
            try:
                json_message = json.loads(message_value)
                print(f"Received [{msg.topic()}]: {json.dumps(json_message, indent=2)}")
            except json.JSONDecodeError:
                print(f"Received non-JSON message from {msg.topic()}: {message_value}")

    finally:
        consumer.close()

if __name__ == "__main__":
    args = parse_args()
    
    consumer_config = create_consumer_config(args.bootstrap_servers, args.ssl_certificate)
    consumer = Consumer(consumer_config)
    topics = ["rt-anomalies", "nsp-act-action-event","test-topic"]

    consumer.subscribe(topics)
    consume_messages(consumer, topics)
