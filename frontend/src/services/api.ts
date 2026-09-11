import type {
  Activity,
  Goal,
  HealthResponse,
  Recommendation,
  Recovery,
  StravaSyncResult,
  TrainingSummary,
  WeeklyTrainingLoad,
} from "../types";

const API_BASE_URL = "http://127.0.0.1:8000";

async function getJson<T>(endpoint: string): Promise<T> {
  const response = await fetch(`${API_BASE_URL}${endpoint}`);

  if (!response.ok) {
    throw new Error(
      `API request failed: ${response.status} ${response.statusText}`
    );
  }

  return response.json() as Promise<T>;
}

export function getHealth(): Promise<HealthResponse> {
  return getJson<HealthResponse>("/health");
}

export function getSummary(): Promise<TrainingSummary> {
  return getJson<TrainingSummary>("/summary");
}

export function getTrainingLoad(): Promise<WeeklyTrainingLoad[]> {
  return getJson<WeeklyTrainingLoad[]>("/training-load");
}

export function getRecovery(): Promise<Recovery> {
  return getJson<Recovery>("/recovery");
}

export function getActivities(limit = 20): Promise<Activity[]> {
  return getJson<Activity[]>(`/activities?limit=${limit}`);
}

export function getRecommendation(): Promise<Recommendation> {
  return getJson<Recommendation>("/recommendation");
}

export function getGoal(): Promise<Goal | null> {
  return getJson<Goal | null>("/goals");
}
export async function saveGoal(goal: Goal): Promise<Goal> {
  const response = await fetch(`${API_BASE_URL}/goals`, {
    method: "PUT",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(goal),
  });

  if (!response.ok) {
    throw new Error(
      `API request failed: ${response.status} ${response.statusText}`
    );
  }

  return response.json() as Promise<Goal>;
}

export async function syncStrava(): Promise<StravaSyncResult> {
  const response = await fetch(
    `${API_BASE_URL}/strava/sync`,
    {
      method: "POST",
    }
  );

  if (!response.ok) {
    throw new Error(
      `API request failed: ${response.status} ${response.statusText}`
    );
  }

  return response.json() as Promise<StravaSyncResult>;
}