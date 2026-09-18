import sqlite3


DATABASE_FILE = "tritracker.db"


def get_connection():
    return sqlite3.connect(DATABASE_FILE)


def initialise_database():
    with get_connection() as connection:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS activities (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                strava_id INTEGER UNIQUE NOT NULL,
                date TEXT NOT NULL,
                sport TEXT NOT NULL,
                activity_type TEXT,
                distance_km REAL NOT NULL,
                duration_min INTEGER NOT NULL,
                avg_hr INTEGER
            )
        """)

        cursor = connection.execute("PRAGMA table_info(activities)")
        columns = [row[1] for row in cursor.fetchall()]

        if "activity_type" not in columns:
            connection.execute("""
                ALTER TABLE activities
                ADD COLUMN activity_type TEXT
            """)


def activity_exists(strava_id):
    with get_connection() as connection:
        cursor = connection.execute(
            "SELECT 1 FROM activities WHERE strava_id = ?",
            (strava_id,)
        )

        return cursor.fetchone() is not None


def insert_activity(activity):
    if activity_exists(activity["strava_id"]):
        return False

    with get_connection() as connection:
        connection.execute("""
            INSERT INTO activities (
                strava_id,
                date,
                sport,
                activity_type,
                distance_km,
                duration_min,
                avg_hr
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            activity["strava_id"],
            activity["date"],
            activity["sport"],
            activity.get("activity_type"),
            activity["distance_km"],
            activity["duration_min"],
            activity["avg_hr"],
        ))

    return True


def get_all_activities():
    with get_connection() as connection:
        connection.row_factory = sqlite3.Row

        cursor = connection.execute("""
            SELECT
                strava_id,
                date,
                sport,
                activity_type,
                distance_km,
                duration_min,
                avg_hr
            FROM activities
            ORDER BY date DESC
        """)

        activities = cursor.fetchall()

    return [dict(activity) for activity in activities]
def initialise_goals_table():
    with get_connection() as connection:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS goals (
                id INTEGER PRIMARY KEY CHECK (id = 1),
                race_name TEXT NOT NULL,
                race_date TEXT,
                swim_distance_km REAL NOT NULL,
                bike_distance_km REAL NOT NULL,
                run_distance_km REAL NOT NULL,
                swim_target_min INTEGER,
                bike_target_min INTEGER,
                run_target_min INTEGER,
                overall_target_min INTEGER
            )
        """)


def get_goal():
    with get_connection() as connection:
        connection.row_factory = sqlite3.Row

        cursor = connection.execute("""
            SELECT
                race_name,
                race_date,
                swim_distance_km,
                bike_distance_km,
                run_distance_km,
                swim_target_min,
                bike_target_min,
                run_target_min,
                overall_target_min
            FROM goals
            WHERE id = 1
        """)

        goal = cursor.fetchone()

    return dict(goal) if goal else None


def save_goal(goal):
    with get_connection() as connection:
        connection.execute("""
            INSERT INTO goals (
                id,
                race_name,
                race_date,
                swim_distance_km,
                bike_distance_km,
                run_distance_km,
                swim_target_min,
                bike_target_min,
                run_target_min,
                overall_target_min
            )
            VALUES (1, ?, ?, ?, ?, ?, ?, ?, ?, ?)

            ON CONFLICT(id) DO UPDATE SET
                race_name = excluded.race_name,
                race_date = excluded.race_date,
                swim_distance_km = excluded.swim_distance_km,
                bike_distance_km = excluded.bike_distance_km,
                run_distance_km = excluded.run_distance_km,
                swim_target_min = excluded.swim_target_min,
                bike_target_min = excluded.bike_target_min,
                run_target_min = excluded.run_target_min,
                overall_target_min = excluded.overall_target_min
        """, (
            goal["race_name"],
            goal.get("race_date"),
            goal["swim_distance_km"],
            goal["bike_distance_km"],
            goal["run_distance_km"],
            goal.get("swim_target_min"),
            goal.get("bike_target_min"),
            goal.get("run_target_min"),
            goal.get("overall_target_min"),
        ))


def initialise_hr_profile_table():
    with get_connection() as connection:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS hr_profile (
                id INTEGER PRIMARY KEY CHECK (id = 1),
                max_hr INTEGER NOT NULL,
                resting_hr INTEGER NOT NULL
            )
        """)


def get_hr_profile():
    initialise_hr_profile_table()

    with get_connection() as connection:
        connection.row_factory = sqlite3.Row

        cursor = connection.execute("""
            SELECT
                max_hr,
                resting_hr
            FROM hr_profile
            WHERE id = 1
        """)

        profile = cursor.fetchone()

    return dict(profile) if profile else None


def save_hr_profile(profile):
    initialise_hr_profile_table()

    with get_connection() as connection:
        connection.execute("""
            INSERT INTO hr_profile (
                id,
                max_hr,
                resting_hr
            )
            VALUES (1, ?, ?)

            ON CONFLICT(id) DO UPDATE SET
                max_hr = excluded.max_hr,
                resting_hr = excluded.resting_hr
        """, (
            profile["max_hr"],
            profile["resting_hr"],
        ))

def update_activity(activity):
    with get_connection() as connection:
        connection.execute("""
            UPDATE activities
            SET
                date = ?,
                sport = ?,
                activity_type = ?,
                distance_km = ?,
                duration_min = ?,
                avg_hr = ?
            WHERE strava_id = ?
        """, (
            activity["date"],
            activity["sport"],
            activity.get("activity_type"),
            activity["distance_km"],
            activity["duration_min"],
            activity["avg_hr"],
            activity["strava_id"],
        ))


def delete_activity(strava_id):
    with get_connection() as connection:
        connection.execute(
            """
            DELETE FROM activities
            WHERE strava_id = ?
            """,
            (strava_id,),
        )