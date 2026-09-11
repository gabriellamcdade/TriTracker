type MetricCardProps = {
  title: string;
  value: string;
  subtitle: string;
};

function MetricCard({ title, value, subtitle }: MetricCardProps) {
  return (
    <article className="metric-card">
      <p className="metric-title">{title}</p>
      <h2 className="metric-value">{value}</h2>
      <p className="metric-subtitle">{subtitle}</p>
    </article>
  );
}

export default MetricCard;