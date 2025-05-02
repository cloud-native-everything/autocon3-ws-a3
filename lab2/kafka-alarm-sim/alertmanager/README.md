Here’s a step-by-step guide on how to install Alertmanager, set it up with Docker, and integrate your anomaly detection exporter with an existing Prometheus instance.

---

## **1. Install Alertmanager with Docker**
To install Alertmanager using Docker, follow these steps:

### **Step 1: Pull the Alertmanager Docker Image**
```sh
docker pull prom/alertmanager
```

---

### **Step 2: Run Alertmanager as a Docker Container**
Run Alertmanager and mount the configuration file:

```sh
docker run -d --name=alertmanager \
  -p 9093:9093 \
  prom/alertmanager
```

Now, Alertmanager should be running and listening on port `9093`.

---

## **2. Configure Prometheus to Use Alertmanager**
Modify your Prometheus configuration (`prometheus.yml`) to integrate Alertmanager.

### **Step 1: Open the Prometheus Configuration File**
```sh
nano ~/prometheus/prometheus.yml
```

### **Step 2: Add Alertmanager Configuration**
Find the `alerting` section and modify it as follows:

```yaml
alerting:
  alertmanagers:
    - static_configs:
        - targets:
          - 'alertmanager:9093'  # Make sure this matches your Alertmanager container hostname

rule_files:
  - "alert_rules.yml"  # Create this file to define alerting rules
```

Save and exit (`CTRL + X`, then `Y`, then `ENTER`).

---

### **Step 3: Add Alerting Rules**
Create an alerting rules file:

```sh
nano ~/prometheus/alert_rules.yml
```

Add the following alert rule for anomaly detection and threshold violations:

```yaml
groups:
  - name: anomaly_alerts
    rules:
      - alert: AnomalyDetected
        expr: anomaly_detected > 0
        for: 1m
        labels:
          severity: critical
        annotations:
          summary: "Anomaly detected in {{ $labels.neName }}"
          description: "Anomaly detected for {{ $labels.neName }} with counter {{ $labels.counter }}."

      - alert: ThresholdViolation
        expr: threshold_violation > 0
        for: 1m
        labels:
          severity: warning
        annotations:
          summary: "Threshold Violation in {{ $labels.source_neName }}"
          description: "Threshold {{ $labels.payload_thresholdName }} crossed in {{ $labels.source_neName }}."
```

Save and exit.

---

### **Step 4: Restart Prometheus**
If running Prometheus in Docker, restart it:

```sh
docker restart prometheus
```

If running manually:

```sh
docker run -d --name=prometheus \
  -p 9090:9090 \
  -v ~/prometheus/prometheus.yml:/etc/prometheus/prometheus.yml \
  -v ~/prometheus/alert_rules.yml:/etc/prometheus/alert_rules.yml \
  prom/prometheus --config.file=/etc/prometheus/prometheus.yml
```

---

## **3. Add Your Exporter to Prometheus**
### **Step 1: Modify `prometheus.yml` to Scrape Your Exporter**
Edit the Prometheus config file again:

```sh
nano ~/prometheus/prometheus.yml
```

Add the exporter job to the `scrape_configs` section:

```yaml
scrape_configs:
  - job_name: 'anomaly_exporter'
    static_configs:
      - targets: ['your_exporter_host:port']  # Replace with actual exporter host and port
```

Save and exit.

### **Step 2: Restart Prometheus**
```sh
docker restart prometheus
```

---

## **4. Test the Setup**
### **Check Prometheus Targets**
Visit:
```
http://localhost:9090/targets
```
Ensure the anomaly exporter is listed and UP.

### **Check Alerts**
Visit:
```
http://localhost:9090/alerts
```
Check if anomalies or threshold violations are triggering alerts.

### **Check Alertmanager**
Visit:
```
http://localhost:9093
```
Verify alerts are being received.

### **Verify Microsoft Teams Webhook**
Once an alert is triggered, check your Teams channel to ensure notifications are coming through.

---

## **Summary**
1. Installed Alertmanager via Docker.
2. Configured Alertmanager to send alerts to Microsoft Teams.
3. Modified Prometheus to integrate with Alertmanager.
4. Added alerting rules for anomaly detection.
5. Configured Prometheus to scrape data from the anomaly detection exporter.
6. Restarted services and verified alerts.

Your setup should now be functional! 🚀