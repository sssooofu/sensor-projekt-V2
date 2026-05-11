# Dashboard Agent

> **Scope: `dashboard/` only. Do not read, modify, or suggest changes to files outside this directory.**

Vanilla HTML/JS frontend. No build step, no framework, no bundler. Served as static files by the FastAPI server.

## Stack

- Plain HTML5 + CSS3
- Vanilla JavaScript (ES2020 modules)
- Chart.js (loaded via CDN) for time-series charts

**No framework unless explicitly changed.** If you're tempted to add React/Vue/Svelte — don't. Ask first.

## File Layout

```
dashboard/
├── index.html       # single-page app shell, loads all scripts
├── src/
│   ├── api.js       # all fetch() calls to backend — one function per endpoint
│   ├── charts.js    # Chart.js setup, dataset management, sensor toggles
│   ├── relay.js     # relay manual button + automation rule editor UI
│   └── app.js       # page init, device selector, wires everything together
└── styles/
    └── main.css
```

## API Endpoints Used

All base URLs are relative (same host, port 8080). Full shapes in root `CLAUDE.md`.

| Call | Where used |
|------|-----------|
| `GET /api/devices` | `app.js` — populates device selector on load |
| `GET /api/readings?...` | `api.js` → `charts.js` — fetches data for chart |
| `POST /api/commands` | `relay.js` — sends manual relay_on / relay_off |

## How to Add a New Sensor

1. Add a toggle `<input type="checkbox">` in `index.html`
2. Add a dataset to the chart in `charts.js` keyed by the new field name
3. The API already returns the new field if the server was updated — nothing else needed here

## Relay UI

- Manual button: sends `POST /api/commands` with `action: "relay_on"` and a duration
- Status indicator: shows last known relay state (derived from most recent command)
- Rule display: read-only view of `relay_rules` from latest device config (future feature)

## Rules

- All backend calls go through `api.js` — no raw fetch() in other files
- Device selector in `app.js` determines which `device_id` is used globally
- No inline styles — everything in `main.css`
