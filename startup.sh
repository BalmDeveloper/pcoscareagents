#!/bin/bash

# Install Python dependencies
pip install -r requirements-azure.txt

# Start the FastAPI server
gunicorn -w 4 -k uvicorn.workers.UvicornWorker preview_server:app --bind 0.0.0.0:8000
