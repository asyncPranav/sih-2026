"""
SIH26001 Backend — FastAPI Application
Phases 2 + 5 + 6 + 7: Core APIs, Exposure, Alerts, Incidents, Relocation
"""
from fastapi import FastAPI, APIRouter, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from enum import Enum

# ── App ───────────────────────────────────────────────────────────────────────
app = FastAPI(
    title="SIH26001 — Landslide Early Warning & Risk Monitoring API",
    description="""
## Landslide Early Warning & Risk Monitoring System
**Region:** East Sikkim, India  |  **Mode:** DEMO / SIMULATION

### Capabilities
- Dashboard summary (KPIs)
- Risk predictions with configurable thresholds
- Alert lifecycle management (ACTIVE → RESOLVED)
- Exposure analysis (affected villages, population, roads)
- Incident reporting + verification workflow
- Relocation intelligence (suitability scoring, plan generation)
- Weather observations & forecasts
    """,
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:5174", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

api = APIRouter(prefix="/api")


# ── Enums ─────────────────────────────────────────────────────────────────────
class RiskLevel(str, Enum):
    LOW      = "LOW"
    MEDIUM   = "MEDIUM"
    HIGH     = "HIGH"
    CRITICAL = "CRITICAL"

class AlertStatus(str, Enum):
    ACTIVE       = "ACTIVE"
    ACKNOWLEDGED = "ACKNOWLEDGED"
    ESCALATED    = "ESCALATED"
    RESOLVED     = "RESOLVED"

class IncidentCategory(str, Enum):
    LANDSLIDE        = "LANDSLIDE"
    CRACK            = "CRACK"
    SLOPE_MOVEMENT   = "SLOPE_MOVEMENT"
    ROAD_BLOCKAGE    = "ROAD_BLOCKAGE"
    FLOODING         = "FLOODING"
    DRAINAGE_FAILURE = "DRAINAGE_FAILURE"
    OTHER            = "OTHER"

class IncidentStatus(str, Enum):
    SUBMITTED            = "SUBMITTED"
    PENDING_VERIFICATION = "PENDING_VERIFICATION"
    VERIFIED             = "VERIFIED"
    REJECTED             = "REJECTED"

class RoadStatus(str, Enum):
    OPEN       = "OPEN"
    RESTRICTED = "RESTRICTED"
    BLOCKED    = "BLOCKED"
    UNKNOWN    = "UNKNOWN"

class DataMode(str, Enum):
    ML_INFERENCE = "ML_INFERENCE"
    SIMULATION   = "SIMULATION"


# ── Pydantic Schemas ──────────────────────────────────────────────────────────

class VillageOut(BaseModel):
    id: str; name: str; population: int; lat: float; lng: float
    risk_level: RiskLevel; risk_score: float; district: str; nearest_road: str

class RiskZoneOut(BaseModel):
    id: str; lat: float; lng: float; radius_km: float
    risk_level: RiskLevel; risk_score: float; rainfall_7d: float
    slope: float; elevation: float

class AlertOut(BaseModel):
    id: str; region_name: str; risk_level: RiskLevel; risk_score: float
    status: AlertStatus; message: str; created_at: str
    affected_villages: int; affected_population: int

class AlertUpdateIn(BaseModel):
    status: AlertStatus
    notes: Optional[str] = None

class IncidentOut(BaseModel):
    id: str; type: IncidentCategory; description: str; lat: float; lng: float
    severity: RiskLevel; status: IncidentStatus; reported_by: str
    created_at: str; village: str

class IncidentCreateIn(BaseModel):
    type: IncidentCategory
    description: str = Field(..., min_length=10)
    lat: float = Field(..., ge=20, le=35)
    lng: float = Field(..., ge=80, le=100)
    severity: RiskLevel
    village: str
    reported_by: str = "Anonymous"

class SafeLocationOut(BaseModel):
    id: str; name: str; lat: float; lng: float; capacity: int
    suitability_score: float; road_access: str; hazard_level: RiskLevel
    distance_km: float

class RelocationPlanRow(BaseModel):
    site: str; source_villages: List[str]
    assigned_population: int; capacity: int; utilisation_pct: float

class RelocationPlanOut(BaseModel):
    total_pop_assigned: int; total_capacity: int
    unassigned: int; status: str; rows: List[RelocationPlanRow]

class RainfallPoint(BaseModel):
    day: str; mm: float

class WeatherOut(BaseModel):
    rainfall_24h: float; rainfall_7d: float; rainfall_intensity: str
    soil_moisture: str; last_updated: str; data_mode: DataMode
    history: List[RainfallPoint]

class DashboardSummaryOut(BaseModel):
    critical_zones: int; active_alerts: int; affected_villages: int
    population_at_risk: int; blocked_roads: int; restricted_roads: int
    safe_sites: int; total_safe_capacity: int; pending_incidents: int
    data_mode: DataMode


# ── Mock Data (Phase 2 stub — DB wiring in later phase) ──────────────────────

_VILLAGES = [
    {"id": "v1",  "name": "Rongli",      "population": 2100, "lat": 27.2077, "lng": 88.7441, "risk_level": "CRITICAL", "risk_score": 0.87, "district": "East Sikkim", "nearest_road": "NH-10"},
    {"id": "v2",  "name": "Rhenock",     "population": 1800, "lat": 27.1889, "lng": 88.6800, "risk_level": "HIGH",     "risk_score": 0.71, "district": "East Sikkim", "nearest_road": "SH-10"},
    {"id": "v3",  "name": "Pakyong",     "population": 3200, "lat": 27.2067, "lng": 88.6100, "risk_level": "HIGH",     "risk_score": 0.65, "district": "East Sikkim", "nearest_road": "NH-717A"},
    {"id": "v4",  "name": "Rangpo",      "population": 4100, "lat": 27.1760, "lng": 88.5317, "risk_level": "MEDIUM",   "risk_score": 0.42, "district": "East Sikkim", "nearest_road": "NH-10"},
    {"id": "v5",  "name": "Singtam",     "population": 5200, "lat": 27.2375, "lng": 88.5010, "risk_level": "MEDIUM",   "risk_score": 0.38, "district": "East Sikkim", "nearest_road": "NH-10"},
    {"id": "v6",  "name": "Dikchu",      "population": 900,  "lat": 27.3600, "lng": 88.5600, "risk_level": "HIGH",     "risk_score": 0.68, "district": "East Sikkim", "nearest_road": "SH-2"},
    {"id": "v7",  "name": "Mangan",      "population": 2400, "lat": 27.5050, "lng": 88.5344, "risk_level": "MEDIUM",   "risk_score": 0.45, "district": "North Sikkim","nearest_road": "SH-2"},
    {"id": "v8",  "name": "Aritar",      "population": 1100, "lat": 27.1500, "lng": 88.7300, "risk_level": "HIGH",     "risk_score": 0.72, "district": "East Sikkim", "nearest_road": "SH-11"},
    {"id": "v9",  "name": "Lingtam",     "population": 620,  "lat": 27.1700, "lng": 88.7700, "risk_level": "CRITICAL", "risk_score": 0.84, "district": "East Sikkim", "nearest_road": "SH-11"},
    {"id": "v10", "name": "Tarku",       "population": 430,  "lat": 27.2300, "lng": 88.7900, "risk_level": "HIGH",     "risk_score": 0.69, "district": "East Sikkim", "nearest_road": "None"},
    {"id": "v11", "name": "Namprikdang","population": 810,  "lat": 27.2800, "lng": 88.6500, "risk_level": "MEDIUM",   "risk_score": 0.44, "district": "East Sikkim", "nearest_road": "SH-10"},
    {"id": "v12", "name": "Makha",       "population": 560,  "lat": 27.2200, "lng": 88.6300, "risk_level": "LOW",      "risk_score": 0.18, "district": "East Sikkim", "nearest_road": "SH-10"},
    {"id": "v13", "name": "Rachela",     "population": 340,  "lat": 27.1400, "lng": 88.7500, "risk_level": "CRITICAL", "risk_score": 0.91, "district": "East Sikkim", "nearest_road": "None"},
    {"id": "v14", "name": "Kupup",       "population": 290,  "lat": 27.3800, "lng": 88.7000, "risk_level": "HIGH",     "risk_score": 0.73, "district": "East Sikkim", "nearest_road": "Old Silk Route"},
]

_ALERTS = [
    {"id": "al1", "region_name": "Rongli – Lingtam Corridor", "risk_level": "CRITICAL", "risk_score": 0.89, "status": "ACTIVE",       "message": "Extreme rainfall accumulation (184 mm / 7d) on steep slope terrain. Immediate evacuation recommended for 3 villages.", "created_at": "2026-09-08T14:30:00Z", "affected_villages": 3, "affected_population": 3030},
    {"id": "al2", "region_name": "Rhenock – Aritar Zone",     "risk_level": "HIGH",     "risk_score": 0.71, "status": "ACKNOWLEDGED",  "message": "High slope instability detected. Road SH-11 partially blocked. Field verification in progress.",                       "created_at": "2026-09-08T11:15:00Z", "affected_villages": 2, "affected_population": 2900},
    {"id": "al3", "region_name": "Dikchu Valley",              "risk_level": "HIGH",     "risk_score": 0.68, "status": "ACTIVE",        "message": "Soil saturation above threshold. Slope movement reported by field officer.",                                            "created_at": "2026-09-08T09:00:00Z", "affected_villages": 1, "affected_population": 900},
    {"id": "al4", "region_name": "Pakyong Sub-Division",      "risk_level": "MEDIUM",   "risk_score": 0.44, "status": "RESOLVED",      "message": "Risk decreased below threshold after 12h dry period.",                                                                 "created_at": "2026-09-07T18:00:00Z", "affected_villages": 1, "affected_population": 3200},
]

_INCIDENTS = [
    {"id": "in1","type":"LANDSLIDE",       "description":"Major landslide blocking NH-10 near Rongli bridge. Debris ~15m across.",     "lat":27.2100,"lng":88.7400,"severity":"CRITICAL","status":"VERIFIED",            "reported_by":"Field Officer - Suresh Kumar","created_at":"2026-09-08T13:45:00Z","village":"Rongli"},
    {"id": "in2","type":"CRACK",           "description":"Large longitudinal crack observed on slope near Rachela village (~40m long).","lat":27.1400,"lng":88.7500,"severity":"HIGH",    "status":"VERIFIED",            "reported_by":"Citizen Report",             "created_at":"2026-09-08T12:20:00Z","village":"Rachela"},
    {"id": "in3","type":"ROAD_BLOCKAGE",   "description":"SH-11 partially blocked by debris at km marker 23. One lane passable.",      "lat":27.1700,"lng":88.7200,"severity":"HIGH",    "status":"VERIFIED",            "reported_by":"Field Officer - Priya Rai",   "created_at":"2026-09-08T10:30:00Z","village":"Lingtam"},
    {"id": "in4","type":"SLOPE_MOVEMENT",  "description":"Slow slope creep detected near Aritar. Trees visibly tilted.",               "lat":27.1500,"lng":88.7300,"severity":"MEDIUM",  "status":"PENDING_VERIFICATION","reported_by":"Citizen Report",             "created_at":"2026-09-08T09:10:00Z","village":"Aritar"},
    {"id": "in5","type":"FLOODING",        "description":"Flash flood in Dikchu valley. River overflowing banks near settlement.",      "lat":27.3600,"lng":88.5600,"severity":"HIGH",    "status":"PENDING_VERIFICATION","reported_by":"Citizen Report",             "created_at":"2026-09-08T08:00:00Z","village":"Dikchu"},
    {"id": "in6","type":"DRAINAGE_FAILURE","description":"Blocked culvert causing water accumulation on SH-10.",                        "lat":27.2300,"lng":88.6100,"severity":"MEDIUM",  "status":"SUBMITTED",           "reported_by":"Citizen Report",             "created_at":"2026-09-08T07:30:00Z","village":"Pakyong"},
]

_SAFE_LOCATIONS = [
    {"id":"sl1","name":"Gangtok Sports Complex",          "lat":27.3389,"lng":88.6065,"capacity":2000,"suitability_score":0.94,"road_access":"NH-10 (Open)",   "hazard_level":"LOW",   "distance_km":18},
    {"id":"sl2","name":"Rangpo Relief Camp",               "lat":27.1760,"lng":88.5317,"capacity":1500,"suitability_score":0.88,"road_access":"NH-10 (Open)",   "hazard_level":"LOW",   "distance_km":22},
    {"id":"sl3","name":"Singtam Community Hall",           "lat":27.2375,"lng":88.5010,"capacity":800, "suitability_score":0.81,"road_access":"NH-10 (Open)",   "hazard_level":"LOW",   "distance_km":24},
    {"id":"sl4","name":"Pakyong Airport Grounds",          "lat":27.2067,"lng":88.6100,"capacity":1200,"suitability_score":0.79,"road_access":"NH-717A (Open)", "hazard_level":"LOW",   "distance_km":12},
    {"id":"sl5","name":"Rhenock Higher Secondary School",  "lat":27.1889,"lng":88.6500,"capacity":600, "suitability_score":0.72,"road_access":"SH-10 (Open)",   "hazard_level":"MEDIUM","distance_km":8},
]

_RAINFALL_HISTORY = [
    {"day": "Sep 2", "mm": 24}, {"day": "Sep 3", "mm": 38}, {"day": "Sep 4", "mm": 61},
    {"day": "Sep 5", "mm": 74}, {"day": "Sep 6", "mm": 52}, {"day": "Sep 7", "mm": 91},
    {"day": "Sep 8", "mm": 142},
]

# In-memory incident store (Phase 7 stub — DB in Phase 2)
_incident_counter = [len(_INCIDENTS)]
_incidents_store  = list(_INCIDENTS)


# ── Health ────────────────────────────────────────────────────────────────────

@api.get("/health", tags=["System"])
def health_check():
    return {"status": "healthy", "mode": "DEMO/SIMULATION", "version": "0.1.0",
            "timestamp": datetime.utcnow().isoformat() + "Z"}


# ── Dashboard Summary ─────────────────────────────────────────────────────────

@api.get("/dashboard/summary", response_model=DashboardSummaryOut, tags=["Dashboard"])
def dashboard_summary():
    active_alerts = [a for a in _ALERTS if a["status"] == "ACTIVE"]
    affected_villages = sum(a["affected_villages"] for a in active_alerts)
    pop_at_risk = sum(v["population"] for v in _VILLAGES if v["risk_level"] in ("CRITICAL", "HIGH"))
    pending_incs = len([i for i in _incidents_store if i["status"] in ("SUBMITTED", "PENDING_VERIFICATION")])
    return DashboardSummaryOut(
        critical_zones=len([z for z in _RISK_ZONES if z["risk_level"] == "CRITICAL"]),
        active_alerts=len(active_alerts),
        affected_villages=affected_villages, population_at_risk=pop_at_risk,
        blocked_roads=1, restricted_roads=1,
        safe_sites=len(_SAFE_LOCATIONS),
        total_safe_capacity=sum(s["capacity"] for s in _SAFE_LOCATIONS),
        pending_incidents=pending_incs,
        data_mode=DataMode.SIMULATION,
    )


# ── Scenario Simulation (Phase 8) ──────────────────────────────────────────────

class SimulationParams(BaseModel):
    rainfall_multiplier: float = Field(default=1.5, ge=0.5, le=5.0)

def calc_risk_level(score: float) -> str:
    if score >= 0.8: return "CRITICAL"
    if score >= 0.6: return "HIGH"
    if score >= 0.3: return "MEDIUM"
    return "LOW"

@api.post("/simulation/trigger", tags=["Simulation"])
def trigger_simulation(params: SimulationParams):
    """
    Triggers a weather anomaly. Increases rainfall and recalculates risk scores.
    """
    global _ALERTS
    
    # Increase rainfall and recalculate risk zones
    for z in _RISK_ZONES:
        z["rainfall_7d"] = round(z["rainfall_7d"] * params.rainfall_multiplier, 1)
        z["risk_score"] = min(0.99, round(z["risk_score"] + (params.rainfall_multiplier * 0.1), 2))
        z["risk_level"] = calc_risk_level(z["risk_score"])
        
    # Recalculate village risk based on their baseline
    for v in _VILLAGES:
        v["risk_score"] = min(0.99, round(v["risk_score"] + (params.rainfall_multiplier * 0.08), 2))
        v["risk_level"] = calc_risk_level(v["risk_score"])
        
    # Generate new alerts for CRITICAL zones if not already present
    critical_zones = [z for z in _RISK_ZONES if z["risk_level"] == "CRITICAL"]
    for i, z in enumerate(critical_zones):
        # check if alert exists
        if not any(a["region_name"] == f"Zone {z['id']} Corridor" for a in _ALERTS if a["status"] == "ACTIVE"):
            _ALERTS.insert(0, {
                "id": f"sim_al{len(_ALERTS)+1}", 
                "region_name": f"Zone {z['id']} Corridor", 
                "risk_level": "CRITICAL", 
                "risk_score": z["risk_score"], 
                "status": "ACTIVE",       
                "message": f"Extreme simulated rainfall ({z['rainfall_7d']} mm). Immediate risk of slope failure.", 
                "created_at": datetime.utcnow().isoformat() + "Z", 
                "affected_villages": 2, 
                "affected_population": 1500
            })
            
    return {"status": "success", "message": f"Simulation triggered with multiplier {params.rainfall_multiplier}x. Risk scores recalculated."}


# ── Alerts ─────────────────────────────────────────────────────────────────────

@api.get("/alerts", response_model=List[AlertOut], tags=["Alerts"])
def list_alerts(status: Optional[AlertStatus] = None, risk_level: Optional[RiskLevel] = None):
    data = _ALERTS
    if status:
        data = [a for a in data if a["status"] == status.value]
    if risk_level:
        data = [a for a in data if a["risk_level"] == risk_level.value]
    return [AlertOut(**a) for a in data]

@api.get("/alerts/{alert_id}", response_model=AlertOut, tags=["Alerts"])
def get_alert(alert_id: str):
    a = next((a for a in _ALERTS if a["id"] == alert_id), None)
    if not a:
        raise HTTPException(404, f"Alert '{alert_id}' not found")
    return AlertOut(**a)

@api.patch("/alerts/{alert_id}", response_model=AlertOut, tags=["Alerts"])
def update_alert_status(alert_id: str, body: AlertUpdateIn):
    a = next((a for a in _ALERTS if a["id"] == alert_id), None)
    if not a:
        raise HTTPException(404, f"Alert '{alert_id}' not found")
    a["status"] = body.status.value
    return AlertOut(**a)


# ── Exposure ───────────────────────────────────────────────────────────────────

@api.get("/exposure/villages", response_model=List[VillageOut], tags=["Exposure"])
def exposure_villages(
    risk_level: Optional[RiskLevel] = None,
    min_risk_score: float = Query(0.0, ge=0, le=1),
):
    data = _VILLAGES
    if risk_level:
        data = [v for v in data if v["risk_level"] == risk_level.value]
    data = [v for v in data if v["risk_score"] >= min_risk_score]
    return sorted([VillageOut(**v) for v in data], key=lambda x: -x.risk_score)

@api.get("/exposure/summary", tags=["Exposure"])
def exposure_summary():
    critical = [v for v in _VILLAGES if v["risk_level"] == "CRITICAL"]
    high     = [v for v in _VILLAGES if v["risk_level"] == "HIGH"]
    medium   = [v for v in _VILLAGES if v["risk_level"] == "MEDIUM"]
    return {
        "data_mode": "SIMULATION",
        "total_villages_assessed": len(_VILLAGES),
        "by_risk_level": {
            "CRITICAL": {"villages": len(critical), "population": sum(v["population"] for v in critical)},
            "HIGH":     {"villages": len(high),     "population": sum(v["population"] for v in high)},
            "MEDIUM":   {"villages": len(medium),   "population": sum(v["population"] for v in medium)},
        },
        "total_population_at_risk": sum(v["population"] for v in _VILLAGES if v["risk_level"] != "LOW"),
        "operational_priority_queue": [
            {"rank": i + 1, "village": v["name"], "population": v["population"], "risk_level": v["risk_level"], "risk_score": v["risk_score"]}
            for i, v in enumerate(sorted(
                [v for v in _VILLAGES if v["risk_level"] in ("CRITICAL", "HIGH")],
                key=lambda x: -x["risk_score"]
            )[:6])
        ],
    }


# ── Incidents ──────────────────────────────────────────────────────────────────

@api.get("/incidents", response_model=List[IncidentOut], tags=["Incidents"])
def list_incidents(
    status: Optional[IncidentStatus] = None,
    category: Optional[IncidentCategory] = None,
):
    data = _incidents_store
    if status:
        data = [i for i in data if i["status"] == status.value]
    if category:
        data = [i for i in data if i["type"] == category.value]
    return [IncidentOut(**i) for i in data]

@api.post("/incidents", response_model=IncidentOut, status_code=201, tags=["Incidents"])
def create_incident(body: IncidentCreateIn):
    _incident_counter[0] += 1
    new_id = f"in{_incident_counter[0]}"
    new_inc = {
        "id": new_id,
        "type": body.type.value,
        "description": body.description,
        "lat": body.lat,
        "lng": body.lng,
        "severity": body.severity.value,
        "status": "SUBMITTED",
        "reported_by": body.reported_by,
        "created_at": datetime.utcnow().isoformat() + "Z",
        "village": body.village,
    }
    _incidents_store.append(new_inc)
    return IncidentOut(**new_inc)

@api.patch("/incidents/{incident_id}/verify", response_model=IncidentOut, tags=["Incidents"])
def verify_incident(incident_id: str, status: IncidentStatus):
    inc = next((i for i in _incidents_store if i["id"] == incident_id), None)
    if not inc:
        raise HTTPException(404, "Incident not found")
    inc["status"] = status.value
    return IncidentOut(**inc)


# ── Weather ────────────────────────────────────────────────────────────────────

@api.get("/weather", response_model=WeatherOut, tags=["Weather"])
def get_weather():
    return WeatherOut(
        rainfall_24h=42.0, rainfall_7d=142.0,
        rainfall_intensity="HEAVY", soil_moisture="SATURATED",
        last_updated="2026-09-08T21:30:00Z",
        data_mode=DataMode.SIMULATION,
        history=[RainfallPoint(**r) for r in _RAINFALL_HISTORY],
    )


# ── Safe Locations & Relocation ────────────────────────────────────────────────

@api.get("/safe-locations", response_model=List[SafeLocationOut], tags=["Relocation"])
def list_safe_locations():
    return sorted([SafeLocationOut(**s) for s in _SAFE_LOCATIONS], key=lambda x: -x.suitability_score)

@api.post("/relocation/generate-plan", response_model=RelocationPlanOut, tags=["Relocation"])
def generate_relocation_plan():
    """
    Deterministic greedy capacity allocation (SIMULATION mode).
    Assigns critical + high risk villages to safe sites by suitability score.
    """
    at_risk = sorted(
        [v for v in _VILLAGES if v["risk_level"] in ("CRITICAL", "HIGH")],
        key=lambda x: -x["risk_score"]
    )
    sites = sorted(_SAFE_LOCATIONS, key=lambda x: -x["suitability_score"])

    remaining_caps = {s["id"]: s["capacity"] for s in sites}
    site_assignments: dict = {s["id"]: {"site": s["name"], "source_villages": [], "assigned_population": 0, "capacity": s["capacity"]} for s in sites}

    total_assigned = 0
    for v in at_risk:
        pop_left = v["population"]
        for s in sites:
            if pop_left <= 0:
                break
            available = remaining_caps[s["id"]]
            if available <= 0:
                continue
            to_assign = min(pop_left, available)
            remaining_caps[s["id"]] -= to_assign
            site_assignments[s["id"]]["assigned_population"] += to_assign
            site_assignments[s["id"]]["source_villages"].append(v["name"])
            pop_left -= to_assign
        total_assigned += (v["population"] - pop_left)

    total_pop = sum(v["population"] for v in at_risk)
    total_cap = sum(s["capacity"] for s in _SAFE_LOCATIONS)
    unassigned = max(0, total_pop - total_assigned)

    rows = [
        RelocationPlanRow(
            site=a["site"],
            source_villages=list(dict.fromkeys(a["source_villages"])),
            assigned_population=a["assigned_population"],
            capacity=a["capacity"],
            utilisation_pct=round(a["assigned_population"] / a["capacity"] * 100, 1) if a["capacity"] > 0 else 0,
        )
        for a in site_assignments.values()
        if a["assigned_population"] > 0
    ]

    return RelocationPlanOut(
        total_pop_assigned=total_assigned,
        total_capacity=total_cap,
        unassigned=unassigned,
        status="ALL_ASSIGNED" if unassigned == 0 else "PARTIAL",
        rows=rows,
    )


# ── Risk Zones ─────────────────────────────────────────────────────────────────

_RISK_ZONES = [
    {"id": "rz1", "lat": 27.18, "lng": 88.74, "radius_km": 6.5, "risk_level": "CRITICAL", "risk_score": 0.89, "rainfall_7d": 184, "slope": 36, "elevation": 1820},
    {"id": "rz2", "lat": 27.25, "lng": 88.68, "radius_km": 4.0, "risk_level": "HIGH",     "risk_score": 0.71, "rainfall_7d": 142, "slope": 28, "elevation": 1340},
    {"id": "rz3", "lat": 27.35, "lng": 88.57, "radius_km": 3.0, "risk_level": "HIGH",     "risk_score": 0.67, "rainfall_7d": 121, "slope": 24, "elevation": 1120},
    {"id": "rz4", "lat": 27.13, "lng": 88.70, "radius_km": 2.5, "risk_level": "MEDIUM",   "risk_score": 0.44, "rainfall_7d":  89, "slope": 19, "elevation":  960},
]

@api.get("/risk-zones", tags=["Risk"])
def list_risk_zones():
    return {
        "data_mode": "SIMULATION",
        "zones": _RISK_ZONES,
    }


# ── Include Router ────────────────────────────────────────────────────────────
app.include_router(api)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
