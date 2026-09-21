from src.database import get_all_activities, insert_activity


DEMO_ACTIVITIES = [
    {
        "strava_id": 900001,
        "date": "2026-08-24",
        "sport": "Run",
        "activity_type": "Outdoor Run",
        "distance_km": 5.2,
        "duration_min": 34,
        "avg_hr": 151,
    },
    {
        "strava_id": 900002,
        "date": "2026-08-25",
        "sport": "Bike",
        "activity_type": "Outdoor Ride",
        "distance_km": 24.0,
        "duration_min": 82,
        "avg_hr": 142,
    },
    {
        "strava_id": 900003,
        "date": "2026-08-27",
        "sport": "Swim",
        "activity_type": "Pool Swim",
        "distance_km": 1.2,
        "duration_min": 34,
        "avg_hr": 136,
    },
    {
        "strava_id": 900004,
        "date": "2026-08-29",
        "sport": "Run",
        "activity_type": "Outdoor Run",
        "distance_km": 7.0,
        "duration_min": 44,
        "avg_hr": 155,
    },
    {
        "strava_id": 900005,
        "date": "2026-08-30",
        "sport": "Bike",
        "activity_type": "Outdoor Ride",
        "distance_km": 32.0,
        "duration_min": 105,
        "avg_hr": 146,
    },

    {
        "strava_id": 900006,
        "date": "2026-09-01",
        "sport": "Swim",
        "activity_type": "Pool Swim",
        "distance_km": 1.4,
        "duration_min": 38,
        "avg_hr": 138,
    },
    {
        "strava_id": 900007,
        "date": "2026-09-02",
        "sport": "Run",
        "activity_type": "Outdoor Run",
        "distance_km": 6.0,
        "duration_min": 37,
        "avg_hr": 153,
    },
    {
        "strava_id": 900008,
        "date": "2026-09-04",
        "sport": "Bike",
        "activity_type": "Outdoor Ride",
        "distance_km": 28.5,
        "duration_min": 91,
        "avg_hr": 144,
    },
    {
        "strava_id": 900009,
        "date": "2026-09-06",
        "sport": "Run",
        "activity_type": "Long Run",
        "distance_km": 9.0,
        "duration_min": 57,
        "avg_hr": 157,
    },

    {
        "strava_id": 900010,
        "date": "2026-09-08",
        "sport": "Swim",
        "activity_type": "Pool Swim",
        "distance_km": 1.5,
        "duration_min": 39,
        "avg_hr": 137,
    },
    {
        "strava_id": 900011,
        "date": "2026-09-09",
        "sport": "Run",
        "activity_type": "Tempo Run",
        "distance_km": 6.5,
        "duration_min": 38,
        "avg_hr": 164,
    },
    {
        "strava_id": 900012,
        "date": "2026-09-11",
        "sport": "Bike",
        "activity_type": "Outdoor Ride",
        "distance_km": 35.0,
        "duration_min": 108,
        "avg_hr": 148,
    },
    {
        "strava_id": 900013,
        "date": "2026-09-13",
        "sport": "Run",
        "activity_type": "Long Run",
        "distance_km": 10.0,
        "duration_min": 61,
        "avg_hr": 158,
    },

    {
        "strava_id": 900014,
        "date": "2026-09-14",
        "sport": "Swim",
        "activity_type": "Open Water Swim",
        "distance_km": 1.6,
        "duration_min": 40,
        "avg_hr": 140,
    },
    {
        "strava_id": 900015,
        "date": "2026-09-16",
        "sport": "Run",
        "activity_type": "Easy Run",
        "distance_km": 5.5,
        "duration_min": 33,
        "avg_hr": 149,
    },
    {
        "strava_id": 900016,
        "date": "2026-09-17",
        "sport": "Bike",
        "activity_type": "Outdoor Ride",
        "distance_km": 40.0,
        "duration_min": 118,
        "avg_hr": 147,
    },
    {
        "strava_id": 900017,
        "date": "2026-09-19",
        "sport": "Swim",
        "activity_type": "Pool Swim",
        "distance_km": 1.5,
        "duration_min": 37,
        "avg_hr": 139,
    },
    {
        "strava_id": 900018,
        "date": "2026-09-20",
        "sport": "Run",
        "activity_type": "Long Run",
        "distance_km": 10.5,
        "duration_min": 62,
        "avg_hr": 156,
    },
]


def seed_demo_data():
    """Add demo activities only when the database has no activities."""

    if get_all_activities():
        return False

    for activity in DEMO_ACTIVITIES:
        insert_activity(activity)

    return True