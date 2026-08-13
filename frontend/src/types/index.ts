export type Sport = "Run" | "Bike" | "Swim";

export type HealthResponse = {
  status: string;
  service: string;
};

export type Activity = {
  strava_id: number;
  date: string;
  sport: Sport;
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
  sports: Partial<Record<Sport, number>>;
  total_training_load: number;
  percentage_change: number | null;
};

export type RecoveryStatus = "GOOD" | "CAUTION" | "LOW";
export type RecommendedIntensity = "MODERATE" | "EASY" | "REST";

export type Recovery = {
  score: number;
  status: RecoveryStatus;
  recommendation: RecommendedIntensity;
  recent_week: string;
  recent_load: number;
  previous_load: number;
  load_change: number;
  high_intensity_percent: number;
};

type RestRecommendation = {
  workout_type: "REST";
  sport: null;
  duration_min: 0;
  intensity: "Zone 1 or lower";
  workout_plan: string[];
  reason: string;
  recovery_score: number;
};

type WorkoutRecommendation = {
  workout_type: "EASY" | "QUALITY";
  sport: Sport;
  duration_min: number;
  intensity: "Zone 2" | "Zone 3";
  workout_plan: string[];
  recent_sport_minutes: number;
  target_sport_minutes: number;
  race_distance: string;
  recovery_score: number;
  reason: string;
};

export type Recommendation =
  | RestRecommendation
  | WorkoutRecommendation;