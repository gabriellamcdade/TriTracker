import csv
from collections import defaultdict

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