def print_recommendation(profile, recent_sports, recovery_data):
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

    race_distance = profile["race_distance"]
    weekly_target_minutes = profile["weekly_hours"] * 60

    recent_sport_minutes = {
        "Run": 0,
        "Bike": 0,
        "Swim": 0
    }

    for sport, values in recent_sports.items():
        recent_sport_minutes[sport] = values["duration"]

    balance_scores = {}

    for sport in ["Run", "Bike", "Swim"]:
        target_minutes = (
            weekly_target_minutes *
            training_balance[race_distance][sport]
        )

        actual_minutes = recent_sport_minutes[sport]
        balance_scores[sport] = actual_minutes / target_minutes

    recommended_sport = min(balance_scores, key=balance_scores.get)

    print("\n========================================")
    print("          TRITRACKER RECOMMENDATION")
    print("========================================")

    # Low recovery means rest instead of a workout
    if recovery_data["score"] < 50:
        print("\n🛌 REST DAY")
        print("\nRest or gentle walking")
        print("Intensity: Zone 1 or lower")

        print("\nWHY?")
        print("\nYour recovery score is low.")
        print("Prioritise sleep, food, hydration, and recovery.")

        print("\nRecommended intensity:")
        print("REST")
        return

    # Good recovery permits a quality workout
    if recovery_data["score"] >= 70:
        workout_type = "QUALITY"
        duration, workout_plan = (
            quality_workouts[race_distance][recommended_sport]
        )
        intensity = "Zone 3"
    else:
        workout_type = "EASY"
        duration, workout_plan = (
            easy_workouts[race_distance][recommended_sport]
        )
        intensity = "Zone 2"

    target_minutes = (
        weekly_target_minutes *
        training_balance[race_distance][recommended_sport]
    )

    actual_minutes = recent_sport_minutes[recommended_sport]

    print(
        f"\n{sport_icons[recommended_sport]} "
        f"{workout_type} {sport_names[recommended_sport]}"
    )

    print(f"\nDuration: {duration} minutes")
    print(f"Intensity: {intensity}")
    print(f"\n{workout_plan}")

    print("\nWHY?")
    print(
        f"\nYour recent {recommended_sport.lower()} volume is "
        f"{actual_minutes:.0f} minutes,"
    )
    print(
        f"while your target is {target_minutes:.0f} minutes "
        f"for an {race_distance} triathlon."
    )
    print(f"\nYour recovery score is {recovery_data['score']:.0f}/100.")

    print("\nRecommended intensity:")
    print(intensity)