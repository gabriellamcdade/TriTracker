import type {
  Activity,
  HealthResponse,
  Recommendation,
  Recovery,
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