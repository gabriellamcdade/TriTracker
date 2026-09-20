def test_sync_deletes_missing_recent_activity(
    monkeypatch,
):
    from datetime import date, timedelta
    from src import strava_sync

    today = date.today()

    two_days_ago = (
        today - timedelta(days=2)
    ).isoformat()

    yesterday = (
        today - timedelta(days=1)
    ).isoformat()

    strava_data = [
        {
            "id": 100,
            "start_date_local":
                f"{two_days_ago}T10:00:00Z",
            "sport_type": "Run",
            "distance": 5000,
            "moving_time": 1800,
            "average_heartrate": 145,
        },
        {
            "id": 102,
            "start_date_local":
                f"{today.isoformat()}T10:00:00Z",
            "sport_type": "Ride",
            "distance": 20000,
            "moving_time": 3600,
            "average_heartrate": 135,
        },
    ]

    local_data = [
        {
            "strava_id": 100,
            "date": two_days_ago,
            "sport": "Run",
            "activity_type": "Outdoor Run",
            "distance_km": 5.0,
            "duration_min": 30,
            "avg_hr": 145,
        },
        {
            "strava_id": 101,
            "date": yesterday,
            "sport": "Run",
            "activity_type": "Outdoor Run",
            "distance_km": 5.0,
            "duration_min": 30,
            "avg_hr": 145,
        },
        {
            "strava_id": 102,
            "date": today.isoformat(),
            "sport": "Bike",
            "activity_type": "Outdoor Ride",
            "distance_km": 20.0,
            "duration_min": 60,
            "avg_hr": 135,
        },
    ]

    deleted_ids = []

    monkeypatch.setattr(
        strava_sync,
        "get_activities_since",
        lambda after_timestamp, per_page:
        strava_data,
    )

    monkeypatch.setattr(
        strava_sync,
        "get_all_activities",
        lambda: local_data,
    )

    monkeypatch.setattr(
        strava_sync,
        "delete_activity",
        lambda strava_id:
            deleted_ids.append(strava_id),
    )

    monkeypatch.setattr(
        strava_sync,
        "initialise_database",
        lambda: None,
    )

    result = (
        strava_sync.sync_strava_activities()
    )

    assert deleted_ids == [101]
    assert result["deleted"] == 1


def test_sync_does_not_delete_activity_outside_fetched_window(
    monkeypatch,
):
    from src import strava_sync

    strava_data = [
        {
            "id": 200,
            "start_date_local":
                "2026-09-10T10:00:00Z",
            "sport_type": "Run",
            "distance": 5000,
            "moving_time": 1800,
            "average_heartrate": 145,
        },
        {
            "id": 201,
            "start_date_local":
                "2026-09-12T10:00:00Z",
            "sport_type": "Ride",
            "distance": 20000,
            "moving_time": 3600,
            "average_heartrate": 135,
        },
    ]

    local_data = [
        {
            "strava_id": 999,
            "date": "2026-01-01",
            "sport": "Run",
            "activity_type": "Outdoor Run",
            "distance_km": 10.0,
            "duration_min": 60,
            "avg_hr": 140,
        },
    ]

    deleted_ids = []

    monkeypatch.setattr(
        strava_sync,
        "get_activities_since",
        lambda after_timestamp, per_page:
        strava_data,
    )

    monkeypatch.setattr(
        strava_sync,
        "get_all_activities",
        lambda: local_data,
    )

    monkeypatch.setattr(
        strava_sync,
        "insert_activity",
        lambda activity: True,
    )

    monkeypatch.setattr(
        strava_sync,
        "delete_activity",
        lambda strava_id:
            deleted_ids.append(strava_id),
    )

    monkeypatch.setattr(
        strava_sync,
        "initialise_database",
        lambda: None,
    )

    result = (
        strava_sync.sync_strava_activities()
    )

    assert deleted_ids == []
    assert result["deleted"] == 0


def test_sync_updates_changed_activity(
    monkeypatch,
):
    from src import strava_sync

    strava_data = [
        {
            "id": 300,
            "start_date_local":
                "2026-09-15T10:00:00Z",
            "sport_type": "Run",
            "distance": 6000,
            "moving_time": 2100,
            "average_heartrate": 150,
        },
    ]

    local_data = [
        {
            "strava_id": 300,
            "date": "2026-09-15",
            "sport": "Run",
            "activity_type": "Outdoor Run",
            "distance_km": 5.0,
            "duration_min": 30,
            "avg_hr": 145,
        },
    ]

    updated_activities = []

    monkeypatch.setattr(
        strava_sync,
        "get_activities_since",
        lambda after_timestamp, per_page:
        strava_data,
    )

    monkeypatch.setattr(
        strava_sync,
        "get_all_activities",
        lambda: local_data,
    )

    monkeypatch.setattr(
        strava_sync,
        "update_activity",
        lambda activity:
            updated_activities.append(activity),
    )

    monkeypatch.setattr(
        strava_sync,
        "initialise_database",
        lambda: None,
    )

    result = (
        strava_sync.sync_strava_activities()
    )

    assert len(updated_activities) == 1

    updated = updated_activities[0]

    assert updated["strava_id"] == 300
    assert updated["distance_km"] == 6.0
    assert updated["duration_min"] == 35
    assert updated["avg_hr"] == 150

    assert result["updated"] == 1
    assert result["added"] == 0
    assert result["deleted"] == 0

def test_get_activities_since_fetches_multiple_pages(
    monkeypatch,
):
    from src import strava_api

    calls = []

    first_page = [
        {"id": activity_id}
        for activity_id in range(100)
    ]

    second_page = [
        {"id": 100},
        {"id": 101},
    ]

    def fake_authenticated_get(url, params=None):
        calls.append(params)

        if params["page"] == 1:
            return first_page

        if params["page"] == 2:
            return second_page

        return []

    monkeypatch.setattr(
        strava_api,
        "authenticated_get",
        fake_authenticated_get,
    )

    activities = (
        strava_api.get_activities_since(
            after_timestamp=1234567890,
            per_page=100,
        )
    )

    assert len(activities) == 102

    assert calls == [
        {
            "page": 1,
            "per_page": 100,
            "after": 1234567890,
        },
        {
            "page": 2,
            "per_page": 100,
            "after": 1234567890,
        },
    ]