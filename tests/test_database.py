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
def test_save_and_get_goal(monkeypatch, tmp_path):
    database_file = tmp_path / "test_tritracker.db"

    monkeypatch.setattr(
        "src.database.DATABASE_FILE",
        str(database_file),
    )

    from src.database import (
        initialise_goals_table,
        save_goal,
        get_goal,
    )

    initialise_goals_table()

    goal = {
        "race_name": "Test Triathlon",
        "race_date": "2026-10-20",
        "swim_distance_km": 1.5,
        "bike_distance_km": 40,
        "run_distance_km": 10,
        "swim_target_min": 30,
        "bike_target_min": 80,
        "run_target_min": 55,
        "overall_target_min": 175,
    }

    save_goal(goal)

    saved_goal = get_goal()

    assert saved_goal is not None
    assert saved_goal["race_name"] == "Test Triathlon"
    assert saved_goal["race_date"] == "2026-10-20"
    assert saved_goal["swim_distance_km"] == 1.5
    assert saved_goal["bike_distance_km"] == 40
    assert saved_goal["run_distance_km"] == 10
    assert saved_goal["overall_target_min"] == 175

def test_save_goal_updates_existing_goal(
    monkeypatch,
    tmp_path,
):
    database_file = tmp_path / "test_tritracker.db"

    monkeypatch.setattr(
        "src.database.DATABASE_FILE",
        str(database_file),
    )

    from src.database import (
        initialise_goals_table,
        save_goal,
        get_goal,
    )

    initialise_goals_table()

    first_goal = {
        "race_name": "First Race",
        "race_date": "2026-10-20",
        "swim_distance_km": 1.5,
        "bike_distance_km": 40,
        "run_distance_km": 10,
        "swim_target_min": 30,
        "bike_target_min": 80,
        "run_target_min": 55,
        "overall_target_min": 180,
    }

    updated_goal = {
        **first_goal,
        "race_name": "Updated Race",
        "overall_target_min": 170,
    }

    save_goal(first_goal)
    save_goal(updated_goal)

    saved_goal = get_goal()

    assert saved_goal is not None
    assert saved_goal["race_name"] == "Updated Race"
    assert saved_goal["overall_target_min"] == 170