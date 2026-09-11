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
  const [activePage, setActivePage] = useState("Dashboard");

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
          </>
        )}

        {activePage === "Activities" && (
          <div className="dashboard-panel">
            <p className="eyebrow">TRITRACKER</p>
            <h1>Activities</h1>

            <p className="subtitle">
              Your training activities will appear here.
            </p>

            <div style={{ marginTop: "30px" }}>
              <p>Outdoor Run</p>
              <p>Treadmill</p>
              <p>Outdoor Ride</p>
              <p>Indoor Cycle</p>
              <p>Pool Swim</p>
              <p>Open Water Swim</p>
            </div>
          </div>
        )}

        {activePage === "Training" && (
          <div className="dashboard-panel">
            <p className="eyebrow">TRITRACKER</p>
            <h1>Training</h1>

            <p className="subtitle">
              Training load, weekly volume and performance trends
              will appear here.
            </p>
          </div>
        )}

        {activePage === "Recovery" && (
          <div className="dashboard-panel">
            <p className="eyebrow">TRITRACKER</p>
            <h1>Recovery</h1>

            <p className="subtitle">
              Recovery score, readiness and fatigue analysis
              will appear here.
            </p>
          </div>
        )}

        {activePage === "Goals" && (
          <div className="dashboard-panel">
            <p className="eyebrow">TRITRACKER</p>
            <h1>Goals</h1>

            <p className="subtitle">
              Triathlon goals and progress tracking will appear here.
            </p>
          </div>
        )}

      </main>
    </div>
  );
}

export default App;