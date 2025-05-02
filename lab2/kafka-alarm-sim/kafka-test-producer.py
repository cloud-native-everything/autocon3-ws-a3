#!/usr/bin/env python3

# use: python3 kafka-test-producer.py --bootstrap-servers kafka:9092 --message "This is a test message"


import json
import argparse
from confluent_kafka import Producer

def delivery_report(err, msg):
    if err is not None:
        print(f"❌ Message delivery failed: {err}")
    else:
        print(f"✅ Message delivered to {msg.topic()} [{msg.partition()}]")




# Parse command-line arguments
parser = argparse.ArgumentParser(description="Kafka Test Producer")
parser.add_argument("--bootstrap-servers", required=True, help="Kafka bootstrap servers (e.g., 127.0.0.1:9092)")
parser.add_argument("--message", required=True, help="Message to send to Kafka")
args = parser.parse_args()

# Kafka producer configuration
producer_config = {"bootstrap.servers": args.bootstrap_servers}
producer = Producer(producer_config)

TOPIC = "test-topic"

# Produce a message
message = {"message": args.message}
producer.produce(TOPIC, key="test-key", value=json.dumps(message), callback=delivery_report)
producer.flush()

print(f"✅ Produced [test-topic]: {json.dumps(message, indent=2)}")