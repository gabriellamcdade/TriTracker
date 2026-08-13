from src import database


def test_insert_activity(tmp_path, monkeypatch):
    test_database = tmp_path / "test_tritracker.db"
    monkeypatch.setattr(database, "DATABASE_FILE", test_database)

    database.initialise_database()

    activity = {
        "strava_id": 123456,
        "date": "2026-08-12",
        "sport": "Run",
        "distance_km": 8.5,
        "duration_min": 45,
        "avg_hr": 152,
    }

    was_inserted = database.insert_activity(activity)

    assert was_inserted is True


def test_retrieve_activities(tmp_path, monkeypatch):
    test_database = tmp_path / "test_tritracker.db"
    monkeypatch.setattr(database, "DATABASE_FILE", test_database)

    database.initialise_database()

    activity = {
        "strava_id": 123456,
        "date": "2026-08-12",
        "sport": "Run",
        "distance_km": 8.5,
        "duration_min": 45,
        "avg_hr": 152,
    }

    database.insert_activity(activity)
    saved_activities = database.get_all_activities()

    assert len(saved_activities) == 1
    assert saved_activities[0]["strava_id"] == 123456
    assert saved_activities[0]["sport"] == "Run"
    assert saved_activities[0]["distance_km"] == 8.5
    assert saved_activities[0]["avg_hr"] == 152


def test_duplicate_strava_id_is_not_inserted(tmp_path, monkeypatch):
    test_database = tmp_path / "test_tritracker.db"
    monkeypatch.setattr(database, "DATABASE_FILE", test_database)

    database.initialise_database()

    activity = {
        "strava_id": 123456,
        "date": "2026-08-12",
        "sport": "Run",
        "distance_km": 8.5,
        "duration_min": 45,
        "avg_hr": None,
    }

    first_insert = database.insert_activity(activity)
    second_insert = database.insert_activity(activity)

    saved_activities = database.get_all_activities()

    assert first_insert is True
    assert second_insert is False
    assert len(saved_activities) == 1