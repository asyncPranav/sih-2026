import React, { useEffect } from 'react';
import { MapContainer, TileLayer, CircleMarker, Circle, Popup, useMap } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';
import {
  villages, riskZones, safeLocations, incidents,
  riskColor, riskBg, type RiskLevel,
} from '../mock/data';

interface LayerState {
  riskZones: boolean;
  villages: boolean;
  roads: boolean;
  safeLocations: boolean;
  incidents: boolean;
}

interface Props {
  layers: LayerState;
  center?: [number, number];
  zoom?: number;
}

// Converts km to approx meters for Leaflet
const kmToM = (km: number) => km * 1000;

const riskOpacity: Record<RiskLevel, number> = {
  CRITICAL: 0.22, HIGH: 0.16, MEDIUM: 0.12, LOW: 0.08,
};

export default function LeafletMap({ layers, center = [27.2800, 88.6400], zoom = 10 }: Props) {
  return (
    <MapContainer
      center={center}
      zoom={zoom}
      style={{ width: '100%', height: '100%' }}
      zoomControl={false}
      attributionControl={false}
    >
      {/* Dark base tiles */}
      <TileLayer
        url="https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png"
        attribution='&copy; <a href="https://carto.com/">CARTO</a>'
        maxZoom={18}
      />

      {/* Risk Zones */}
      {layers.riskZones && riskZones.map(zone => (
        <React.Fragment key={zone.id}>
          <Circle
            center={[zone.lat, zone.lng]}
            radius={kmToM(zone.radiusKm)}
            pathOptions={{
              color: riskColor(zone.riskLevel),
              fillColor: riskColor(zone.riskLevel),
              fillOpacity: riskOpacity[zone.riskLevel],
              weight: 1.5,
              dashArray: zone.riskLevel === 'CRITICAL' ? undefined : '4 4',
            }}
          >
            <Popup>
              <div style={{ fontFamily: 'Outfit, sans-serif', minWidth: 200 }}>
                <div style={{ fontWeight: 700, color: riskColor(zone.riskLevel), fontSize: 12, textTransform: 'uppercase', letterSpacing: '0.05em' }}>
                  {zone.riskLevel} RISK ZONE
                </div>
                <div style={{ marginTop: 8, fontSize: 13, color: '#e2e8f0' }}>
                  <div>Risk Score: <b>{zone.riskScore}</b></div>
                  <div>Rainfall 7d: <b>{zone.rainfall7d} mm</b></div>
                  <div>Slope: <b>{zone.slope}°</b></div>
                  <div>Elevation: <b>{zone.elevation} m</b></div>
                </div>
                <div style={{ marginTop: 6, fontSize: 10, color: '#7a9088', fontStyle: 'italic' }}>
                  ⚠ DEMO/SIMULATION DATA
                </div>
              </div>
            </Popup>
          </Circle>
        </React.Fragment>
      ))}

      {/* Villages */}
      {layers.villages && villages.map(v => (
        <CircleMarker
          key={v.id}
          center={[v.lat, v.lng]}
          radius={v.riskLevel === 'CRITICAL' ? 8 : v.riskLevel === 'HIGH' ? 6 : 5}
          pathOptions={{
            color: riskColor(v.riskLevel),
            fillColor: riskColor(v.riskLevel),
            fillOpacity: 0.85,
            weight: 2,
          }}
        >
          <Popup>
            <div style={{ fontFamily: 'Outfit, sans-serif', minWidth: 190 }}>
              <div style={{ fontWeight: 700, fontSize: 14, color: '#f0f5f2' }}>{v.name}</div>
              <div style={{ fontSize: 10, color: '#7a9088', marginBottom: 8 }}>{v.district}</div>
              <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 4, fontSize: 12 }}>
                <div style={{ color: '#7a9088' }}>Population</div><div style={{ color: '#f0f5f2', fontWeight: 600 }}>{v.population.toLocaleString()}</div>
                <div style={{ color: '#7a9088' }}>Risk Level</div>
                <div style={{ color: riskColor(v.riskLevel), fontWeight: 700 }}>{v.riskLevel}</div>
                <div style={{ color: '#7a9088' }}>Risk Score</div><div style={{ color: '#f0f5f2', fontWeight: 600 }}>{v.riskScore}</div>
                <div style={{ color: '#7a9088' }}>Road</div><div style={{ color: '#f0f5f2' }}>{v.nearestRoad}</div>
              </div>
            </div>
          </Popup>
        </CircleMarker>
      ))}

      {/* Safe Locations */}
      {layers.safeLocations && safeLocations.map(sl => (
        <CircleMarker
          key={sl.id}
          center={[sl.lat, sl.lng]}
          radius={7}
          pathOptions={{
            color: '#00c896',
            fillColor: '#00c896',
            fillOpacity: 0.9,
            weight: 2.5,
          }}
        >
          <Popup>
            <div style={{ fontFamily: 'Outfit, sans-serif', minWidth: 190 }}>
              <div style={{ fontWeight: 700, fontSize: 13, color: '#00c896' }}>✓ SAFE SITE</div>
              <div style={{ fontWeight: 600, fontSize: 14, color: '#f0f5f2', marginTop: 4 }}>{sl.name}</div>
              <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 4, fontSize: 12, marginTop: 8 }}>
                <div style={{ color: '#7a9088' }}>Capacity</div><div style={{ color: '#f0f5f2', fontWeight: 600 }}>{sl.capacity.toLocaleString()}</div>
                <div style={{ color: '#7a9088' }}>Suitability</div><div style={{ color: '#00c896', fontWeight: 700 }}>{(sl.suitabilityScore * 100).toFixed(0)}%</div>
                <div style={{ color: '#7a9088' }}>Road Access</div><div style={{ color: '#f0f5f2' }}>{sl.roadAccess}</div>
                <div style={{ color: '#7a9088' }}>Distance</div><div style={{ color: '#f0f5f2' }}>{sl.distanceKm} km</div>
              </div>
            </div>
          </Popup>
        </CircleMarker>
      ))}

      {/* Incidents */}
      {layers.incidents && incidents.filter(i => i.status === 'VERIFIED').map(inc => (
        <CircleMarker
          key={inc.id}
          center={[inc.lat, inc.lng]}
          radius={6}
          pathOptions={{
            color: '#f59e0b',
            fillColor: '#f59e0b',
            fillOpacity: 0.9,
            weight: 2,
          }}
        >
          <Popup>
            <div style={{ fontFamily: 'Outfit, sans-serif', minWidth: 200 }}>
              <div style={{ fontWeight: 700, fontSize: 12, color: '#f59e0b', textTransform: 'uppercase' }}>{inc.type.replace('_', ' ')}</div>
              <div style={{ fontSize: 12, color: '#f0f5f2', marginTop: 6 }}>{inc.description}</div>
              <div style={{ fontSize: 11, color: '#7a9088', marginTop: 4 }}>Reported: {inc.reportedBy}</div>
            </div>
          </Popup>
        </CircleMarker>
      ))}
    </MapContainer>
  );
}
