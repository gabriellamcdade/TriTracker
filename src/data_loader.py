import csv


def load_activities(filename):
    activities = []

    with open(filename, "r", newline="") as file:
        for activity in csv.DictReader(file):
            activity["distance_km"] = float(activity["distance_km"])
            activity["duration_min"] = int(activity["duration_min"])
            activity["avg_hr"] = int(activity["avg_hr"])

            activities.append(activity)

    return activities


def load_profile(filename):
    with open(filename, "r", newline="") as file:
        profile = next(csv.DictReader(file))

    profile["goal_hours"] = float(profile["goal_hours"])
    profile["weekly_hours"] = float(profile["weekly_hours"])

    return profile