from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse


BASE_DIR = Path(__file__).resolve().parent
FRONTEND_DIR = BASE_DIR / "frontend"


app = FastAPI(
    title="FlexGrid API",
    description="Neighbourhood Energy Flexibility for Reliable Renewable Power",
    version="1.0.0"
)


@app.get("/", response_class=FileResponse)
def root():
    return FileResponse(FRONTEND_DIR / "index.html")


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }


@app.get("/about")
def about():
    return {
        "name": "FlexGrid",
        "description": "Neighbourhood Energy Flexibility for Reliable Renewable Power",
        "pipeline": [
            "Solar + Demand",
            "Forecast",
            "Shortfall Detection",
            "Decision Engine",
            "Battery + Flexible Loads",
            "Reliability Evaluation"
        ]
    }