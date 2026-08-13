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
                distance_km REAL NOT NULL,
                duration_min INTEGER NOT NULL,
                avg_hr INTEGER
            )
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
                distance_km,
                duration_min,
                avg_hr
            )
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            activity["strava_id"],
            activity["date"],
            activity["sport"],
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
                distance_km,
                duration_min,
                avg_hr
            FROM activities
            ORDER BY date DESC
        """)

        activities = cursor.fetchall()

    return [dict(activity) for activity in activities]