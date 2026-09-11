import { useEffect, useState } from "react";
import "./App.css";

import Sidebar from "./components/Sidebar";
import MetricCard from "./components/MetricCard";
import TrainingLoadChart from "./components/TrainingLoadChart";
import RecoveryGauge from "./components/RecoveryGauge";
import RecommendationCard from "./components/RecommendationCard";
import ActivityList from "./components/ActivityList";

type HealthResponse = {
  status: string;
  service: string;
};

function App() {
  const [backendConnected, setBackendConnected] = useState(false);

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

  return (
    <div className="dashboard">
      <Sidebar />

      <main className="dashboard-main">
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
                backendConnected ? "connected" : "disconnected"
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
            value="0 km"
            subtitle="This week"
          />

          <MetricCard
            title="Training Time"
            value="0h 00m"
            subtitle="This week"
          />

          <MetricCard
            title="Training Load"
            value="0"
            subtitle="7-day load"
          />

          <MetricCard
            title="Activities"
            value="0"
            subtitle="This week"
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
      </main>
    </div>
  );
}

export default App;