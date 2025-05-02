#!/usr/bin/env python3

import json
import time
import random
import os
import uuid
import re
import yaml
import argparse
import sys
import logging
import threading
from datetime import datetime
from confluent_kafka import Producer

# ---------------------- Logging Setup ----------------------
LOG_FILE = "kafka-alarm-producer.log"
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler(sys.stdout)
    ]
)

# ---------------------- CLI Arguments ----------------------
parser = argparse.ArgumentParser(description="Kafka JSON Template Producer")
parser.add_argument("--config", required=True, help="Path to the YAML config file")
parser.add_argument("--bootstrap-servers", required=True, help="Kafka bootstrap servers (e.g., 127.0.0.1:9092)")
parser.add_argument("--template-dir", required=True, help="Directory containing JSON templates")
args = parser.parse_args()

# ---------------------- Load YAML Config ----------------------
def load_config(config_path):
    if not os.path.exists(config_path):
        logging.error(f"Config file '{config_path}' not found. Exiting...")
        sys.exit(1)
    with open(config_path, "r") as file:
        return yaml.safe_load(file)

config = load_config(args.config)

BOOTSTRAP_SERVERS = args.bootstrap_servers
TEMPLATE_DIR = args.template_dir
TOPIC_MAPPING = config["topics"]
TEMPLATE_CATEGORIES = config["templates"]["categories"]

producer_config = {"bootstrap.servers": BOOTSTRAP_SERVERS}
producer = Producer(producer_config)

logging.info(f"Kafka producer started with config '{args.config}' and bootstrap server '{BOOTSTRAP_SERVERS}'")

# ---------------------- Template Loading ----------------------
def load_templates():
    templates = {category: [] for category in TEMPLATE_CATEGORIES.keys()}
    
    if not os.path.exists(TEMPLATE_DIR):
        logging.error(f"Template directory '{TEMPLATE_DIR}' not found. Exiting...")
        return templates

    for filename in os.listdir(TEMPLATE_DIR):
        if filename.endswith(".json"):
            file_path = os.path.join(TEMPLATE_DIR, filename)
            try:
                with open(file_path, "r") as f:
                    data = json.load(f)
                    for category, conditions in TEMPLATE_CATEGORIES.items():
                        if isinstance(conditions, list):
                            condition_keys = [cond for cond in conditions if isinstance(cond, str)]
                        else:
                            condition_keys = []
                        if all(re.search(cond, json.dumps(data)) for cond in condition_keys):
                            templates[category].append(data)
                            break
            except json.JSONDecodeError:
                logging.warning(f"Skipping invalid JSON file: {filename}")
    return templates

# ---------------------- Placeholder Replacement ----------------------
def process_placeholder(value):
    if value == "{{timestamp}}":
        return datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
    if value == "{{random_string}}":
        return str(uuid.uuid4()).replace("-", "_")
    if "{{choice(" in value:
        choices = re.findall(r"choice\(\[(.*?)\]\)", value)
        if choices:
            options = [opt.strip().strip("'") for opt in choices[0].split(",")]
            return random.choice(options)
    if "{{random(" in value:
        matches = re.findall(r"random\((\d+.?\d*),\s*(\d+.?\d*)\)", value)
        if matches:
            min_val, max_val = map(float, matches[0])
            precision = 4 if "value" in value else 0
            return round(random.uniform(min_val, max_val), precision)
    return value

def replace_placeholders_in_string(value):
    return re.sub(r"\{\{.*?\}\}", lambda m: str(process_placeholder(m.group(0))), value)

def replace_placeholders(data):
    if isinstance(data, dict):
        return {key: replace_placeholders(value) for key, value in data.items()}
    elif isinstance(data, list):
        return [replace_placeholders(item) for item in data]
    elif isinstance(data, str):
        return replace_placeholders_in_string(data)
    return data

# ---------------------- Per-Category Message Sender ----------------------
def send_category_messages(category, templates, topic, time_slot_min, time_slot_max):
    while True:
        if not templates[category]:
            logging.warning(f"No templates found for category '{category}'")
            time.sleep(5)
            continue

        template = random.choice(templates[category])
        modified_message = replace_placeholders(template)

        try:
            producer.produce(topic, key=str(random.randint(1, 1000)), value=json.dumps(modified_message))
            producer.flush()
            logging.info(f"Produced message to topic '{topic}': {json.dumps(modified_message, indent=2)}")
        except Exception as e:
            logging.error(f"Failed to produce message to topic '{topic}': {e}")
        
        sleep_time = random.randint(time_slot_min, time_slot_max)
        logging.info(f"Sleeping for {sleep_time} seconds before next message to '{topic}'...")
        time.sleep(sleep_time)

# ---------------------- Main Message Dispatcher ----------------------
def send_messages():
    templates = load_templates()
    if all(not v for v in templates.values()):
        logging.error("No valid JSON templates found. Exiting...")
        return

    threads = []

    for category in templates:
        topic = TOPIC_MAPPING.get(category, "default-topic")
        time_slot_min = next((cond["timeSlotMin"] for cond in TEMPLATE_CATEGORIES[category] if isinstance(cond, dict) and "timeSlotMin" in cond), 1800)
        time_slot_max = next((cond["timeSlotMax"] for cond in TEMPLATE_CATEGORIES[category] if isinstance(cond, dict) and "timeSlotMax" in cond), 7200)

        thread = threading.Thread(
            target=send_category_messages,
            args=(category, templates, topic, time_slot_min, time_slot_max),
            daemon=True
        )
        thread.start()
        threads.append(thread)
        logging.info(f"Started thread for category '{category}' on topic '{topic}'")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        logging.info("Shutdown requested. Exiting Kafka producer.")

# ---------------------- Entry Point ----------------------
if __name__ == "__main__":
    send_messages()
