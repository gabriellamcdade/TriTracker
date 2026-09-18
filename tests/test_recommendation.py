from src.recommendation import get_recommendation


def test_recommends_easy_bike_when_bike_is_below_target():
    profile = {
        "race_distance": "Olympic",
        "weekly_hours": 7.0,
    }

    recent_sports = {
        "Run": {
            "distance": 25.0,
            "duration": 200,
            "training_load": 170,
        },
        "Bike": {
            "distance": 25.0,
            "duration": 50,
            "training_load": 40,
        },
        "Swim": {
            "distance": 4.0,
            "duration": 100,
            "training_load": 80,
        },
    }

    recovery_data = {
        "score": 68,
    }

    recommendation = get_recommendation(
        profile,
        recent_sports,
        recovery_data,
    )

    assert recommendation["workout_type"] == "EASY"
    assert recommendation["sport"] == "Bike"
    assert recommendation["duration_min"] == 60
    assert recommendation["intensity"] == "Zone 2"

def test_recommendation_uses_goal_weekly_target():
    from src.recommendation import (
        get_recommendation,
    )

    profile = {
        "race_distance": "Olympic",
        "weekly_hours": 20,
    }

    goal = {
        "swim_distance_km": 1.5,
        "bike_distance_km": 40,
        "run_distance_km": 10,
        "weekly_target_hours": 5,
    }

    recent_sports = {
        "Run": {
            "duration": 0,
        },
        "Bike": {
            "duration": 0,
        },
        "Swim": {
            "duration": 0,
        },
    }

    recovery_data = {
        "score": 80,
    }

    recommendation = get_recommendation(
        profile,
        recent_sports,
        recovery_data,
        goal,
    )

    assert recommendation["race_distance"] == "Olympic"
    assert recommendation["sport"] == "Run"
    assert recommendation["target_sport_minutes"] == 96.0