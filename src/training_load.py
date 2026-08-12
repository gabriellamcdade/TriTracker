from collections import defaultdict
from datetime import datetime


SPORTS = ["Run", "Bike", "Swim"]

SPORT_TITLES = {
    "Run": "RUNNING",
    "Bike": "CYCLING",
    "Swim": "SWIMMING",
}


def build_weekly_data(activities):
    weekly_data = defaultdict(lambda: defaultdict(lambda: {
        "distance": 0,
        "duration": 0,
        "training_load": 0
    }))

    for activity in activities:
        date = datetime.strptime(activity["date"], "%Y-%m-%d")
        iso_date = date.isocalendar()
        week = f"{iso_date.year} - Week {iso_date.week}"

        sport = activity["sport"]
        distance = activity["distance_km"]
        duration = activity["duration_min"]
        heart_rate = activity["avg_hr"]

        intensity = heart_rate / 180
        training_load = duration * intensity

        weekly_data[week][sport]["distance"] += distance
        weekly_data[week][sport]["duration"] += duration
        weekly_data[week][sport]["training_load"] += training_load

    return weekly_data


def get_sorted_weeks(weekly_data):
    return sorted(
        weekly_data.items(),
        key=lambda item: (
            int(item[0].split(" - Week ")[0]),
            int(item[0].split(" - Week ")[1])
        )
    )


def print_weekly_training_summary(weekly_data):
    print("\nWEEKLY TRAINING SUMMARY")

    for week, sports in get_sorted_weeks(weekly_data):
        print(f"\n{week}")

        total_training_time = 0

        for sport in SPORTS:
            if sport in sports:
                distance = sports[sport]["distance"]
                duration = sports[sport]["duration"]
                total_training_time += duration

                hours = duration // 60
                minutes = duration % 60

                print(f"\n{SPORT_TITLES[sport]}")
                print(f"Distance: {distance:.1f} km")
                print(f"Time: {hours}h {minutes}m")

        total_hours = total_training_time // 60
        total_minutes = total_training_time % 60

        print(f"\nTotal training time: {total_hours}h {total_minutes}m")


def print_weekly_training_load(weekly_data):
    print("\nWEEKLY TRAINING LOAD")

    for week, sports in get_sorted_weeks(weekly_data):
        print(f"\n{week}")

        total_load = 0

        for sport in SPORTS:
            if sport in sports:
                load = sports[sport]["training_load"]
                total_load += load

                print(f"\n{SPORT_TITLES[sport]}")
                print(f"Training load: {load:.1f}")

        print(f"\nTotal training load: {total_load:.1f}")


def print_training_load_trend(sorted_weeks):
    print("\nTRAINING LOAD TREND")

    previous_load = None

    for position, (week, sports) in enumerate(sorted_weeks, start=1):
        total_load = sum(
            values["training_load"]
            for values in sports.values()
        )

        if previous_load is None:
            print(f"Week {position:<4} {total_load:.0f}")

        else:
            percentage_change = (
                (total_load - previous_load) / previous_load
            ) * 100

            if percentage_change > 15:
                interpretation = "Significant increase"
            elif percentage_change > 0:
                interpretation = "Increase"
            elif percentage_change < -15:
                interpretation = "Significant decrease"
            elif percentage_change < 0:
                interpretation = "Decrease"
            else:
                interpretation = "No change"

            if percentage_change > 0:
                arrow = "↑"
            elif percentage_change < 0:
                arrow = "↓"
            else:
                arrow = "–"

            print(
                f"Week {position:<4} {total_load:.0f}   "
                f"{arrow} {abs(percentage_change):.1f}% "
                f"— {interpretation}"
            )

        previous_load = total_load