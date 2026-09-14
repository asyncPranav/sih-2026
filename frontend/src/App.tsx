import React, { useState, Suspense, lazy } from 'react';
import {
  Activity, Map as MapIcon, Bell, AlertTriangle,
  Users, Navigation, CloudRain, ShieldAlert,
  Settings, Search, Radio, Layers, TrendingUp,
} from 'lucide-react';
import { useApi } from './hooks/useApi';
import { ApiService, type Alert } from './api/services';
import RightPanel from './components/RightPanel';

const AlertCenter = lazy(() => import('./pages/AlertCenter'));
const Incidents   = lazy(() => import('./pages/Incidents'));
const Exposure    = lazy(() => import('./pages/Exposure'));
const Relocation  = lazy(() => import('./pages/Relocation'));
const Analytics   = lazy(() => import('./pages/Analytics'));
const Weather     = lazy(() => import('./pages/Weather'));
const LeafletMap  = lazy(() => import('./components/LeafletMap'));

type Page = 'overview' | 'riskmap' | 'alerts' | 'incidents' | 'exposure' | 'relocation' | 'analytics' | 'weather';

const defaultLayers = { riskZones: true, villages: true, roads: false, safeLocations: true, incidents: true };

/* ── KPI Card ─────────────────────────────────── */
function KPICard({
  label, value, sub, danger = false, accent = false, loading = false,
}: {
  label: string; value: string | number; sub?: string;
  danger?: boolean; accent?: boolean; loading?: boolean;
}) {
  const color = loading ? 'var(--color-text-faint)'
    : danger ? 'var(--color-danger)'
    : accent ? 'var(--color-primary)'
    : 'var(--color-text)';

  return (
    <div className="kpi-card">
      <span className="kpi-label">{label}</span>
      <span className="kpi-value" style={{ color }}>
        {loading ? '—' : value}
      </span>
      {sub && <span className="kpi-sub">{sub}</span>}
    </div>
  );
}

/* ── Sidebar ──────────────────────────────────── */
function Sidebar({
  page, setPage, activeAlertCount,
}: { page: Page; setPage: (p: Page) => void; activeAlertCount: number }) {
  const NAV: { id: Page; label: string; icon: React.ReactNode; badge?: number }[] = [
    { id: 'overview',   label: 'Overview',   icon: <Activity size={14} /> },
    { id: 'riskmap',    label: 'Risk Map',   icon: <MapIcon size={14} /> },
    { id: 'alerts',     label: 'Alerts',     icon: <Bell size={14} />,         badge: activeAlertCount || undefined },
    { id: 'incidents',  label: 'Incidents',  icon: <AlertTriangle size={14}/>, badge: 3 },
    { id: 'exposure',   label: 'Exposure',   icon: <Users size={14} /> },
    { id: 'relocation', label: 'Relocation', icon: <Navigation size={14} /> },
    { id: 'analytics',  label: 'Analytics',  icon: <TrendingUp size={14} /> },
  ];

  return (
    <aside style={{
      width: 220, flexShrink: 0,
      background: 'var(--color-surface)',
      borderRight: '1px solid var(--color-border)',
      display: 'flex', flexDirection: 'column', height: '100%',
    }}>
      {/* Brand */}
      <div style={{ padding: '18px 16px 16px', borderBottom: '1px solid var(--color-border)', display: 'flex', alignItems: 'center', gap: 10 }}>
        <div style={{
          width: 30, height: 30, borderRadius: 8,
          background: 'var(--color-primary-dim)',
          border: '1px solid var(--color-primary-border)',
          display: 'flex', alignItems: 'center', justifyContent: 'center',
        }}>
          <Activity size={15} style={{ color: 'var(--color-primary)' }} />
        </div>
        <div>
          <div style={{ fontSize: '0.82rem', fontWeight: 700, color: 'var(--color-text)', lineHeight: 1.2 }}>SIH 26001</div>
          <div style={{ fontSize: '0.6rem', fontWeight: 600, letterSpacing: '0.1em', textTransform: 'uppercase', color: 'var(--color-text-muted)', marginTop: 1 }}>
            Command Center
          </div>
        </div>
      </div>

      {/* Alert Banner */}
      {activeAlertCount > 0 && (
        <button onClick={() => setPage('alerts')} style={{
          margin: '12px 10px 0', padding: '10px 12px', borderRadius: 8,
          background: 'var(--color-danger-dim)', border: '1px solid var(--color-danger-border)',
          cursor: 'pointer', textAlign: 'left',
        }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: 6, marginBottom: 4 }}>
            <div className="status-dot" style={{ background: 'var(--color-danger)', boxShadow: '0 0 6px var(--color-danger)' }} />
            <span style={{ fontSize: '0.65rem', fontWeight: 700, letterSpacing: '0.08em', textTransform: 'uppercase', color: 'var(--color-danger)' }}>
              {activeAlertCount} Active Alert{activeAlertCount > 1 ? 's' : ''}
            </span>
          </div>
          <div style={{ fontSize: '0.78rem', fontWeight: 600, color: 'var(--color-text)' }}>East Sikkim Corridor</div>
          <div style={{ fontSize: '0.7rem', color: 'var(--color-text-2)', marginTop: 2 }}>Risk 0.89 · 3,030 at risk</div>
        </button>
      )}

      {/* Nav */}
      <nav style={{ flex: 1, padding: '12px 10px', overflowY: 'auto', display: 'flex', flexDirection: 'column', gap: 1 }}>
        <div className="section-label" style={{ marginTop: 4, marginBottom: 8 }}>Operations</div>
        {NAV.map(item => (
          <button key={item.id} className={`nav-item ${page === item.id ? 'active' : ''}`} onClick={() => setPage(item.id)}>
            <span className="nav-item-inner">{item.icon}{item.label}</span>
            {item.badge ? (
              <span style={{ fontSize: '0.6rem', fontWeight: 700, padding: '2px 6px', borderRadius: 4, background: 'var(--color-danger)', color: 'white' }}>
                {item.badge}
              </span>
            ) : null}
          </button>
        ))}

        <div className="divider" style={{ margin: '10px 0' }} />
        <div className="section-label" style={{ marginBottom: 8 }}>System</div>
        {[
          { id: 'weather' as Page, icon: <CloudRain size={14} />, label: 'Weather' },
          { id: null, icon: <ShieldAlert size={14} />, label: 'Audit Logs' },
          { id: null, icon: <Settings size={14} />, label: 'Settings' },
        ].map(item => (
          <button key={item.label}
            className={`nav-item ${page === item.id ? 'active' : ''}`}
            onClick={() => item.id && setPage(item.id)}>
            <span className="nav-item-inner">{item.icon}{item.label}</span>
          </button>
        ))}
      </nav>

      {/* User */}
      <div style={{ padding: '12px 16px', borderTop: '1px solid var(--color-border)', display: 'flex', alignItems: 'center', gap: 10 }}>
        <div style={{
          width: 28, height: 28, borderRadius: 7,
          background: 'linear-gradient(135deg, var(--color-primary) 0%, var(--color-accent) 100%)',
          display: 'flex', alignItems: 'center', justifyContent: 'center',
          fontSize: '0.65rem', fontWeight: 700, color: '#0c0e0d', flexShrink: 0,
        }}>JD</div>
        <div>
          <div style={{ fontSize: '0.78rem', fontWeight: 600, color: 'var(--color-text)' }}>John Doe</div>
          <div style={{ fontSize: '0.65rem', color: 'var(--color-text-muted)' }}>District Officer</div>
        </div>
      </div>
    </aside>
  );
}

/* ── Top Bar ──────────────────────────────────── */
function TopBar({ page, backendOnline }: { page: Page; backendOnline: boolean }) {
  const labels: Record<Page, string> = {
    overview: 'Overview', riskmap: 'Risk Map', alerts: 'Alerts',
    incidents: 'Incidents', exposure: 'Exposure', relocation: 'Relocation',
    analytics: 'Analytics', weather: 'Weather',
  };
  return (
    <div style={{
      height: 52, flexShrink: 0,
      borderBottom: '1px solid var(--color-border)',
      background: 'var(--color-surface)',
      display: 'flex', alignItems: 'center', justifyContent: 'space-between',
      padding: '0 20px',
    }}>
      <div style={{ display: 'flex', alignItems: 'center', gap: 16 }}>
        <span style={{ fontSize: '0.9rem', fontWeight: 700, color: 'var(--color-text)' }}>{labels[page]}</span>
        <span style={{ width: 1, height: 16, background: 'var(--color-border)', display: 'block' }} />
        <span style={{ display: 'flex', alignItems: 'center', gap: 5, fontSize: '0.75rem', color: 'var(--color-text-muted)' }}>
          <CloudRain size={12} style={{ color: 'var(--color-primary-light)' }} />
          142 mm / 7d
          <span className="badge badge-danger" style={{ marginLeft: 4 }}>+38%</span>
        </span>
        {/* Backend status */}
        <span style={{ display: 'flex', alignItems: 'center', gap: 5 }}>
          <div className="status-dot" style={{
            background: backendOnline ? 'var(--color-success)' : 'var(--color-danger)',
            boxShadow: `0 0 5px ${backendOnline ? 'var(--color-success)' : 'var(--color-danger)'}`,
          }} />
          <span style={{ fontSize: '0.7rem', fontWeight: 600, color: backendOnline ? 'var(--color-success)' : 'var(--color-danger)' }}>
            {backendOnline ? 'API LIVE' : 'API OFFLINE'}
          </span>
        </span>
      </div>
      <div style={{ display: 'flex', alignItems: 'center', gap: 10 }}>
        <div style={{ position: 'relative' }}>
          <Search size={13} style={{ position: 'absolute', left: 10, top: '50%', transform: 'translateY(-50%)', color: 'var(--color-text-faint)' }} />
          <input className="input" style={{ paddingLeft: 30, width: 240 }} placeholder="Search villages, roads…" />
        </div>
        <span className="badge badge-warning">DEMO</span>
      </div>
    </div>
  );
}

/* ── Map with layer controls ─────────────── */
function RiskMapPage() {
  const [layers, setLayers] = useState(defaultLayers);
  const toggle = (k: keyof typeof layers) => setLayers(p => ({ ...p, [k]: !p[k] }));
  return (
    <div style={{ flex: 1, display: 'flex', flexDirection: 'column', overflow: 'hidden' }}>
      <div style={{ display: 'flex', alignItems: 'center', gap: 10, padding: '8px 16px', borderBottom: '1px solid var(--color-border)', background: 'var(--color-surface)' }}>
        <Layers size={13} style={{ color: 'var(--color-text-muted)' }} />
        <span style={{ fontSize: '0.65rem', fontWeight: 700, letterSpacing: '0.08em', textTransform: 'uppercase', color: 'var(--color-text-muted)' }}>Layers</span>
        {(Object.keys(layers) as (keyof typeof layers)[]).map(k => (
          <button key={k} className={`btn ${layers[k] ? 'btn-primary' : 'btn-ghost'}`}
            style={{ padding: '0.25rem 0.75rem', fontSize: '0.7rem' }}
            onClick={() => toggle(k)}>
            {k.replace(/([A-Z])/g, ' $1').trim()}
          </button>
        ))}
      </div>
      <div style={{ flex: 1, overflow: 'hidden' }}>
        <Suspense fallback={<MapLoader />}><LeafletMap layers={layers} /></Suspense>
      </div>
    </div>
  );
}

/* ── Overview (wired to real dashboard API) ── */
function Overview({ setPage }: { setPage: (p: Page) => void }) {
  const { data: summary, loading } = useApi(ApiService.getDashboard);
  const [layers] = useState(defaultLayers);

  return (
    <div style={{ flex: 1, display: 'flex', flexDirection: 'column', overflow: 'hidden' }}>
      {/* KPIs */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: 12, padding: '14px 16px', flexShrink: 0 }}>
        <KPICard label="Critical Zones"     value={summary?.critical_zones ?? 0}                             sub="Active risk zones"                                        danger  loading={loading} />
        <KPICard label="Population at Risk" value={summary ? summary.population_at_risk.toLocaleString() : 0} sub={`${summary?.affected_villages ?? 0} villages affected`}  danger  loading={loading} />
        <KPICard label="Blocked Roads"      value={summary?.blocked_roads ?? 0}                              sub="NH-10 affected"                                           danger  loading={loading} />
        <KPICard label="Safe Sites Ready"   value={summary?.safe_sites ?? 0}                                 sub={`${(summary?.total_safe_capacity ?? 0).toLocaleString()} capacity`} accent loading={loading} />
      </div>

      {/* Map + Right Panel */}
      <div style={{ flex: 1, display: 'flex', overflow: 'hidden', padding: '0 16px 16px', gap: 12 }}>
        <div style={{ flex: 1, overflow: 'hidden', borderRadius: 10, border: '1px solid var(--color-border)', position: 'relative' }}>
          <Suspense fallback={<MapLoader />}><LeafletMap layers={layers} /></Suspense>
          <button onClick={() => setPage('alerts')} style={{
            position: 'absolute', bottom: 14, left: 14, zIndex: 500,
            display: 'flex', alignItems: 'center', gap: 10,
            padding: '10px 14px', borderRadius: 8,
            background: 'rgba(12,14,13,0.92)', border: '1px solid var(--color-danger-border)',
            backdropFilter: 'blur(12px)', cursor: 'pointer',
          }}>
            <div className="status-dot" style={{ background: 'var(--color-danger)', boxShadow: '0 0 6px var(--color-danger)', flexShrink: 0 }} />
            <div style={{ textAlign: 'left' }}>
              <div style={{ fontSize: '0.75rem', fontWeight: 700, color: 'var(--color-danger)' }}>CRITICAL — Rongli–Lingtam Corridor</div>
              <div style={{ fontSize: '0.68rem', color: 'var(--color-text-2)', marginTop: 2 }}>Risk 0.89 · 3,030 people at risk · View alert →</div>
            </div>
          </button>
        </div>
        <RightPanel />
      </div>
    </div>
  );
}

function MapLoader() {
  return (
    <div style={{ width: '100%', height: '100%', display: 'flex', alignItems: 'center', justifyContent: 'center', background: 'var(--color-surface-2)' }}>
      <div style={{ textAlign: 'center' }}>
        <div style={{ width: 24, height: 24, border: '2px solid var(--color-primary)', borderTopColor: 'transparent', borderRadius: '50%', animation: 'spin 0.8s linear infinite', margin: '0 auto 10px' }} />
        <div style={{ fontSize: '0.75rem', color: 'var(--color-text-muted)' }}>Loading map…</div>
      </div>
    </div>
  );
}

/* ── Root ─────────────────────────────────────── */
export default function App() {
  const [page, setPage] = useState<Page>('overview');

  // Fetch alerts to drive sidebar badge + API health indicator
  const { data: alerts, error: alertsError } = useApi(ApiService.getAlerts);
  const backendOnline = !alertsError;
  const activeAlertCount = alerts?.filter(a => a.status === 'ACTIVE').length ?? 0;

  return (
    <div style={{ height: '100vh', width: '100vw', display: 'flex', overflow: 'hidden', background: 'var(--color-bg)', fontFamily: "'Outfit', sans-serif" }}>
      <style>{`@keyframes spin { to { transform: rotate(360deg); } }`}</style>
      <Sidebar page={page} setPage={setPage} activeAlertCount={activeAlertCount} />
      <div style={{ flex: 1, display: 'flex', flexDirection: 'column', overflow: 'hidden' }}>
        <TopBar page={page} backendOnline={backendOnline} />
        <div style={{ flex: 1, overflow: 'hidden', display: 'flex' }}>
          <Suspense fallback={<div style={{ flex: 1, display: 'flex', alignItems: 'center', justifyContent: 'center', color: 'var(--color-text-muted)', fontSize: '0.82rem' }}>Loading…</div>}>
            {page === 'overview'   && <Overview setPage={setPage} />}
            {page === 'riskmap'   && <RiskMapPage />}
            {page === 'alerts'    && <AlertCenter />}
            {page === 'incidents' && <Incidents />}
            {page === 'exposure'  && <Exposure />}
            {page === 'relocation'&& <Relocation />}
            {page === 'analytics' && <Analytics />}
            {page === 'weather'   && <Weather />}
          </Suspense>
        </div>
      </div>
    </div>
  );
}
