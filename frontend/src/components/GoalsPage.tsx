function GoalsPage() {
  const goals = [
    {
      sport: "Swim",
      distance: "1.5 km",
      target: "30 min",
      progress: 70,
    },
    {
      sport: "Bike",
      distance: "40 km",
      target: "1h 20m",
      progress: 62,
    },
    {
      sport: "Run",
      distance: "10 km",
      target: "55 min",
      progress: 78,
    },
  ];

  return (
    <div>
      <header className="dashboard-header">
        <div>
          <p className="eyebrow">TRITRACKER</p>
          <h1>Goals</h1>

          <p className="subtitle">
            Track your progress towards race day.
          </p>
        </div>
      </header>

      <section className="dashboard-panel race-goal-card">
        <div>
          <p className="panel-label">TARGET RACE</p>
          <h2>Olympic Triathlon</h2>
          <p className="muted">
            1.5 km swim · 40 km bike · 10 km run
          </p>
        </div>

        <div className="race-target">
          <span>Target finish</span>
          <strong>Under 3 hours</strong>
        </div>
      </section>

      <section className="goal-grid">
        {goals.map((goal) => (
          <article className="dashboard-panel goal-card" key={goal.sport}>
            <div className="goal-heading">
              <div>
                <p className="panel-label">
                  {goal.sport.toUpperCase()}
                </p>

                <h2>{goal.distance}</h2>
              </div>

              <strong className="goal-percentage">
                {goal.progress}%
              </strong>
            </div>

            <p className="muted">
              Target: {goal.target}
            </p>

            <div className="goal-progress-track">
              <div
                className="goal-progress-bar"
                style={{ width: `${goal.progress}%` }}
              />
            </div>
          </article>
        ))}
      </section>

      <section className="dashboard-panel">
        <p className="panel-label">OVERALL GOAL</p>
        <h2>Race Readiness</h2>

        <p className="muted">
          Build consistent training across swimming, cycling and
          running while gradually increasing your weekly workload.
        </p>
      </section>
    </div>
  );
}

export default GoalsPage;