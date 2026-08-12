

from src.recovery import calculate_recovery
from src.training_load import build_weekly_data, get_sorted_weeks


def test_calculate_recovery():
    activities = [
        # Week 31: training load = 30 × (150 / 180) = 25
        {
            "date": "2026-08-01",
            "sport": "Run",
            "distance_km": 5.0,
            "duration_min": 30,
            "avg_hr": 150
        },

        # Week 32: training load = 60 × (150 / 180) = 50
        {
            "date": "2026-08-03",
            "sport": "Bike",
            "distance_km": 30.0,
            "duration_min": 60,
            "avg_hr": 150
        }
    ]

    weekly_data = build_weekly_data(activities)
    sorted_weeks = get_sorted_weeks(weekly_data)

    recovery_data = calculate_recovery(activities, sorted_weeks)

    assert recovery_data["recent_load"] == 50.0
    assert recovery_data["previous_load"] == 25.0
    assert recovery_data["load_change"] == 100.0

    # Latest activity is 150 bpm: Zone 3, so no Zone 4–5 minutes
    assert recovery_data["high_intensity_percent"] == 0.0

    # Recent load < 200 = base 90
    # 100% increase = -20 penalty
    # 0% high intensity = -0 penalty
    # Final score = 70
    assert recovery_data["score"] == 70
    assert recovery_data["status"] == "GOOD"
    assert recovery_data["recommendation"] == "MODERATE"