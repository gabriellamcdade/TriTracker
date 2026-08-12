import csv

run_distance = 0
run_duration = 0
bike_distance = 0
bike_duration = 0

with open("data/activities.csv", "r", newline="") as file:
    activities = csv.DictReader(file)

    for activity in activities:
        sport = activity["sport"]
        distance = float(activity["distance_km"])
        duration = float(activity["duration_min"])

        if sport == "Run":
            run_distance += distance
            run_duration += duration

        elif sport == "Bike":
            bike_distance += distance
            bike_duration += duration

run_pace = run_duration / run_distance
bike_speed = bike_distance / (bike_duration / 60)

print("TRITRACKER SUMMARY")
print("\nRUNNING")
print(f"Distance: {run_distance:.1f} km")
print(f"Average pace: {run_pace:.2f} min/km")

print("\nCYCLING")
print(f"Distance: {bike_distance:.1f} km")
print(f"Average speed: {bike_speed:.1f} km/h")