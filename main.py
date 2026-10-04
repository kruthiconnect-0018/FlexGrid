from fastapi import FastAPI

app = FastAPI(
    title="FlexGrid API",
    description="Neighbourhood Energy Flexibility for Reliable Renewable Power",
    version="1.0.0"
)


@app.get("/")
def root():
    return {
        "project": "FlexGrid",
        "status": "online",
        "message": "FlexGrid API is running"
    }


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