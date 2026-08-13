from datetime import datetime


def calculate_recovery(activities, sorted_weeks):
    if len(sorted_weeks) < 2:
        raise ValueError("At least two weeks of activities are needed.")

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

    if previous_load == 0:
        load_change = 0
    else:
        load_change = (
                              (recent_load - previous_load) / previous_load
                      ) * 100

    high_intensity_minutes = 0
    recent_total_minutes = 0

    for activity in activities:
        date = datetime.strptime(activity["date"], "%Y-%m-%d")
        iso_date = date.isocalendar()
        activity_week = f"{iso_date.year} - Week {iso_date.week}"

        if activity_week == recent_week:
            duration = activity["duration_min"]
            heart_rate = activity["avg_hr"]

            recent_total_minutes += duration

            if heart_rate is not None and heart_rate >= 155:
                high_intensity_minutes += duration

    high_intensity_percent = (
        high_intensity_minutes / recent_total_minutes
    ) * 100

    # Base score from current weekly training load
    if recent_load < 200:
        base_score = 90
    elif recent_load < 350:
        base_score = 75
    elif recent_load < 500:
        base_score = 55
    else:
        base_score = 35

    # Penalty from increasing training load
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

    # Penalty from Zone 4–5 time
    if high_intensity_percent < 10:
        intensity_penalty = 0
    elif high_intensity_percent <= 20:
        intensity_penalty = 5
    elif high_intensity_percent <= 30:
        intensity_penalty = 10
    else:
        intensity_penalty = 15

    recovery_score = (
        base_score
        - load_change_penalty
        - intensity_penalty
    )

    recovery_score = max(0, min(100, recovery_score))

    if recovery_score >= 70:
        status = "GOOD"
        recommendation = "MODERATE"
    elif recovery_score >= 50:
        status = "CAUTION"
        recommendation = "EASY"
    else:
        status = "LOW"
        recommendation = "REST"

    return {
        "score": recovery_score,
        "status": status,
        "recommendation": recommendation,
        "recent_week": recent_week,
        "recent_load": recent_load,
        "previous_load": previous_load,
        "load_change": load_change,
        "high_intensity_percent": high_intensity_percent
    }


def print_recovery(recovery_data):
    print("\nTRITRACKER RECOVERY")

    print(f"Recovery Score: {recovery_data['score']:.0f} / 100")
    print(f"Status: {recovery_data['status']}")

    print(f"\nRecent Load:       {recovery_data['recent_load']:.0f}")
    print(f"Previous Week:     {recovery_data['previous_load']:.0f}")
    print(f"Load Change:       {recovery_data['load_change']:+.1f}%")
    print(
        f"High Intensity:    "
        f"{recovery_data['high_intensity_percent']:.0f}%"
    )

    print("\n--------------------------------")

    if recovery_data["load_change"] > 15:
        print("\nYour recent training load has increased significantly.")
    elif recovery_data["load_change"] > 0:
        print("\nYour recent training load has increased.")
    else:
        print("\nYour recent training load has not increased.")

    if recovery_data["high_intensity_percent"] < 20:
        print("High-intensity training remains moderate.")
    else:
        print("High-intensity training is elevated.")

    print("\nRecommended intensity:")
    print(recovery_data["recommendation"])