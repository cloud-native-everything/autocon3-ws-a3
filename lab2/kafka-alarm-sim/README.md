# **Kafka Alert Simulator**

This project is a **Kafka-based simulator** that generates and produces **realistic alert messages** based on predefined templates. It mimics the structure and values of actual alert messages used in monitoring and analytics applications.

---

## **Features**
- 📡 **Simulates alerts** from network events and performance monitoring.  
- 🔄 **Uses JSON templates** to generate structured messages dynamically.  
- 📥 **Publishes messages to Kafka topics** for real-time processing.  
- 🎲 **Randomizes values** to simulate different alert conditions.  
- 🔧 **Easy setup with Docker & Python**.

---

## **Steps to Set Up Your Kafka Simulator**
### **1. Install Kafka Locally (Optional)**
If you don't already have Kafka running, you can start a local instance using Docker:
```sh
sudo docker compose up -d
```

---

### **2. Install Required Python Packages**
It is recommended to use a virtual environment to isolate project dependencies. Use the following commands:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Then install the required Kafka library:

```sh
pip install confluent-kafka
```

---

### **3. Run the Kafka Producer**
Once Kafka is running, start the **Kafka producer** to generate messages:

```sh
python3 kafka-producer.py
```

It will start publishing messages to two Kafka topics:
- **rt-anomalies** → Baseline analytics alerts  
- **nsp-act-action-event** → Network event indicators  

Messages are printed in JSON format for visibility.

---

### **4. Run the Kafka Consumer**
To consume messages in real-time:

```sh
python3 kafka-consumer.py
```

This will listen to the configured topics and display incoming alerts.

---

### **Message Structure**
The simulator generates messages based on JSON templates with placeholders dynamically replaced at runtime. Examples include:

- **Baseline Alerts (rt-anomalies)**:
  ```json
  {
    "version": 3,
    "baselineName": "MTCHSD0102M-PIRRSDBW03M - lag-200  - Egress",
    "timestamp": "2025-03-07T23:20:14Z",
    "originalDeviation": "7145154506.0",
    "measured": "340784341918.0",
    "expected": "307927711012.0"
  }
  ```

- **Network Event Alerts (nsp-act-action-event)**:
  ```json
  {
    "data": {
      "ietf-restconf:notification": {
        "nsp-act:action-event": {
          "type": "Threshold-Crossing",
          "rule": "ind_threshold_xxxx",
          "process": "Interface_8.0_increasing",
          "payload": {
            "direction": "FALLING",
            "threshold": "6.0",
            "value": "6.0"
          }
        }
      }
    }
  }
  ```

---

### **Customization**
- JSON **templates** are located in the same directory as the script.
- Modify templates to generate **custom alerts**.
- Adjust **thresholds, timestamps, and randomization logic** as needed.

---

### **✅ Ready to Simulate Kafka Alerts!**
Now your Kafka instance will continuously receive **real-time alert messages** for testing and validation. 🚀