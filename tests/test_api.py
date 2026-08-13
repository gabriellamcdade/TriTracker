from fastapi.testclient import TestClient

import api


client = TestClient(api.app)


def test_get_activities_uses_test_data(monkeypatch):
    test_activities = [
        {
            "strava_id": 1,
            "date": "2026-08-12",
            "sport": "Run",
            "distance_km": 8.5,
            "duration_min": 45,
            "avg_hr": 152,
        },
        {
            "strava_id": 2,
            "date": "2026-08-11",
            "sport": "Bike",
            "distance_km": 25.0,
            "duration_min": 60,
            "avg_hr": None,
        },
    ]

    # Replaces the real database function only for this test.
    monkeypatch.setattr(api, "get_all_activities", lambda: test_activities)

    response = client.get("/activities?limit=1")

    assert response.status_code == 200
    assert response.json() == [test_activities[0]]

def test_get_summary_uses_test_activities(monkeypatch):
    test_activities = [
        {
            "strava_id": 1,
            "date": "2026-08-12",
            "sport": "Run",
            "distance_km": 5.0,
            "duration_min": 30,
            "avg_hr": 150,
        },
        {
            "strava_id": 2,
            "date": "2026-08-11",
            "sport": "Bike",
            "distance_km": 20.0,
            "duration_min": 60,
            "avg_hr": 140,
        },
    ]

    # Prevents the route from using your real SQLite database.
    monkeypatch.setattr(api, "get_all_activities", lambda: test_activities)

    response = client.get("/summary")

    assert response.status_code == 200

    assert response.json() == {
        "Run": {
            "distance_km": 5.0,
            "duration_min": 30,
        },
        "Bike": {
            "distance_km": 20.0,
            "duration_min": 60,
        },
        "Swim": {
            "distance_km": 0,
            "duration_min": 0,
        },
        "total_training_minutes": 90,
    }