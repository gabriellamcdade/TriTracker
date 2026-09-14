import { useEffect, useState } from "react";
import {
  getHRProfile,
  saveHRProfile,
} from "../services/api";

import type { HRProfile } from "../types";

type HeartRateZone = {
  name: string;
  range: string;
  description: string;
};

function calculateHeartRateZones(
  profile: HRProfile
): HeartRateZone[] {
  const heartRateReserve =
    profile.max_hr - profile.resting_hr;

  function bpm(percent: number) {
    return Math.round(
      profile.resting_hr +
        heartRateReserve * percent
    );
  }

  return [
    {
      name: "Zone 1",
      range: `${bpm(0.5)}–${bpm(0.6)} bpm`,
      description: "Recovery",
    },
    {
      name: "Zone 2",
      range: `${bpm(0.6)}–${bpm(0.7)} bpm`,
      description: "Easy aerobic",
    },
    {
      name: "Zone 3",
      range: `${bpm(0.7)}–${bpm(0.8)} bpm`,
      description: "Tempo",
    },
    {
      name: "Zone 4",
      range: `${bpm(0.8)}–${bpm(0.9)} bpm`,
      description: "Threshold",
    },
    {
      name: "Zone 5",
      range: `${bpm(0.9)}–${bpm(1.0)} bpm`,
      description: "High intensity",
    },
  ];
}

function SettingsPage() {
  const [profile, setProfile] =
    useState<HRProfile | null>(null);

  const [maxHrInput, setMaxHrInput] =
    useState("");

  const [restingHrInput, setRestingHrInput] =
    useState("");

  const [loading, setLoading] =
    useState(true);

  const [editing, setEditing] =
    useState(false);

  const [saving, setSaving] =
    useState(false);

  const [error, setError] =
    useState("");

  useEffect(() => {
    async function loadProfile() {
      try {
        const data = await getHRProfile();

        setProfile(data);

        if (data) {
          setMaxHrInput(
            data.max_hr.toString()
          );

          setRestingHrInput(
            data.resting_hr.toString()
          );
        } else {
          setEditing(true);
        }
      } catch {
        setError(
          "Could not load your heart rate profile."
        );
      } finally {
        setLoading(false);
      }
    }

    loadProfile();
  }, []);

  async function handleSave() {
    const maxHr = Number(maxHrInput);
    const restingHr =
      Number(restingHrInput);

    if (
      !maxHr ||
      !restingHr ||
      restingHr >= maxHr
    ) {
      setError(
        "Resting heart rate must be lower than maximum heart rate."
      );
      return;
    }

    try {
      setSaving(true);
      setError("");

      const savedProfile =
        await saveHRProfile({
          max_hr: maxHr,
          resting_hr: restingHr,
        });

      setProfile(savedProfile);

      setMaxHrInput(
        savedProfile.max_hr.toString()
      );

      setRestingHrInput(
        savedProfile.resting_hr.toString()
      );

      setEditing(false);
    } catch {
      setError(
        "Could not save your heart rate profile."
      );
    } finally {
      setSaving(false);
    }
  }

  function handleCancel() {
    if (!profile) {
      return;
    }

    setMaxHrInput(
      profile.max_hr.toString()
    );

    setRestingHrInput(
      profile.resting_hr.toString()
    );

    setError("");
    setEditing(false);
  }

  if (loading) {
    return (
      <p className="muted">
        Loading settings...
      </p>
    );
  }

  const zones = profile
    ? calculateHeartRateZones(profile)
    : [];

  return (
    <div>
      <header className="dashboard-header">
        <div>
          <p className="eyebrow">
            TriTracker
          </p>

          <h1>Settings</h1>

          <p className="subtitle">
            Personalise your training data.
          </p>
        </div>

        {profile && !editing && (
          <button
            className="goal-edit-button"
            onClick={() =>
              setEditing(true)
            }
          >
            Edit HR Profile
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
              HEART RATE PROFILE
            </p>

            <h2>
              Personalise your HR zones
            </h2>

            <p className="muted">
              Enter your maximum and resting
              heart rates. TriTracker will
              calculate your zones automatically.
            </p>
          </div>

          <div className="goal-form-grid">
            <label className="goal-form-field">
              <span>
                Maximum heart rate (bpm)
              </span>

              <input
                type="number"
                min="1"
                max="250"
                value={maxHrInput}
                onChange={(event) =>
                  setMaxHrInput(
                    event.target.value
                  )
                }
              />
            </label>

            <label className="goal-form-field">
              <span>
                Resting heart rate (bpm)
              </span>

              <input
                type="number"
                min="1"
                max="150"
                value={restingHrInput}
                onChange={(event) =>
                  setRestingHrInput(
                    event.target.value
                  )
                }
              />
            </label>
          </div>

          <div className="goal-form-actions">
            {profile && (
              <button
                className="goal-cancel-button"
                onClick={handleCancel}
                disabled={saving}
              >
                Cancel
              </button>
            )}

            <button
              className="goal-save-button"
              onClick={handleSave}
              disabled={saving}
            >
              {saving
                ? "Saving..."
                : "Save HR Profile"}
            </button>
          </div>
        </section>
      ) : (
        profile && (
          <>
            <section className="dashboard-panel race-goal-card">
              <div>
                <p className="panel-label">
                  HEART RATE PROFILE
                </p>

                <h2>
                  Personalised Zones
                </h2>

                <p className="muted">
                  Calculated using heart rate
                  reserve.
                </p>
              </div>

              <div className="race-target">
                <span>Max HR</span>

                <strong>
                  {profile.max_hr} bpm
                </strong>
              </div>

              <div className="race-target">
                <span>Resting HR</span>

                <strong>
                  {profile.resting_hr} bpm
                </strong>
              </div>
            </section>

            <section className="goal-grid">
              {zones.map((zone) => (
                <article
                  className="dashboard-panel goal-card"
                  key={zone.name}
                >
                  <p className="panel-label">
                    {zone.name.toUpperCase()}
                  </p>

                  <h2>{zone.range}</h2>

                  <p className="muted">
                    {zone.description}
                  </p>
                </article>
              ))}
            </section>
          </>
        )
      )}
    </div>
  );
}

export default SettingsPage;