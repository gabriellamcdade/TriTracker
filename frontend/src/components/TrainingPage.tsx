import { useEffect, useState } from "react";
import { getSummary, getTrainingLoad } from "../services/api";
import type {
  TrainingSummary,
  WeeklyTrainingLoad,
  Sport,
} from "../types";

function TrainingPage() {
  const [summary, setSummary] = useState<TrainingSummary | null>(null);
  const [trainingLoad, setTrainingLoad] =
    useState<WeeklyTrainingLoad[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function loadTrainingData() {
      try {
        const [summaryData, loadData] = await Promise.all([
          getSummary(),
          getTrainingLoad(),
        ]);

        setSummary(summaryData);
        setTrainingLoad(loadData);
      } catch (error) {
        console.error("Could not load training data:", error);
      } finally {
        setLoading(false);
      }
    }

    loadTrainingData();
  }, []);

  if (loading) {
    return <p className="muted">Loading training data...</p>;
  }

  if (!summary) {
    return <p className="muted">Could not load training data.</p>;
  }

  const sports: Sport[] = ["Run", "Bike", "Swim"];

  const maxLoad = Math.max(
    ...trainingLoad.map((week) => week.total_training_load),
    1
  );

  return (
    <div>
      <header className="dashboard-header">
        <div>
          <p className="eyebrow">TriTracker</p>
          <h1>Training</h1>
          <p className="subtitle">
            Your training volume and weekly performance trends.
          </p>
        </div>
      </header>

      <section className="training-sport-grid">
        {sports.map((sport) => {
          const data = summary[sport];

          return (
            <article className="training-sport-card" key={sport}>
              <p className="panel-label">{sport.toUpperCase()}</p>

              <h2>{data.distance_km.toFixed(1)} km</h2>

              <p className="muted">
                {Math.floor(data.duration_min / 60)}h{" "}
                {data.duration_min % 60}m
              </p>
            </article>
          );
        })}
      </section>

      <section className="dashboard-panel">
        <div className="panel-heading">
          <div>
            <p className="panel-label">LOAD</p>
            <h2>Weekly Training Load</h2>
          </div>
        </div>

        {trainingLoad.length === 0 ? (
          <p className="muted" style={{ marginTop: "25px" }}>
            No training load data available yet.
          </p>
        ) : (
          <div className="training-page-chart">
            {trainingLoad.slice(-8).map((week) => {
              const height =
                (week.total_training_load / maxLoad) * 100;

              return (
                <div className="training-page-column" key={week.week}>
                  <div className="training-page-value">
                    {Math.round(week.total_training_load)}
                  </div>

                  <div className="training-page-track">
                    <div
                      className="training-page-bar"
                      style={{
                        height: `${Math.max(height, 4)}%`,
                      }}
                    />
                  </div>

                  <span>{week.week}</span>
                </div>
              );
            })}
          </div>
        )}
      </section>
    </div>
  );
}

export default TrainingPage;