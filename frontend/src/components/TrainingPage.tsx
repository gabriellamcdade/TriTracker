import { useEffect, useState } from "react";

import {
  getPerformance,
  getPerformanceTrends,
  getSummary,
  getTrainingLoad,
} from "../services/api";

import type {
  PerformanceSummary,
  PerformanceTrends,
  Sport,
  TrainingSummary,
  WeeklyTrainingLoad,
} from "../types";

import PerformanceTrendChart from "./PerformanceTrendChart";

function formatPace(value: number | null) {
  if (value === null) {
    return "—";
  }

  const minutes = Math.floor(value);
  const seconds = Math.round(
    (value - minutes) * 60
  );

  return `${minutes}:${seconds
    .toString()
    .padStart(2, "0")}`;
}

function TrainingPage() {
  const [summary, setSummary] =
    useState<TrainingSummary | null>(null);

  const [performance, setPerformance] =
    useState<PerformanceSummary | null>(null);

  const [performanceTrends, setPerformanceTrends] =
    useState<PerformanceTrends | null>(null);

  const [trainingLoad, setTrainingLoad] =
    useState<WeeklyTrainingLoad[]>([]);

  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function loadTrainingData() {
      try {
        const [
          summaryData,
          performanceData,
          trendData,
          loadData,
        ] = await Promise.all([
          getSummary(),
          getPerformance(),
          getPerformanceTrends(),
          getTrainingLoad(),
        ]);

        setSummary(summaryData);
        setPerformance(performanceData);
        setPerformanceTrends(trendData);
        setTrainingLoad(loadData);
      } catch (error) {
        console.error(
          "Could not load training data:",
          error
        );
      } finally {
        setLoading(false);
      }
    }

    loadTrainingData();
  }, []);

  if (loading) {
    return (
      <p className="muted">
        Loading training data...
      </p>
    );
  }

  if (
    !summary ||
    !performance ||
    !performanceTrends
  ) {
    return (
      <p className="muted">
        Could not load training data.
      </p>
    );
  }

  const sports: Sport[] = [
    "Run",
    "Bike",
    "Swim",
  ];

  const maxLoad = Math.max(
    ...trainingLoad.map(
      (week) => week.total_training_load
    ),
    1
  );

  function getPerformanceValue(
    sport: Sport
  ) {
    if (sport === "Run") {
      return {
        value: formatPace(
          performance.Run
            .average_pace_min_per_km
        ),
        label: "30-day average pace / km",
      };
    }

    if (sport === "Bike") {
      return {
        value:
          performance.Bike
            .average_speed_kmh === null
            ? "—"
            : `${performance.Bike.average_speed_kmh.toFixed(
                1
              )} km/h`,
        label: "30-day average speed",
      };
    }

    return {
      value: formatPace(
        performance.Swim
          .average_pace_min_per_100m
      ),
      label: "30-day average pace / 100m",
    };
  }

  return (
    <div>
      <header className="dashboard-header">
        <div>
          <p className="eyebrow">
            TriTracker
          </p>

          <h1>Training</h1>

          <p className="subtitle">
            Your training volume and
            performance trends.
          </p>
        </div>
      </header>

      <section className="training-sport-grid">
        {sports.map((sport) => {
          const weeklyData =
            summary[sport];

          const performanceData =
            performance[sport];

          const performanceMetric =
            getPerformanceValue(sport);

          return (
            <article
              className="training-sport-card"
              key={sport}
            >
              <p className="panel-label">
                {sport.toUpperCase()}
              </p>

              <h2>
                {weeklyData.distance_km.toFixed(
                  1
                )}{" "}
                km
              </h2>

              <p className="muted">
                {Math.floor(
                  weeklyData.duration_min / 60
                )}
                h{" "}
                {weeklyData.duration_min % 60}
                m this week
              </p>

              <div
                style={{
                  marginTop: "22px",
                }}
              >
                <strong
                  style={{
                    display: "block",
                    fontSize: "1.25rem",
                  }}
                >
                  {performanceMetric.value}
                </strong>

                <span className="muted">
                  {performanceMetric.label}
                </span>
              </div>

              <div
                style={{
                  marginTop: "14px",
                }}
              >
                <strong
                  style={{
                    display: "block",
                  }}
                >
                  {performanceData.average_hr ??
                    "—"}

                  {performanceData.average_hr !==
                    null && " bpm"}
                </strong>

                <span className="muted">
                  30-day average heart rate
                </span>
              </div>
            </article>
          );
        })}
      </section>

      <section className="dashboard-panel">
        <div className="panel-heading">
          <div>
            <p className="panel-label">
              PERFORMANCE
            </p>

            <h2>
              30-Day Performance Trends
            </h2>
          </div>
        </div>

        <div className="training-sport-grid">
          <article className="training-sport-card">
            <p className="panel-label">
              RUN PACE
            </p>

            <PerformanceTrendChart
              sport="Run"
              data={performanceTrends.Run}
            />
          </article>

          <article className="training-sport-card">
            <p className="panel-label">
              BIKE SPEED
            </p>

            <PerformanceTrendChart
              sport="Bike"
              data={performanceTrends.Bike}
            />
          </article>

          <article className="training-sport-card">
            <p className="panel-label">
              SWIM PACE
            </p>

            <PerformanceTrendChart
              sport="Swim"
              data={performanceTrends.Swim}
            />
          </article>
        </div>
      </section>

      <section className="dashboard-panel">
        <div className="panel-heading">
          <div>
            <p className="panel-label">
              LOAD
            </p>

            <h2>
              Weekly Training Load
            </h2>
          </div>
        </div>

        {trainingLoad.length === 0 ? (
          <p
            className="muted"
            style={{
              marginTop: "25px",
            }}
          >
            No training load data
            available yet.
          </p>
        ) : (
          <div className="training-page-chart">
            {trainingLoad
              .slice(-8)
              .map((week) => {
                const height =
                  (week.total_training_load /
                    maxLoad) *
                  100;

                return (
                  <div
                    className="training-page-column"
                    key={week.week}
                  >
                    <div className="training-page-value">
                      {Math.round(
                        week.total_training_load
                      )}
                    </div>

                    <div className="training-page-track">
                      <div
                        className="training-page-bar"
                        style={{
                          height: `${Math.max(
                            height,
                            4
                          )}%`,
                        }}
                      />
                    </div>

                    <span>
                      {week.week}
                    </span>
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