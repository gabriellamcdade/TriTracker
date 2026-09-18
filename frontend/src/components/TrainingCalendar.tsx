import { useEffect, useMemo, useState } from "react";
import { getTrainingCalendar } from "../services/api";
import type {
  Activity,
  CalendarActivity,
  TrainingCalendar as TrainingCalendarData,
} from "../types";

const WEEKDAYS = [
  "Mon",
  "Tue",
  "Wed",
  "Thu",
  "Fri",
  "Sat",
  "Sun",
];

type TrainingCalendarProps = {
  onActivityClick: (activity: Activity) => void;
};

function getDateKey(
  year: number,
  month: number,
  day: number
) {
  const monthText = String(month + 1).padStart(
    2,
    "0"
  );

  const dayText = String(day).padStart(
    2,
    "0"
  );

  return `${year}-${monthText}-${dayText}`;
}

function formatMonth(
  year: number,
  month: number
) {
  return new Intl.DateTimeFormat("en-GB", {
    month: "long",
    year: "numeric",
  }).format(new Date(year, month, 1));
}

function formatSelectedDate(dateKey: string) {
  const [year, month, day] = dateKey
    .split("-")
    .map(Number);

  return new Intl.DateTimeFormat("en-GB", {
    weekday: "long",
    day: "numeric",
    month: "long",
  }).format(
    new Date(year, month - 1, day)
  );
}

function getSportLetter(
  activity: CalendarActivity
) {
  return activity.sport.charAt(0);
}

function toActivity(
  activity: CalendarActivity,
  date: string
): Activity {
  return {
    strava_id: activity.strava_id,
    date,
    sport: activity.sport,
    activity_type: activity.type,
    distance_km: activity.distance,
    duration_min: activity.duration,
    avg_hr: activity.avg_hr,
  };
}

function TrainingCalendar({
  onActivityClick,
}: TrainingCalendarProps) {
  const today = new Date();

  const [calendar, setCalendar] =
    useState<TrainingCalendarData>({});

  const [displayYear, setDisplayYear] =
    useState(today.getFullYear());

  const [displayMonth, setDisplayMonth] =
    useState(today.getMonth());

  const [selectedDate, setSelectedDate] =
    useState<string | null>(null);

  const [loading, setLoading] =
    useState(true);

  const [error, setError] =
    useState("");

  useEffect(() => {
    async function loadCalendar() {
      try {
        const data =
          await getTrainingCalendar();

        setCalendar(data);
      } catch {
        setError(
          "Could not load training calendar."
        );
      } finally {
        setLoading(false);
      }
    }

    loadCalendar();
  }, []);

  const calendarDays = useMemo(() => {
    const firstDay = new Date(
      displayYear,
      displayMonth,
      1
    );

    const daysInMonth = new Date(
      displayYear,
      displayMonth + 1,
      0
    ).getDate();

    const leadingBlankDays =
      (firstDay.getDay() + 6) % 7;

    const days: Array<number | null> = [];

    for (
      let index = 0;
      index < leadingBlankDays;
      index += 1
    ) {
      days.push(null);
    }

    for (
      let day = 1;
      day <= daysInMonth;
      day += 1
    ) {
      days.push(day);
    }

    return days;
  }, [displayYear, displayMonth]);

  const selectedActivities =
    selectedDate
      ? calendar[selectedDate] || []
      : [];

  function previousMonth() {
    if (displayMonth === 0) {
      setDisplayMonth(11);
      setDisplayYear(
        (year) => year - 1
      );
    } else {
      setDisplayMonth(
        (month) => month - 1
      );
    }

    setSelectedDate(null);
  }

  function nextMonth() {
    if (displayMonth === 11) {
      setDisplayMonth(0);
      setDisplayYear(
        (year) => year + 1
      );
    } else {
      setDisplayMonth(
        (month) => month + 1
      );
    }

    setSelectedDate(null);
  }

  return (
    <section className="dashboard-panel training-calendar-panel">
      {loading ? (
        <p className="muted">
          Loading calendar...
        </p>
      ) : error ? (
        <p className="muted">
          {error}
        </p>
      ) : (
        <>
          <div className="training-calendar-header">
            <div>
              <p className="panel-label">
                TRAINING HISTORY
              </p>

              <h2>
                {formatMonth(
                  displayYear,
                  displayMonth
                )}
              </h2>
            </div>

            <div className="calendar-navigation">
              <button
                type="button"
                onClick={previousMonth}
                aria-label="Previous month"
              >
                ‹
              </button>

              <button
                type="button"
                onClick={nextMonth}
                aria-label="Next month"
              >
                ›
              </button>
            </div>
          </div>

          <div className="calendar-weekdays">
            {WEEKDAYS.map((weekday) => (
              <span key={weekday}>
                {weekday}
              </span>
            ))}
          </div>

          <div className="training-calendar-grid">
            {calendarDays.map(
              (day, index) => {
                if (day === null) {
                  return (
                    <div
                      className="calendar-day empty"
                      key={`empty-${index}`}
                    />
                  );
                }

                const dateKey = getDateKey(
                  displayYear,
                  displayMonth,
                  day
                );

                const activities =
                  calendar[dateKey] || [];

                const isSelected =
                  selectedDate === dateKey;

                const isToday =
                  dateKey ===
                  getDateKey(
                    today.getFullYear(),
                    today.getMonth(),
                    today.getDate()
                  );

                return (
                  <button
                    type="button"
                    key={dateKey}
                    className={[
                      "calendar-day",
                      activities.length > 0
                        ? "has-activity"
                        : "",
                      isSelected
                        ? "selected"
                        : "",
                      isToday
                        ? "today"
                        : "",
                    ]
                      .filter(Boolean)
                      .join(" ")}
                    onClick={() =>
                      setSelectedDate(
                        dateKey
                      )
                    }
                  >
                    <span className="calendar-day-number">
                      {day}
                    </span>

                    <div className="calendar-activity-dots">
                      {activities
                        .slice(0, 3)
                        .map(
                          (
                            activity,
                            activityIndex
                          ) => (
                            <span
                              className={`calendar-sport-dot ${activity.sport.toLowerCase()}`}
                              key={`${activity.strava_id}-${activityIndex}`}
                              title={
                                activity.type ||
                                activity.sport
                              }
                            >
                              {getSportLetter(
                                activity
                              )}
                            </span>
                          )
                        )}

                      {activities.length >
                        3 && (
                        <span className="calendar-more">
                          +
                          {activities.length -
                            3}
                        </span>
                      )}
                    </div>
                  </button>
                );
              }
            )}
          </div>

          {selectedDate && (
            <div className="calendar-selected-day">
              <div>
                <p className="panel-label">
                  SELECTED DAY
                </p>

                <h3>
                  {formatSelectedDate(
                    selectedDate
                  )}
                </h3>
              </div>

              {selectedActivities.length ===
              0 ? (
                <p className="muted">
                  No training recorded.
                </p>
              ) : (
                <div className="calendar-selected-activities">
                  {selectedActivities.map(
                    (activity) => (
                      <button
                        type="button"
                        className="calendar-selected-activity clickable-calendar-activity"
                        key={
                          activity.strava_id
                        }
                        onClick={() =>
                          onActivityClick(
                            toActivity(
                              activity,
                              selectedDate
                            )
                          )
                        }
                      >
                        <div
                          className={`activity-detail-sport-badge ${activity.sport.toLowerCase()}`}
                        >
                          {getSportLetter(
                            activity
                          )}
                        </div>

                        <div>
                          <strong>
                            {activity.type ||
                              activity.sport}
                          </strong>

                          <span>
                            {
                              activity.distance
                            }{" "}
                            km
                            {" · "}
                            {
                              activity.duration
                            }{" "}
                            min
                          </span>
                        </div>
                      </button>
                    )
                  )}
                </div>
              )}
            </div>
          )}
        </>
      )}
    </section>
  );
}

export default TrainingCalendar;