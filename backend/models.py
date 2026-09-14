from sqlalchemy import (
    Column, Integer, String, Float, DateTime, Text,
    Boolean, ForeignKey, Enum as SAEnum, func
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import enum

try:
    from geoalchemy2 import Geometry
    HAS_GEOALCHEMY = True
except ImportError:
    HAS_GEOALCHEMY = False
    Geometry = None

Base = declarative_base()


# ── Enums ─────────────────────────────────────────────────────────────────────

class UserRole(str, enum.Enum):
    ADMIN            = "ADMIN"
    DISTRICT_OFFICER = "DISTRICT_OFFICER"
    FIELD_OFFICER    = "FIELD_OFFICER"
    VIEWER           = "VIEWER"

class RiskLevel(str, enum.Enum):
    LOW      = "LOW"
    MEDIUM   = "MEDIUM"
    HIGH     = "HIGH"
    CRITICAL = "CRITICAL"

class AlertStatus(str, enum.Enum):
    ACTIVE       = "ACTIVE"
    ACKNOWLEDGED = "ACKNOWLEDGED"
    ESCALATED    = "ESCALATED"
    RESOLVED     = "RESOLVED"
    EXPIRED      = "EXPIRED"

class RoadStatus(str, enum.Enum):
    OPEN       = "OPEN"
    RESTRICTED = "RESTRICTED"
    BLOCKED    = "BLOCKED"
    UNKNOWN    = "UNKNOWN"

class IncidentCategory(str, enum.Enum):
    LANDSLIDE        = "LANDSLIDE"
    CRACK            = "CRACK"
    SLOPE_MOVEMENT   = "SLOPE_MOVEMENT"
    ROAD_BLOCKAGE    = "ROAD_BLOCKAGE"
    FLOODING         = "FLOODING"
    DRAINAGE_FAILURE = "DRAINAGE_FAILURE"
    OTHER            = "OTHER"

class IncidentStatus(str, enum.Enum):
    SUBMITTED            = "SUBMITTED"
    PENDING_VERIFICATION = "PENDING_VERIFICATION"
    VERIFIED             = "VERIFIED"
    REJECTED             = "REJECTED"

class PlanStatus(str, enum.Enum):
    PLANNED     = "PLANNED"
    APPROVED    = "APPROVED"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED   = "COMPLETED"
    CANCELLED   = "CANCELLED"

class DataMode(str, enum.Enum):
    ML_INFERENCE = "ML_INFERENCE"
    SIMULATION   = "SIMULATION"


# ── Models ────────────────────────────────────────────────────────────────────

class User(Base):
    __tablename__ = "users"
    id            = Column(Integer, primary_key=True, index=True)
    name          = Column(String(128), nullable=False)
    email         = Column(String(256), unique=True, nullable=False, index=True)
    hashed_pw     = Column(String(256), nullable=False)
    role          = Column(SAEnum(UserRole), default=UserRole.VIEWER, nullable=False)
    is_active     = Column(Boolean, default=True)
    created_at    = Column(DateTime(timezone=True), server_default=func.now())


class Region(Base):
    __tablename__ = "regions"
    id   = Column(Integer, primary_key=True)
    name = Column(String(128), unique=True, nullable=False)
    # geometry: Polygon / MultiPolygon (PostGIS, SRID 4326)
    if HAS_GEOALCHEMY:
        geom = Column(Geometry("MULTIPOLYGON", srid=4326))

    villages       = relationship("Village",       back_populates="region")
    risk_preds     = relationship("RiskPrediction", back_populates="region")
    reloc_plans    = relationship("RelocationPlan", back_populates="region")


class Village(Base):
    __tablename__ = "villages"
    id          = Column(Integer, primary_key=True)
    name        = Column(String(128), nullable=False)
    region_id   = Column(Integer, ForeignKey("regions.id"), nullable=True)
    population  = Column(Integer, nullable=False, default=0)
    district    = Column(String(128))
    taluk       = Column(String(128))
    if HAS_GEOALCHEMY:
        geom    = Column(Geometry("POINT", srid=4326))

    region      = relationship("Region", back_populates="villages")
    assignments = relationship("RelocationAssignment", back_populates="village")


class Road(Base):
    __tablename__ = "roads"
    id           = Column(Integer, primary_key=True)
    name         = Column(String(256), nullable=False)
    road_type    = Column(String(64))                  # NH, SH, MDR, etc.
    status       = Column(SAEnum(RoadStatus), default=RoadStatus.OPEN)
    criticality  = Column(Float, default=0.5)          # 0–1
    location_desc = Column(Text)
    last_updated = Column(DateTime(timezone=True), server_default=func.now())
    if HAS_GEOALCHEMY:
        geom     = Column(Geometry("LINESTRING", srid=4326))


class HistoricalLandslide(Base):
    __tablename__ = "historical_landslides"
    id         = Column(Integer, primary_key=True)
    date       = Column(DateTime(timezone=True))
    severity   = Column(SAEnum(RiskLevel))
    source     = Column(String(256))
    notes      = Column(Text)
    if HAS_GEOALCHEMY:
        geom   = Column(Geometry("POINT", srid=4326))


class WeatherObservation(Base):
    __tablename__ = "weather_observations"
    id              = Column(Integer, primary_key=True)
    region_id       = Column(Integer, ForeignKey("regions.id"), nullable=True)
    station_name    = Column(String(128))
    observed_rainfall_mm = Column(Float)
    temperature_c   = Column(Float)
    humidity_pct    = Column(Float)
    soil_moisture   = Column(Float)
    timestamp       = Column(DateTime(timezone=True), nullable=False)
    data_source     = Column(String(128))    # IMD, OpenWeather, sensor, etc.
    if HAS_GEOALCHEMY:
        geom        = Column(Geometry("POINT", srid=4326))


class WeatherForecast(Base):
    __tablename__ = "weather_forecasts"
    id              = Column(Integer, primary_key=True)
    region_id       = Column(Integer, ForeignKey("regions.id"), nullable=True)
    forecast_rainfall_mm = Column(Float)
    forecast_for    = Column(DateTime(timezone=True))   # target time
    issued_at       = Column(DateTime(timezone=True), server_default=func.now())
    model_source    = Column(String(128))


class RiskPrediction(Base):
    __tablename__ = "risk_predictions"
    id              = Column(Integer, primary_key=True)
    region_id       = Column(Integer, ForeignKey("regions.id"), nullable=True)
    risk_score      = Column(Float, nullable=False)
    risk_level      = Column(SAEnum(RiskLevel), nullable=False)
    rainfall_7d     = Column(Float)
    slope_degrees   = Column(Float)
    elevation_m     = Column(Float)
    soil_saturation = Column(Float)
    data_mode       = Column(SAEnum(DataMode), default=DataMode.SIMULATION)
    model_version   = Column(String(64))
    predicted_at    = Column(DateTime(timezone=True), server_default=func.now())
    if HAS_GEOALCHEMY:
        geom        = Column(Geometry("POLYGON", srid=4326))

    region = relationship("Region", back_populates="risk_preds")
    alerts = relationship("Alert",  back_populates="risk_prediction")


class Alert(Base):
    __tablename__ = "alerts"
    id                  = Column(Integer, primary_key=True)
    risk_prediction_id  = Column(Integer, ForeignKey("risk_predictions.id"), nullable=True)
    region_name         = Column(String(256), nullable=False)
    severity            = Column(SAEnum(RiskLevel), nullable=False)
    status              = Column(SAEnum(AlertStatus), default=AlertStatus.ACTIVE)
    message             = Column(Text)
    affected_villages   = Column(Integer, default=0)
    affected_population = Column(Integer, default=0)
    risk_score          = Column(Float)
    created_at          = Column(DateTime(timezone=True), server_default=func.now())
    updated_at          = Column(DateTime(timezone=True), onupdate=func.now())
    acknowledged_by_id  = Column(Integer, ForeignKey("users.id"), nullable=True)

    risk_prediction = relationship("RiskPrediction", back_populates="alerts")


class Incident(Base):
    __tablename__ = "incidents"
    id              = Column(Integer, primary_key=True)
    category        = Column(SAEnum(IncidentCategory), nullable=False)
    description     = Column(Text, nullable=False)
    severity        = Column(SAEnum(RiskLevel), nullable=False)
    status          = Column(SAEnum(IncidentStatus), default=IncidentStatus.SUBMITTED)
    reported_by     = Column(String(256))
    reporter_role   = Column(SAEnum(UserRole), default=UserRole.VIEWER)
    village_id      = Column(Integer, ForeignKey("villages.id"), nullable=True)
    village_name    = Column(String(128))          # denormalized for offline reports
    nearest_road_id = Column(Integer, ForeignKey("roads.id"), nullable=True)
    image_url       = Column(String(512))
    notes           = Column(Text)
    created_at      = Column(DateTime(timezone=True), server_default=func.now())
    verified_at     = Column(DateTime(timezone=True), nullable=True)
    verified_by_id  = Column(Integer, ForeignKey("users.id"), nullable=True)
    if HAS_GEOALCHEMY:
        geom        = Column(Geometry("POINT", srid=4326))


class SafeLocation(Base):
    __tablename__ = "safe_locations"
    id                = Column(Integer, primary_key=True)
    name              = Column(String(256), nullable=False)
    total_capacity    = Column(Integer, nullable=False)
    suitability_score = Column(Float)            # 0–1
    road_access       = Column(String(256))
    hazard_level      = Column(SAEnum(RiskLevel), default=RiskLevel.LOW)
    distance_km       = Column(Float)
    if HAS_GEOALCHEMY:
        geom          = Column(Geometry("POINT", srid=4326))

    assignments = relationship("RelocationAssignment", back_populates="safe_location")


class RelocationPlan(Base):
    __tablename__ = "relocation_plans"
    id               = Column(Integer, primary_key=True)
    region_id        = Column(Integer, ForeignKey("regions.id"), nullable=True)
    total_population = Column(Integer, default=0)
    status           = Column(SAEnum(PlanStatus), default=PlanStatus.PLANNED)
    notes            = Column(Text)
    created_by_id    = Column(Integer, ForeignKey("users.id"), nullable=True)
    created_at       = Column(DateTime(timezone=True), server_default=func.now())

    region      = relationship("Region",              back_populates="reloc_plans")
    assignments = relationship("RelocationAssignment", back_populates="plan")


class RelocationAssignment(Base):
    __tablename__ = "relocation_assignments"
    id                  = Column(Integer, primary_key=True)
    plan_id             = Column(Integer, ForeignKey("relocation_plans.id"), nullable=False)
    village_id          = Column(Integer, ForeignKey("villages.id"), nullable=True)
    safe_location_id    = Column(Integer, ForeignKey("safe_locations.id"), nullable=False)
    assigned_population = Column(Integer, nullable=False)
    transport_info      = Column(Text)
    priority            = Column(Integer, default=1)   # P1, P2, P3 ...
    status              = Column(SAEnum(PlanStatus), default=PlanStatus.PLANNED)

    plan          = relationship("RelocationPlan",  back_populates="assignments")
    village       = relationship("Village",         back_populates="assignments")
    safe_location = relationship("SafeLocation",    back_populates="assignments")


class AuditLog(Base):
    __tablename__ = "audit_logs"
    id         = Column(Integer, primary_key=True)
    actor_id   = Column(Integer, ForeignKey("users.id"), nullable=True)
    action     = Column(String(128), nullable=False)
    target     = Column(String(256))
    details    = Column(Text)
    timestamp  = Column(DateTime(timezone=True), server_default=func.now())
