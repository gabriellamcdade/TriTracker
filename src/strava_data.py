def transform_activity(strava_activity):
    sport_mapping = {
        "Run": "Run",
        "TrailRun": "Run",
        "VirtualRun": "Run",
        "Ride": "Bike",
        "MountainBikeRide": "Bike",
        "GravelRide": "Bike",
        "VirtualRide": "Bike",
        "Swim": "Swim",
    }

    type_mapping = {
        "Run": "Outdoor Run",
        "TrailRun": "Trail Run",
        "VirtualRun": "Treadmill",
        "Ride": "Outdoor Ride",
        "MountainBikeRide": "Mountain Bike",
        "GravelRide": "Gravel Ride",
        "VirtualRide": "Indoor Cycle",
        "Swim": "Swim",
    }

    strava_sport = (
        strava_activity.get("sport_type")
        or strava_activity.get("type")
    )

    if strava_sport not in sport_mapping:
        return None

    distance_metres = strava_activity.get("distance", 0)
    moving_time_seconds = strava_activity.get("moving_time", 0)
    start_date_local = strava_activity.get("start_date_local", "")

    average_heartrate = strava_activity.get("average_heartrate")

    activity_type = type_mapping[strava_sport]

    if strava_sport == "Swim":
        if strava_activity.get("trainer"):
            activity_type = "Pool Swim"
        else:
            activity_type = "Open Water Swim"

    return {
        "strava_id": strava_activity["id"],
        "date": start_date_local[:10],
        "sport": sport_mapping[strava_sport],
        "activity_type": activity_type,
        "distance_km": round(distance_metres / 1000, 2),
        "duration_min": round(moving_time_seconds / 60),
        "avg_hr": (
            round(average_heartrate)
            if average_heartrate is not None
            else None
        ),
    }