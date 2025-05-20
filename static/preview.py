# preview.py
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pathlib import Path
import uvicorn
import os

app = FastAPI()

# Create necessary directories
os.makedirs("templates", exist_ok=True)
os.makedirs("static/css", exist_ok=True)

# Write a simple HTML template
with open("templates/index.html", "w") as f:
    f.write("""
    <!DOCTYPE html>
    <html>
    <head>
        <title>PCOS Research System - Preview</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
        <style>
            body { padding: 20px; }
            .card { margin: 10px 0; }
            .navbar { margin-bottom: 20px; }
        </style>
    </head>
    <body>
        <nav class="navbar navbar-expand-lg navbar-dark bg-primary">
            <div class="container-fluid">
                <a class="navbar-brand" href="#">PCOS Research System</a>
            </div>
        </nav>

        <div class="container">
            <h1 class="mb-4">Welcome to PCOS Research System</h1>
            
            <div class="row">
                <div class="col-md-4">
                    <div class="card">
                        <div class="card-body">
                            <h5 class="card-title">Research Papers</h5>
                            <p class="display-4">42</p>
                            <a href="#" class="btn btn-primary">View All</a>
                        </div>
                    </div>
                </div>
                <div class="col-md-4">
                    <div class="card">
                        <div class="card-body">
                            <h5 class="card-title">Clinical Trials</h5>
                            <p class="display-4">18</p>
                            <a href="#" class="btn btn-primary">View All</a>
                        </div>
                    </div>
                </div>
                <div class="col-md-4">
                    <div class="card">
                        <div class="card-body">
                            <h5 class="card-title">Treatment Pathways</h5>
                            <p class="display-4">7</p>
                            <a href="#" class="btn btn-primary">View All</a>
                        </div>
                    </div>
                </div>
            </div>

            <div class="card mt-4">
                <div class="card-header">
                    <h5>Recent Research</h5>
                </div>
                <div class="card-body">
                    <ul class="list-group">
                        <li class="list-group-item">
                            <h6>Metformin vs Inositol in PCOS</h6>
                            <p class="mb-1">A comparative study of treatment efficacy</p>
                            <small class="text-muted">Published: 2023-05-15</small>
                        </li>
                        <li class="list-group-item">
                            <h6>Gut Microbiome in PCOS</h6>
                            <p class="mb-1">Analysis of gut microbiome alterations</p>
                            <small class="text-muted">Published: 2023-04-20</small>
                        </li>
                    </ul>
                </div>
            </div>
        </div>

        <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
    </body>
    </html>
    """)

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return open("templates/index.html").read()

if __name__ == "__main__":
    uvicorn.run("preview:app", host="0.0.0.0", port=8000, reload=True)
    