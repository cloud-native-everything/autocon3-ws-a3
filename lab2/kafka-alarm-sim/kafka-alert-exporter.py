#!/usr/bin/env python3

from prometheus_client import start_http_server, Gauge, Counter
import json
import argparse
import sys
import yaml
from datetime import datetime
from kafka import KafkaConsumer, TopicPartition

# Prometheus metrics for alarms
alarm_gauge = {}
alarm_counter = {}

def parse_kafka_message(message):
    try:
        return json.loads(message)
    except json.JSONDecodeError:
        print(f"{datetime.now()} - ERROR: Error decoding JSON from Kafka message")
        return None

def extract_label_value(data, keys):
    """Recursively extract nested values from a JSON object."""
    value = data
    for key in keys.split('.'):
        if isinstance(value, dict):
            value = value.get(key, '')
        else:
            return ''
    return str(value) if value is not None else ''

def find_relevant_data(data, label):
    """Recursively searches for a label in a deeply nested JSON structure."""
    keys = label.split('.')
    value = data
    for key in keys:
        if isinstance(value, dict) and key in value:
            value = value[key]
        elif isinstance(value, dict):
            for sub_key, sub_value in value.items():
                if isinstance(sub_value, dict):
                    result = find_relevant_data(sub_value, '.'.join(keys[keys.index(key):]))
                    if result != '':
                        return result
            return ''
        else:
            return ''
    return str(value) if value is not None else ''

def update_alarms(alert_data, alarm_metrics, debug):
    for key, metric in alarm_metrics.items():
        labels = {}
        for label in metric['labels']:
            prom_label = label.replace('-', '_').replace('.', '_')
            value = find_relevant_data(alert_data, label)
            labels[prom_label] = value
            if debug:
                print(f"{datetime.now()} - DEBUG: Extracted {label} = {value}")
                print(f"{datetime.now()} - DEBUG: Prometheus label {prom_label} = {value}")
        if debug:
            print(f"{datetime.now()} - DEBUG: Updating metric {metric['name']} with labels {labels}")
        try:
            alarm_gauge[metric['name']].labels(**labels).set(1)
            alarm_counter[metric['name']].labels(**labels).inc()
        except ValueError as e:
            print(f"{datetime.now()} - ERROR: Failed to update metric {metric['name']} due to label mismatch: {e}")
            print(f"{datetime.now()} - ERROR: Labels provided: {labels}")

def start_app(bootstrap, cert, port, config, debug, use_ssl):
    start_http_server(int(port))
    print(f"{datetime.now()} - INFO: Prometheus alerts server running on port {port}")

    try:
        consumer = KafkaConsumer(
            bootstrap_servers=[bootstrap],
            security_protocol='SSL' if use_ssl else 'PLAINTEXT',
            ssl_cafile=cert if use_ssl else None
        )
    except Exception as e:
        print(f"{datetime.now()} - ERROR: Error creating Kafka consumer. {e}")
        sys.exit(1)

    topic_partitions = [TopicPartition(alarm['topic'], alarm['partition']) for alarm in config['alarms']]
    consumer.assign(topic_partitions)

    for alarm in config['alarms']:
        for alarm_name, alarm_info in alarm['counters'].items():
            sanitized_labels = [label.replace('-', '_').replace('.', '_') for label in alarm_info['labels']]
            alarm_gauge[alarm_info['name']] = Gauge(
                alarm_info['name'],
                alarm_info['description'],
                sanitized_labels
            )
            alarm_counter[alarm_info['name']] = Counter(
                f"{alarm_info['name']}_count",
                f"Count of {alarm_info['description']}",
                sanitized_labels
            )

    for message in consumer:
        if debug:
            print(f"{datetime.now()} - DEBUG: Kafka Consumer Message: {message}")
        data = parse_kafka_message(message.value)
        if data:
            for alarm_config in config['alarms']:
                if message.topic == alarm_config['topic']:
                    telemetry_data = data
                    update_alarms(telemetry_data, alarm_config['counters'], debug)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Kafka Alert Exporter to Prometheus')
    parser.add_argument('--bootstrap-servers', required=True, type=str, help='Kafka Bootstrap Server')
    parser.add_argument('--cert', type=str, help='CA certificate path for Kafka')
    parser.add_argument('--port', type=str, default="8001", help='HTTP server port (default: 8001)')
    parser.add_argument('--config', required=True, type=str, help='YAML file with alert topics and metrics')
    parser.add_argument('--debug', action='store_true', help='Activate debug mode')
    parser.add_argument('--plaintext', action='store_true', help='Use plaintext Kafka connection (no SSL)')

    args = parser.parse_args()
    debug = 1 if args.debug else 0
    use_ssl = not args.plaintext

    try:
        with open(args.config, 'r') as file:
            config = yaml.safe_load(file)
    except Exception as e:
        print(f"{datetime.now()} - ERROR: Error reading configuration file: {e}")
        sys.exit()

    start_app(args.bootstrap_servers, args.cert, args.port, config, debug, use_ssl)
