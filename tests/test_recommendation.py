from src.recommendation import print_recommendation


def test_recommends_easy_bike_when_bike_is_below_target(capsys):
    profile = {
        "race_distance": "Olympic",
        "weekly_hours": 7.0
    }

    recent_sports = {
        "Run": {
            "distance": 25.0,
            "duration": 200,
            "training_load": 170
        },
        "Bike": {
            "distance": 25.0,
            "duration": 50,
            "training_load": 40
        },
        "Swim": {
            "distance": 4.0,
            "duration": 100,
            "training_load": 80
        }
    }

    recovery_data = {
        "score": 68
    }

    print_recommendation(profile, recent_sports, recovery_data)

    output = capsys.readouterr().out

    assert "TRITRACKER RECOMMENDATION" in output
    assert "EASY BIKE" in output
    assert "Duration: 60 minutes" in output
    assert "Intensity: Zone 2" in output