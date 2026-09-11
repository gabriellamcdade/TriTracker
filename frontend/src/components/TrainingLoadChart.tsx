const trainingLoad = [
  { day: "Mon", value: 40 },
  { day: "Tue", value: 65 },
  { day: "Wed", value: 35 },
  { day: "Thu", value: 75 },
  { day: "Fri", value: 50 },
  { day: "Sat", value: 90 },
  { day: "Sun", value: 60 },
];

function TrainingLoadChart() {
  return (
    <div>
      <div className="panel-heading">
        <div>
          <p className="panel-label">TRAINING</p>
          <h2>Weekly Load</h2>
        </div>
        <span className="panel-value">415</span>
      </div>

      <div className="training-chart">
        {trainingLoad.map((item) => (
          <div className="chart-column" key={item.day}>
            <div className="chart-track">
              <div
                className="chart-bar"
                style={{ height: `${item.value}%` }}
              />
            </div>
            <span>{item.day}</span>
          </div>
        ))}
      </div>
    </div>
  );
}

export default TrainingLoadChart;