import csv

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