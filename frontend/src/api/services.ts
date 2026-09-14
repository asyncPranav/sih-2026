// ─────────────────────────────────────────────────────────────
//  Typed API service functions — one per backend endpoint
// ─────────────────────────────────────────────────────────────
import { api } from './client';

// ── Types (mirror backend Pydantic schemas) ───────────────────

export type RiskLevel    = 'LOW' | 'MEDIUM' | 'HIGH' | 'CRITICAL';
export type AlertStatus  = 'ACTIVE' | 'ACKNOWLEDGED' | 'ESCALATED' | 'RESOLVED';
export type IncidentCat  = 'LANDSLIDE' | 'CRACK' | 'SLOPE_MOVEMENT' | 'ROAD_BLOCKAGE' | 'FLOODING' | 'DRAINAGE_FAILURE' | 'OTHER';
export type IncidentStat = 'SUBMITTED' | 'PENDING_VERIFICATION' | 'VERIFIED' | 'REJECTED';

export interface DashboardSummary {
  critical_zones: number;
  active_alerts: number;
  affected_villages: number;
  population_at_risk: number;
  blocked_roads: number;
  restricted_roads: number;
  safe_sites: number;
  total_safe_capacity: number;
  pending_incidents: number;
  data_mode: string;
}

export interface Alert {
  id: string;
  region_name: string;
  risk_level: RiskLevel;
  risk_score: number;
  status: AlertStatus;
  message: string;
  created_at: string;
  affected_villages: number;
  affected_population: number;
}

export interface Village {
  id: string;
  name: string;
  population: number;
  lat: number;
  lng: number;
  risk_level: RiskLevel;
  risk_score: number;
  district: string;
  nearest_road: string;
}

export interface ExposureSummary {
  data_mode: string;
  total_villages_assessed: number;
  by_risk_level: Record<RiskLevel, { villages: number; population: number }>;
  total_population_at_risk: number;
  operational_priority_queue: Array<{
    rank: number; village: string; population: number;
    risk_level: RiskLevel; risk_score: number;
  }>;
}

export interface Incident {
  id: string;
  type: IncidentCat;
  description: string;
  lat: number;
  lng: number;
  severity: RiskLevel;
  status: IncidentStat;
  reported_by: string;
  created_at: string;
  village: string;
}

export interface SafeLocation {
  id: string;
  name: string;
  lat: number;
  lng: number;
  capacity: number;
  suitability_score: number;
  road_access: string;
  hazard_level: RiskLevel;
  distance_km: number;
}

export interface RelocationRow {
  site: string;
  source_villages: string[];
  assigned_population: number;
  capacity: number;
  utilisation_pct: number;
}

export interface RelocationPlan {
  total_pop_assigned: number;
  total_capacity: number;
  unassigned: number;
  status: string;
  rows: RelocationRow[];
}

export interface WeatherData {
  rainfall_24h: number;
  rainfall_7d: number;
  rainfall_intensity: string;
  soil_moisture: string;
  last_updated: string;
  data_mode: string;
  history: Array<{ day: string; mm: number }>;
}

export interface RiskZone {
  id: string;
  lat: number;
  lng: number;
  radius_km: number;
  risk_level: RiskLevel;
  risk_score: number;
  rainfall_7d: number;
  slope: number;
  elevation: number;
}

// ── Service calls ─────────────────────────────────────────────

export const ApiService = {
  // Dashboard
  getDashboard: () =>
    api.get<DashboardSummary>('/dashboard/summary'),

  // Alerts
  getAlerts: (status?: AlertStatus) =>
    api.get<Alert[]>(`/alerts${status ? `?status=${status}` : ''}`),
  getAlert: (id: string) =>
    api.get<Alert>(`/alerts/${id}`),
  updateAlertStatus: (id: string, status: AlertStatus) =>
    api.patch<Alert>(`/alerts/${id}`, { status }),

  // Exposure
  getVillages: (riskLevel?: RiskLevel) =>
    api.get<Village[]>(`/exposure/villages${riskLevel ? `?risk_level=${riskLevel}` : ''}`),
  getExposureSummary: () =>
    api.get<ExposureSummary>('/exposure/summary'),

  // Incidents
  getIncidents: (status?: IncidentStat, category?: IncidentCat) => {
    const params = new URLSearchParams();
    if (status)   params.set('status',   status);
    if (category) params.set('category', category);
    const q = params.toString();
    return api.get<Incident[]>(`/incidents${q ? `?${q}` : ''}`);
  },
  createIncident: (body: {
    type: IncidentCat; description: string; lat: number; lng: number;
    severity: RiskLevel; village: string; reported_by?: string;
  }) => api.post<Incident>('/incidents', body),
  verifyIncident: (id: string, status: IncidentStat) =>
    api.patch<Incident>(`/incidents/${id}/verify?status=${status}`, {}),

  // Safe Locations
  getSafeLocations: () =>
    api.get<SafeLocation[]>('/safe-locations'),

  // Relocation Plan
  generateRelocationPlan: () =>
    api.post<RelocationPlan>('/relocation/generate-plan', {}),

  // Weather
  getWeather: () =>
    api.get<WeatherData>('/weather'),

  // Risk Zones
  getRiskZones: () =>
    api.get<{ data_mode: string; zones: RiskZone[] }>('/risk-zones'),

  // Simulation
  triggerSimulation: (multiplier: number) =>
    api.post<{ status: string; message: string }>('/simulation/trigger', { rainfall_multiplier: multiplier }),
};
