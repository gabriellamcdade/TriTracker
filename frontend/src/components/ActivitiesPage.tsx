import { useEffect, useState } from "react";
import { getActivities } from "../services/api";
import type { Activity, Sport } from "../types";
import TrainingCalendar from "./TrainingCalendar";
import ActivityDetail from "./ActivityDetail";

type Filter = "All" | Sport;

function ActivitiesPage() {
  const [activities, setActivities] = useState<Activity[]>([]);
  const [filter, setFilter] = useState<Filter>("All");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [selectedActivity, setSelectedActivity] =
    useState<Activity | null>(null);

  useEffect(() => {
    async function loadActivities() {
      try {
        const data = await getActivities(50);
        setActivities(data);
      } catch {
        setError("Could not load activities.");
      } finally {
        setLoading(false);
      }
    }

    loadActivities();
  }, []);

  const filteredActivities =
    filter === "All"
      ? activities
      : activities.filter(
          (activity) => activity.sport === filter
        );

  return (
    <div>
      <header className="dashboard-header">
        <div>
          <p className="eyebrow">
            TriTracker
          </p>

          <h1>Activities</h1>

          <p className="subtitle">
            Explore your training history
            across run, bike and swim.
          </p>
        </div>
      </header>

      <TrainingCalendar
        onActivityClick={(activity) =>
            setSelectedActivity(activity)
            }
      />

      <section className="activities-history-section">
        <div className="activities-history-header">
          <div>
            <p className="panel-label">
              ACTIVITY HISTORY
            </p>

            <h2>Recent Activities</h2>
          </div>

          <div className="activity-filters">
            {(
              [
                "All",
                "Run",
                "Bike",
                "Swim",
              ] as Filter[]
            ).map((item) => (
              <button
                key={item}
                className={`activity-filter ${
                  filter === item
                    ? "active"
                    : ""
                }`}
                onClick={() =>
                  setFilter(item)
                }
              >
                {item}
              </button>
            ))}
          </div>
        </div>

        <section className="dashboard-panel activities-page-panel">
          {loading && (
            <p className="muted">
              Loading activities...
            </p>
          )}

          {error && (
            <p className="muted">
              {error}
            </p>
          )}

          {!loading &&
            !error &&
            filteredActivities.length === 0 && (
              <p className="muted">
                No activities found.
              </p>
            )}

          <div className="activities-page-list">
            {filteredActivities.map(
              (activity) => (
                <article
                  className="activities-page-row clickable-activity-row"
                  key={activity.strava_id}
                  onClick={() =>
                    setSelectedActivity(
                      activity
                    )
                  }
                  tabIndex={0}
                  role="button"
                  onKeyDown={(event) => {
                    if (
                      event.key ===
                        "Enter" ||
                      event.key === " "
                    ) {
                      setSelectedActivity(
                        activity
                      );
                    }
                  }}
                >
                  <div className="activity-type-badge">
                    {activity.sport.charAt(
                      0
                    )}
                  </div>

                  <div className="activities-page-info">
                    <strong>
                      {activity.activity_type ||
                        activity.sport}
                    </strong>

                    <span>
                      {activity.date}
                    </span>
                  </div>

                  <div className="activities-page-metric">
                    <strong>
                      {activity.distance_km} km
                    </strong>

                    <span>
                      Distance
                    </span>
                  </div>

                  <div className="activities-page-metric">
                    <strong>
                      {activity.duration_min} min
                    </strong>

                    <span>
                      Duration
                    </span>
                  </div>

                  <div className="activities-page-metric">
                    <strong>
                      {activity.avg_hr
                        ? `${activity.avg_hr} bpm`
                        : "—"}
                    </strong>

                    <span>
                      Avg HR
                    </span>
                  </div>


                </article>
              )
            )}
          </div>
        </section>
      </section>

      {selectedActivity && (
        <ActivityDetail
          activity={selectedActivity}
          onClose={() =>
            setSelectedActivity(null)
          }
        />
      )}
    </div>
  );
}

export default ActivitiesPage;