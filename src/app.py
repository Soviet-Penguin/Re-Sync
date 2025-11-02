# app.py
from flask import Flask, render_template_string, request, jsonify

app = Flask(__name__)

# ---------------------------
# DASHBOARD HTML ("/")
# ---------------------------
INDEX_HTML = """
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width,initial-scale=1" />
<title>RESYNC — Dashboard</title>
<style>
:root{
  --bg:#0b0f14;
  --card:#0f1418;
  --muted:#9aa7b2;
  --accent:#7c88ff;
  --accent-2:#4dd0e1;
  --glass: rgba(255,255,255,0.03);
}
html,body{height:100%;margin:0;background:radial-gradient(1200px 600px at 10% 10%, rgba(124,136,255,0.04), transparent), linear-gradient(180deg,#06070a,#0b0f14);font-family:Inter,ui-sans-serif,system-ui,-apple-system,Segoe UI,Roboto,"Helvetica Neue",Arial;color:#e6eef6;overflow:hidden}
.center {
  height:100vh; display:flex; align-items:center; justify-content:center; gap:40px; padding:28px; box-sizing:border-box;
}
.card {
  width:min(760px,92vw);
  border-radius:14px;
  background:linear-gradient(180deg, rgba(255,255,255,0.012), rgba(255,255,255,0.008));
  box-shadow: 0 10px 40px rgba(2,6,23,0.7);
  border:1px solid var(--glass);
  overflow:hidden;
  display:flex;
  gap:0;
}
.left {
  flex:0 0 360px;
  padding:28px;
  display:flex;
  flex-direction:column;
  gap:18px;
  backdrop-filter: blur(6px);
}
.brand {
  font-weight:800; font-size:28px; color:#fff; letter-spacing:0.6px;
}
.tag { color:var(--muted); font-size:13px; margin-top:2px }
.weather {
  margin-top:6px; display:flex; gap:14px; align-items:center;
}
.weather .icon {
  width:84px; height:84px; border-radius:12px; display:flex; align-items:center; justify-content:center;
  background:linear-gradient(180deg, rgba(255,255,255,0.02), rgba(255,255,255,0.01));
  box-shadow: 0 8px 30px rgba(77,208,225,0.04), inset 0 -6px 20px rgba(0,0,0,0.6);
}
.weather .vals { display:flex; flex-direction:column; gap:6px; }
.temp { font-size:28px; font-weight:700; }
.small-muted { color:var(--muted); font-size:13px }
.start-btn {
  margin-top:14px;
  padding:12px 16px;
  border-radius:12px;
  background:linear-gradient(90deg,var(--accent),#5e6eff);
  border:none; color:white; font-weight:700; cursor:pointer; box-shadow:0 12px 30px rgba(124,136,255,0.12);
}
.left .meta { margin-top:auto; color:var(--muted); font-size:12px }

.right {
  flex:1; position:relative; min-height:320px;
  display:flex; align-items:center; justify-content:center; overflow:hidden;
}
.motion {
  position:absolute; inset:0; z-index:0; background:
    radial-gradient(circle at 20% 30%, rgba(124,136,255,0.035), transparent 8%),
    radial-gradient(circle at 80% 70%, rgba(77,208,225,0.02), transparent 8%);
  filter: blur(10px);
  animation: slow-shift 12s linear infinite;
}
@keyframes slow-shift { from{ transform:translateY(0)} to{ transform:translateY(-20px)} }
.center-hud {
  position:relative; z-index:2; width:100%; display:flex; align-items:center; justify-content:center; padding:20px;
}
.hud-card {
  width:min(680px,86%); border-radius:12px; padding:22px; background:linear-gradient(180deg, rgba(255,255,255,0.01), rgba(255,255,255,0.006)); border:1px solid var(--glass);
  display:flex; align-items:center; justify-content:space-between; gap:18px; box-shadow:0 8px 30px rgba(2,6,23,0.6);
}
.hud-left { display:flex; gap:14px; align-items:center; min-width:0; }
.logo-square { width:56px; height:56px; border-radius:10px; background:linear-gradient(180deg,var(--accent),#5e6eff); display:flex; align-items:center; justify-content:center; font-weight:800; font-size:20px; color:white; box-shadow: 0 10px 30px rgba(92,100,255,0.12);}
.hud-text { min-width:0 }
.hud-title { font-size:18px; font-weight:700; white-space:nowrap; overflow:hidden; text-overflow:ellipsis; }
.hud-sub { color:var(--muted); font-size:13px; margin-top:4px; }

.loader {
  width:120px; height:120px; border-radius:60px; display:flex; align-items:center; justify-content:center;
  position:relative;
}
.pulse {
  width:100%; height:100%; border-radius:50%; background:radial-gradient(circle at 30% 30%, rgba(124,136,255,0.08), rgba(124,136,255,0.02));
  animation: pulse 1600ms infinite;
  box-shadow: 0 18px 60px rgba(124,136,255,0.06);
}
@keyframes pulse { 0%{transform:scale(0.86);opacity:0.9}50%{transform:scale(1.06);opacity:0.6}100%{transform:scale(0.86);opacity:0.9} }

.footer-small { position:absolute; bottom:14px; left:20px; color:var(--muted); font-size:12px; z-index:4 }

@media (max-width:880px){
  .card{flex-direction:column}
  .left{flex:unset;width:100%}
  .center-hud{padding:8px}
}
</style>
</head>
<body>
<div class="center">
  <div class="card" role="main">
    <div class="left">
      <div>
        <div class="brand">RESYNC</div>
        <div class="tag">Smart Navigation — Modern matte dark demo</div>
      </div>

      <div class="weather" id="weatherBlock">
        <div class="icon" id="weatherIcon" aria-hidden="true">
          <!-- SVG icon injected -->
        </div>
        <div class="vals">
          <div class="temp" id="temp">--°C</div>
          <div class="small-muted" id="cond">Detecting location & weather…</div>
          <div class="small-muted" id="hum">Humidity: --%</div>
        </div>
      </div>

      <button class="start-btn" id="startBtn">Start Navigation</button>

      <div class="meta">Auto-location + real weather (Open-Meteo) — demo routing uses free public services.</div>
    </div>

    <div class="right">
      <div class="motion" aria-hidden="true"></div>

      <div class="center-hud">
        <div class="hud-card">
          <div class="hud-left">
            <div class="logo-square">R</div>
            <div class="hud-text">
              <div class="hud-title">Ready when you are</div>
              <div class="hud-sub">Tap Start to open the live map and search for places.</div>
            </div>
          </div>
          <div style="display:flex;align-items:center;gap:14px">
            <div class="loader" aria-hidden="true"><div class="pulse"></div></div>
            <div style="min-width:120px"></div>
          </div>
        </div>
      </div>

      <div class="footer-small">Demo: no API keys required. Works offline for styling; routes use public OSRM & Photon services.</div>
    </div>
  </div>
</div>

<script>
/* -- Utilities -- */
function $(id){return document.getElementById(id)}
function setSVGIcon(container, code){
  container.innerHTML = code;
}

/* -- Weather fetch (Open-Meteo free, no key) -- */
async function fetchWeather(lat, lon){
  try {
    // current weather + hourly humidity; timezone auto to align hour index
    const url = `https://api.open-meteo.com/v1/forecast?latitude=${lat}&longitude=${lon}&current_weather=true&hourly=relativehumidity_2m&timezone=auto`;
    const r = await fetch(url);
    const j = await r.json();
    if(!j || !j.current_weather) return null;
    const temp = j.current_weather.temperature;
    // approximate humidity from hourly matching current hour index
    let humidity = '--';
    if(j.hourly && j.hourly.relativehumidity_2m){
      const idx = j.hourly.time.indexOf(j.current_weather.time);
      if(idx>=0) humidity = j.hourly.relativehumidity_2m[idx];
      else humidity = j.hourly.relativehumidity_2m[0];
    }
    return { temp: Math.round(temp), humidity, code: j.current_weather.weathercode, windspeed: j.current_weather.windspeed };
  } catch(e){
    console.error('weather fail', e);
    return null;
  }
}

/* map weather code -> premium SVG */
function weatherSVG(code){
  // Simplified mapping for demo
  if(code===0) return '<svg width="56" height="56" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><defs><filter id="g"><feGaussianBlur stdDeviation="4" result="b"/></filter></defs><g filter="url(#g)"><circle cx="12" cy="10" r="5" fill="url(#g1)"/></g><circle cx="12" cy="10" r="5" stroke="rgba(255,255,255,0.06)"/></svg>';
  if([1,2,3].includes(code)) return '<svg width="56" height="56" viewBox="0 0 24 24"><path d="M3 12h18" stroke="rgba(255,255,255,0.08)" stroke-width="2" stroke-linecap="round"/></svg>';
  if([61,63,65,80,81,82].includes(code)) return '<svg width="56" height="56"><path d="M6 14l2 2 2-2 2 2 2-2 2 2" stroke="rgba(77,208,225,0.9)" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></svg>';
  return '<svg width="56" height="56"><circle cx="12" cy="12" r="7" fill="rgba(124,136,255,0.08)"/></svg>';
}

/* -- Geolocate & show weather -- */
async function initDashboard(){
  const icon = $('weatherIcon'), tempEl = $('temp'), cond = $('cond'), hum = $('hum');
  if(!navigator.geolocation){
    cond.textContent = 'Geolocation unavailable. Allow location or use map search.';
    return;
  }
  cond.textContent = 'Detecting location…';
  navigator.geolocation.getCurrentPosition(async (pos) => {
    const lat = pos.coords.latitude.toFixed(6), lon = pos.coords.longitude.toFixed(6);
    cond.textContent = 'Fetching weather…';
    const w = await fetchWeather(lat, lon);
    if(!w){ cond.textContent = 'Weather unavailable'; return; }
    tempEl.textContent = `${w.temp}°C`;
    hum.textContent = `Humidity: ${w.humidity}% • Wind ${Math.round(w.windspeed)} km/h`;
    cond.textContent = 'Current conditions';
    setSVGIcon(icon, weatherSVG(w.code));
  }, (err) => {
    console.warn('geoloc err', err);
    cond.textContent = 'Location denied — grant location or use map search.';
    tempEl.textContent = '--°C';
    hum.textContent = 'Humidity: --%';
    setSVGIcon(icon, weatherSVG(0));
  }, { maximumAge:60000, timeout:8000 });
}

/* -- Start button -> map (opens /map) -- */
$('startBtn').addEventListener('click', async () => {
  // Smooth fade then navigate
  document.body.style.transition = 'opacity .36s ease';
  document.body.style.opacity = '0';
  setTimeout(()=> location.href = '/map', 340);
});

/* init */
initDashboard();
</script>
</body>
</html>
"""

# ---------------------------
# MAP PAGE HTML ("/map")
# ---------------------------
MAP_HTML = """
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width,initial-scale=1" />
<title>RESYNC — Live Map</title>

<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css"
  integrity="" crossorigin=""/>

<style>
:root{
  --bg:#06070a; --muted:#9aa7b2; --card:rgba(255,255,255,0.02);
  --accent:#5e6eff; --accent-2:#4dd0e1;
}
html,body,#map{height:100%;margin:0;background:linear-gradient(180deg,#04050a,#0b0f14);color:#e6eef6;font-family:Inter,system-ui,Segoe UI,Roboto,Arial}
.app {
  display:grid; grid-template-columns: 360px 1fr; height:100vh; gap:18px; padding:16px; box-sizing:border-box;
}
.sidebar {
  border-radius:14px; padding:16px; background:linear-gradient(180deg, rgba(255,255,255,0.012), rgba(255,255,255,0.008)); border:1px solid rgba(255,255,255,0.03);
  min-width:300px; display:flex; flex-direction:column; gap:12px; box-shadow: 0 12px 40px rgba(2,6,23,0.6);
}
.title { font-weight:800; color:var(--accent); font-size:18px }
.hint { color:var(--muted); font-size:13px }
.input { padding:12px;border-radius:12px;border:1px solid rgba(255,255,255,0.03); background:transparent; color:inherit; outline:none; font-size:14px; }
.controls { display:flex; gap:8px }
.btn { padding:10px 12px; border-radius:10px; border:none; cursor:pointer; background:linear-gradient(90deg,var(--accent),#4f5bff); color:white; font-weight:700 }
.small { font-size:13px; padding:8px 10px; background:transparent; border:1px dashed rgba(255,255,255,0.03); color:var(--muted) }

.suggestions { position:relative }
.dropdown { position:absolute; top:48px; left:0; right:0; background:linear-gradient(180deg,#0f1720,#0b1320); border-radius:10px; max-height:220px; overflow:auto; border:1px solid rgba(255,255,255,0.03); z-index:9999; }
.dropdown div { padding:10px 12px; cursor:pointer; color:#dbefff; font-size:13px }
.dropdown div:hover { background:rgba(255,255,255,0.02) }

.map-wrap { border-radius:14px; overflow:hidden; box-shadow: 0 18px 50px rgba(2,6,23,0.7); border:1px solid rgba(255,255,255,0.03); position:relative; }
#map { height:100%; width:100%; }

.directions { margin-top:6px; border-radius:10px; background:rgba(255,255,255,0.01); padding:10px; max-height:36vh; overflow:auto; color:var(--muted); font-size:13px; }
.step { padding:8px; border-bottom:1px solid rgba(255,255,255,0.02); color:#e6eef6 }

.loader-overlay {
  position:absolute; inset:0; display:flex; align-items:center; justify-content:center; z-index:3000; pointer-events:none;
}
.radar {
  width:120px; height:120px; border-radius:60px; display:flex; align-items:center; justify-content:center;
  background:radial-gradient(circle at 30% 30%, rgba(94,110,255,0.06), transparent);
  box-shadow:0 30px 80px rgba(94,110,255,0.06);
}
.radar .ring { position:absolute; width:100%; height:100%; border-radius:50%; border:1px solid rgba(94,110,255,0.08); animation:spin 1400ms linear infinite; opacity:0.9 }
@keyframes spin { from{transform:scale(0.88) rotate(0deg)} to{transform:scale(1.12) rotate(360deg)} }

.legend { margin-top:8px; display:flex; gap:10px; align-items:center; color:var(--muted); font-size:13px }
.legend .dot{ width:12px;height:8px;border-radius:6px; display:inline-block; margin-right:6px }

@media (max-width:900px){
  .app{grid-template-columns:1fr; grid-template-rows:340px 1fr; padding:10px}
  .sidebar{min-width:unset}
}
</style>
</head>
<body>
<div class="app">
  <div class="sidebar" role="navigation" aria-label="controls">
    <div>
      <div class="title">RESYNC — Live Map</div>
      <div class="hint">Search places, get route & visual traffic (demo-mode).</div>
    </div>

    <label class="small-muted">From</label>
    <div class="suggestions">
      <input id="from" class="input" placeholder="Enter origin" autocomplete="off">
      <div id="from-list" class="dropdown" style="display:none"></div>
    </div>

    <label class="small-muted">To</label>
    <div class="suggestions">
      <input id="to" class="input" placeholder="Enter destination" autocomplete="off">
      <div id="to-list" class="dropdown" style="display:none"></div>
    </div>

    <div class="controls">
      <button id="routeBtn" class="btn">Get Directions</button>
      <button id="swapBtn" class="small">Swap</button>
      <button id="clearBtn" class="small">Clear</button>
    </div>

    <div class="directions" id="directions"><div class="hint">Turn-by-turn will appear here.</div></div>

    <div class="legend">
      <div><span class="dot" style="background:rgb(52,199,89)"></span> Smooth</div>
      <div><span class="dot" style="background:rgb(255,195,0)"></span> Slow</div>
      <div><span class="dot" style="background:rgb(255,80,80)"></span> Heavy</div>
    </div>

  </div>

  <div class="map-wrap">
    <div id="map" aria-hidden="false"></div>

    <div class="loader-overlay" id="loader">
      <div class="radar"><div class="ring"></div></div>
    </div>

  </div>
</div>

<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>

<script>
/* ======= Config ======= */
const PHOTON_API = 'https://photon.komoot.io/api/?q=';
const OSRM_API = 'https://router.project-osrm.org/route/v1/driving/';
/* ====================== */

let map, routeLayer, fromMarker, toMarker, carMarker, animHandle;
let fromCoord=null, toCoord=null;

/* ---------- Map init ---------- */
function initMap(){
  map = L.map('map', { zoomControl:true, preferCanvas:true }).setView([20.5937,78.9629], 5);
  L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}.png', { maxZoom:19, attribution:'&copy; OpenStreetMap contributors & CartoDB' }).addTo(map);
  routeLayer = L.layerGroup().addTo(map);
}

/* ---------- Helpers ---------- */
function debounce(fn, ms=250){ let t; return (...a)=>{ clearTimeout(t); t=setTimeout(()=>fn(...a), ms); }; }
function $(id){return document.getElementById(id)}
function escapeHtml(s){ return s.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;'); }

/* ---------- Autocomplete (Photon) ---------- */
async function photonSearch(q){
  if(!q || q.length<2) return [];
  const res = await fetch(PHOTON_API + encodeURIComponent(q) + '&limit=6');
  if(!res.ok) return [];
  const j = await res.json();
  if(!j.features) return [];
  return j.features.map(f=>({
    name: (f.properties.name || '') + (f.properties.city?(', '+f.properties.city):'') + (f.properties.country?(', '+f.properties.country):''),
    coords: [f.geometry.coordinates[1], f.geometry.coordinates[0]],
    raw: f
  }));
}

const fromInput = $('from'), toInput = $('to'), fromList = $('from-list'), toList = $('to-list');
const showSuggestions = (listEl, items)=>{
  if(!items || items.length===0){ listEl.style.display='none'; listEl.innerHTML=''; return; }
  listEl._items = items;
  listEl.innerHTML = items.map((it,i)=>`<div data-idx="${i}">${escapeHtml(it.name)}</div>`).join('');
  listEl.style.display='block';
};
fromInput.addEventListener('input', debounce(async (e)=>{ showSuggestions(fromList, await photonSearch(e.target.value)); },280));
toInput.addEventListener('input', debounce(async (e)=>{ showSuggestions(toList, await photonSearch(e.target.value)); },280));
fromList.addEventListener('click',(ev)=>{ const d=ev.target.closest('div'); if(!d) return; const it=fromList._items[d.dataset.idx]; fromInput.value = d.textContent; fromCoord = it.coords; fromList.style.display='none'; setFromMarker(fromCoord); });
toList.addEventListener('click',(ev)=>{ const d=ev.target.closest('div'); if(!d) return; const it=toList._items[d.dataset.idx]; toInput.value = d.textContent; toCoord = it.coords; toList.style.display='none'; setToMarker(toCoord); });

/* ---------- Markers ---------- */
function glowIcon(color='#7c88ff'){
  return L.divIcon({ className:'glow', html:`<div style="width:18px;height:18px;border-radius:50%;background:${color};box-shadow:0 8px 28px ${color}33;"></div>`, iconSize:[18,18], iconAnchor:[9,9]});
}
function setFromMarker(latlng){
  if(fromMarker) map.removeLayer(fromMarker);
  fromMarker = L.marker(latlng, {icon:glowIcon('#7c88ff')}).addTo(map).bindPopup('Origin').openPopup();
  map.flyTo(latlng, 12);
}
function setToMarker(latlng){
  if(toMarker) map.removeLayer(toMarker);
  toMarker = L.marker(latlng, {icon:glowIcon('#4dd0e1')}).addTo(map).bindPopup('Destination').openPopup();
  map.flyTo(latlng, 12);
}

/* ---------- Routing (OSRM) ---------- */
async function getRoute(from, to){
  const url = OSRM_API + `${from[1]},${from[0]};${to[1]},${to[0]}?overview=full&geometries=geojson&steps=true`;
  const r = await fetch(url);
  if(!r.ok) throw new Error('Routing failed');
  return await r.json();
}

/* ---------- Traffic-coloring logic ----------
   Colors segments based on a speed heuristic:
   speed = distance(m) / duration(s) -> m/s -> convert km/h
   thresholds produce green/yellow/red.
*/
function colorSegmentsFromRoute(route){
  const coords = route.geometry.coordinates; // [lon,lat]
  // Build segment features with speed metric by mapping over steps (more reliable)
  const segs = [];
  if(route.legs && route.legs.length){
    route.legs.forEach(leg=>{
      leg.steps.forEach(step=>{
        const geom = step.geometry || null;
        let points = [];
        if(geom && geom.coordinates) points = geom.coordinates.map(c=>[c[1],c[0]]);
        else {
          // fallback: small segment from maneuver
          const m = step.maneuver && step.maneuver.location ? [step.maneuver.location[1], step.maneuver.location[0]] : [];
          if(m.length) points = [m];
        }
        if(points.length){
          const speed_kmh = step.duration>0 ? ( (step.distance/1000) / (step.duration/3600) ) : 0;
          let color = '#34c759'; // green
          if(speed_kmh < 15) color = '#ff5050'; // heavy
          else if(speed_kmh < 35) color = '#ffc300'; // slow
          segs.push({ points, color, distance:step.distance, duration:step.duration });
        }
      });
    });
  }
  return segs;
}

/* ---------- Render route & traffic ---------- */
function clearRoute(){
  routeLayer.clearLayers();
  if(carMarker){ map.removeLayer(carMarker); carMarker = null; if(animHandle){ cancelAnimationFrame(animHandle); animHandle=null; } }
  $('directions').innerHTML = '<div class="hint">Turn-by-turn will appear here.</div>';
}

function renderRoute(data){
  routeLayer.clearLayers();
  const route = data.routes && data.routes[0];
  if(!route) return;
  // full polyline
  const latlngs = route.geometry.coordinates.map(c=>[c[1],c[0]]);
  L.polyline(latlngs, { color:'#7c88ff', weight:4, opacity:0.12 }).addTo(routeLayer);

  // color segments by steps (traffic-like)
  const segs = colorSegmentsFromRoute(route);
  segs.forEach(s=>{
    L.polyline(s.points, { color:s.color, weight:6, opacity:0.95, lineCap:'round' }).addTo(routeLayer);
  });

  // fit bounds
  const bounds = L.latLngBounds(latlngs);
  map.fitBounds(bounds.pad(0.08));

  // steps text
  const steps = [];
  route.legs.forEach(leg=>{
    leg.steps.forEach(step=>{
      const instr = step.maneuver.instruction || (step.maneuver.type + ' ' + (step.maneuver.modifier||''));
      steps.push({ instr, dist:step.distance, dur:step.duration });
    });
  });
  showSteps(steps);

  // animate car along route (smooth)
  startCarAnimation(latlngs, route.duration || 60);
}

/* ---------- Steps display ---------- */
function showSteps(steps){
  const el = $('directions');
  if(!steps.length){ el.innerHTML = '<div class="hint">No directions found.</div>'; return; }
  el.innerHTML = steps.map((s,i)=>`<div class="step"><strong>${i+1}.</strong> ${escapeHtml(s.instr)} <div class="small-muted">${(s.dist/1000).toFixed(2)} km • ${(s.dur/60).toFixed(0)} min</div></div>`).join('');
}

/* ---------- Car animation ---------- */
function startCarAnimation(latlngs, totalDurationSec){
  if(!latlngs || latlngs.length<2) return;
  // create car marker
  if(carMarker) map.removeLayer(carMarker);
  const carEl = L.divIcon({ className:'car-icon', html: `
    <div style="width:34px;height:16px;border-radius:8px;background:linear-gradient(90deg,#98a8ff,#5e6eff);box-shadow:0 10px 30px rgba(94,110,255,0.14);transform:rotate(0deg);"></div>
  `, iconSize:[34,16], iconAnchor:[17,8] });
  carMarker = L.marker(latlngs[0], { icon: carEl, interactive:false }).addTo(map);

  // precompute cumulative distances
  const dists = [0];
  let total = 0;
  for(let i=1;i<latlngs.length;i++){
    total += map.distance(latlngs[i-1], latlngs[i]);
    dists.push(total);
  }
  if(total===0) return;
  const start = performance.now();
  function step(now){
    const elapsed = (now - start) / 1000;
    const frac = Math.min(1, elapsed / Math.max(1, totalDurationSec));
    const s = frac * total;
    // find segment
    let idx = 0;
    while(idx < dists.length && dists[idx] < s) idx++;
    const i1 = Math.max(0, idx-1), i2 = Math.min(latlngs.length-1, idx);
    const segLen = dists[i2] - dists[i1] || 1;
    const t = (s - dists[i1]) / segLen;
    const lat = latlngs[i1][0] + (latlngs[i2][0] - latlngs[i1][0]) * t;
    const lon = latlngs[i1][1] + (latlngs[i2][1] - latlngs[i1][1]) * t;
    carMarker.setLatLng([lat, lon]);
    if(frac < 1) animHandle = requestAnimationFrame(step);
    else animHandle = null;
  }
  animHandle = requestAnimationFrame(step);
}

/* ---------- UI Buttons ---------- */
$('routeBtn').addEventListener('click', async ()=>{
  if(!fromCoord || !toCoord){ alert('Select both origin and destination from suggestions.'); return; }
  try {
    $('loader').style.pointerEvents = 'auto';
    $('loader').style.opacity = '1';
    $('loader').style.visibility = 'visible';
    const data = await getRoute(fromCoord, toCoord);
    renderRoute(data);
  } catch(e){
    console.error(e);
    alert('Routing error. Try another pair.');
  } finally {
    setTimeout(()=>{ $('loader').style.opacity = '0'; $('loader').style.pointerEvents = 'none'; $('loader').style.visibility='hidden'; }, 600);
  }
});

$('swapBtn').addEventListener('click', ()=>{
  const fv = fromInput.value, tv = toInput.value, fc = fromCoord, tc = toCoord;
  fromInput.value = tv; toInput.value = fv;
  fromCoord = tc; toCoord = fc;
  if(fromMarker){ map.removeLayer(fromMarker); fromMarker=null; }
  if(toMarker){ map.removeLayer(toMarker); toMarker=null; }
  if(fromCoord) setFromMarker(fromCoord);
  if(toCoord) setToMarker(toCoord);
  clearRoute();
});

$('clearBtn').addEventListener('click', ()=>{
  fromInput.value=''; toInput.value=''; fromCoord=toCoord=null;
  if(fromMarker){ map.removeLayer(fromMarker); fromMarker=null; }
  if(toMarker){ map.removeLayer(toMarker); toMarker=null; }
  clearRoute();
});

/* ---------- Close dropdowns on outside click ---------- */
document.addEventListener('click', (ev)=>{
  if(!ev.target.closest('.suggestions')){ fromList.style.display='none'; toList.style.display='none'; }
});

/* ---------- Auto-locate user to center map on load ---------- */
function tryAutoLocate(){
  if(!navigator.geolocation) return;
  navigator.geolocation.getCurrentPosition((pos)=>{
    const lat = pos.coords.latitude, lon = pos.coords.longitude;
    map.setView([lat, lon], 13);
    // show a marker for current location
    const cur = L.circleMarker([lat, lon], { radius:8, fill:true, fillColor:'#4dd0e1', color:'rgba(255,255,255,0.06)', weight:1, opacity:0.95 }).addTo(map);
    cur.bindPopup('You are here').openPopup();
  }, ()=>{}, { timeout:5000 });
}

/* ---------- Init ---------- */
window.addEventListener('load', ()=>{
  initMap();
  tryAutoLocate();
  // hide loader after map tiles settled
  setTimeout(()=>{ $('loader').style.opacity = '0'; $('loader').style.visibility='hidden'; $('loader').style.pointerEvents='none'; }, 900);

  // neat UX: when user focuses input and geolocation permission denied, we center to world
});

/* End */
</script>
</body>
</html>
"""

# ---------------------------
# ROUTES
# ---------------------------
@app.route("/")
def index():
    return render_template_string(INDEX_HTML)

@app.route("/map")
def map_page():
    return render_template_string(MAP_HTML)

if __name__ == "__main__":
    # debug disabled by default for "spotless" but turn on when dev
    app.run(host="127.0.0.1", port=5000, debug=False)
