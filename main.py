import csv
from collections import defaultdict
#total  of each sport
totals = defaultdict(float)

with open("data/activities.csv", "r", newline="") as file:
    activities = csv.DictReader(file)

    for activity in activities:
        totals[activity["sport"]] += float(activity["distance_km"])

print("TriTracker Training Summary\n")


names = {
    "Run": "Running",
    "Bike": "Cycling",
    "Swim": "Swimming",
}

for sport, distance in totals.items():
    print(f"{names[sport]}: {distance:.1f} km")
#running pace calc
run_distance = 0
run_duration = 0

with open("data/activities.csv", "r", newline="") as file:
    activities = csv.DictReader(file)

    for activity in activities:
        if activity["sport"] == "Run":
            run_distance += float(activity["distance_km"])
            run_duration += float(activity["duration_min"])

average_pace = run_duration / run_distance

print(f"Average running pace: {average_pace:.2f} min/km")