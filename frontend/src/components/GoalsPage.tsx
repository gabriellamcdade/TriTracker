import { useEffect, useState } from "react";
import {
  getGoal,
  saveGoal,
} from "../services/api";
import type { Goal } from "../types";

function formatMinutes(
  minutes: number | null
) {
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

function calculateOverallTarget(
  goal: Goal
) {
  const targets = [
    goal.swim_target_min,
    goal.bike_target_min,
    goal.run_target_min,
  ];

  if (
    targets.some(
      (target) => target === null
    )
  ) {
    return null;
  }

  return targets.reduce(
    (total, target) =>
      total + (target ?? 0),
    0
  );
}

function GoalsPage() {
  const [goal, setGoal] =
    useState<Goal | null>(null);

  const [formGoal, setFormGoal] =
    useState<Goal | null>(null);

  const [loading, setLoading] =
    useState(true);

  const [editing, setEditing] =
    useState(false);

  const [saving, setSaving] =
    useState(false);

  const [error, setError] =
    useState("");

  useEffect(() => {
    async function loadGoal() {
      try {
        const data = await getGoal();

        setGoal(data);
        setFormGoal(data);
      } catch {
        setError(
          "Could not load your race goal."
        );
      } finally {
        setLoading(false);
      }
    }

    loadGoal();
  }, []);

  function updateField(
    field: keyof Goal,
    value: string
  ) {
    if (!formGoal) {
      return;
    }

    const textFields = [
      "race_name",
      "race_date",
    ];

    setFormGoal({
      ...formGoal,
      [field]: textFields.includes(field)
        ? value
        : value === ""
        ? null
        : Number(value),
    });
  }

  async function handleSave() {
    if (!formGoal) {
      return;
    }

    try {
      setSaving(true);
      setError("");

      const overallTarget =
        calculateOverallTarget(formGoal);

      const savedGoal = await saveGoal({
        ...formGoal,
        overall_target_min:
          overallTarget,
      });

      setGoal(savedGoal);
      setFormGoal(savedGoal);
      setEditing(false);
    } catch {
      setError(
        "Could not save your race goal."
      );
    } finally {
      setSaving(false);
    }
  }

  function handleCancel() {
    setFormGoal(goal);
    setEditing(false);
    setError("");
  }

  if (loading) {
    return (
      <p className="muted">
        Loading goal...
      </p>
    );
  }

  if (!goal || !formGoal) {
    return (
      <div>
        <header className="dashboard-header">
          <div>
            <p className="eyebrow">
              TriTracker
            </p>

            <h1>Goals</h1>
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

  const disciplineGoals = [
    {
      sport: "Swim",
      distance:
        goal.swim_distance_km,
      target:
        goal.swim_target_min,
    },
    {
      sport: "Bike",
      distance:
        goal.bike_distance_km,
      target:
        goal.bike_target_min,
    },
    {
      sport: "Run",
      distance:
        goal.run_distance_km,
      target:
        goal.run_target_min,
    },
  ];

  const calculatedFormTarget =
    calculateOverallTarget(formGoal);

  return (
    <div>
      <header className="dashboard-header">
        <div>
          <p className="eyebrow">
            TriTracker
          </p>

          <h1>Goals</h1>

          <p className="subtitle">
            Track your progress towards
            race day.
          </p>
        </div>

        {!editing && (
          <button
            className="goal-edit-button"
            onClick={() =>
              setEditing(true)
            }
          >
            Edit Goal
          </button>
        )}
      </header>

      {error && (
        <p className="goal-error">
          {error}
        </p>
      )}

      {editing ? (
        <section className="dashboard-panel goal-edit-panel">
          <div>
            <p className="panel-label">
              EDIT TARGET
            </p>

            <h2>Race Goal</h2>
          </div>

          <div className="goal-form-grid">

            {/* Race */}

            <label className="goal-form-field">
              <span>Race name</span>

              <input
                type="text"
                value={
                  formGoal.race_name
                }
                onChange={(event) =>
                  updateField(
                    "race_name",
                    event.target.value
                  )
                }
              />
            </label>

            <label className="goal-form-field">
              <span>Race date</span>

              <input
                type="date"
                value={
                  formGoal.race_date ||
                  ""
                }
                onChange={(event) =>
                  updateField(
                    "race_date",
                    event.target.value
                  )
                }
              />
            </label>

            {/* Weekly target */}

            <label className="goal-form-field goal-form-field-full">
              <span>
                Weekly training target
                (hours)
              </span>

              <input
                type="number"
                min="0.5"
                max="30"
                step="0.5"
                value={
                  formGoal.weekly_target_hours
                }
                onChange={(event) =>
                  updateField(
                    "weekly_target_hours",
                    event.target.value
                  )
                }
              />
            </label>

            {/* Swim */}

            <label className="goal-form-field">
              <span>
                Swim distance (km)
              </span>

              <input
                type="number"
                min="0"
                step="0.1"
                value={
                  formGoal.swim_distance_km
                }
                onChange={(event) =>
                  updateField(
                    "swim_distance_km",
                    event.target.value
                  )
                }
              />
            </label>

            <label className="goal-form-field">
              <span>
                Swim target (minutes)
              </span>

              <input
                type="number"
                min="1"
                value={
                  formGoal.swim_target_min ??
                  ""
                }
                onChange={(event) =>
                  updateField(
                    "swim_target_min",
                    event.target.value
                  )
                }
              />
            </label>

            {/* Bike */}

            <label className="goal-form-field">
              <span>
                Bike distance (km)
              </span>

              <input
                type="number"
                min="0"
                step="0.1"
                value={
                  formGoal.bike_distance_km
                }
                onChange={(event) =>
                  updateField(
                    "bike_distance_km",
                    event.target.value
                  )
                }
              />
            </label>

            <label className="goal-form-field">
              <span>
                Bike target (minutes)
              </span>

              <input
                type="number"
                min="1"
                value={
                  formGoal.bike_target_min ??
                  ""
                }
                onChange={(event) =>
                  updateField(
                    "bike_target_min",
                    event.target.value
                  )
                }
              />
            </label>

            {/* Run */}

            <label className="goal-form-field">
              <span>
                Run distance (km)
              </span>

              <input
                type="number"
                min="0"
                step="0.1"
                value={
                  formGoal.run_distance_km
                }
                onChange={(event) =>
                  updateField(
                    "run_distance_km",
                    event.target.value
                  )
                }
              />
            </label>

            <label className="goal-form-field">
              <span>
                Run target (minutes)
              </span>

              <input
                type="number"
                min="1"
                value={
                  formGoal.run_target_min ??
                  ""
                }
                onChange={(event) =>
                  updateField(
                    "run_target_min",
                    event.target.value
                  )
                }
              />
            </label>

          </div>

          <div className="goal-calculated-target">
            <div>
              <span>
                Calculated finish target
              </span>

              <strong>
                {formatMinutes(
                  calculatedFormTarget
                )}
              </strong>
            </div>

            <p className="muted">
              Swim + Bike + Run,
              excluding transitions.
            </p>
          </div>

          <div className="goal-form-actions">
            <button
              className="goal-cancel-button"
              onClick={handleCancel}
              disabled={saving}
            >
              Cancel
            </button>

            <button
              className="goal-save-button"
              onClick={handleSave}
              disabled={saving}
            >
              {saving
                ? "Saving..."
                : "Save Goal"}
            </button>
          </div>
        </section>
      ) : (
        <>
          <section className="dashboard-panel race-goal-card">
            <div>
              <p className="panel-label">
                TARGET RACE
              </p>

              <h2>
                {goal.race_name}
              </h2>

              <p className="muted">
                {goal.race_date ||
                  "Race date not set"}
              </p>
            </div>

            <div className="race-target">
              <span>
                Target finish
              </span>

              <strong>
                {formatMinutes(
                  goal.overall_target_min
                )}
              </strong>

              <small>
                Excluding transitions
              </small>
            </div>
          </section>

          <section className="goal-grid">
            {disciplineGoals.map(
              (item) => (
                <article
                  className="dashboard-panel goal-card"
                  key={item.sport}
                >
                  <p className="panel-label">
                    {item.sport.toUpperCase()}
                  </p>

                  <h2>
                    {item.distance} km
                  </h2>

                  <p className="muted">
                    Target:{" "}
                    {formatMinutes(
                      item.target
                    )}
                  </p>
                </article>
              )
            )}
          </section>

          <section className="dashboard-panel">
            <p className="panel-label">
              TRAINING TARGET
            </p>

            <h2>
              {goal.weekly_target_hours}{" "}
              hours / week
            </h2>

            <p className="muted">
              Used by TriTracker to
              balance your weekly swim,
              bike and run training.
            </p>
          </section>

          <section className="dashboard-panel">
            <p className="panel-label">
              RACE PLAN
            </p>

            <h2>
              Target Breakdown
            </h2>

            <p className="muted">
              Swim{" "}
              {goal.swim_distance_km} km
              {" · "}
              Bike{" "}
              {goal.bike_distance_km} km
              {" · "}
              Run{" "}
              {goal.run_distance_km} km
            </p>
          </section>
        </>
      )}
    </div>
  );
}

export default GoalsPage;