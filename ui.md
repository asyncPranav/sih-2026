I searched current, real-world disaster/GIS systems, with extra weight on **India-specific government systems**, **landslide/hazard mapping**, and **emergency command-center dashboards**. For SIH26001, these are the 12 references I would actually study.
### 0. ArcGIS dashboards 
— probably the most relevant inspiration. Look at how they combine a large map with statistics, filters, alerts, and operational information.


### 1. India — ISRO/NRSC National Database for Emergency Management (NDEM)

**Best overall reference for SIH26001**

NDEM is particularly relevant because it combines GIS layers, disaster dashboards, warnings, satellite-derived products, incident information and decision-support functions for disaster managers. Its current public portal includes landslide products, weather forecasts/warnings and disaster dashboards. ([NDEM][1])

**Borrow:**

* Government/command-center information hierarchy
* Disaster categories and service navigation
* Map + warning + event-card structure
* Separate operational tools from informational content
* State/district-oriented navigation

[Open NDEM](https://ndem.nrsc.gov.in/?utm_source=chatgpt.com)

---

### 2. India — NDEM Landslide Early Warning & Hazard Maps

This is one of the **closest conceptual references** to your project. The NDEM interface has separate views for **Landslide Early Warning**, **Landslide Hazard**, rainfall forecast and landslide forecast, with region/route and date selection. ([NDEM][2])

**Borrow heavily:**

* Hazard vs forecast distinction
* Region/route filters
* Forecast date controls
* Side-by-side environmental inputs and hazard output
* Landslide-specific terminology

For your UI, this could become:

`Rainfall + Terrain + Historical Slides → AI Risk → Risk Forecast`

[Open NDEM landslide section](https://ndem.nrsc.gov.in/?utm_source=chatgpt.com)

---

### 3. India — Himachal Pradesh Disaster Management System / आपदा रक्षक

**Probably the best visual/conceptual reference for your dashboard.**

The current Himachal system presents **Dashboard Overview, Hazard Monitoring, Analytics & Reports, GIS Map View, Weather & Alerts, Incident History and Decision Support**, while also surfacing incident counts such as landslides, flash floods and road blockages. ([hpsdma.hp.gov.in][3])

**Borrow:**

* Top-level operational modules
* Incident counters
* "Monitor → Analyze → Respond → Decide" workflow
* GIS + weather + incidents in one product
* Dedicated decision-support area

This is extremely close to the product you're designing.

[Open Himachal Disaster Management System](https://hpsdma.hp.gov.in/Home_Disaster.aspx?utm_source=chatgpt.com)

---

### 4. India — IMD Current Weather Monitoring Dashboard

The IMD dashboard combines **rainfall, satellite, radar, lightning, present weather and district warnings** in one monitoring interface. ([dss.imd.gov.in][4])

**Borrow:**

* Environmental monitoring panels
* Time-based forecast selection
* Weather layers as supporting evidence rather than decoration
* Compact monitoring widgets
* Clear separation between current conditions and warnings

For SIH26001, your Risk Intelligence screen should work similarly:

**Rainfall → slope → soil → forecast → predicted landslide risk**

[Open IMD Current Weather Dashboard](https://dss.imd.gov.in/dwr_img/GIS/currentwx/currentwx.html?utm_source=chatgpt.com)

---

### 5. India — IMD Rainfall Monitoring Map

IMD's rainfall interface provides district-level map interaction and lets users switch between **daily, weekly, monthly and cumulative rainfall** views. ([Mausam][5])

**Borrow:**

* Time-period switcher
* District-level drill-down
* Map-driven analytics
* Rainfall legend
* Historical vs current comparison

This maps directly to your **7-day rainfall → landslide risk** concept.

[Open IMD Rainfall Information](https://mausam.imd.gov.in/responsive/rainfallinformation_swd.php?utm_source=chatgpt.com)

---

### 6. USA — USGS Landslide Inventory & Susceptibility Map

**Best reference for your actual landslide GIS screen.**

The USGS combines historical landslide inventory and susceptibility into a searchable interactive map. Its current product visualizes susceptibility from lower to higher risk and lets users inspect individual landslide information. ([USGS][6])

**Borrow:**

* Minimal map-first interface
* Strong hazard legend
* Searchable geography
* Historical landslides as map objects
* Click → inspect underlying evidence
* Don't clutter the map with huge UI cards

[Open USGS Landslide Inventory & Susceptibility Map](https://www.usgs.gov/tools/us-landslide-inventory-and-susceptibility-map?utm_source=chatgpt.com)

---

### 7. USA — USGS Post-Fire Debris-Flow Hazard Assessment Dashboard

This is another excellent **hazard-analysis UI reference**. Users can pan/zoom, filter assessments by **year, state and fire event**, and click an assessment to inspect its summary/data links. ([USGS][7])

**Borrow:**

* Filterable geospatial hazard data
* Map-first investigation
* Clickable hazard regions
* Contextual information panel
* Data provenance/access from map objects

Your equivalent could be:

`State → District → Risk level → Date → Rainfall window → Prediction`

[Open USGS Post-Fire Debris-Flow Dashboard](https://www.usgs.gov/programs/landslide-hazards/science/postfire-debris-flow-hazard-maps?utm_source=chatgpt.com)

---

### 8. USA — FEMA Hurricane Helene Geospatial Damage Assessment Dashboard

**Best reference for "map + KPI cards + severity".**

The FEMA dashboard uses large summary counters for different damage categories while displaying mapped incident/damage points.

![Image](https://www.arcgis.com/sharing/rest/content/items/ff4eb86beb974387b3e26f9bb020d7f0/resources/20241009_0906_USGSlandslide_sm.png?v=1739812937734)

![Image](https://images.openai.com/static-rsc-4/WI6DYdge7k-9PCWR-WdPeELVR3K5cWPAMQeRUur-AMVGe5_Gs4z4C_i206OKXM4x6kdWLp9eLGVLsxWEUiTnaThdjeBq-T-o5lMs2iNNyoqEjR5lr9e_yL3Iecg0lcNFjzny1YZyOOhSq_6TrL_5-ARWVNwJNofOrQtzj8bafsaiM1jhrz9-cvrgm-Jz4b0h?purpose=fullsize)

**Borrow directly:**

* Large KPI numbers
* Severity categories
* Map as primary evidence
* Filters above/around the map
* Selected region → detailed assessment

For SIH26001:

`Critical Zones | People at Risk | Villages | Blocked Roads | Active Alerts`

---

### 9. USA — Raleigh Emergency Operations Dashboard

Raleigh's EOC dashboard was designed specifically to put real-time emergency information in one place so the command team doesn't need to switch between multiple information sources. ([Esri][8])

**Borrow:**

* **Command-center mentality**
* Map dominating the interface
* Operational counters
* Road closure/incident visibility
* High information density without unnecessary decoration

This is much closer to your intended UI than a normal SaaS dashboard.

---

### 10. USA — Esri Incident Awareness & Assessment Dashboard

The National Guard example combines a map with incident/event tables and operational counts such as **areas of interest, facilities and civilian infrastructure**.

**Borrow:**

* Map + operational entity counts
* Incident table below/alongside map
* Infrastructure visibility
* Event-oriented rather than generic analytics

For your project:

`Risk Zone → Villages → Roads → Facilities → Safe Sites`

[Open Esri Incident Awareness example](https://www.esri.com/arcgis-blog/products/arcgis-solutions/defense/streamline-national-guard-disaster-response-with-the-incident-awareness-and-assessment-solution?utm_source=chatgpt.com)

---

### 11. Europe — Copernicus Emergency Management Service

**Best reference for professional disaster geospatial visualization.**

Copernicus EMS provides mapping for natural hazards and humanitarian emergencies and supports preparedness, emergency response and recovery. Its activation viewers allow interactive geodata visualization, including 2D/3D views, with accompanying situational reports and dashboards. ([Copernicus EMS][9])

**Borrow:**

* High-quality satellite/terrain visualization
* Hazard polygons
* 2D/3D thinking
* Situational-report integration
* Separate map analysis from narrative explanation

[Open Copernicus EMS](https://mapping.emergency.copernicus.eu/?utm_source=chatgpt.com)

---

### 12. Global — GDACS (Global Disaster Alert and Coordination System)

GDACS provides a global multi-hazard disaster map and event system used for disaster awareness and coordination. The current interface shows recent events and allows users to inspect disaster information spatially. ([GDACS][10])

**Borrow:**

* Global/region overview
* Disaster markers
* Severity/event categorization
* Map + event list
* Fast scanning of active hazards

[Open GDACS](https://gdacs.org/?utm_source=chatgpt.com)

---

## The 5 I would study most closely

For **SIH26001 specifically**, I would rank them:

| Rank  | Reference                               | What you should steal conceptually       |
| ----- | --------------------------------------- | ---------------------------------------- |
| **1** | **Himachal Disaster Management System** | Overall product structure                |
| **2** | **ISRO NDEM**                           | India-specific disaster/GIS architecture |
| **3** | **USGS Landslide Map**                  | Actual landslide risk-map UX             |
| **4** | **FEMA Damage Dashboard**               | KPIs + severity + map                    |
| **5** | **IMD Monitoring Dashboard**            | Rainfall/weather evidence                |
| 6     | Copernicus EMS                          | Professional geospatial visualization    |
| 7     | Raleigh EOC                             | Command-center dashboard philosophy      |
| 8     | USGS Debris-Flow Dashboard              | Hazard filtering/drill-down              |
| 9     | Esri Incident Awareness                 | Infrastructure + incidents               |
| 10    | GDACS                                   | Multi-hazard event overview              |
| 11    | IMD Rainfall                            | Time-based rainfall analysis             |
| 12    | NDEM Landslide Early Warning            | Landslide forecast workflow              |

### What this means for your SIH26001 UI

I would **not copy one dashboard**.

The strongest design would combine:

**NDEM/Himachal**
→ information architecture

**USGS**
→ landslide map

**IMD**
→ rainfall/weather evidence

**FEMA**
→ severity + KPI cards

**Raleigh/Esri**
→ emergency command-center workflow

**Copernicus**
→ professional GIS visualization

That gives you something like:

```text
┌─────────────────────────────────────────────────────────────────────┐
│ SIH26001 • NER LANDSLIDE RISK COMMAND CENTER       ● LIVE  20:42   │
├────────────┬───────────────────────────────────────┬───────────────┤
│ Overview   │                                       │ ACTIVE ALERT  │
│ Risk Map   │                                       │ CRITICAL      │
│ Alerts     │             GIS RISK MAP              │ East Sikkim   │
│ Incidents  │                                       │ 78 villages   │
│ Villages   │    🔴 Critical                       │ 12,480 people │
│ Roads      │    🟠 High                           │               │
│ Relocation │    🟡 Medium                         │ [VIEW ALERT]  │
│ Analytics  │                                       ├───────────────┤
│            │                                       │ RAINFALL      │
│            │                                       │ 142 mm / 7d   │
│            │                                       │ +38% forecast │
├────────────┴───────────────────────────────────────┴───────────────┤
│ CRITICAL ZONES │ PEOPLE AT RISK │ VILLAGES │ BLOCKED ROADS │ SITES │
└─────────────────────────────────────────────────────────────────────┘
```

And the **most important design decision**: don't make it look like a generic "AI dashboard." The real-world references consistently point toward a **map-first emergency decision system** where the UI answers:

> **Where is the hazard? How severe is it? Who is affected? What is changing? What should the authority do next?**

That is the visual direction I'd use for your SIH26001 build. ([Esri][11])

[1]: https://ndem.nrsc.gov.in/main.php?action=login&pid=0&utm_source=chatgpt.com "National Database for Emergency Management"
[2]: https://ndem.nrsc.gov.in/login.php/meteorologicaldisasters/tpl/sitemap.php?utm_source=chatgpt.com "National Database for Emergency Management"
[3]: https://hpsdma.hp.gov.in/Home_Disaster.aspx?utm_source=chatgpt.com "HPSDMA"
[4]: https://dss.imd.gov.in/dwr_img/GIS/currentwx/currentwx.html?utm_source=chatgpt.com "Current Weather Dashboard"
[5]: https://mausam.imd.gov.in/responsive/rainfallinformation_swd.php?utm_source=chatgpt.com "Rainfall Information | India Meteorological Department"
[6]: https://www.usgs.gov/tools/us-landslide-inventory-and-susceptibility-map?utm_source=chatgpt.com "U.S. Landslide Inventory and Susceptibility Map | U.S. Geological Survey"
[7]: https://www.usgs.gov/programs/landslide-hazards/science/postfire-debris-flow-hazard-maps?utm_source=chatgpt.com "Postfire debris-flow hazard maps | U.S. Geological Survey"
[8]: https://www.esri.com/en-us/landing-page/product/2020/raleigh-nc-case-study?utm_source=chatgpt.com "Raleigh Enhances Situational Awareness for Emergency Response"
[9]: https://mapping.emergency.copernicus.eu/?framed=true&utm_source=chatgpt.com "Home | Copernicus EMS On Demand Mapping"
[10]: https://gdacs.org/?utm_source=chatgpt.com "GDACS - Global Disaster Awareness and Coordination System"
[11]: https://www.esri.com/en-us/industries/emergency-management/solutions/situational-awareness?utm_source=chatgpt.com "Emergency Management Response | Situational Awareness Dashboard Using GIS"
