from fastapi import FastAPI, Query
from src.database import get_all_activities

app = FastAPI(
    title="TriTracker API",
    description="API for TriTracker training data and analysis",
    version="1.0.0",
)


@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "service": "TriTracker API"
    }
@app.get("/activities")
def get_activities(
    limit: int = Query(default=20, ge=1, le=100)
):
    activities = get_all_activities()
    return activities[:limit]