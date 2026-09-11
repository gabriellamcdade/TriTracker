import { useEffect, useState } from "react";
import { getGoal } from "../services/api";
import type { Goal } from "../types";

function formatMinutes(minutes: number | null) {
  if (minutes === null) {
    return "Not set";
  }

  const hours = Math.floor(minutes / 60);
  const remainingMinutes = minutes % 60;

  if (hours === 0) {
    return `${remainingMinutes} min`;
  }

  return `${hours}h ${remainingMinutes
    .toString()
    .padStart(2, "0")}m`;
}

function GoalsPage() {
  const [goal, setGoal] = useState<Goal | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function loadGoal() {
      try {
        const data = await getGoal();
        setGoal(data);
      } catch (error) {
        console.error("Could not load goal:", error);
      } finally {
        setLoading(false);
      }
    }

    loadGoal();
  }, []);

  if (loading) {
    return <p className="muted">Loading goal...</p>;
  }

  if (!goal) {
    return (
      <div>
        <header className="dashboard-header">
          <div>
            <p className="eyebrow">TRITRACKER</p>
            <h1>Goals</h1>
            <p className="subtitle">
              Track your progress towards race day.
            </p>
          </div>
        </header>

        <section className="dashboard-panel">
          <p className="muted">
            No race goal has been saved yet.
          </p>
        </section>
      </div>
    );
  }

  const goals = [
    {
      sport: "Swim",
      distance: `${goal.swim_distance_km} km`,
      target: formatMinutes(goal.swim_target_min),
    },
    {
      sport: "Bike",
      distance: `${goal.bike_distance_km} km`,
      target: formatMinutes(goal.bike_target_min),
    },
    {
      sport: "Run",
      distance: `${goal.run_distance_km} km`,
      target: formatMinutes(goal.run_target_min),
    },
  ];

  return (
    <div>
      <header className="dashboard-header">
        <div>
          <p className="eyebrow">TRITRACKER</p>
          <h1>Goals</h1>

          <p className="subtitle">
            Track your progress towards race day.
          </p>
        </div>
      </header>

      <section className="dashboard-panel race-goal-card">
        <div>
          <p className="panel-label">TARGET RACE</p>
          <h2>{goal.race_name}</h2>

          <p className="muted">
            {goal.race_date || "Race date not set"}
          </p>
        </div>

        <div className="race-target">
          <span>Target finish</span>
          <strong>
            {formatMinutes(goal.overall_target_min)}
          </strong>
        </div>
      </section>

      <section className="goal-grid">
        {goals.map((item) => (
          <article
            className="dashboard-panel goal-card"
            key={item.sport}
          >
            <div className="goal-heading">
              <div>
                <p className="panel-label">
                  {item.sport.toUpperCase()}
                </p>

                <h2>{item.distance}</h2>
              </div>
            </div>

            <p className="muted">
              Target: {item.target}
            </p>
          </article>
        ))}
      </section>

      <section className="dashboard-panel">
        <p className="panel-label">RACE PLAN</p>
        <h2>Target Breakdown</h2>

        <p className="muted">
          Swim {goal.swim_distance_km} km · Bike{" "}
          {goal.bike_distance_km} km · Run{" "}
          {goal.run_distance_km} km
        </p>
      </section>
    </div>
  );
}

export default GoalsPage;