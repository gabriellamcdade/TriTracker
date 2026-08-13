def get_recommendation(profile, recent_sports, recovery_data):
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

    if recovery_data["score"] < 50:
        return {
            "workout_type": "REST",
            "sport": None,
            "duration_min": 0,
            "intensity": "Zone 1 or lower",
            "workout_plan": ["Rest or gentle walking"],
            "reason": "Your recovery score is low.",
            "recovery_score": recovery_data["score"],
        }

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

    return {
        "workout_type": workout_type,
        "sport": recommended_sport,
        "duration_min": duration,
        "intensity": intensity,
        "workout_plan": workout_plan.split("\n"),
        "recent_sport_minutes": actual_minutes,
        "target_sport_minutes": round(target_minutes, 1),
        "race_distance": race_distance,
        "recovery_score": recovery_data["score"],
        "reason": (
            f"{recommended_sport} is furthest below its weekly "
            f"target for your {race_distance} triathlon."
        ),
    }