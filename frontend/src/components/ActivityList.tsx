const activities = [
  {
    sport: "Run",
    title: "Easy Run",
    distance: "6.2 km",
    time: "38 min",
  },
  {
    sport: "Bike",
    title: "Endurance Ride",
    distance: "32.4 km",
    time: "1h 28m",
  },
  {
    sport: "Swim",
    title: "Pool Session",
    distance: "1.5 km",
    time: "35 min",
  },
];

function ActivityList() {
  return (
    <div>
      <div className="panel-heading">
        <div>
          <p className="panel-label">RECENT</p>
          <h2>Activities</h2>
        </div>
      </div>

      <div className="activity-list">
        {activities.map((activity) => (
          <div className="activity-row" key={activity.title}>
            <div className="activity-icon">
              {activity.sport.charAt(0)}
            </div>

            <div className="activity-details">
              <strong>{activity.title}</strong>
              <span>{activity.sport}</span>
            </div>

            <div className="activity-stats">
              <strong>{activity.distance}</strong>
              <span>{activity.time}</span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

export default ActivityList;