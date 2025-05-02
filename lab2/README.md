# **Lab Guide: Data Transformation & Automation**

Integrating Kafka for real-time network event streaming and transforming data into insightful visualizations and alerts with Grafana and Prometheus. We'll be using Kafka events related to telemetry and alarms from anomaly events coming from advanced analytics as an example.  
At the end of this lab, you should be able to transform data from any sort of source or subscription into useful information to gain better insight into your network state.

---

## Infrastructure Setup

Following are the steps to set up the environment.

Get into the workspace folder for this part of the lab:

```bash
# change into Part 2 directory
cd /workspaces/autocon3-ws-a3/lab2
```

---

## **Kafka-Based Alert Simulation & Export to Prometheus**

This part of the lab focuses on simulating **realistic network alerts** using Kafka producers and exposing them as **Prometheus metrics** using a lightweight Python exporter. The goal is to create a reproducible alert simulation and monitoring environment using Docker.

---

### **1. Build Kafka Producer and Exporter Images**

#### Kafka Alarm Producer
```bash
docker build -t kafka-alarm-producer . -f Dockerfile.kafka-alarm-producer
```

#### Alert Prometheus Exporter
```bash
docker build -t kafka-alert-exporter  . -f Dockerfile.kafka-alert-exporter
```

---

### **2. Start the Kafka + Exporter Stack**

Start the infrastructure using Docker Compose:
```bash
docker compose up -d
```

This will launch:
- Zookeeper
- Kafka broker
- Kafka Alarm Producer (NSP Kafka Message Simulator: Not in the scope of this lab)
- Kafka Alert Exporter (Prometheus endpoint)
- Grafana (including Dashboard and Datasourcer settings)
- Prometheus (includig Target settings)
- Alertmanager (includig Alarm Settings)

---

### **5. Prometheus Exporter**

You can check Kafka connectivity using:
```bash
docker exec -ti kafka-alert-exporter python3 kafka-check.py --bootstrap-servers kafka:9092
```

And see actual messages via:
```bash
docker exec -ti kafka-alert-exporter python3 kafka-msgs.py --bootstrap-servers kafka:9092
``` 

kafka-alert-exporter instance is running `kafka-alert-exporter.py` and consumes messages and translates them into Prometheus metrics.

- Accessible at port 8001 (use port mapping in VSCode for access)
- Defined in `alarms.yml`

Sample metric definition:
```yaml
alarms:
  - topic: 'rt-anomalies'
    partition: 0
    counters:
      anomaly_detected:
        name: 'anomaly_detected'
        description: 'Anomaly detected in real-time telemetry'
        labels: ['neId', 'neName', 'counter']
```

To view logs:
```bash
sudo docker exec -ti kafka-alert-exporter tail -f /app/kafka-alert-exporter.log
```

---

## **Monitoring and Validation**

### **6. View Prometheus**

Access Prometheus UI at port 9095 using VSCode Port mapping link

### **7. Grafana**

Check grafana Dashboard at port 3000 (admin/secret)

### **8. Alert Manager**

Check Alert manager at port 9093. Use port mapping in VSCode to access the link.

## **Cleaning Up**

Stop and remove the containers:
```bash
sudo docker compose down
```

Or kill individual components:
```bash
sudo docker kill kafka-alarm-producer kafka-alert-exporter prometheus alertmanager
```
