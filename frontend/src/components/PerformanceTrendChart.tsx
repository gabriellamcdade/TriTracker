import type {
  PerformanceTrendPoint,
  Sport,
} from "../types";

type Props = {
  sport: Sport;
  data: PerformanceTrendPoint[];
};

function formatPace(value: number) {
  const minutes = Math.floor(value);
  const seconds = Math.round(
    (value - minutes) * 60
  );

  return `${minutes}:${seconds
    .toString()
    .padStart(2, "0")}`;
}

function PerformanceTrendChart({
  sport,
  data,
}: Props) {
  if (data.length === 0) {
    return (
      <p className="muted">
        No recent {sport.toLowerCase()} data.
      </p>
    );
  }

  const values = data.map(
    (point) => point.value
  );

  const minValue = Math.min(...values);
  const maxValue = Math.max(...values);

  const range =
    maxValue - minValue || 1;

  const points = data.map(
    (point, index) => {
      const x =
        data.length === 1
          ? 50
          : (index /
              (data.length - 1)) *
            100;

    const normalized =
        (point.value - minValue) / range;

    const y =
      sport === "Bike"
        ? 90 - normalized * 70
        : 20 + normalized * 70;

      return {
        ...point,
        x,
        y,
      };
    }
  );

  const polylinePoints = points
    .map(
      (point) =>
        `${point.x},${point.y}`
    )
    .join(" ");

  function formatValue(value: number) {
    if (sport === "Bike") {
      return `${value.toFixed(1)} km/h`;
    }

    if (sport === "Run") {
      return `${formatPace(value)} /km`;
    }

    return `${formatPace(value)} /100m`;
  }

  return (
    <div className="performance-trend-chart">
      <svg
        viewBox="0 0 100 100"
        preserveAspectRatio="xMidYMid meet"
        className="performance-trend-svg"
      >
        <polyline
          points={polylinePoints}
          fill="none"
          stroke="currentColor"
          strokeWidth="2"
          vectorEffect="non-scaling-stroke"
        />

        {points.map((point) => (
          <circle
            key={`${point.date}-${point.value}`}
            cx={point.x}
            cy={point.y}
            r="2"
            fill="currentColor"
            vectorEffect="non-scaling-stroke"
          />
        ))}
      </svg>

      <div className="performance-trend-labels">
        <span>
          {data[0].date}
        </span>

        <span>
          {data[data.length - 1].date}
        </span>
      </div>

      <div className="performance-trend-latest">
        Latest:{" "}
        <strong>
          {formatValue(
            data[data.length - 1].value
          )}
        </strong>
      </div>
    </div>
  );
}

export default PerformanceTrendChart;