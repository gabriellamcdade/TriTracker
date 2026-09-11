import { useEffect, useState } from "react";
import { getRecommendation } from "../services/api";
import type { Recommendation } from "../types";

function RecommendationCard() {
  const [recommendation, setRecommendation] =
    useState<Recommendation | null>(null);

  useEffect(() => {
    async function loadRecommendation() {
      try {
        const data = await getRecommendation();
        setRecommendation(data);
      } catch (error) {
        console.error("Could not load recommendation:", error);
      }
    }

    loadRecommendation();
  }, []);

  if (!recommendation) {
    return (
      <div>
        <div className="panel-heading">
          <div>
            <p className="panel-label">TODAY</p>
            <h2>Training Recommendation</h2>
          </div>
        </div>

        <p className="muted" style={{ marginTop: "30px" }}>
          Loading recommendation...
        </p>
      </div>
    );
  }

  const isRest = recommendation.workout_type === "REST";

  return (
    <div>
      <div className="panel-heading">
        <div>
          <p className="panel-label">TODAY</p>
          <h2>Training Recommendation</h2>
        </div>
      </div>

      <div className="recommendation">
        <span className="recommendation-type">
          {isRest ? "REST" : recommendation.sport}
        </span>

        <h3>
          {isRest
            ? "Recovery day"
            : `${recommendation.workout_type} ${recommendation.sport}`}
        </h3>

        <p className="muted">
          {recommendation.reason}
        </p>

        <div className="recommendation-stats">
          <div>
            <strong>
              {isRest
                ? "Rest"
                : `${recommendation.duration_min} min`}
            </strong>
            <span>Duration</span>
          </div>

          <div>
            <strong>{recommendation.intensity}</strong>
            <span>Intensity</span>
          </div>

          <div>
            <strong>{recommendation.recovery_score}</strong>
            <span>Recovery</span>
          </div>
        </div>
      </div>
    </div>
  );
}

export default RecommendationCard;