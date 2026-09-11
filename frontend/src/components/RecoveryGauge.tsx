function RecoveryGauge() {
  const recoveryScore = 78;

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
            <strong>{recoveryScore}</strong>
            <span>/ 100</span>
          </div>
        </div>

        <div>
          <p className="recovery-status">Good recovery</p>
          <p className="muted">
            You're ready for a productive training session.
          </p>
        </div>
      </div>
    </div>
  );
}

export default RecoveryGauge;