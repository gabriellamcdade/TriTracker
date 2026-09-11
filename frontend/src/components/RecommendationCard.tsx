function RecommendationCard() {
  return (
    <div>
      <div className="panel-heading">
        <div>
          <p className="panel-label">TODAY</p>
          <h2>Training Recommendation</h2>
        </div>
      </div>

      <div className="recommendation">
        <span className="recommendation-type">RUN</span>

        <h3>Easy aerobic run</h3>

        <p className="muted">
          Keep the effort comfortable and focus on building aerobic fitness.
        </p>

        <div className="recommendation-stats">
          <div>
            <strong>45 min</strong>
            <span>Duration</span>
          </div>

          <div>
            <strong>Zone 2</strong>
            <span>Intensity</span>
          </div>
        </div>
      </div>
    </div>
  );
}

export default RecommendationCard;