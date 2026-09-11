import { useEffect, useState } from "react";
import { getRecovery } from "../services/api";
import type { Recovery } from "../types";

function RecoveryPage() {
  const [recovery, setRecovery] = useState<Recovery | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function loadRecovery() {
      try {
        const data = await getRecovery();
        setRecovery(data);
      } catch (error) {
        console.error("Could not load recovery data:", error);
      } finally {
        setLoading(false);
      }
    }

    loadRecovery();
  }, []);

  if (loading) {
    return <p className="muted">Loading recovery data...</p>;
  }

  if (!recovery) {
    return <p className="muted">Could not load recovery data.</p>;
  }

  return (
    <div>
      <header className="dashboard-header">
        <div>
          <p className="eyebrow">TRITRACKER</p>
          <h1>Recovery</h1>

          <p className="subtitle">
            Understand your current training readiness and fatigue.
          </p>
        </div>
      </header>

      <section className="recovery-page-grid">
        <article className="dashboard-panel recovery-score-card">
          <p className="panel-label">READINESS</p>

          <div
            className="recovery-page-gauge"
            style={{
              background: `conic-gradient(
                #52d6a5 ${recovery.score * 3.6}deg,
                #253131 0deg
              )`,
            }}
          >
            <div className="recovery-page-inner">
              <strong>{Math.round(recovery.score)}</strong>
              <span>/ 100</span>
            </div>
          </div>

          <h2>{recovery.status}</h2>

          <p className="muted">
            Recommended training: {recovery.recommendation}
          </p>
        </article>

        <article className="dashboard-panel">
          <p className="panel-label">TRAINING LOAD</p>
          <h2>Load Analysis</h2>

          <div className="recovery-stat-list">
            <div>
              <span>Current load</span>
              <strong>{Math.round(recovery.recent_load)}</strong>
            </div>

            <div>
              <span>Previous load</span>
              <strong>{Math.round(recovery.previous_load)}</strong>
            </div>

            <div>
              <span>Load change</span>
              <strong>
                {recovery.load_change > 0 ? "+" : ""}
                {recovery.load_change.toFixed(1)}%
              </strong>
            </div>

            <div>
              <span>High intensity</span>
              <strong>
                {recovery.high_intensity_percent.toFixed(1)}%
              </strong>
            </div>
          </div>
        </article>
      </section>

      <section className="dashboard-panel recovery-advice">
        <p className="panel-label">TODAY</p>
        <h2>Recovery Guidance</h2>

        <p className="muted">
          {recovery.recommendation === "REST"
            ? "Your recent training load suggests taking a recovery day. Prioritise rest and light movement."
            : recovery.recommendation === "EASY"
            ? "Keep today's training controlled and easy while your body adapts to your recent workload."
            : "Your current training load supports a normal training session today."}
        </p>
      </section>
    </div>
  );
}

export default RecoveryPage;