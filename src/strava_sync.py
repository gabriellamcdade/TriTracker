from src.strava_api import get_activities
from src.strava_data import transform_activity
from src.database import initialise_database, insert_activity


def sync_strava_activities(per_page=50):
    initialise_database()

    strava_activities = get_activities(
        page=1,
        per_page=per_page,
    )

    added = 0
    already_stored = 0
    skipped = 0

    for strava_activity in strava_activities:
        activity = transform_activity(strava_activity)

        if activity is None:
            skipped += 1
            continue

        if insert_activity(activity):
            added += 1
        else:
            already_stored += 1

    return {
        "downloaded": len(strava_activities),
        "added": added,
        "already_stored": already_stored,
        "skipped": skipped,
    }