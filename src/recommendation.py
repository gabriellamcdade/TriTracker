def get_race_distance_from_goal(goal):
    if not goal:
        return None

    swim_distance = goal.get("swim_distance_km", 0)
    bike_distance = goal.get("bike_distance_km", 0)
    run_distance = goal.get("run_distance_km", 0)

    race_distances = {
        "Sprint": {
            "swim": 0.75,
            "bike": 20,
            "run": 5,
        },
        "Olympic": {
            "swim": 1.5,
            "bike": 40,
            "run": 10,
        },
        "Half Ironman": {
            "swim": 1.9,
            "bike": 90,
            "run": 21.1,
        },
        "Ironman": {
            "swim": 3.8,
            "bike": 180,
            "run": 42.2,
        },
    }

    best_match = None
    smallest_difference = float("inf")

    for race_name, distances in race_distances.items():
        difference = (
            abs(swim_distance - distances["swim"])
            + abs(bike_distance - distances["bike"]) / 10
            + abs(run_distance - distances["run"]) / 5
        )

        if difference < smallest_difference:
            smallest_difference = difference
            best_match = race_name

    return best_match


def get_recommendation(
    profile,
    recent_sports,
    recovery_data,
    goal=None,
):
    training_balance = {
        "Sprint": {
            "Run": 0.35,
            "Bike": 0.40,
            "Swim": 0.25,
        },
        "Olympic": {
            "Run": 0.32,
            "Bike": 0.45,
            "Swim": 0.23,
        },
        "Half Ironman": {
            "Run": 0.32,
            "Bike": 0.48,
            "Swim": 0.20,
        },
        "Ironman": {
            "Run": 0.30,
            "Bike": 0.50,
            "Swim": 0.20,
        },
    }

    easy_workouts = {
        "Sprint": {
            "Run": (
                40,
                "10 min  Easy\n"
                "25 min  Zone 2\n"
                "5 min   Easy",
            ),
            "Bike": (
                45,
                "10 min  Easy\n"
                "25 min  Zone 2\n"
                "10 min  Easy",
            ),
            "Swim": (
                35,
                "10 min  Easy\n"
                "20 min  Zone 2\n"
                "5 min   Easy",
            ),
        },
        "Olympic": {
            "Run": (
                50,
                "10 min  Easy\n"
                "30 min  Zone 2\n"
                "10 min  Easy",
            ),
            "Bike": (
                60,
                "15 min  Easy\n"
                "35 min  Zone 2\n"
                "10 min  Easy",
            ),
            "Swim": (
                45,
                "10 min  Easy\n"
                "30 min  Zone 2\n"
                "5 min   Easy",
            ),
        },
        "Half Ironman": {
            "Run": (
                65,
                "10 min  Easy\n"
                "45 min  Zone 2\n"
                "10 min  Easy",
            ),
            "Bike": (
                75,
                "15 min  Easy\n"
                "50 min  Zone 2\n"
                "10 min  Easy",
            ),
            "Swim": (
                55,
                "10 min  Easy\n"
                "40 min  Zone 2\n"
                "5 min   Easy",
            ),
        },
        "Ironman": {
            "Run": (
                75,
                "10 min  Easy\n"
                "55 min  Zone 2\n"
                "10 min  Easy",
            ),
            "Bike": (
                90,
                "15 min  Easy\n"
                "60 min  Zone 2\n"
                "15 min  Easy",
            ),
            "Swim": (
                60,
                "10 min  Easy\n"
                "45 min  Zone 2\n"
                "5 min   Easy",
            ),
        },
    }

    quality_workouts = {
        "Sprint": {
            "Run": (
                45,
                "10 min  Easy\n"
                "25 min  Zone 3\n"
                "10 min  Easy",
            ),
            "Bike": (
                50,
                "10 min  Easy\n"
                "30 min  Zone 3\n"
                "10 min  Easy",
            ),
            "Swim": (
                40,
                "10 min  Easy\n"
                "25 min  Zone 3\n"
                "5 min   Easy",
            ),
        },
        "Olympic": {
            "Run": (
                60,
                "15 min  Easy\n"
                "30 min  Zone 3\n"
                "15 min  Easy",
            ),
            "Bike": (
                70,
                "15 min  Easy\n"
                "40 min  Zone 3\n"
                "15 min  Easy",
            ),
            "Swim": (
                50,
                "10 min  Easy\n"
                "35 min  Zone 3\n"
                "5 min   Easy",
            ),
        },
        "Half Ironman": {
            "Run": (
                70,
                "15 min  Easy\n"
                "40 min  Zone 3\n"
                "15 min  Easy",
            ),
            "Bike": (
                85,
                "15 min  Easy\n"
                "55 min  Zone 3\n"
                "15 min  Easy",
            ),
            "Swim": (
                60,
                "10 min  Easy\n"
                "45 min  Zone 3\n"
                "5 min   Easy",
            ),
        },
        "Ironman": {
            "Run": (
                80,
                "15 min  Easy\n"
                "50 min  Zone 3\n"
                "15 min  Easy",
            ),
            "Bike": (
                100,
                "15 min  Easy\n"
                "70 min  Zone 3\n"
                "15 min  Easy",
            ),
            "Swim": (
                70,
                "10 min  Easy\n"
                "55 min  Zone 3\n"
                "5 min   Easy",
            ),
        },
    }

    race_distance = get_race_distance_from_goal(
        goal
    )

    if race_distance is None:
        race_distance = profile[
            "race_distance"
        ]

    if (
            goal
            and goal.get("weekly_target_hours")
            is not None
    ):
        weekly_target_hours = goal[
            "weekly_target_hours"
        ]
    else:
        weekly_target_hours = profile[
            "weekly_hours"
        ]

    weekly_target_minutes = (
            weekly_target_hours * 60
    )

    recent_sport_minutes = {
        "Run": 0,
        "Bike": 0,
        "Swim": 0,
    }

    for sport, values in recent_sports.items():
        if sport in recent_sport_minutes:
            recent_sport_minutes[sport] = (
                values["duration"]
            )

    balance_scores = {}

    for sport in [
        "Run",
        "Bike",
        "Swim",
    ]:
        target_minutes = (
            weekly_target_minutes
            * training_balance[
                race_distance
            ][sport]
        )

        actual_minutes = (
            recent_sport_minutes[sport]
        )

        if target_minutes > 0:
            balance_scores[sport] = (
                actual_minutes
                / target_minutes
            )
        else:
            balance_scores[sport] = 0

    recommended_sport = min(
        balance_scores,
        key=balance_scores.get,
    )

    if recovery_data["score"] < 50:
        return {
            "workout_type": "REST",
            "sport": None,
            "duration_min": 0,
            "intensity": "Zone 1 or lower",
            "workout_plan": [
                "Rest or gentle walking"
            ],
            "reason":
                "Your recovery score is low.",
            "recovery_score":
                recovery_data["score"],
        }

    if recovery_data["score"] >= 70:
        workout_type = "QUALITY"

        duration, workout_plan = (
            quality_workouts[
                race_distance
            ][recommended_sport]
        )

        intensity = "Zone 3"

    else:
        workout_type = "EASY"

        duration, workout_plan = (
            easy_workouts[
                race_distance
            ][recommended_sport]
        )

        intensity = "Zone 2"

    target_minutes = (
        weekly_target_minutes
        * training_balance[
            race_distance
        ][recommended_sport]
    )

    actual_minutes = (
        recent_sport_minutes[
            recommended_sport
        ]
    )

    return {
        "workout_type": workout_type,
        "sport": recommended_sport,
        "duration_min": duration,
        "intensity": intensity,
        "workout_plan":
            workout_plan.split("\n"),
        "recent_sport_minutes":
            actual_minutes,
        "target_sport_minutes":
            round(target_minutes, 1),
        "race_distance":
            race_distance,
        "recovery_score":
            recovery_data["score"],
        "reason": (
            f"{recommended_sport} is "
            f"furthest below its weekly "
            f"target for your "
            f"{race_distance} triathlon."
        ),
    }