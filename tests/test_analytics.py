from src.analytics import get_zone


def test_zone_1():
    assert get_zone(119) == "Zone 1"


def test_zone_2():
    assert get_zone(120) == "Zone 2"
    assert get_zone(139) == "Zone 2"


def test_zone_3():
    assert get_zone(140) == "Zone 3"
    assert get_zone(154) == "Zone 3"


def test_zone_4():
    assert get_zone(155) == "Zone 4"
    assert get_zone(169) == "Zone 4"


def test_zone_5():
    assert get_zone(170) == "Zone 5"

def test_build_training_calendar_groups_activities_by_date():
    from src.analytics import build_training_calendar

    activities = [
        {
            "strava_id": 101,
            "date": "2026-09-15",
            "sport": "Run",
            "activity_type": "Outdoor Run",
            "distance_km": 5.0,
            "duration_min": 30,
            "avg_hr": 150,
        },
        {
            "strava_id": 102,
            "date": "2026-09-15",
            "sport": "Bike",
            "activity_type": "Outdoor Ride",
            "distance_km": 20.0,
            "duration_min": 60,
            "avg_hr": 140,
        },
        {
            "strava_id": 103,
            "date": "2026-09-16",
            "sport": "Swim",
            "activity_type": "Pool Swim",
            "distance_km": 1.5,
            "duration_min": 35,
            "avg_hr": 135,
        },
    ]

    calendar = build_training_calendar(activities)

    assert len(calendar["2026-09-15"]) == 2
    assert len(calendar["2026-09-16"]) == 1

    assert calendar["2026-09-15"][0] == {
        "strava_id": 101,
        "sport": "Run",
        "type": "Outdoor Run",
        "distance": 5.0,
        "duration": 30,
        "avg_hr": 150,
    }

    assert calendar["2026-09-15"][1]["sport"] == "Bike"
    assert calendar["2026-09-16"][0]["sport"] == "Swim"