from prometheus_client import start_http_server, Counter
import random
import time

# Define a metric to count requests
REQUEST_COUNT = Counter("app_requests_total", "Total number of requests")

if __name__ == "__main__":
    start_http_server(8000)
    while True:
        REQUEST_COUNT.inc()
        time.sleep(random.uniform(0.5, 2.0))
