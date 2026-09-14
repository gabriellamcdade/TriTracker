import { useEffect, useState } from "react";
import "./App.css";

import Sidebar from "./components/Sidebar";
import MetricCard from "./components/MetricCard";
import TrainingLoadChart from "./components/TrainingLoadChart";
import RecoveryGauge from "./components/RecoveryGauge";
import RecommendationCard from "./components/RecommendationCard";
import ActivityList from "./components/ActivityList";
import ActivitiesPage from "./components/ActivitiesPage";
import TrainingPage from "./components/TrainingPage";
import RecoveryPage from "./components/RecoveryPage";
import GoalsPage from "./components/GoalsPage";
import SettingsPage from "./components/SettingsPage";

import {
  getActivities,
  getPerformance,
  getRaceProgress,
  getSummary,
  getTrainingLoad,
  syncStrava,
} from "./services/api";

import type {
  Activity,
  PerformanceSummary,
  RaceProgress,
  TrainingSummary,
  WeeklyTrainingLoad,
} from "./types";

type HealthResponse = {
  status: string;
  service: string;
};

function formatPace(value: number | null) {
  if (value === null) {
    return "—";
  }

  let minutes = Math.floor(value);
  let seconds = Math.round(
    (value - minutes) * 60
  );

  if (seconds === 60) {
    minutes += 1;
    seconds = 0;
  }

  return `${minutes}:${seconds
    .toString()
    .padStart(2, "0")}`;
}
function getTargetStatus(
  current: number | null | undefined,
  target: number | null,
  lowerIsBetter: boolean
) {
  if (current == null || target == null) {
    return null;
  }

  const difference = lowerIsBetter
    ? target - current
    : current - target;

  const percentageDifference =
    Math.abs(difference / target) * 100;

  if (percentageDifference <= 2) {
    return "On target";
  }

  return difference > 0
    ? "Ahead of target"
    : "Behind target";
}
function App() {
  const [backendConnected, setBackendConnected] =
    useState(false);

  const [activePage, setActivePage] =
    useState("Dashboard");

  const [raceProgress, setRaceProgress] =
    useState<RaceProgress | null>(null);

  const [performance, setPerformance] =
    useState<PerformanceSummary | null>(null);

  const [summary, setSummary] =
    useState<TrainingSummary | null>(null);

  const [activities, setActivities] =
    useState<Activity[]>([]);

  const [trainingLoad, setTrainingLoad] =
    useState<WeeklyTrainingLoad[]>([]);

  const [syncing, setSyncing] = useState(false);
  const [syncMessage, setSyncMessage] =
    useState("");

  const [refreshKey, setRefreshKey] =
    useState(0);

  useEffect(() => {
    async function checkBackendHealth() {
      try {
        const response = await fetch(
          "http://127.0.0.1:8000/health"
        );

        if (!response.ok) {
          throw new Error(
            "Backend request failed"
          );
        }

        const data: HealthResponse =
          await response.json();

        setBackendConnected(
          data.status === "ok"
        );
      } catch {
        setBackendConnected(false);
      }
    }

    checkBackendHealth();
  }, []);

  async function loadDashboardData() {
    try {
      const [
        summaryData,
        activityData,
        trainingLoadData,
        raceProgressData,
        performanceData,
      ] = await Promise.all([
        getSummary(),
        getActivities(100),
        getTrainingLoad(),
        getRaceProgress(),
        getPerformance(),
      ]);

      setSummary(summaryData);
      setActivities(activityData);
      setTrainingLoad(trainingLoadData);
      setRaceProgress(raceProgressData);
      setPerformance(performanceData);
    } catch (error) {
      console.error(
        "Could not load dashboard data:",
        error
      );
    }
  }

  useEffect(() => {
    loadDashboardData();
  }, []);

  async function handleStravaSync() {
    try {
      setSyncing(true);
      setSyncMessage("");

      const result = await syncStrava();

      await loadDashboardData();

      setRefreshKey(
        (currentKey) => currentKey + 1
      );

      if (result.added === 0) {
        setSyncMessage(
          "Strava is up to date"
        );
      } else if (result.added === 1) {
        setSyncMessage(
          "1 new activity added"
        );
      } else {
        setSyncMessage(
          `${result.added} new activities added`
        );
      }
    } catch (error) {
      console.error(
        "Could not sync Strava:",
        error
      );

      setSyncMessage(
        "Strava sync failed"
      );
    } finally {
      setSyncing(false);
    }
  }

  const today = new Date();

  const startOfWeek =
    new Date(today);

  const day =
    today.getDay() === 0
      ? 6
      : today.getDay() - 1;

  startOfWeek.setDate(
    today.getDate() - day
  );

  startOfWeek.setHours(
    0,
    0,
    0,
    0
  );

  const endOfWeek =
    new Date(startOfWeek);

  endOfWeek.setDate(
    startOfWeek.getDate() + 7
  );

  const weeklyActivities =
    activities.filter((activity) => {
      const activityDate = new Date(
        `${activity.date}T12:00:00`
      );

      return (
        activityDate >= startOfWeek &&
        activityDate < endOfWeek
      );
    });

  const totalDistance = summary
    ? summary.Run.distance_km +
      summary.Bike.distance_km +
      summary.Swim.distance_km
    : 0;

  const totalMinutes =
    summary?.total_training_minutes ?? 0;

  const hours = Math.floor(
    totalMinutes / 60
  );

  const minutes =
    totalMinutes % 60;

  const latestTrainingLoad =
    trainingLoad.length > 0
      ? trainingLoad[
          trainingLoad.length - 1
        ].total_training_load
      : 0;

  const swimStatus = getTargetStatus(
      performance?.Swim
        .average_pace_min_per_100m,
      raceProgress
        ?.swim_target_pace_min_per_100m ?? null,
      true
    );

    const bikeStatus = getTargetStatus(
      performance?.Bike.average_speed_kmh,
      raceProgress
        ?.bike_target_speed_kmh ?? null,
      false
    );

    const runStatus = getTargetStatus(
      performance?.Run
        .average_pace_min_per_km,
      raceProgress
        ?.run_target_pace_min_per_km ?? null,
      true
    );

  return (
    <div className="dashboard">
      <Sidebar
        activePage={activePage}
        onPageChange={setActivePage}
      />

      <main className="dashboard-main">
        {activePage === "Dashboard" && (
          <>
            <header className="dashboard-header">
              <div>
                <p className="eyebrow">
                  TriTracker
                </p>

                <h1>
                  Training Dashboard
                </h1>

                <p className="subtitle">
                  Connected training. Smarter
                  performance.
                </p>
              </div>

              <div className="dashboard-actions">
                <div className="sync-area">
                  <button
                    className="strava-sync-button"
                    onClick={handleStravaSync}
                    disabled={syncing}
                  >
                    {syncing
                      ? "Syncing..."
                      : "↻ Sync Strava"}
                  </button>

                  {syncMessage && (
                    <span className="sync-message">
                      {syncMessage}
                    </span>
                  )}
                </div>

                <div className="backend-status">
                  <span
                    className={`status-dot ${
                      backendConnected
                        ? "connected"
                        : "disconnected"
                    }`}
                  />

                  {backendConnected
                    ? "Backend connected"
                    : "Backend disconnected"}
                </div>
              </div>
            </header>

            <section className="metrics-grid">
              <MetricCard
                title="Weekly Distance"
                value={`${totalDistance.toFixed(
                  1
                )} km`}
                subtitle="This week"
              />

              <MetricCard
                title="Training Time"
                value={`${hours}h ${minutes
                  .toString()
                  .padStart(2, "0")}m`}
                subtitle="This week"
              />

              <MetricCard
                title="Training Load"
                value={latestTrainingLoad.toString()}
                subtitle="Latest week"
              />

              <MetricCard
                title="Activities"
                value={weeklyActivities.length.toString()}
                subtitle="This week"
              />
            </section>

            {raceProgress && (
              <section className="dashboard-panel race-progress-card">
                <div className="panel-heading">
                  <div>
                    <p className="panel-label">
                      NEXT RACE
                    </p>

                    <h2>
                      {raceProgress.race_name}
                    </h2>
                  </div>

                  <div className="race-countdown">
                    <strong>
                      {
                        raceProgress.days_remaining
                      }
                    </strong>

                    <span>
                      days to go
                    </span>
                  </div>
                </div>

                <div className="race-target-grid">
                  <div>
                    <strong>
                      {raceProgress.overall_target_min !==
                      null
                        ? `${Math.floor(
                            raceProgress.overall_target_min /
                              60
                          )}h ${
                            raceProgress.overall_target_min %
                            60
                          }m`
                        : "—"}
                    </strong>

                    <span>
                      Target finish
                    </span>
                  </div>

                  <div>
                    <strong>
                      {formatPace(
                        raceProgress.swim_target_pace_min_per_100m
                      )}{" "}
                      /100m
                    </strong>

                    <span>
                      Swim target
                    </span>

                    <span>
                      Current:{" "}
                      {formatPace(
                        performance?.Swim
                          .average_pace_min_per_100m ??
                          null
                      )}{" "}
                      /100m
                    </span>
                    {swimStatus && (
                      <span className="race-target-status">
                        {swimStatus}
                      </span>
                    )}
                  </div>

                  <div>
                    <strong>
                      {raceProgress.bike_target_speed_kmh !==
                      null
                        ? `${raceProgress.bike_target_speed_kmh.toFixed(
                            1
                          )} km/h`
                        : "—"}
                    </strong>

                    <span>
                      Bike target
                    </span>

                    <span>
                      Current:{" "}
                      {performance?.Bike
                        .average_speed_kmh !==
                        null &&
                      performance?.Bike
                        .average_speed_kmh !==
                        undefined
                        ? `${performance.Bike.average_speed_kmh.toFixed(
                            1
                          )} km/h`
                        : "—"}
                    </span>
                    {bikeStatus && (
                      <span className="race-target-status">
                        {bikeStatus}
                      </span>
                    )}
                  </div>

                  <div>
                    <strong>
                      {formatPace(
                        raceProgress.run_target_pace_min_per_km
                      )}{" "}
                      /km
                    </strong>

                    <span>
                      Run target
                    </span>

                    <span>
                      Current:{" "}
                      {formatPace(
                        performance?.Run
                          .average_pace_min_per_km ??
                          null
                      )}{" "}
                      /km
                    </span>
                    {runStatus && (
                      <span className="race-target-status">
                        {runStatus}
                      </span>
                    )}
                  </div>
                </div>
              </section>
            )}

            <section className="dashboard-grid">
              <div className="dashboard-panel chart-panel">
                <TrainingLoadChart
                  key={`training-${refreshKey}`}
                />
              </div>

              <div className="dashboard-panel recovery-panel">
                <RecoveryGauge
                  key={`recovery-${refreshKey}`}
                />
              </div>
            </section>

            <section className="dashboard-grid lower-grid">
              <div className="dashboard-panel">
                <RecommendationCard
                  key={`recommendation-${refreshKey}`}
                />
              </div>

              <div className="dashboard-panel">
                <ActivityList
                  key={`activities-${refreshKey}`}
                />
              </div>
            </section>
          </>
        )}

        {activePage === "Activities" && (
          <ActivitiesPage />
        )}

        {activePage === "Training" && (
          <TrainingPage />
        )}

        {activePage === "Recovery" && (
          <RecoveryPage />
        )}

        {activePage === "Goals" && (
          <GoalsPage />
        )}

        {activePage === "Settings" && (
          <SettingsPage />
        )}
      </main>
    </div>
  );
}

export default App;