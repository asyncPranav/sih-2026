# SIH26001 — Landslide Early Warning & Risk Monitoring System

## AI-Based Early Warning, Monitoring, GIS Intelligence & Disaster Response Platform

**Problem Statement:** SIH26001
**Organization:** Ministry of Development of North Eastern Region (MDoNER)
**Theme:** Disaster Management
**Category:** Software
**Target Region:** North Eastern Region (NER), India

---

# 1. Project Overview

## 1.1 Problem

The North Eastern Region of India is highly vulnerable to landslides, flash floods, road blockages, and slope failures because of:

* Heavy and irregular rainfall
* Fragile mountainous terrain
* Steep slopes
* Unplanned hill cutting
* Changing climate conditions
* Limited real-time monitoring
* Remote settlements with poor connectivity

Current disaster monitoring is often reactive and dependent on manual reporting.

The system must provide an AI-enabled platform capable of identifying potentially dangerous areas, issuing warnings, visualizing affected infrastructure and settlements, collecting field reports, and supporting emergency decision-making.

---

# 2. Project Goal

Build an integrated disaster intelligence platform following:

**Predict → Monitor → Warn → Assess → Prioritize → Respond**

The system should:

1. Collect environmental and geographical data.
2. Predict landslide risk.
3. Display risk geographically.
4. Detect/track high-risk areas.
5. Identify affected villages and population.
6. Monitor vulnerable roads and infrastructure.
7. Allow citizens/field officials to submit geo-tagged reports.
8. Generate real-time/semi-real-time warnings.
9. Recommend safer areas for emergency relocation.
10. Estimate accommodation/carrying capacity.
11. Prioritize emergency response.
12. Support low-network/offline field reporting.
13. Provide multilingual warning/report interfaces.
14. Provide a web-based command dashboard.
15. Provide a mobile-friendly field interface.

---

# 3. Target Users

## 3.1 Disaster Management Authorities

Primary users.

They need to:

* Monitor regional risk.
* View active warnings.
* Identify affected villages.
* View population at risk.
* Monitor road connectivity.
* View field reports.
* Prioritize emergencies.
* View safe relocation locations.
* Generate relocation plans.

---

## 3.2 District Administration

Should be able to:

* Monitor district-level risk.
* View affected areas.
* View population exposure.
* Track incidents.
* Manage warnings.
* Monitor road accessibility.
* View recommended relocation sites.

---

## 3.3 Field Officials

Should be able to:

* Submit incident reports.
* Upload photos/videos.
* Automatically attach GPS coordinates.
* Report landslides.
* Report cracks.
* Report slope movement.
* Report blocked roads.
* Report flooding.
* Update incident status.
* Work with poor/no connectivity.

---

## 3.4 Citizens

Should be able to:

* Receive warnings.
* View local risk information.
* Submit geo-tagged incident reports.
* Upload photos/videos.
* Report blocked roads or visible slope problems.
* View basic safety information.

---

# 4. High-Level System Architecture

```text
                    DATA SOURCES
                         │
       ┌─────────────────┼──────────────────┐
       │                 │                  │
    Rainfall          Terrain            Historical
    Weather           DEM/Slope          Landslides
       │                 │                  │
       └─────────────────┼──────────────────┘
                         ↓
                 DATA PROCESSING
                         ↓
                  ML RISK ENGINE
                         ↓
                  RISK PREDICTION
                         ↓
              ┌──────────┴──────────┐
              ↓                     ↓
        EARLY WARNING         EXPOSURE ENGINE
              │                     │
              │               Villages/Population
              │                     │
              └──────────┬──────────┘
                         ↓
                   GIS ENGINE
                         ↓
              ┌──────────┴──────────┐
              ↓                     ↓
       ROAD MONITORING       SAFE LOCATION
                                   │
                                   ↓
                         CARRYING CAPACITY
                                   │
                                   ↓
                         RELOCATION PLAN
                                   │
                         ┌─────────┴─────────┐
                         ↓                   ↓
                   WEB/PWA DASHBOARD    MOBILE/FIELD UI
```

---

# 5. Technology Requirements

## 5.1 Frontend

Recommended:

* React
* TypeScript
* Vite
* Tailwind CSS
* Leaflet / React-Leaflet
* PWA support
* Recharts or equivalent chart library

Responsibilities:

* Dashboard
* GIS map
* Risk visualization
* Alerts
* Incident reports
* Relocation recommendations
* Analytics
* Field reporting interface

---

# 5.2 Backend

fastAPi 

The backend should act as the central integration layer.

```text
React / PWA
     ↓
Express API
     ↓
PostgreSQL/PostGIS
     ↓
ML/GIS services
```

FastAPI may be used for the Python ML/GIS service if required.

---

# 5.3 Database

Recommended:

* PostgreSQL
* PostGIS

PostGIS is required/recommended because the application depends heavily on:

* Coordinates
* Polygons
* Risk zones
* Villages
* Roads
* Safe locations
* Spatial intersections
* Distance calculations

---

# 5.4 AI/ML

Recommended:

* Python
* pandas
* NumPy
* scikit-learn
* XGBoost

---

# 5.5 GIS/Data Processing

Recommended:

* GeoPandas
* Rasterio
* GDAL
* Shapely

---

# 6. Functional Requirements

# FR-01 — User Authentication

The system must support authentication.

### Roles

```text
ADMIN
AUTHORITY
FIELD_OFFICIAL
CITIZEN
```

### Requirements

* User registration where appropriate.
* Login.
* Logout.
* JWT authentication.
* Password hashing.
* Role-based access.
* Protected APIs.
* User profile.

---

# FR-02 — Region Management

The system must support geographical regions.

Each region should contain:

* Region ID
* State
* District
* Name
* Boundary geometry
* Risk status

Example:

```json
{
  "id": "region-001",
  "name": "Sample District",
  "state": "Sikkim",
  "riskLevel": "HIGH"
}
```

---

# FR-03 — Environmental Data Management

The system should ingest/store environmental data.

### Required data

* Rainfall
* Soil moisture where available
* Terrain
* Elevation
* Slope
* Historical landslides
* Soil type

### Data pipeline

```text
External Source
      ↓
Data Collection
      ↓
Validation
      ↓
Transformation
      ↓
Database
      ↓
ML/GIS Processing
```

---

# FR-04 — Rainfall Monitoring

The system should monitor rainfall information.

Required information:

* Current rainfall
* Recent rainfall
* 24-hour rainfall
* 3-day rainfall
* 7-day rainfall
* Rainfall intensity
* Historical comparison where available

The system should support integration with weather APIs.

For the MVP, historical/sample weather data may be used if live API access is unavailable.

---

# FR-05 — Terrain Analysis

The system must use terrain information.

Required derived features:

* Elevation
* Slope
* Aspect where useful
* Terrain-related risk

DEM data should be processed into usable spatial layers.

---

# FR-06 — Historical Landslide Data

The system should store historical landslide events.

Each event should ideally contain:

* Location
* Date
* Severity
* Geometry
* Cause where available
* Source
* Description

Historical events will be used for ML training and visualization.

---

# FR-07 — Landslide Risk Prediction

This is the primary AI requirement.

The system must generate a landslide risk score.

### Candidate input features

```text
Slope
Elevation
Rainfall
Rainfall accumulation
Soil type
Historical landslide density
Soil moisture
Terrain characteristics
```

Not every feature needs to be available for the MVP.

---

## FR-07.1 Risk Score

Output:

```text
0.0 — 1.0
```

Example:

```text
0.82
```

---

## FR-07.2 Risk Categories

```text
0.00 – 0.20 → LOW
0.20 – 0.50 → MEDIUM
0.50 – 0.80 → HIGH
0.80 – 1.00 → CRITICAL
```

Thresholds should be configurable.

---

## FR-07.3 Model

Recommended MVP:

**XGBoost Classifier**

The system should expose:

* Prediction probability
* Risk category
* Prediction timestamp
* Model version

Example:

```json
{
  "riskScore": 0.87,
  "riskLevel": "CRITICAL",
  "modelVersion": "xgb-v1",
  "timestamp": "2026-09-08T12:00:00Z"
}
```

---

# FR-08 — Risk Map

The frontend must display risk geographically.

### Requirements

* Interactive map
* Zoom
* Pan
* Risk heatmap/layer
* Risk polygons/cells
* Legend
* Risk filtering

### Risk colors

```text
LOW       → Green
MEDIUM    → Yellow
HIGH      → Orange
CRITICAL  → Red
```

The exact visual implementation may differ.

---

# FR-09 — Early Warning Engine

The system must automatically create warnings when risk crosses configurable thresholds.

Example:

```text
Risk Score = 0.84
       ↓
Threshold = 0.80
       ↓
CRITICAL WARNING
```

Alert should contain:

* Alert ID
* Region
* Geometry
* Risk score
* Risk level
* Timestamp
* Reason
* Status

---

# FR-10 — Alert Management

Authorities should be able to:

* View alerts.
* Acknowledge alerts.
* Resolve alerts.
* Escalate alerts.
* View alert history.

Alert states:

```text
ACTIVE
ACKNOWLEDGED
RESOLVED
EXPIRED
```

---

# FR-11 — Affected Village Detection

The system must identify settlements affected by high-risk areas.

Logic:

```text
Risk Zone
     ↓
Spatial Intersection
     ↓
Affected Villages
```

A village should be identified as affected when its geometry/location intersects or falls within a configured risk zone.

---

# FR-12 — Population at Risk

For every affected region:

Calculate:

```text
Total affected villages
Total population at risk
```

Example:

```json
{
  "villagesAffected": 14,
  "populationAtRisk": 12480
}
```

---

# FR-13 — Village Risk Information

Clicking a village should display:

* Village name
* Population
* Risk level
* Risk score
* Distance from hazard
* Nearby roads
* Nearby safe locations
* Active incidents

---

# FR-14 — Road Connectivity Monitoring

The system must represent road connectivity.

Road states:

```text
OPEN
PARTIALLY_BLOCKED
BLOCKED
UNKNOWN
```

Each road incident may contain:

* Road name
* Location
* Status
* Report source
* Timestamp
* Photo/video
* Severity

---

# FR-15 — Emergency Response Prioritization

The system should rank incidents/areas according to urgency.

Possible factors:

```text
Risk severity
Population exposed
Road connectivity
Distance from settlements
Incident severity
Number of reports
```

Example:

```text
Priority Score =
Risk × 0.40
+ Population Exposure × 0.30
+ Road Criticality × 0.20
+ Incident Severity × 0.10
```

Weights must remain configurable.

Output:

```text
P1 — CRITICAL
P2 — HIGH
P3 — MEDIUM
P4 — LOW
```

---

# FR-16 — Field Incident Reporting

Users must be able to submit reports.

### Report types

```text
LANDSLIDE
CRACK
SLOPE_MOVEMENT
BLOCKED_ROAD
FLOOD
ROCKFALL
OTHER
```

### Report fields

```text
Report ID
User ID
Incident Type
Description
Latitude
Longitude
Timestamp
Photo
Video
Severity
Status
```

---

# FR-17 — Geo-tagged Media

The application must support:

* Camera/photo upload
* Video upload
* GPS coordinates
* Timestamp

Example:

```json
{
  "type": "CRACK",
  "latitude": 27.331,
  "longitude": 88.613,
  "description": "Large crack near road"
}
```

---

# FR-18 — Incident Verification

Authorities should be able to review submitted reports.

Status:

```text
PENDING
VERIFIED
REJECTED
RESOLVED
```

A verified incident can influence the dashboard and prioritization system.

---

# FR-19 — Safe Location Finder

The system must identify potentially suitable relocation locations.

This is a major differentiating feature.

---

## FR-19.1 Exclusion Criteria

Remove locations that have:

* Existing landslide hazard
* High hazard exposure
* Flood risk
* Very steep slope
* Other configured hazards
* Dense urban development where inappropriate

Example:

```text
Slope > 35°
        ↓
EXCLUDE
```

---

## FR-19.2 Desirability Criteria

Score locations based on:

* Low hazard exposure
* Road accessibility
* Flat terrain
* Nearby facilities
* Distance from affected villages
* Available land
* Other configurable criteria

---

# FR-20 — Safe Location Suitability Score

Each candidate should receive a score:

```text
0.0 – 1.0
```

Example:

```text
Site A
Safety:             0.95
Road Access:        0.90
Facility Access:    0.80
Terrain:            0.95

Final Score:        0.91
```

Weights should be configurable.

---

# FR-21 — Top Safe Locations

The system must return approximately:

**2–3 recommended locations**

for the MVP.

Each location should show:

* Name
* Coordinates
* Suitability score
* Distance
* Road accessibility
* Hazard level
* Terrain
* Available land
* Estimated capacity

---

# FR-22 — Carrying Capacity

The system must estimate how many people a safe location can accommodate.

MVP formula:

```text
capacity =
buildable_land_area / space_per_person
```

Example assumption:

```text
25 m²/person
```

This value must be configurable.

The output should contain:

```text
Available land
Land in hectares
Estimated people capacity
Estimated family capacity
```

---

# FR-23 — Relocation Planning

The system must create a basic relocation plan.

Input:

```text
Population requiring relocation
+
Available safe locations
+
Capacity
+
Distance
+
Suitability
```

Output:

```text
Site A → 500 people
Site B → 450 people
Site C → 290 people
```

The algorithm should attempt to:

1. Accommodate everyone.
2. Prefer safer locations.
3. Prefer accessible locations.
4. Minimize unnecessary travel.
5. Avoid exceeding site capacity.

---

# FR-24 — Relocation Status

Display:

```text
TOTAL POPULATION
TOTAL CAPACITY
ASSIGNED POPULATION
UNASSIGNED POPULATION
```

Example:

```text
Population:       1240
Capacity:         1300
Assigned:         1240
Unassigned:       0

STATUS: FULLY ACCOMMODATED
```

If capacity is insufficient:

```text
⚠ CAPACITY SHORTAGE

Population: 1240
Available: 900
Unallocated: 340
```

---

# FR-25 — GIS Map Layers

The dashboard should support multiple layers.

Required:

```text
Risk Zones
Villages
Population
Roads
Historical Landslides
Hazard Zones
Safe Locations
Field Reports
Active Alerts
```

Users should be able to turn layers on/off.

---

# FR-26 — Map Interaction

Users should be able to:

* Zoom
* Pan
* Search locations
* Click villages
* Click risk zones
* Click incidents
* Click safe sites
* View detailed information
* Filter layers

---

# FR-27 — Main Authority Dashboard

Dashboard must display:

```text
Active Alerts
Critical Zones
High-Risk Zones
Villages Affected
Population at Risk
Blocked Roads
Pending Reports
Available Safe Sites
```

---

# FR-28 — Risk Analytics

Dashboard should provide:

* Risk distribution
* Rainfall trends
* Risk trends
* Number of active alerts
* Population exposure
* Incident statistics
* Road status statistics

Charts should support time-based visualization where data exists.

---

# FR-29 — Weather-linked Risk Forecast

The system should associate weather conditions with risk.

Example:

```text
Rainfall increasing
        ↓
Soil/terrain vulnerability
        ↓
Risk increases
        ↓
Warning level changes
```

Display:

```text
Current rainfall
24h rainfall
7-day accumulation
Risk forecast
```

For MVP, this may use historical or simulated forecast data if live APIs are unavailable.

---

# FR-30 — Multilingual Support

The system should support multiple languages.

Minimum MVP:

```text
English
Hindi
One NER-relevant language
```

The architecture must allow additional languages.

Translation should cover:

* Alerts
* Risk levels
* Safety instructions
* Incident forms
* Important notifications

---

# FR-31 — Offline / Low-Network Support

The field interface must continue functioning under poor connectivity.

Minimum MVP:

```text
Offline
 ↓
Create report
 ↓
Save locally
 ↓
Internet returns
 ↓
Synchronize
```

Offline data should include:

* Incident type
* Description
* GPS
* Timestamp
* Photo where feasible

---

# FR-32 — Sync Management

Each offline report should have:

```text
LOCAL
PENDING_SYNC
SYNCING
SYNCED
SYNC_FAILED
```

The UI should clearly indicate synchronization status.

---

# FR-33 — Notification System

The system should support application warnings.

Possible channels:

```text
Dashboard
PWA notification
Mobile notification
SMS
```

For MVP, implement at least:

**Dashboard + application notification**

SMS can be integrated/simulated depending on available services.

---

# FR-34 — Notification Targeting

Warnings should be targeted based on:

* Region
* District
* Village
* Risk zone
* User role

Example:

```text
Critical warning
       ↓
Affected district
       ↓
Authorities + field officials + affected users
```

---

# FR-35 — Search

Users should be able to search:

* Villages
* Districts
* Roads
* Safe sites
* Incident reports

---

# FR-36 — Filters

Dashboard filters:

```text
Risk level
District
Village
Incident type
Road status
Alert status
Date
```

---

# FR-37 — Audit / Activity Log

Important system actions should be recorded.

Examples:

```text
Alert created
Alert acknowledged
Report submitted
Report verified
Risk updated
Relocation plan generated
```

---

# 7. API Requirements

The backend should expose APIs similar to:

## Authentication

```text
POST /api/auth/register
POST /api/auth/login
POST /api/auth/logout
GET  /api/auth/me
```

## Regions

```text
GET /api/regions
GET /api/regions/:id
```

## Risk

```text
GET /api/risk/:regionId
GET /api/risk/:regionId/map
GET /api/risk/:regionId/history
```

## Alerts

```text
GET  /api/alerts
GET  /api/alerts/:id
POST /api/alerts
PATCH /api/alerts/:id/status
```

## Villages

```text
GET /api/villages
GET /api/villages/:id
GET /api/villages/:id/exposure
```

## Incidents

```text
POST /api/incidents
GET /api/incidents
GET /api/incidents/:id
PATCH /api/incidents/:id
POST /api/incidents/:id/verify
```

## Roads

```text
GET /api/roads
GET /api/roads/:id
PATCH /api/roads/:id/status
```

## Safe Locations

```text
GET /api/safe-locations/:regionId
GET /api/safe-locations/:regionId/recommended
```

## Relocation

```text
GET /api/relocation/:regionId
POST /api/relocation/:regionId/generate
```

## GIS

```text
GET /api/gis/risk/:regionId
GET /api/gis/villages/:regionId
GET /api/gis/roads/:regionId
GET /api/gis/incidents/:regionId
GET /api/gis/safe-sites/:regionId
```

---

# 8. Suggested Database Entities

## User

```text
id
name
email
passwordHash
role
phone
preferredLanguage
createdAt
updatedAt
```

## Region

```text
id
name
state
district
boundary
```

## Village

```text
id
name
regionId
population
location
geometry
```

## RiskPrediction

```text
id
regionId
geometry
riskScore
riskLevel
rainfall
slope
elevation
predictionTime
modelVersion
```

## Alert

```text
id
regionId
riskPredictionId
severity
message
geometry
status
createdAt
acknowledgedAt
resolvedAt
```

## Incident

```text
id
userId
type
description
location
severity
media
status
createdAt
verifiedAt
```

## Road

```text
id
name
geometry
status
severity
lastUpdated
```

## SafeLocation

```text
id
name
location
geometry
hazardScore
slope
roadDistance
facilityDistance
availableLand
capacity
suitabilityScore
```

## RelocationPlan

```text
id
regionId
populationAtRisk
totalCapacity
assignedPopulation
unassignedPopulation
status
createdAt
```

## RelocationAssignment

```text
id
planId
villageId
safeLocationId
populationAssigned
distance
```

---

# 9. Frontend Pages

## 9.1 Landing Page

Should explain:

* Problem
* Solution
* Live risk concept
* Benefits
* Emergency information

---

## 9.2 Login

Role-aware authentication.

---

## 9.3 Main Dashboard

Primary authority interface.

---

## 9.4 Risk Map

Full-screen GIS interface.

---

## 9.5 Village Details

Display:

* Population
* Risk
* Exposure
* Nearby incidents
* Roads
* Safe sites

---

## 9.6 Alert Center

Display:

* Active alerts
* Severity
* Region
* Time
* Status

---

## 9.7 Incident Reports

Display:

* Incoming reports
* Location
* Media
* Type
* Severity
* Verification status

---

## 9.8 Safe Locations

Display ranked locations.

---

## 9.9 Relocation Planner

Display:

* Population
* Capacity
* Assignments
* Unallocated population
* Recommended sites
* Map visualization

---

## 9.10 Analytics

Display:

* Risk trends
* Rainfall
* Population exposure
* Alerts
* Incidents
* Roads

---

## 9.11 Field Reporting Interface

Mobile-first.

Must support:

```text
Choose incident
 ↓
Capture media
 ↓
Get GPS
 ↓
Description
 ↓
Submit
```

---

# 10. Main End-to-End Workflow

## Scenario: Landslide Risk Increases

```text
Rainfall data received
        ↓
Data preprocessing
        ↓
ML model prediction
        ↓
Risk = 0.84
        ↓
CRITICAL
        ↓
Create alert
        ↓
Find affected risk zone
        ↓
Find affected villages
        ↓
Calculate population
        ↓
Check road connectivity
        ↓
Find safe locations
        ↓
Calculate capacity
        ↓
Generate relocation plan
        ↓
Notify users
        ↓
Display everything on GIS dashboard
```

---

# 11. Field Incident Workflow

```text
Field officer sees crack
        ↓
Open application
        ↓
Take photograph
        ↓
GPS captured
        ↓
Submit report
        ↓
No internet?
        ↓
Save locally
        ↓
Internet restored
        ↓
Automatic sync
        ↓
Authority receives report
        ↓
Authority verifies
        ↓
Incident appears on GIS map
        ↓
Risk/priority analysis updated
```

---

# 12. GIS Safe Location Algorithm

The MVP should use multi-criteria suitability analysis.

## Exclusion

```text
IF slope > threshold
    EXCLUDE

IF hazard exposure > threshold
    EXCLUDE

IF flood risk == HIGH
    EXCLUDE
```

## Scoring

Example:

```text
Suitability Score =

Safety             × 0.35
Road Accessibility × 0.20
Terrain             × 0.15
Facility Access     × 0.10
Distance            × 0.10
Land Availability  × 0.10
```

Weights should be configurable.

The exact values must be validated and clearly described as prototype assumptions.

---

# 13. ML Requirements

The ML system must not only produce predictions.

It should provide:

* Training pipeline
* Data preprocessing
* Feature engineering
* Model training
* Validation
* Evaluation metrics
* Prediction API
* Model versioning
* Prediction output

Required evaluation:

```text
Accuracy
Precision
Recall
F1 Score
ROC-AUC
Confusion Matrix
```

Because disaster prediction is safety-sensitive, **recall for landslide events should receive particular attention**, rather than optimizing only overall accuracy.

---

# 14. Data Requirements

The project should initially focus on **1–2 NER regions** rather than attempting nationwide coverage.

Potential pilot areas may include:

* Sikkim
* Arunachal Pradesh
* Meghalaya
* Nagaland
* Manipur
* Mizoram
* Tripura
* Assam hill regions

The exact pilot region should be selected based on data availability.

Required datasets:

```text
DEM
Rainfall
Historical landslides
Soil
Villages
Population
Roads
Hazard zones
Flood zones where available
Facilities
```

---

# 15. MVP Scope

The MVP MUST contain:

### AI

* Landslide risk prediction
* Risk score
* Risk classification

### GIS

* Interactive map
* Risk layer
* Village layer
* Road layer
* Incident layer
* Safe-location layer

### Exposure

* Affected villages
* Population at risk

### Relocation

* Safe-location ranking
* Capacity estimation
* Basic relocation plan

### Monitoring

* Rainfall
* Risk status
* Road status
* Incident reports

### Alerts

* Automatic risk-based warning
* Alert dashboard

### Field Reporting

* GPS
* Photo
* Incident type
* Description

### Offline

* Offline report storage
* Synchronization

### Web

* Authority dashboard
* Mobile-friendly field interface

---

# 16. Stretch Features

Only build these after the MVP is stable:

* Expo native field application
* SMS integration
* Push notifications
* Live satellite feed
* Advanced satellite image deep learning
* IoT soil-moisture integration
* Real-time sensor streaming
* Advanced evacuation routing
* Traffic-aware evacuation
* Multiple evacuation stages
* Advanced multilingual support
* Voice alerts
* AI-generated incident summaries
* Computer vision for crack detection
* Computer vision for landslide detection
* Predictive road blockage
* Nationwide coverage

---

# 17. Features NOT to Build Initially

Do NOT prioritize:

```text
Nationwide deployment
Custom deep-learning satellite model
Hardware sensors
Dedicated complex logistics optimizer
Government-scale infrastructure
Full emergency communication network
Complex mobile ecosystem
```

First make the complete MVP work for one pilot region.

---

# 18. Demo Scenario

The final SIH demonstration should follow a realistic scenario.

## Step 1

Show normal conditions.

```text
Risk: LOW
```

## Step 2

Increase rainfall in the simulation.

```text
Rainfall ↑
```

## Step 3

Run prediction.

```text
Risk Score: 0.84
Risk Level: CRITICAL
```

## Step 4

System automatically creates:

```text
CRITICAL ALERT
```

## Step 5

GIS identifies:

```text
4 affected villages
1,240 people at risk
```

## Step 6

System checks roads.

```text
Road A → BLOCKED
Road B → OPEN
Road C → PARTIALLY BLOCKED
```

## Step 7

Safe-location engine produces:

```text
Site A → 500 capacity → 91%
Site B → 450 capacity → 86%
Site C → 350 capacity → 81%
```

## Step 8

Relocation engine generates:

```text
Site A → 500
Site B → 450
Site C → 290
```

## Step 9

System displays:

```text
1240 / 1240 PEOPLE ACCOMMODATED
```

## Step 10

Field officer submits a geo-tagged landslide photo.

The report appears on the authority map.

This should be the **central story of the SIH demo**.

---

# 19. Non-Functional Requirements

## Performance

* Dashboard should load quickly.
* GIS layers should be loaded efficiently.
* APIs should use pagination where appropriate.
* Large GeoJSON should not unnecessarily be sent in a single response.
* Spatial queries should use PostGIS indexes.

---

## Reliability

The system should gracefully handle:

* API failure
* Missing weather data
* ML service unavailable
* Invalid GPS
* Upload failure
* Offline operation

---

## Security

Implement:

* Password hashing
* JWT authentication
* Role-based authorization
* Input validation
* File upload validation
* File size limits
* Rate limiting
* Secure environment variables
* CORS configuration
* API error handling

---

## Scalability

The architecture should allow:

```text
1 region
   ↓
Multiple districts
   ↓
Multiple states
   ↓
Entire NER
```

Do not optimize for nationwide scale during MVP development.

---

# 20. Observability

The system should log:

* API errors
* ML prediction failures
* Data ingestion failures
* Sync failures
* Alert generation
* Authentication failures

Recommended:

* Structured logging
* Request IDs
* Error logs

---

# 21. Testing Requirements

## Backend

Test:

* Authentication
* Authorization
* APIs
* Validation
* Error handling
* Incident reporting
* Relocation calculation

## ML

Test:

* Data preprocessing
* Model predictions
* Evaluation metrics
* Edge cases

## GIS

Test:

* Spatial intersection
* Risk zone generation
* Village exposure
* Distance calculation
* Safe-site filtering

## Frontend

Test:

* Dashboard
* Map
* Filters
* Alerts
* Forms
* Offline reporting

---

# 22. Deployment

Recommended architecture:

```text
React PWA
     ↓
Vercel / equivalent
     ↓
Node.js API
     ↓
Cloud server
     ↓
PostgreSQL + PostGIS

Python ML/GIS service
     ↓
Cloud server/container
```

Use Docker for services where practical.

---

# 23. Development Priorities

## Priority 1 — Core Intelligence

```text
Data
 ↓
Risk Model
 ↓
Risk Map
```

## Priority 2 — Exposure

```text
Risk
 ↓
Villages
 ↓
Population
```

## Priority 3 — Relocation

```text
Safe Sites
 ↓
Capacity
 ↓
Relocation
```

## Priority 4 — Application

```text
Backend
 ↓
Dashboard
 ↓
GIS
```

## Priority 5 — Field Operations

```text
Reports
 ↓
GPS
 ↓
Media
 ↓
Offline
```

## Priority 6 — Advanced Features

```text
SMS
Satellite
Sensors
Advanced AI
Native Mobile App
```

---

# 24. Definition of Done

The MVP is considered complete when a judge can perform this workflow:

```text
1. Open application
        ↓
2. Select pilot region
        ↓
3. View live/simulated environmental conditions
        ↓
4. View predicted landslide risk
        ↓
5. View risk zones on map
        ↓
6. View affected villages
        ↓
7. View population at risk
        ↓
8. View blocked roads
        ↓
9. View active warning
        ↓
10. View recommended safe locations
        ↓
11. View capacity
        ↓
12. Generate relocation plan
        ↓
13. Submit field incident
        ↓
14. See incident on map
        ↓
15. Demonstrate offline submission
        ↓
16. Synchronize when connection returns
```

If this entire workflow works, the team has a **complete SIH26001 MVP**.

---

# 25. Team Responsibilities

## AI/ML Engineer

Own:

* Dataset preparation
* Feature engineering
* Model training
* Model evaluation
* Risk prediction
* Model serving

---

## GIS Engineer

Own:

* DEM processing
* Raster processing
* Spatial analysis
* Risk polygons
* Safe-location analysis
* Spatial datasets

---

## YOU — Backend + Full-Stack Engineer

Own:

* Backend architecture
* REST APIs
* Authentication
* Database integration
* PostGIS integration
* ML/GIS service integration
* Alert system
* Incident reporting
* Road status APIs
* Relocation APIs
* React dashboard
* GIS map integration
* PWA
* Offline reporting
* Frontend/backend integration

---

# 26. Your Backend Architecture

Recommended:

```text
backend/
├── src/
│   ├── config/
│   ├── controllers/
│   ├── routes/
│   ├── models/
│   ├── services/
│   ├── middlewares/
│   ├── validators/
│   ├── utils/
│   ├── integrations/
│   │   ├── ml/
│   │   ├── weather/
│   │   └── gis/
│   └── app.js
│
├── tests/
├── .env
├── .env.example
├── package.json
└── Dockerfile
```

---

# 27. Your Frontend Architecture

```text
frontend/
├── src/
│   ├── components/
│   ├── pages/
│   ├── layouts/
│   ├── features/
│   │   ├── dashboard/
│   │   ├── map/
│   │   ├── alerts/
│   │   ├── incidents/
│   │   ├── villages/
│   │   ├── roads/
│   │   ├── safeLocations/
│   │   └── relocation/
│   ├── services/
│   ├── hooks/
│   ├── store/
│   ├── utils/
│   └── types/
│
├── public/
├── package.json
└── vite.config.ts
```

---

# 28. Core Product Principle

The application should never stop at:

> "There is a landslide risk."

It must answer:

> **Where?**

> **How dangerous?**

> **Who is affected?**

> **How many people are at risk?**

> **Which roads are affected?**

> **Where can they go?**

> **How many people can each location accommodate?**

> **How should people be distributed?**

> **What should authorities do next?**

This is the central product philosophy of SIH26001.

---

# 29. Final Product

The final platform should combine:

```text
AI
+
GIS
+
Real-time/near-real-time monitoring
+
Crowdsourced field intelligence
+
Risk alerts
+
Population exposure
+
Road monitoring
+
Safe-location intelligence
+
Carrying capacity
+
Relocation planning
+
Offline field operations
```

into one integrated disaster-management platform.

### Product tagline

**Predict → Warn → Decide → Relocate**

### Core value proposition

> **From predicting landslides to making actionable disaster-response decisions.**
