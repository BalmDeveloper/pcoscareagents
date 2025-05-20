# preview_server.py
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import os

app = FastAPI()

# Create a static directory if it doesn't exist
os.makedirs("static", exist_ok=True)

# Serve static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Simple HTML template
html_content = """
<!DOCTYPE html>
<html>
<head>
    <title>PCOS Research System - Preview</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        body { padding: 20px; }
        .card { margin: 10px 0; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
        .navbar { margin-bottom: 20px; }
        .stat-card { text-align: center; padding: 20px; border-radius: 10px; color: white; }
        #researchList { max-height: 400px; overflow-y: auto; }
    </style>
</head>
<body>
    <nav class="navbar navbar-expand-lg navbar-dark" style="background-color: #9c27b0;">
        <div class="container-fluid">
            <a class="navbar-brand" href="#">PCOS Research System</a>
            <div class="navbar-nav">
                <a class="nav-link" href="#">Dashboard</a>
                <a class="nav-link" href="#">Research</a>
                <a class="nav-link" href="#">Clinical Trials</a>
                <a class="nav-link" href="#">Analysis</a>
            </div>
        </div>
    </nav>

    <div class="container">
        <h1 class="mb-4">PCOS Research Dashboard</h1>
        
        <div class="row">
            <div class="col-md-4">
                <div class="stat-card" style="background-color: #673ab7;">
                    <h3>Research Papers</h3>
                    <h1>42</h1>
                    <p>Latest: Metformin Study (2023)</p>
                </div>
            </div>
            <div class="col-md-4">
                <div class="stat-card" style="background-color: #3f51b5;">
                    <h3>Clinical Trials</h3>
                    <h1>18</h1>
                    <p>8 Active, 10 Completed</p>
                </div>
            </div>
            <div class="col-md-4">
                <div class="stat-card" style="background-color: #2196f3;">
                    <h3>Treatment Pathways</h3>
                    <h1>7</h1>
                    <p>Metabolic, Hormonal, etc.</p>
                </div>
            </div>
        </div>

        <div class="row mt-4">
            <div class="col-md-8">
                <div class="card">
                    <div class="card-header">
                        <h5 class="mb-0">Recent Research</h5>
                    </div>
                    <div class="card-body" id="researchList">
                        <div class="card mb-3">
                            <div class="card-body">
                                <h5 class="card-title">Metformin vs Inositol in PCOS</h5>
                                <h6 class="card-subtitle mb-2 text-muted">Published: May 15, 2023</h6>
                                <p class="card-text">Comparative study of metformin and inositol in improving insulin resistance in PCOS patients.</p>
                                <a href="#" class="btn btn-sm btn-primary">View Details</a>
                            </div>
                        </div>
                        <div class="card mb-3">
                            <div class="card-body">
                                <h5 class="card-title">Gut Microbiome in PCOS</h5>
                                <h6 class="card-subtitle mb-2 text-muted">Published: April 20, 2023</h6>
                                <p class="card-text">Analysis of gut microbiome alterations in women with PCOS compared to controls.</p>
                                <a href="#" class="btn btn-sm btn-primary">View Details</a>
                            </div>
                        </div>
                        <div class="card">
                            <div class="card-body">
                                <h5 class="card-title">Vitamin D Supplementation</h5>
                                <h6 class="card-subtitle mb-2 text-muted">Published: March 5, 2023</h6>
                                <p class="card-text">Effects of vitamin D supplementation on metabolic parameters in PCOS patients.</p>
                                <a href="#" class="btn btn-sm btn-primary">View Details</a>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            <div class="col-md-4">
                <div class="card">
                    <div class="card-header">
                        <h5 class="mb-0">Quick Actions</h5>
                    </div>
                    <div class="card-body">
                        <div class="d-grid gap-2">
                            <button class="btn btn-primary">Add New Research</button>
                            <button class="btn btn-outline-primary">Run Analysis</button>
                            <button class="btn btn-outline-secondary">Generate Report</button>
                            <button class="btn btn-outline-info">View Statistics</button>
                        </div>
                    </div>
                </div>
                <div class="card mt-4">
                    <div class="card-header">
                        <h5 class="mb-0">Research Focus Areas</h5>
                    </div>
                    <div class="card-body">
                        <div class="mb-2">
                            <span>Metabolic Research</span>
                            <div class="progress" style="height: 20px;">
                                <div class="progress-bar" role="progressbar" style="width: 75%;">75%</div>
                            </div>
                        </div>
                        <div class="mb-2">
                            <span>Hormonal Studies</span>
                            <div class="progress" style="height: 20px;">
                                <div class="progress-bar bg-success" role="progressbar" style="width: 60%;">60%</div>
                            </div>
                        </div>
                        <div class="mb-2">
                            <span>Lifestyle Interventions</span>
                            <div class="progress" style="height: 20px;">
                                <div class="progress-bar bg-info" role="progressbar" style="width: 45%;">45%</div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
    <script>
        // Simple interactive element
        document.addEventListener('DOMContentLoaded', function() {
            const cards = document.querySelectorAll('.card');
            cards.forEach(card => {
                card.addEventListener('mouseenter', function() {
                    this.style.transform = 'translateY(-5px)';
                    this.style.transition = 'transform 0.3s';
                });
                card.addEventListener('mouseleave', function() {
                    this.style.transform = 'translateY(0)';
                });
            });
        });
    </script>
</body>
</html>
"""

@app.get("/", response_class=HTMLResponse)
async def read_root():
    return HTMLResponse(content=html_content, status_code=200)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("preview_server:app", host="0.0.0.0", port=8000, reload=True)