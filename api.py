from fastapi import FastAPI, Query
from pydantic import BaseModel, Field
from fastapi.middleware.cors import CORSMiddleware
from src.strava_sync import sync_strava_activities

from src.analytics import (
    calculate_training_summary,
    get_current_week_activities,
)
from src.database import (
    get_all_activities,
    get_goal,
    save_goal,
)
from src.training_load import (
    get_weekly_training_load,
    build_weekly_data,
    get_sorted_weeks,
)
from src.recovery import calculate_recovery
from src.data_loader import load_profile
from src.recommendation import get_recommendation


app = FastAPI(
    title="TriTracker API",
    description="API for TriTracker training data and analysis",
    version="1.0.0",
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
    ],
    allow_credentials=False,
    allow_methods=["GET", "PUT", "POST"],
    allow_headers=["Content-Type"],
)


class GoalInput(BaseModel):
    race_name: str
    race_date: str | None = None

    swim_distance_km: float = Field(gt=0)
    bike_distance_km: float = Field(gt=0)
    run_distance_km: float = Field(gt=0)

    swim_target_min: int | None = Field(default=None, gt=0)
    bike_target_min: int | None = Field(default=None, gt=0)
    run_target_min: int | None = Field(default=None, gt=0)
    overall_target_min: int | None = Field(default=None, gt=0)


@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "service": "TriTracker API",
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

    current_week_activities = get_current_week_activities(
        activities
    )

    return calculate_training_summary(
        current_week_activities
    )


@app.get("/training-load")
def get_training_load():
    activities = get_all_activities()
    return get_weekly_training_load(activities)


@app.get("/recovery")
def get_recovery():
    activities = get_all_activities()

    weekly_data = build_weekly_data(activities)
    sorted_weeks = get_sorted_weeks(weekly_data)

    return calculate_recovery(activities, sorted_weeks)


@app.get("/recommendation")
def get_training_recommendation():
    activities = get_all_activities()

    weekly_data = build_weekly_data(activities)
    sorted_weeks = get_sorted_weeks(weekly_data)

    recovery_data = calculate_recovery(
        activities,
        sorted_weeks,
    )

    profile = load_profile("data/user_profile.csv")

    recent_week, recent_sports = sorted_weeks[-1]

    return get_recommendation(
        profile,
        recent_sports,
        recovery_data,
    )
@app.post("/strava/sync")
def sync_strava():
    return sync_strava_activities()


@app.get("/goals")
def get_goals():
    return get_goal()


@app.put("/goals")
def update_goals(goal: GoalInput):
    save_goal(goal.model_dump())
    return get_goal()