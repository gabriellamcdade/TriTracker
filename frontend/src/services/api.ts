import type {
  Activity,
  HealthResponse,
  Recommendation,
  Recovery,
  TrainingSummary,
  WeeklyTrainingLoad,
} from "../types";

const API_BASE_URL = "http://127.0.0.1:8000";

export type HealthResponse = {
  status: string;
  service: string;
};

export type Activity = {
  strava_id: number;
  date: string;
  sport: "Run" | "Bike" | "Swim";
  distance_km: number;
  duration_min: number;
  avg_hr: number | null;
};

export type SportSummary = {
  distance_km: number;
  duration_min: number;
};

export type TrainingSummary = {
  Run: SportSummary;
  Bike: SportSummary;
  Swim: SportSummary;
  total_training_minutes: number;
};

export type WeeklyTrainingLoad = {
  week: string;
  sports: Partial<Record<"Run" | "Bike" | "Swim", number>>;
  total_training_load: number;
  percentage_change: number | null;
};

export type Recovery = {
  score: number;
  status: "GOOD" | "CAUTION" | "LOW";
  recommendation: "MODERATE" | "EASY" | "REST";
  recent_week: string;
  recent_load: number;
  previous_load: number;
  load_change: number;
  high_intensity_percent: number;
};

export type Recommendation = {
  workout_type: "REST" | "EASY" | "QUALITY";
  sport: "Run" | "Bike" | "Swim" | null;
  duration_min: number;
  intensity: string;
  workout_plan: string[];
  recovery_score: number;
  reason: string;
  recent_sport_minutes?: number;
  target_sport_minutes?: number;
  race_distance?: string;
};

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