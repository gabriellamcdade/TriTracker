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