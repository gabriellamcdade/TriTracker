import { useEffect, useState } from "react";
import { getTrainingLoad } from "../services/api";
import type { WeeklyTrainingLoad } from "../types";

function TrainingLoadChart() {
  const [trainingLoad, setTrainingLoad] =
    useState<WeeklyTrainingLoad[]>([]);

  useEffect(() => {
    async function loadTrainingData() {
      try {
        const data = await getTrainingLoad();
        setTrainingLoad(data);
      } catch (error) {
        console.error("Could not load training load:", error);
      }
    }

    loadTrainingData();
  }, []);

  const recentWeeks = trainingLoad.slice(-7);

  const maxLoad = Math.max(
    ...recentWeeks.map((week) => week.total_training_load),
    1
  );

  const latestLoad =
    recentWeeks.length > 0
      ? recentWeeks[recentWeeks.length - 1].total_training_load
      : 0;

  return (
    <div>
      <div className="panel-heading">
        <div>
          <p className="panel-label">TRAINING</p>
          <h2>Weekly Load</h2>
        </div>

        <span className="panel-value">
          {Math.round(latestLoad)}
        </span>
      </div>

      {recentWeeks.length === 0 ? (
        <p className="muted" style={{ marginTop: "30px" }}>
          No training data yet.
        </p>
      ) : (
        <div className="training-chart">
          {recentWeeks.map((week) => {
            const height =
              (week.total_training_load / maxLoad) * 100;

            return (
              <div className="chart-column" key={week.week}>
                <div className="chart-track">
                  <div
                    className="chart-bar"
                    style={{
                      height: `${Math.max(height, 3)}%`,
                    }}
                  />
                </div>

                <span>{week.week}</span>
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
}

export default TrainingLoadChart;
