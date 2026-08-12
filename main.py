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
    "duration": 0,
    "training_load": 0
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
        heart_rate = int(activity["avg_hr"])
        intensity = heart_rate / 180
        training_load = duration * intensity

        weekly_data[week][sport]["distance"] += distance
        weekly_data[week][sport]["duration"] += duration
        weekly_data[week][sport]["training_load"] += training_load

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

print("\nWEEKLY TRAINING LOAD")

for week, sports in weekly_data.items():
    print(f"\n{week}")

    total_load = 0

    for sport in ["Run", "Bike", "Swim"]:
        if sport in sports:
            load = sports[sport]["training_load"]
            total_load += load

            print(f"\n{sport_titles[sport]}")
            print(f"Training load: {load:.1f}")

    print(f"\nTotal training load: {total_load:.1f}")

print("\nTRAINING LOAD TREND")

# Sort weeks in date order, then number them Week 1, Week 2, etc.
sorted_weeks = sorted(
    weekly_data.items(),
    key=lambda item: (
        int(item[0].split(" - Week ")[0]),
        int(item[0].split(" - Week ")[1])
    )
)

previous_load = None

for position, (week, sports) in enumerate(sorted_weeks, start=1):
    total_load = sum(values["training_load"] for values in sports.values())

    if previous_load is None:
        print(f"Week {position:<4} {total_load:.0f}")

    else:
        percentage_change = ((total_load - previous_load) / previous_load) * 100

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

        arrow = "↑" if percentage_change > 0 else "↓" if percentage_change < 0 else "–"

        print(
            f"Week {position:<4} {total_load:.0f}   "
            f"{arrow} {abs(percentage_change):.1f}% — {interpretation}"
        )

    previous_load = total_load

print("\nACTIVITY INTENSITY")

with open("data/activities.csv", "r", newline="") as file:
    activities = csv.DictReader(file)

    for activity in activities:
        date = activity["date"]
        sport = activity["sport"]
        heart_rate = int(activity["avg_hr"])

        if heart_rate < 120:
            zone = "Zone 1"
        elif heart_rate <= 139:
            zone = "Zone 2"
        elif heart_rate <= 154:
            zone = "Zone 3"
        elif heart_rate <= 169:
            zone = "Zone 4"
        else:
            zone = "Zone 5"

        print(f"{date} | {sport:<4} | {heart_rate} bpm | {zone}")


zone_minutes = {
    "Zone 1": 0,
    "Zone 2": 0,
    "Zone 3": 0,
    "Zone 4": 0,
    "Zone 5": 0,
}

with open("data/activities.csv", "r", newline="") as file:
    activities = csv.DictReader(file)

    for activity in activities:
        heart_rate = int(activity["avg_hr"])
        duration = int(activity["duration_min"])

        if heart_rate < 120:
            zone = "Zone 1"
        elif heart_rate <= 139:
            zone = "Zone 2"
        elif heart_rate <= 154:
            zone = "Zone 3"
        elif heart_rate <= 169:
            zone = "Zone 4"
        else:
            zone = "Zone 5"

        zone_minutes[zone] += duration

total_training_minutes = sum(zone_minutes.values())

print("\nTRAINING INTENSITY DISTRIBUTION\n")

for zone, minutes in zone_minutes.items():
    percentage = (minutes / total_training_minutes) * 100
    print(f"{zone}: {minutes:>4} min   {percentage:>5.1f}%")

print(f"\nTotal: {total_training_minutes:>4} min")

print("\nTRITRACKER RECOVERY")

# Get the most recent two weeks
recent_week, recent_sports = sorted_weeks[-1]
previous_week, previous_sports = sorted_weeks[-2]

recent_load = sum(
    values["training_load"]
    for values in recent_sports.values()
)

previous_load = sum(
    values["training_load"]
    for values in previous_sports.values()
)

# Percentage change from previous week
load_change = (
    (recent_load - previous_load) / previous_load
) * 100

# Work out the percentage of recent-week time spent in Zones 4 and 5
high_intensity_minutes = 0
recent_total_minutes = 0

with open("data/activities.csv", "r", newline="") as file:
    activities = csv.DictReader(file)

    for activity in activities:
        date = datetime.strptime(activity["date"], "%Y-%m-%d")
        iso_date = date.isocalendar()
        activity_week = f"{iso_date.year} - Week {iso_date.week}"

        if activity_week == recent_week:
            duration = int(activity["duration_min"])
            heart_rate = int(activity["avg_hr"])

            recent_total_minutes += duration

            # Zone 4 or Zone 5
            if heart_rate >= 155:
                high_intensity_minutes += duration

high_intensity_percent = (
    high_intensity_minutes / recent_total_minutes
) * 100

# Base recovery score from the latest week's load
if recent_load < 200:
    base_score = 90
elif recent_load < 350:
    base_score = 75
elif recent_load < 500:
    base_score = 55
else:
    base_score = 35

# Penalty for a training-load increase
if load_change < 5:
    load_change_penalty = 0
elif load_change <= 10:
    load_change_penalty = 5
elif load_change <= 15:
    load_change_penalty = 10
elif load_change <= 20:
    load_change_penalty = 15
else:
    load_change_penalty = 20

# Penalty for time spent at high intensity (Zones 4–5)
if high_intensity_percent < 10:
    intensity_penalty = 0
elif high_intensity_percent <= 20:
    intensity_penalty = 5
elif high_intensity_percent <= 30:
    intensity_penalty = 10
else:
    intensity_penalty = 15

# Final recovery score
recovery_score = (
    base_score
    - load_change_penalty
    - intensity_penalty
)

recovery_score = max(0, min(100, recovery_score))

# Status and recommended session intensity
if recovery_score >= 70:
    status = "GOOD"
    recommendation = "MODERATE"
elif recovery_score >= 50:
    status = "CAUTION"
    recommendation = "EASY"
else:
    status = "LOW"
    recommendation = "REST"

# Display the recovery section
print(f"Recovery Score: {recovery_score:.0f} / 100")
print(f"Status: {status}")

print(f"\nRecent Load:       {recent_load:.0f}")
print(f"Previous Week:     {previous_load:.0f}")
print(f"Load Change:       {load_change:+.1f}%")
print(f"High Intensity:    {high_intensity_percent:.0f}%")

print("\n--------------------------------")

if load_change > 15:
    print("\nYour recent training load has increased significantly.")
elif load_change > 0:
    print("\nYour recent training load has increased.")
else:
    print("\nYour recent training load has not increased.")

if high_intensity_percent < 20:
    print("High-intensity training remains moderate.")
else:
    print("High-intensity training is elevated.")

print("\nRecommended intensity:")
print(recommendation)

print("\n========================================")
print("          TRITRACKER RECOMMENDATION")
print("========================================")

# Read the athlete's race profile
with open("data/user_profile.csv", "r", newline="") as file:
    profile = next(csv.DictReader(file))

race_distance = profile["race_distance"]
weekly_hours_target = float(profile["weekly_hours"])

# Target time balance for each race distance
training_balance = {
    "Sprint": {
        "Run": 0.35,
        "Bike": 0.40,
        "Swim": 0.25
    },
    "Olympic": {
        "Run": 0.32,
        "Bike": 0.45,
        "Swim": 0.23
    },
    "Half Ironman": {
        "Run": 0.32,
        "Bike": 0.48,
        "Swim": 0.20
    },
    "Ironman": {
        "Run": 0.30,
        "Bike": 0.50,
        "Swim": 0.20
    }
}

# Minutes trained for each sport in the latest week
recent_sport_minutes = {
    "Run": 0,
    "Bike": 0,
    "Swim": 0
}

for sport, values in recent_sports.items():
    recent_sport_minutes[sport] = values["duration"]

# Find the sport furthest below its target proportion
weekly_target_minutes = weekly_hours_target * 60
balance_scores = {}

for sport in ["Run", "Bike", "Swim"]:
    target_minutes = weekly_target_minutes * training_balance[race_distance][sport]
    actual_minutes = recent_sport_minutes[sport]

    # A lower score means that sport is further behind its target
    balance_scores[sport] = actual_minutes / target_minutes

recommended_sport = min(balance_scores, key=balance_scores.get)

sport_names = {
    "Run": "RUN",
    "Bike": "BIKE",
    "Swim": "SWIM"
}

sport_icons = {
    "Run": "🏃",
    "Bike": "🚴",
    "Swim": "🏊"
}

# Workout plans tailored to the race distance
easy_workouts = {
    "Sprint": {
        "Run": (40, "10 min  Easy\n25 min  Zone 2\n5 min   Easy"),
        "Bike": (45, "10 min  Easy\n25 min  Zone 2\n10 min  Easy"),
        "Swim": (35, "10 min  Easy\n20 min  Zone 2\n5 min   Easy")
    },
    "Olympic": {
        "Run": (50, "10 min  Easy\n30 min  Zone 2\n10 min  Easy"),
        "Bike": (60, "15 min  Easy\n35 min  Zone 2\n10 min  Easy"),
        "Swim": (45, "10 min  Easy\n30 min  Zone 2\n5 min   Easy")
    },
    "Half Ironman": {
        "Run": (65, "10 min  Easy\n45 min  Zone 2\n10 min  Easy"),
        "Bike": (75, "15 min  Easy\n50 min  Zone 2\n10 min  Easy"),
        "Swim": (55, "10 min  Easy\n40 min  Zone 2\n5 min   Easy")
    },
    "Ironman": {
        "Run": (75, "10 min  Easy\n55 min  Zone 2\n10 min  Easy"),
        "Bike": (90, "15 min  Easy\n60 min  Zone 2\n15 min  Easy"),
        "Swim": (60, "10 min  Easy\n45 min  Zone 2\n5 min   Easy")
    }
}

quality_workouts = {
    "Sprint": {
        "Run": (45, "10 min  Easy\n25 min  Zone 3\n10 min  Easy"),
        "Bike": (50, "10 min  Easy\n30 min  Zone 3\n10 min  Easy"),
        "Swim": (40, "10 min  Easy\n25 min  Zone 3\n5 min   Easy")
    },
    "Olympic": {
        "Run": (60, "15 min  Easy\n30 min  Zone 3\n15 min  Easy"),
        "Bike": (70, "15 min  Easy\n40 min  Zone 3\n15 min  Easy"),
        "Swim": (50, "10 min  Easy\n35 min  Zone 3\n5 min   Easy")
    },
    "Half Ironman": {
        "Run": (70, "15 min  Easy\n40 min  Zone 3\n15 min  Easy"),
        "Bike": (85, "15 min  Easy\n55 min  Zone 3\n15 min  Easy"),
        "Swim": (60, "10 min  Easy\n45 min  Zone 3\n5 min   Easy")
    },
    "Ironman": {
        "Run": (80, "15 min  Easy\n50 min  Zone 3\n15 min  Easy"),
        "Bike": (100, "15 min  Easy\n70 min  Zone 3\n15 min  Easy"),
        "Swim": (70, "10 min  Easy\n55 min  Zone 3\n5 min   Easy")
    }
}

# Choose recommendation from recovery score
if recovery_score < 40:
    print("\n🛌 REST DAY")
    print("\nRest or gentle walking")
    print("Intensity: Zone 1 or lower")

    print("\nWHY?")
    print("\nYour recovery score is low.")
    print("Prioritise sleep, food, hydration, and recovery.")

    print("\nRecommended intensity:")
    print("REST")

else:
    if recovery_score >= 70:
        workout_type = "QUALITY"
        duration, workout_plan = quality_workouts[race_distance][recommended_sport]
        intensity = "Zone 3"
    else:
        workout_type = "EASY"
        duration, workout_plan = easy_workouts[race_distance][recommended_sport]
        intensity = "Zone 2"

    print(f"\n{sport_icons[recommended_sport]} {workout_type} "
          f"{sport_names[recommended_sport]}")

    print(f"\nDuration: {duration} minutes")
    print(f"Intensity: {intensity}")

    print(f"\n{workout_plan}")

    target_minutes = (
        weekly_target_minutes *
        training_balance[race_distance][recommended_sport]
    )
    actual_minutes = recent_sport_minutes[recommended_sport]

    print("\nWHY?")
    print(
        f"\nYour recent {recommended_sport.lower()} volume is "
        f"{actual_minutes:.0f} minutes,"
    )
    print(
        f"which is below your {target_minutes:.0f}-minute weekly target"
    )
    print(f"for an {race_distance} triathlon.")

    print(f"\nYour recovery score is {recovery_score:.0f}/100.")

    print("\nRecommended intensity:")
    print(intensity)