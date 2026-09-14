from datetime import date, datetime, timedelta
def get_current_week_activities(activities):
    today = date.today()

    start_of_week = today - timedelta(days=today.weekday())
    end_of_week = start_of_week + timedelta(days=6)

    current_week_activities = []

    for activity in activities:
        activity_date = datetime.strptime(
            activity["date"],
            "%Y-%m-%d"
        ).date()

        if start_of_week <= activity_date <= end_of_week:
            current_week_activities.append(activity)

    return current_week_activities

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

def calculate_training_summary(activities):
    summary = {
        "Run": {
            "distance_km": 0,
            "duration_min": 0,
        },
        "Bike": {
            "distance_km": 0,
            "duration_min": 0,
        },
        "Swim": {
            "distance_km": 0,
            "duration_min": 0,
        },
        "total_training_minutes": 0,
    }

    for activity in activities:
        sport = activity["sport"]

        if sport not in ["Run", "Bike", "Swim"]:
            continue

        summary[sport]["distance_km"] += activity["distance_km"]
        summary[sport]["duration_min"] += activity["duration_min"]
        summary["total_training_minutes"] += activity["duration_min"]

    return summary

def get_recent_activities(activities, days=30):
    today = date.today()
    start_date = today - timedelta(days=days - 1)

    recent_activities = []

    for activity in activities:
        activity_date = datetime.strptime(
            activity["date"],
            "%Y-%m-%d"
        ).date()

        if start_date <= activity_date <= today:
            recent_activities.append(activity)

    return recent_activities

def calculate_performance_summary(activities):
    performance = {
        "Run": {
            "distance_km": 0,
            "duration_min": 0,
            "average_pace_min_per_km": None,
            "average_hr": None,
        },
        "Bike": {
            "distance_km": 0,
            "duration_min": 0,
            "average_speed_kmh": None,
            "average_hr": None,
        },
        "Swim": {
            "distance_km": 0,
            "duration_min": 0,
            "average_pace_min_per_100m": None,
            "average_hr": None,
        },
    }

    heart_rates = {
        "Run": [],
        "Bike": [],
        "Swim": [],
    }

    for activity in activities:
        sport = activity["sport"]

        if sport not in performance:
            continue

        distance = activity["distance_km"]
        duration = activity["duration_min"]
        heart_rate = activity["avg_hr"]

        performance[sport]["distance_km"] += distance
        performance[sport]["duration_min"] += duration

        if heart_rate is not None:
            heart_rates[sport].append(heart_rate)

    run_distance = performance["Run"]["distance_km"]
    run_duration = performance["Run"]["duration_min"]

    if run_distance > 0:
        performance["Run"]["average_pace_min_per_km"] = round(
            run_duration / run_distance,
            2,
        )

    bike_distance = performance["Bike"]["distance_km"]
    bike_duration = performance["Bike"]["duration_min"]

    if bike_duration > 0:
        performance["Bike"]["average_speed_kmh"] = round(
            bike_distance / (bike_duration / 60),
            1,
        )

    swim_distance = performance["Swim"]["distance_km"]
    swim_duration = performance["Swim"]["duration_min"]

    if swim_distance > 0:
        performance["Swim"]["average_pace_min_per_100m"] = round(
            swim_duration / (swim_distance * 10),
            2,
        )

    for sport in heart_rates:
        if heart_rates[sport]:
            performance[sport]["average_hr"] = round(
                sum(heart_rates[sport])
                / len(heart_rates[sport])
            )

    return performance