import { useEffect, useState } from "react";
import { getActivities } from "../services/api";
import type { Activity } from "../types";

function ActivityList() {
  const [activities, setActivities] = useState<Activity[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function loadActivities() {
      try {
        const data = await getActivities(3);
        setActivities(data);
      } catch (error) {
        console.error("Could not load recent activities:", error);
      } finally {
        setLoading(false);
      }
    }

    loadActivities();
  }, []);

  return (
    <div>
      <div className="panel-heading">
        <div>
          <p className="panel-label">RECENT</p>
          <h2>Activities</h2>
        </div>
      </div>

      {loading ? (
        <p className="muted" style={{ marginTop: "20px" }}>
          Loading activities...
        </p>
      ) : activities.length === 0 ? (
        <p className="muted" style={{ marginTop: "20px" }}>
          No activities yet.
        </p>
      ) : (
        <div className="activity-list">
          {activities.map((activity) => (
            <div
              className="activity-row"
              key={activity.strava_id}
            >
              <div className="activity-icon">
                {activity.sport.charAt(0)}
              </div>

              <div className="activity-details">
                <strong>
                  {activity.activity_type || activity.sport}
                </strong>

                <span>{activity.date}</span>
              </div>

              <div className="activity-stats">
                <strong>
                  {activity.distance_km} km
                </strong>

                <span>
                  {activity.duration_min} min
                </span>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

export default ActivityList;