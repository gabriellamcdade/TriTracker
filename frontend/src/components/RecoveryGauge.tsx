import { useEffect, useState } from "react";
import { getRecovery } from "../services/api";
import type { Recovery } from "../types";

function RecoveryGauge() {
  const [recovery, setRecovery] = useState<Recovery | null>(null);

  useEffect(() => {
    async function loadRecovery() {
      try {
        const data = await getRecovery();
        setRecovery(data);
      } catch (error) {
        console.error("Could not load recovery:", error);
      }
    }

    loadRecovery();
  }, []);

  if (!recovery) {
    return (
      <div>
        <div className="panel-heading">
          <div>
            <p className="panel-label">RECOVERY</p>
            <h2>Readiness</h2>
          </div>
        </div>

        <p className="muted" style={{ marginTop: "30px" }}>
          Loading recovery...
        </p>
      </div>
    );
  }

  const recoveryScore = recovery.score;

  return (
    <div>
      <div className="panel-heading">
        <div>
          <p className="panel-label">RECOVERY</p>
          <h2>Readiness</h2>
        </div>
      </div>

      <div className="recovery-content">
        <div
          className="recovery-gauge"
          style={{
            background: `conic-gradient(
              #52d6a5 ${recoveryScore * 3.6}deg,
              #253131 0deg
            )`,
          }}
        >
          <div className="recovery-inner">
            <strong>{Math.round(recoveryScore)}</strong>
            <span>/ 100</span>
          </div>
        </div>

        <div>
          <p className="recovery-status">
            {recovery.status}
          </p>

          <p className="muted">
            Recommended intensity: {recovery.recommendation}
          </p>

          <p className="muted">
            Load change: {recovery.load_change.toFixed(1)}%
          </p>
        </div>
      </div>
    </div>
  );
}

export default RecoveryGauge;