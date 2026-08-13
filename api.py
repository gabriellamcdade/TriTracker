from fastapi import FastAPI, Query
from src.analytics import calculate_training_summary
from src.database import get_all_activities
from src.training_load import get_weekly_training_load

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

@app.get("/summary")
def get_summary():
    activities = get_all_activities()
    return calculate_training_summary(activities)

@app.get("/training-load")
def get_training_load():
    activities = get_all_activities()
    return get_weekly_training_load(activities)