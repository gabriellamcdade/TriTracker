from datetime import date, datetime, timedelta

from src.strava_api import get_activities
from src.strava_data import transform_activity
from src.database import (
    initialise_database,
    insert_activity,
    update_activity,
    delete_activity,
    get_all_activities,
)


RECONCILIATION_DAYS = 30


def sync_strava_activities(per_page=50):
    initialise_database()

    strava_activities = get_activities(
        page=1,
        per_page=per_page,
    )
    if not strava_activities:
        return {
            "downloaded": 0,
            "added": 0,
            "updated": 0,
            "deleted": 0,
            "already_stored": 0,
            "skipped": 0,
        }

    transformed_activities = []
    skipped = 0

    for strava_activity in strava_activities:
        activity = transform_activity(
            strava_activity
        )

        if activity is None:
            skipped += 1
            continue

        transformed_activities.append(
            activity
        )

    local_activities = get_all_activities()

    local_by_id = {
        activity["strava_id"]: activity
        for activity in local_activities
    }

    strava_ids = {
        activity["strava_id"]
        for activity in transformed_activities
    }

    added = 0
    updated = 0
    already_stored = 0
    deleted = 0

    # Add new activities and update changed ones.
    for activity in transformed_activities:
        strava_id = activity["strava_id"]

        if strava_id not in local_by_id:
            insert_activity(activity)
            added += 1
            continue

        local_activity = local_by_id[
            strava_id
        ]

        fields_to_compare = [
            "date",
            "sport",
            "activity_type",
            "distance_km",
            "duration_min",
            "avg_hr",
        ]

        has_changed = any(
            local_activity.get(field)
            != activity.get(field)
            for field in fields_to_compare
        )

        if has_changed:
            update_activity(activity)
            updated += 1
        else:
            already_stored += 1

    # Only reconcile deletions from the last 30 days.
    today = date.today()

    reconciliation_start = (
        today
        - timedelta(
            days=RECONCILIATION_DAYS - 1
        )
    )

    for local_activity in local_activities:
        local_date = datetime.strptime(
            local_activity["date"],
            "%Y-%m-%d",
        ).date()

        is_recent = (
            reconciliation_start
            <= local_date
            <= today
        )

        if (
            is_recent
            and local_activity["strava_id"]
            not in strava_ids
        ):
            delete_activity(
                local_activity["strava_id"]
            )
            deleted += 1

    return {
        "downloaded": len(
            strava_activities
        ),
        "added": added,
        "updated": updated,
        "deleted": deleted,
        "already_stored":
            already_stored,
        "skipped": skipped,
    }