import type { Activity } from "../types";

type ActivityDetailProps = {
  activity: Activity;
  onClose: () => void;
};

function formatDate(date: string) {
  const [year, month, day] = date
    .split("-")
    .map(Number);

  return new Intl.DateTimeFormat("en-GB", {
    weekday: "long",
    day: "numeric",
    month: "long",
    year: "numeric",
  }).format(
    new Date(year, month - 1, day)
  );
}

function formatPace(minutesPerUnit: number) {
  const minutes = Math.floor(minutesPerUnit);
  const seconds = Math.round(
    (minutesPerUnit - minutes) * 60
  );

  if (seconds === 60) {
    return `${minutes + 1}:00`;
  }

  return `${minutes}:${String(seconds).padStart(
    2,
    "0"
  )}`;
}

function ActivityDetail({
  activity,
  onClose,
}: ActivityDetailProps) {
  let performanceLabel = "";
  let performanceValue = "—";

  if (
    activity.sport === "Run" &&
    activity.distance_km > 0
  ) {
    performanceLabel = "Average Pace";

    performanceValue = `${formatPace(
      activity.duration_min /
        activity.distance_km
    )} /km`;
  }

  if (
    activity.sport === "Bike" &&
    activity.duration_min > 0
  ) {
    performanceLabel = "Average Speed";

    const speed =
      activity.distance_km /
      (activity.duration_min / 60);

    performanceValue = `${speed.toFixed(
      1
    )} km/h`;
  }

  if (
    activity.sport === "Swim" &&
    activity.distance_km > 0
  ) {
    performanceLabel = "Average Pace";

    const pacePer100m =
      activity.duration_min /
      (activity.distance_km * 10);

    performanceValue = `${formatPace(
      pacePer100m
    )} /100m`;
  }

  return (
    <div
      className="activity-detail-overlay"
      onClick={onClose}
    >
      <section
        className="activity-detail-card"
        onClick={(event) =>
          event.stopPropagation()
        }
      >
        <div className="activity-detail-header">
          <div>
            <p className="panel-label">
              ACTIVITY DETAILS
            </p>

            <h2>
              {activity.activity_type ||
                activity.sport}
            </h2>

            <p className="muted">
              {formatDate(activity.date)}
            </p>
          </div>

          <button
            type="button"
            className="activity-detail-close"
            onClick={onClose}
            aria-label="Close activity details"
          >
            ×
          </button>
        </div>

        <div className="activity-detail-sport">
          <span
            className={`activity-detail-sport-badge ${activity.sport.toLowerCase()}`}
          >
            {activity.sport.charAt(0)}
          </span>

          <span>{activity.sport}</span>
        </div>

        <div className="activity-detail-metrics">
          <div className="activity-detail-metric">
            <span>Distance</span>

            <strong>
              {activity.distance_km} km
            </strong>
          </div>

          <div className="activity-detail-metric">
            <span>Duration</span>

            <strong>
              {activity.duration_min} min
            </strong>
          </div>

          <div className="activity-detail-metric">
            <span>Average HR</span>

            <strong>
              {activity.avg_hr
                ? `${activity.avg_hr} bpm`
                : "—"}
            </strong>
          </div>

          <div className="activity-detail-metric">
            <span>{performanceLabel}</span>

            <strong>
              {performanceValue}
            </strong>
          </div>
        </div>

        <div className="activity-detail-footer">
          <span>Strava activity</span>

          <span>
            ID {activity.strava_id}
          </span>
        </div>
      </section>
    </div>
  );
}

export default ActivityDetail;