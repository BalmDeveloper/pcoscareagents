import multiprocessing

# Server socket
bind = '0.0.0.0:8000'

# Worker processes
workers = min(multiprocessing.cpu_count() * 2 + 1, 4)
worker_class = 'uvicorn.workers.UvicornWorker'

# Logging
loglevel = 'info'
accesslog = '-'  # Log to stdout
errorlog = '-'   # Log to stderr

# Timeout
timeout = 120
keepalive = 5
