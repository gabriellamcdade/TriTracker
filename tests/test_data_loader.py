import csv

from src.data_loader import load_activities, load_profile


def test_load_activities(tmp_path):
    csv_file = tmp_path / "activities.csv"

    with open(csv_file, "w", newline="") as file:
        writer = csv.writer(file)

        writer.writerow([
            "date",
            "sport",
            "distance_km",
            "duration_min",
            "avg_hr"
        ])

        writer.writerow([
            "2026-08-01",
            "Run",
            "5.2",
            "29",
            "151"
        ])

    activities = load_activities(csv_file)

    assert len(activities) == 1
    assert activities[0]["date"] == "2026-08-01"
    assert activities[0]["sport"] == "Run"
    assert activities[0]["distance_km"] == 5.2
    assert activities[0]["duration_min"] == 29
    assert activities[0]["avg_hr"] == 151


def test_load_profile(tmp_path):
    csv_file = tmp_path / "user_profile.csv"

    with open(csv_file, "w", newline="") as file:
        writer = csv.writer(file)

        writer.writerow([
            "race",
            "race_date",
            "race_distance",
            "goal_hours",
            "weekly_hours"
        ])

        writer.writerow([
            "Barcelona Olympic Triathlon",
            "2026-10-18",
            "Olympic",
            "3",
            "7"
        ])

    profile = load_profile(csv_file)

    assert profile["race"] == "Barcelona Olympic Triathlon"
    assert profile["race_distance"] == "Olympic"
    assert profile["goal_hours"] == 3.0
    assert profile["weekly_hours"] == 7.0