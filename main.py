import csv

from collections import defaultdict
from datetime import datetime

run_distance = run_duration = run_hr_total = run_count = 0
bike_distance = bike_duration = bike_hr_total = bike_count = 0
swim_distance = swim_duration = swim_hr_total = swim_count = 0

with open("data/activities.csv", "r", newline="") as file:
    activities = csv.DictReader(file)

    for activity in activities:
        sport = activity["sport"]
        distance = float(activity["distance_km"])
        duration = float(activity["duration_min"])
        heart_rate = int(activity["avg_hr"])

        if sport == "Run":
            run_distance += distance
            run_duration += duration
            run_hr_total += heart_rate
            run_count += 1

        elif sport == "Bike":
            bike_distance += distance
            bike_duration += duration
            bike_hr_total += heart_rate
            bike_count += 1

        elif sport == "Swim":
            swim_distance += distance
            swim_duration += duration
            swim_hr_total += heart_rate
            swim_count += 1

run_pace = run_duration / run_distance
bike_speed = bike_distance / (bike_duration / 60)
swim_pace_per_100m = swim_duration / (swim_distance * 10)

run_avg_hr = run_hr_total / run_count
bike_avg_hr = bike_hr_total / bike_count
swim_avg_hr = swim_hr_total / swim_count

print("TRITRACKER SUMMARY")

print("\nRUNNING")
print(f"Distance: {run_distance:.1f} km")
print(f"Average pace: {run_pace:.2f} min/km")
print(f"Average heart rate: {run_avg_hr:.0f} bpm")

print("\nCYCLING")
print(f"Distance: {bike_distance:.1f} km")
print(f"Average speed: {bike_speed:.1f} km/h")
print(f"Average heart rate: {bike_avg_hr:.0f} bpm")

print("\nSWIMMING")
print(f"Distance: {swim_distance:.1f} km")
print(f"Average pace: {swim_pace_per_100m:.2f} min/100m")
print(f"Average heart rate: {swim_avg_hr:.0f} bpm")


weekly_data = defaultdict(lambda: defaultdict(lambda: {
    "distance": 0,
    "duration": 0
}))

with open("data/activities.csv", "r", newline="") as file:
    activities = csv.DictReader(file)

    for activity in activities:
        date = datetime.strptime(activity["date"], "%Y-%m-%d")
        week_number = date.isocalendar().week
        year = date.isocalendar().year
        week = f"{year} - Week {week_number}"

        sport = activity["sport"]
        distance = float(activity["distance_km"])
        duration = int(activity["duration_min"])

        weekly_data[week][sport]["distance"] += distance
        weekly_data[week][sport]["duration"] += duration

print("\nWEEKLY TRAINING SUMMARY")

sport_titles = {
    "Run": "RUNNING",
    "Bike": "CYCLING",
    "Swim": "SWIMMING",
}

for week, sports in weekly_data.items():
    print(f"\n{week}")

    total_training_time = 0

    for sport in ["Run", "Bike", "Swim"]:
        if sport in sports:
            distance = sports[sport]["distance"]
            duration = sports[sport]["duration"]
            total_training_time += duration

            hours = duration // 60
            minutes = duration % 60

            print(f"\n{sport_titles[sport]}")
            print(f"Distance: {distance:.1f} km")
            print(f"Time: {hours}h {minutes}m")

    total_hours = total_training_time // 60
    total_minutes = total_training_time % 60
    print(f"\nTotal training time: {total_hours}h {total_minutes}m")