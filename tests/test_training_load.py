from src.training_load import build_weekly_data


def test_build_weekly_data():
    activities = [
        {
            "date": "2026-08-01",
            "sport": "Run",
            "distance_km": 5.0,
            "duration_min": 30,
            "avg_hr": 150
        },
        {
            "date": "2026-08-02",
            "sport": "Bike",
            "distance_km": 20.0,
            "duration_min": 60,
            "avg_hr": 140
        }
    ]

    weekly_data = build_weekly_data(activities)

    week = "2026 - Week 31"

    assert weekly_data[week]["Run"]["distance"] == 5.0
    assert weekly_data[week]["Run"]["duration"] == 30
    assert weekly_data[week]["Run"]["training_load"] == 25.0

    assert weekly_data[week]["Bike"]["distance"] == 20.0
    assert weekly_data[week]["Bike"]["duration"] == 60
    assert weekly_data[week]["Bike"]["training_load"] == 46.666666666666664