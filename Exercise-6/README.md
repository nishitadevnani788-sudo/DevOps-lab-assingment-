# Exercise 6: Real-Time Operations Monitoring and Alerting

## Objective

To create a real-time delivery monitoring system for ZAPPTTO using Python, Prometheus, Grafana, Docker, and Jenkins. The system simulates delivery metrics, displays them on dashboards, and generates alerts when delivery performance exceeds defined thresholds.

## Prerequisites

- Docker
- Python 3.10 or higher
- Prometheus
- Grafana
- Jenkins

Install the Python package:

    pip3 install prometheus-client

## Step 1: Create Project Directory

    mkdir delivery_monitoring
    cd delivery_monitoring

Create the following files:

- `delivery_metrics.py`
- `prometheus.yml`
- `alert_rules.yml`
- `Jenkinsfile`
- `Dockerfile`

## Step 2: Create Python Application

Create `delivery_metrics.py`.

    from prometheus_client import start_http_server, Summary, Gauge
    import random
    import time

    total_deliveries = Gauge("total_deliveries", "Total number of deliveries")
    pending_deliveries = Gauge("pending_deliveries", "Number of pending deliveries")
    on_the_way_deliveries = Gauge("on_the_way_deliveries", "Number of deliveries on the way")
    average_delivery_time = Summary("average_delivery_time", "Average delivery time in seconds")

    def simulate_delivery():
        pending = random.randint(10, 20)
        on_the_way = random.randint(5, 20)
        delivered = random.randint(30, 70)
        avg_time = random.uniform(15, 45)

        total = pending + on_the_way + delivered

        print(f"[DEBUG] Total deliveries: {total}")
        print(f"[DEBUG] Pending deliveries: {pending}")
        print(f"[DEBUG] On-the-way deliveries: {on_the_way}")
        print(f"[DEBUG] Average delivery time: {avg_time:.2f} seconds")

        total_deliveries.set(total)
        pending_deliveries.set(pending)
        on_the_way_deliveries.set(on_the_way)
        average_delivery_time.observe(avg_time)

    if __name__ == "__main__":
        print("[INFO] Starting the HTTP server on port 8000...")
        start_http_server(8000, addr="0.0.0.0")

        while True:
            simulate_delivery()
            time.sleep(1)

Run the application:

    python3 delivery_metrics.py

Access the metrics endpoint:

    http://localhost:8000/metrics

You can also check the metrics using:

    curl http://localhost:8000/metrics

## Step 3: Create Dockerfile

Create a file named `Dockerfile`.

    FROM python:3.12-slim

    WORKDIR /app
    COPY delivery_metrics.py .
    RUN pip install prometheus-client
    EXPOSE 8000
    CMD ["python", "delivery_metrics.py"]

Build the Docker image:

    docker build -t delivery_metrics .

Run the application:

    docker run -d --name delivery_metrics -p 8000:8000 delivery_metrics

Verify the container:

    docker ps

## Step 4: Configure Prometheus

Create `prometheus.yml`.

    global:
      scrape_interval: 15s

    rule_files:
      - /etc/prometheus/alert_rules.yml

    scrape_configs:
      - job_name: "prometheus"
        static_configs:
          - targets: ["localhost:9090"]

      - job_name: "delivery_service"
        static_configs:
          - targets: ["host.docker.internal:8000"]

For Linux, `host.docker.internal` may need to be configured using `--add-host=host.docker.internal:host-gateway`, or replaced with an appropriate reachable host address.

## Step 5: Configure Alert Rules

Create `alert_rules.yml`.

    groups:
      - name: delivery_alerts
        rules:
          - alert: HighPendingDeliveries
            expr: pending_deliveries > 10
            for: 15s
            labels:
              severity: warning
            annotations:
              summary: "High pending deliveries"
              description: "Pending deliveries have remained above 10 for 15 seconds."

          - alert: HighAverageDeliveryTime
            expr: (average_delivery_time_sum / average_delivery_time_count) > 30
            for: 15s
            labels:
              severity: critical
            annotations:
              summary: "High average delivery time"
              description: "Average delivery time has remained above 30 seconds."

The first alert triggers when pending deliveries stay above 10 for 15 seconds. The second triggers when the calculated average delivery time stays above 30 seconds for 15 seconds.

## Step 6: Run Prometheus

Run Prometheus using the configuration files:

    docker run -d --name prometheus -p 9090:9090 --add-host=host.docker.internal:host-gateway -v "$(pwd)/prometheus.yml:/etc/prometheus/prometheus.yml" -v "$(pwd)/alert_rules.yml:/etc/prometheus/alert_rules.yml" prom/prometheus

Verify that the container is running:

    docker ps

Open Prometheus:

    http://localhost:9090

Go to **Status → Targets** to verify that the delivery service target is up.

Go to **Alerts** to check the alert rules.

## Step 7: Set Up Grafana

Run Grafana:

    docker run -d --name grafana -p 3000:3000 grafana/grafana

Open Grafana:

    http://localhost:3000

Default login credentials:

- Username: `admin`
- Password: `admin`

Follow the prompts to log in and update the password if required.

### Add Prometheus as a Data Source

1. Open **Connections → Data sources**.
2. Select **Prometheus**.
3. Enter the Prometheus URL. If Grafana is running in Docker on the same Docker network as Prometheus, use `http://prometheus:9090` after attaching both containers to that network. Otherwise, configure a reachable address such as `http://host.docker.internal:9090`.
4. Click **Save & Test**.

### Create a Dashboard

Create a new dashboard and add the following panels:

- Total Deliveries: `total_deliveries`
- Pending Deliveries: `pending_deliveries`
- On-the-Way Deliveries: `on_the_way_deliveries`
- Average Delivery Time: `average_delivery_time_sum / average_delivery_time_count`

Save the dashboard to monitor delivery performance in real time.

## Step 8: Set Up Jenkins

Check whether a Jenkins container already exists:

    docker ps -a | grep jenkins

If an old container exists and you no longer need it, remove it using its container ID or name.

Start Jenkins:

    docker run -d -p 8080:8080 -p 50000:50000 --name jenkins -v jenkins_home:/var/jenkins_home jenkins/jenkins:lts

Open Jenkins:

    http://localhost:8080

Retrieve the initial administrator password:

    docker exec jenkins cat /var/jenkins_home/secrets/initialAdminPassword

Complete the initial setup and install the recommended plugins.

## Step 9: Create Jenkinsfile

Create a file named `Jenkinsfile`.

    pipeline {
        agent any

        stages {
            stage('Pre-check Docker') {
                steps {
                    sh 'docker --version'
                    sh 'docker info'
                }
            }

            stage('Build Docker Image') {
                steps {
                    sh 'docker build -t delivery_metrics .'
                }
            }

            stage('Run Delivery Monitoring') {
                steps {
                    sh '''
                    docker rm -f delivery_metrics || true
                    docker run -d --name delivery_metrics -p 8000:8000 delivery_metrics
                    '''
                }
            }
        }
    }

This pipeline checks Docker, builds the delivery monitoring image, and starts the application container.

**Note:** Jenkins must have access to the Docker CLI and Docker daemon. Configure the Jenkins agent and permissions accordingly. The pipeline above builds and runs the application; Prometheus and Grafana can be started separately using the commands in this README.

### Create a Pipeline Job

1. Open Jenkins.
2. Select **New Item**.
3. Enter a job name.
4. Select **Pipeline** and click **OK**.
5. Under the Pipeline section, select **Pipeline script**.
6. Paste the Jenkinsfile contents.
7. Save and click **Build Now**.
8. Open **Console Output** to check the build logs.

## Step 10: Simulate Alerts

To generate more pending deliveries, modify the following line in `delivery_metrics.py`:

    pending = random.randint(50, 100)

Restart the application so that the updated code takes effect.

Check **Prometheus → Alerts** to verify the high-pending-deliveries alert.

You can also inspect the dashboard in Grafana to observe changes in delivery metrics.

## Expected Outputs

1. Metrics are available at `http://localhost:8000/metrics`.
2. Prometheus is accessible at `http://localhost:9090`.
3. Prometheus successfully scrapes delivery metrics.
4. Grafana is accessible at `http://localhost:3000`.
5. The Grafana dashboard displays total, pending, and on-the-way deliveries and average delivery time.
6. Prometheus detects high pending deliveries and high average delivery time.
7. Jenkins executes the pipeline and displays the build logs.

## Conclusion

In this exercise, a real-time delivery monitoring system was created using Python, Prometheus, Grafana, Docker, and Jenkins. Delivery metrics were simulated, collected by Prometheus, displayed through Grafana dashboards, and monitored using alert rules. Jenkins automated the Docker build and application startup process.