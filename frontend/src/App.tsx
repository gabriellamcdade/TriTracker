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

import {
  getActivities,
  getSummary,
  getTrainingLoad,
} from "./services/api";

import type {
  Activity,
  TrainingSummary,
  WeeklyTrainingLoad,
} from "./types";

type HealthResponse = {
  status: string;
  service: string;
};

function App() {
  const [backendConnected, setBackendConnected] = useState(false);
  const [activePage, setActivePage] = useState("Dashboard");

  const [summary, setSummary] = useState<TrainingSummary | null>(null);
  const [activities, setActivities] = useState<Activity[]>([]);
  const [trainingLoad, setTrainingLoad] =
    useState<WeeklyTrainingLoad[]>([]);

  // Check whether the backend is running
  useEffect(() => {
    async function checkBackendHealth() {
      try {
        const response = await fetch("http://127.0.0.1:8000/health");

        if (!response.ok) {
          throw new Error("Backend request failed");
        }

        const data: HealthResponse = await response.json();

        setBackendConnected(data.status === "ok");
      } catch {
        setBackendConnected(false);
      }
    }

    checkBackendHealth();
  }, []);

  // Load real dashboard data from the backend
  useEffect(() => {
    async function loadDashboardData() {
      try {
        const [summaryData, activityData, trainingLoadData] =
          await Promise.all([
            getSummary(),
            getActivities(100),
            getTrainingLoad(),
          ]);

        setSummary(summaryData);
        setActivities(activityData);
        setTrainingLoad(trainingLoadData);
      } catch (error) {
        console.error("Could not load dashboard data:", error);
      }
    }

    loadDashboardData();
  }, []);

  // Calculate dashboard values
  const totalDistance = summary
    ? summary.Run.distance_km +
      summary.Bike.distance_km +
      summary.Swim.distance_km
    : 0;

  const totalMinutes = summary?.total_training_minutes ?? 0;

  const hours = Math.floor(totalMinutes / 60);
  const minutes = totalMinutes % 60;

  const latestTrainingLoad =
    trainingLoad.length > 0
      ? trainingLoad[trainingLoad.length - 1].total_training_load
      : 0;

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
                <p className="eyebrow">TRITRACKER</p>
                <h1>Training Dashboard</h1>

                <p className="subtitle">
                  Connected training. Smarter performance.
                </p>
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
            </header>

            <section className="metrics-grid">
              <MetricCard
                title="Weekly Distance"
                value={`${totalDistance.toFixed(1)} km`}
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
                value={activities.length.toString()}
                subtitle="Recent activities"
              />
            </section>

            <section className="dashboard-grid">
              <div className="dashboard-panel chart-panel">
                <TrainingLoadChart />
              </div>

              <div className="dashboard-panel recovery-panel">
                <RecoveryGauge />
              </div>
            </section>

            <section className="dashboard-grid lower-grid">
              <div className="dashboard-panel">
                <RecommendationCard />
              </div>

              <div className="dashboard-panel">
                <ActivityList />
              </div>
            </section>
          </>
        )}

        {activePage === "Activities" && <ActivitiesPage />}

        {activePage === "Training" && <TrainingPage />}

        {activePage === "Recovery" && <RecoveryPage />}

        {activePage === "Goals" && <GoalsPage />}
      </main>
    </div>
  );
}

export default App;