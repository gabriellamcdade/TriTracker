from src.data_loader import load_activities, load_profile
from src.analytics import (
    print_tritracker_summary,
    print_activity_intensity,
    print_intensity_distribution
)
from src.training_load import (
    build_weekly_data,
    get_sorted_weeks,
    print_weekly_training_summary,
    print_weekly_training_load,
    print_training_load_trend
)
from src.recovery import calculate_recovery, print_recovery
from src.recommendation import print_recommendation


activities = load_activities("data/activities.csv")
profile = load_profile("data/user_profile.csv")

print_tritracker_summary(activities)
print_activity_intensity(activities)
print_intensity_distribution(activities)

weekly_data = build_weekly_data(activities)
sorted_weeks = get_sorted_weeks(weekly_data)

print_weekly_training_summary(weekly_data)
print_weekly_training_load(weekly_data)
print_training_load_trend(sorted_weeks)

recovery_data = calculate_recovery(activities, sorted_weeks)
print_recovery(recovery_data)

recent_week, recent_sports = sorted_weeks[-1]

print_recommendation(
    profile,
    recent_sports,
    recovery_data
)
from src.strava_api import get_authenticated_athlete

try:
    athlete = get_authenticated_athlete()

    print("\nSTRAVA ATHLETE")
    print(f"Name: {athlete['firstname']} {athlete['lastname']}")
    print(f"ID: {athlete['id']}")

except RuntimeError as error:
    print(f"\nStrava error: {error}")

from src.strava_api import get_activities

try:
    activities = get_activities(page=1, per_page=10)

    print("\nLATEST STRAVA ACTIVITIES")

    for activity in activities:
        print(
            f"{activity['start_date_local'][:10]} | "
            f"{activity['name']} | "
            f"{activity['type']}"
        )

except RuntimeError as error:
    print(f"\nStrava error: {error}")
from src.strava_api import get_activities
from src.strava_data import transform_activity

try:
    strava_activities = get_activities(page=1, per_page=10)

    print("\nLATEST STRAVA ACTIVITIES")

    for strava_activity in strava_activities:
        activity = transform_activity(strava_activity)

        if activity is None:
            continue

        heart_rate = (
            f"{activity['avg_hr']} bpm"
            if activity["avg_hr"] is not None
            else "No heart-rate data"
        )

        print(
            f"{activity['date']} | "
            f"{activity['sport']:<4} | "
            f"{activity['distance_km']:.2f} km | "
            f"{activity['duration_min']} min | "
            f"{heart_rate}"
        )

except RuntimeError as error:
    print(f"\nStrava error: {error}")

from src.strava_api import get_activities
from src.strava_data import transform_activity
from src.database import (
    initialise_database,
    insert_activity,
    get_all_activities
)


initialise_database()

strava_activities = get_activities(page=1, per_page=10)

print(f"Downloaded {len(strava_activities)} activities from Strava.")

for strava_activity in strava_activities:
    activity = transform_activity(strava_activity)

    if activity is None:
        print(f"Skipped: {strava_activity['name']}")
        continue

    if insert_activity(activity):
        print(f"Added: {activity['name'] if 'name' in activity else activity['sport']}")
    else:
        print(f"Already stored: {activity['sport']} on {activity['date']}")

saved_activities = get_all_activities()

print(f"\nDatabase contains {len(saved_activities)} activities:")

for activity in saved_activities:
    print(activity)