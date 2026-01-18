import psutil
import time # <-- NEW: Import time for manual latency calculation
from flask import Flask, render_template, request
from prometheus_client import generate_latest, Counter, Histogram, Gauge, CONTENT_TYPE_LATEST

app = Flask(__name__)

# --- 1. Define Prometheus Metrics ---

# Standard HTTP Metrics
REQUEST_COUNT = Counter(
    'http_requests_total', 'Total number of HTTP requests',
    ['method', 'endpoint', 'http_status']
)

REQUEST_LATENCY = Histogram(
    'http_request_duration_seconds', 'HTTP request latency in seconds',
    ['method', 'endpoint']
)

IN_PROGRESS_REQUESTS = Gauge(
    'http_requests_in_progress', 'Number of requests currently being processed',
    ['method', 'endpoint']
)

# Application-Specific Metrics (System Metrics)
APP_CPU_USAGE = Gauge(
    'app_host_cpu_usage_percent', 'Current CPU usage percentage of the host machine'
)

APP_MEMORY_USAGE = Gauge(
    'app_host_memory_usage_percent', 'Current Memory usage percentage of the host machine'
)


# --- 2. Request Handling Middleware for Standard Metrics ---

@app.before_request
def before_request():
    # FIX: Store the start time in seconds since the epoch
    request.start_time = time.time()
    IN_PROGRESS_REQUESTS.labels(request.method, request.path).inc()

@app.after_request
def after_request(response):
    # FIX: Calculate the duration and pass it to the Histogram's observe method
    request_latency = time.time() - request.start_time
    
    REQUEST_LATENCY.labels(
        method=request.method,
        endpoint=request.path
    ).observe(request_latency)
    
    # Decrement the in-progress gauge
    IN_PROGRESS_REQUESTS.labels(request.method, request.path).dec()
    
    # Increment the total request counter
    REQUEST_COUNT.labels(
        method=request.method,
        endpoint=request.path,
        http_status=response.status_code
    ).inc()
    
    return response

# --- 3. Production Readiness Probes (Liveness & Readiness) ---

@app.route('/healthz') # Liveness Check
def healthz():
    """Kubernetes liveness probe: indicates if the application is running."""
    # A 200 OK means the process is alive.
    return {"status": "UP"}, 200

@app.route('/readyz') # Readiness Check
def readyz():
    """Kubernetes readiness probe: indicates if the application is ready to receive traffic."""
    # In a real application, you might check external dependencies (DB connection, etc.) here.
    # For now, if the process is up, we assume it's ready.
    return {"status": "READY"}, 200

# --- 4. Monitoring Endpoint for Prometheus ---

@app.route('/metrics')
def metrics():
    """Exposes metrics for Prometheus to scrape."""
    # Collect system metrics right before scraping
    cpu_metric = psutil.cpu_percent(interval=None) 
    mem_metric = psutil.virtual_memory().percent
    APP_CPU_USAGE.set(cpu_metric)
    APP_MEMORY_USAGE.set(mem_metric)
    
    return generate_latest(), 200, {'Content-Type': CONTENT_TYPE_LATEST}


# --- 5. Your Application's Root Endpoint ---

@app.route("/")
def index():
    # System metrics are collected in the /metrics endpoint logic now, 
    # but we can collect them again here to display to the user.
    cpu_metric = psutil.cpu_percent(interval=None)
    mem_metric = psutil.virtual_memory().percent
    
    Message = None
    if cpu_metric > 80 or mem_metric > 80:
        Message = "High CPU or Memory Detected, scale up!!!"
        
    return render_template("index.html", cpu_metric=cpu_metric, mem_metric=mem_metric, message=Message)

if __name__=='__main__':
    # NOTE: For production, you must use a WSGI server like Gunicorn.
    # For local testing, keep the Flask development server:
    # app.run(debug=True, host='0.0.0.0', port=5000)
    
    # We will use Gunicorn in the Dockerfile, but for completeness:
    print("Running Flask development server for local testing. Use Gunicorn in production.")
    app.run(debug=True, host='0.0.0.0')