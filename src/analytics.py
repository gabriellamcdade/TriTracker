def get_zone(heart_rate):
    if heart_rate < 120:
        return "Zone 1"
    elif heart_rate <= 139:
        return "Zone 2"
    elif heart_rate <= 154:
        return "Zone 3"
    elif heart_rate <= 169:
        return "Zone 4"
    else:
        return "Zone 5"


def print_tritracker_summary(activities):
    run_distance = run_duration = run_hr_total = run_count = 0
    bike_distance = bike_duration = bike_hr_total = bike_count = 0
    swim_distance = swim_duration = swim_hr_total = swim_count = 0

    for activity in activities:
        sport = activity["sport"]
        distance = activity["distance_km"]
        duration = activity["duration_min"]
        heart_rate = activity["avg_hr"]

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


def print_activity_intensity(activities):
    print("\nACTIVITY INTENSITY")

    for activity in activities:
        date = activity["date"]
        sport = activity["sport"]
        heart_rate = activity["avg_hr"]
        zone = get_zone(heart_rate)

        print(f"{date} | {sport:<4} | {heart_rate} bpm | {zone}")


def print_intensity_distribution(activities):
    zone_minutes = {
        "Zone 1": 0,
        "Zone 2": 0,
        "Zone 3": 0,
        "Zone 4": 0,
        "Zone 5": 0,
    }

    for activity in activities:
        zone = get_zone(activity["avg_hr"])
        zone_minutes[zone] += activity["duration_min"]

    total_training_minutes = sum(zone_minutes.values())

    print("\nTRAINING INTENSITY DISTRIBUTION\n")

    for zone, minutes in zone_minutes.items():
        percentage = (minutes / total_training_minutes) * 100
        print(f"{zone}: {minutes:>4} min   {percentage:>5.1f}%")

    print(f"\nTotal: {total_training_minutes:>4} min")