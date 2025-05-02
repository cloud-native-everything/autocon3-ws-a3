#!/usr/bin/env python3

# use: python3 kafka-check.py --bootstrap-servers kafka:9092

import argparse
from confluent_kafka.admin import AdminClient

def check_kafka_connection(bootstrap_servers):
    """Check if Kafka server is accessible using PLAINTEXT connection."""
    try:
        admin_client = AdminClient({
            'bootstrap.servers': bootstrap_servers,
            'security.protocol': 'PLAINTEXT'  # Ensure plaintext connection
        })
        topics = admin_client.list_topics(timeout=5).topics  # Timeout after 5 seconds

        if topics:
            print(f"✅ Kafka server at '{bootstrap_servers}' is accessible over PLAINTEXT.")
            print(f"📜 Available Topics: {', '.join(topics.keys())}")
        else:
            print(f"⚠️ Kafka is accessible, but no topics found.")
    except Exception as e:
        print(f"❌ Failed to connect to Kafka: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Check Kafka Server Accessibility (PLAINTEXT)")
    parser.add_argument("--bootstrap-servers", required=True, help="Kafka bootstrap servers (e.g., kafka:9092)")
    
    args = parser.parse_args()
    check_kafka_connection(args.bootstrap_servers)
