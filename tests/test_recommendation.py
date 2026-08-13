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