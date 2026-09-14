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

from datetime import date, timedelta


def test_get_summary_uses_test_activities(monkeypatch):
    today = date.today()
    start_of_week = today - timedelta(days=today.weekday())

    run_date = start_of_week
    bike_date = start_of_week + timedelta(days=1)

    test_activities = [
        {
            "strava_id": 1,
            "date": run_date.isoformat(),
            "sport": "Run",
            "distance_km": 5.0,
            "duration_min": 30,
            "avg_hr": 150,
        },
        {
            "strava_id": 2,
            "date": bike_date.isoformat(),
            "sport": "Bike",
            "distance_km": 20.0,
            "duration_min": 60,
            "avg_hr": 140,
        },
    ]

    monkeypatch.setattr(
        api,
        "get_all_activities",
        lambda: test_activities,
    )

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
def test_get_training_load_uses_test_activities(monkeypatch):
    test_activities = [
        {
            "strava_id": 1,
            "date": "2026-08-01",  # Week 31
            "sport": "Run",
            "distance_km": 5.0,
            "duration_min": 30,
            "avg_hr": 150,
        },
        {
            "strava_id": 2,
            "date": "2026-08-03",  # Week 32
            "sport": "Bike",
            "distance_km": 20.0,
            "duration_min": 60,
            "avg_hr": 150,
        },
    ]

    # Prevents the API route from reading your real SQLite database.
    monkeypatch.setattr(api, "get_all_activities", lambda: test_activities)

    response = client.get("/training-load")

    assert response.status_code == 200

    assert response.json() == [
        {
            "week": "2026 - Week 31",
            "sports": {
                "Run": 25.0
            },
            "total_training_load": 25.0,
            "percentage_change": None,
        },
        {
            "week": "2026 - Week 32",
            "sports": {
                "Bike": 50.0
            },
            "total_training_load": 50.0,
            "percentage_change": 100.0,
        },
    ]

def test_get_recovery_uses_test_activities(monkeypatch):
    test_activities = [
        # Week 31: load = 30 × (150 / 180) = 25
        {
            "strava_id": 1,
            "date": "2026-08-01",
            "sport": "Run",
            "distance_km": 5.0,
            "duration_min": 30,
            "avg_hr": 150,
        },

        # Week 32: load = 60 × (150 / 180) = 50
        {
            "strava_id": 2,
            "date": "2026-08-03",
            "sport": "Bike",
            "distance_km": 20.0,
            "duration_min": 60,
            "avg_hr": 150,
        },
    ]

    # Replaces the database call only while this test runs.
    monkeypatch.setattr(api, "get_all_activities", lambda: test_activities)

    response = client.get("/recovery")

    assert response.status_code == 200

    data = response.json()

    assert data["score"] == 70
    assert data["status"] == "GOOD"
    assert data["recommendation"] == "MODERATE"
    assert data["recent_week"] == "2026 - Week 32"
    assert data["recent_load"] == 50.0
    assert data["previous_load"] == 25.0
    assert data["load_change"] == 100.0
    assert data["high_intensity_percent"] == 0.0

def test_get_recommendation_uses_test_data(monkeypatch):
    test_activities = [
        {
            "strava_id": 1,
            "date": "2026-08-01",
            "sport": "Run",
            "distance_km": 5.0,
            "duration_min": 30,
            "avg_hr": 150,
        },
        {
            "strava_id": 2,
            "date": "2026-08-03",
            "sport": "Run",
            "distance_km": 25.0,
            "duration_min": 200,
            "avg_hr": 150,
        },
        {
            "strava_id": 3,
            "date": "2026-08-04",
            "sport": "Bike",
            "distance_km": 20.0,
            "duration_min": 50,
            "avg_hr": 150,
        },
        {
            "strava_id": 4,
            "date": "2026-08-05",
            "sport": "Swim",
            "distance_km": 3.0,
            "duration_min": 100,
            "avg_hr": 150,
        },
    ]

    test_profile = {
        "race_distance": "Olympic",
        "weekly_hours": 7.0,
    }

    monkeypatch.setattr(api, "get_all_activities", lambda: test_activities)
    monkeypatch.setattr(api, "load_profile", lambda filename: test_profile)

    response = client.get("/recommendation")

    assert response.status_code == 200

    data = response.json()

    assert data["workout_type"] == "EASY"
    assert data["sport"] == "Bike"
    assert data["duration_min"] == 60
    assert data["intensity"] == "Zone 2"
    assert data["race_distance"] == "Olympic"

def test_summary_excludes_old_activities(monkeypatch):
    from datetime import date, timedelta

    today = date.today()
    start_of_week = today - timedelta(
        days=today.weekday()
    )

    old_date = start_of_week - timedelta(days=1)

    test_activities = [
        {
            "strava_id": 1,
            "date": today.isoformat(),
            "sport": "Run",
            "distance_km": 5.0,
            "duration_min": 30,
            "avg_hr": 150,
        },
        {
            "strava_id": 2,
            "date": old_date.isoformat(),
            "sport": "Bike",
            "distance_km": 40.0,
            "duration_min": 120,
            "avg_hr": 140,
        },
    ]

    monkeypatch.setattr(
        api,
        "get_all_activities",
        lambda: test_activities,
    )

    response = client.get("/summary")

    assert response.status_code == 200

    data = response.json()

    assert data["Run"]["duration_min"] == 30
    assert data["Run"]["distance_km"] == 5.0

    assert data["Bike"]["duration_min"] == 0
    assert data["Bike"]["distance_km"] == 0

    assert data["total_training_minutes"] == 30

def test_strava_sync_endpoint(monkeypatch):
    fake_result = {
        "downloaded": 10,
        "added": 3,
        "already_stored": 6,
        "skipped": 1,
    }

    monkeypatch.setattr(
        api,
        "sync_strava_activities",
        lambda: fake_result,
    )

    response = client.post("/strava/sync")

    assert response.status_code == 200
    assert response.json() == fake_result


def test_get_hr_profile(monkeypatch):
    test_profile = {
        "max_hr": 195,
        "resting_hr": 55,
    }

    monkeypatch.setattr(
        api,
        "get_hr_profile",
        lambda: test_profile,
    )

    response = client.get("/hr-profile")

    assert response.status_code == 200
    assert response.json() == test_profile


def test_update_hr_profile(monkeypatch):
    saved_profile = {}

    def fake_save_hr_profile(profile):
        saved_profile.update(profile)

    monkeypatch.setattr(
        api,
        "save_hr_profile",
        fake_save_hr_profile,
    )

    monkeypatch.setattr(
        api,
        "get_hr_profile",
        lambda: saved_profile,
    )

    response = client.put(
        "/hr-profile",
        json={
            "max_hr": 195,
            "resting_hr": 55,
        },
    )

    assert response.status_code == 200

    assert response.json() == {
        "max_hr": 195,
        "resting_hr": 55,
    }