# Geographic Information System (GIS)

A GIS portal to plan, manage and monitor fiber network infrastructure on a map.

## Stack

| Layer    | Tech                  | Responsibility                                                        |
|----------|-----------------------|-----------------------------------------------------------------------|
| Frontend | React + Vite          | UI, Leaflet GIS map, forms, dashboard                                 |
| Backend  | Python + FastAPI      | Business logic, JWT auth, GIS operations, validation (REST / JSON)    |
| Database | PostgreSQL + PostGIS  | Infrastructure records, coordinates, relationships, access control    |

```
React (Vite) ──REST/JSON──▶ FastAPI ──SQLAlchemy/GeoAlchemy2──▶ PostgreSQL + PostGIS
```

## Features

- Login with role-based access (SUPER_ADMIN, ADMIN, EDITOR, FIELD, VIEWER)
- Group (tenant) selector, global search (assets, cables, customers)
- Interactive map: OLT / ODF / FAT / splitters / poles / manholes / ONT points and fiber cable routes
- Sidebar modules: Core, Network, Fiber, Customers, Physical, Tools
- Generic asset CRUD, cable creation with auto-generated cores, GeoJSON map endpoint

## Project layout

```
gis/
├── backend/            FastAPI app (app/main.py, models.py, routers/, core/, seed.py)
├── frontend/           React + Vite app (src/pages, src/components, nav.js)
├── database/init.sql   Enables PostGIS
└── docker-compose.yml  db + backend + frontend
```

## Quick start (Docker)

```bash
docker compose up --build
docker compose exec backend python -m app.seed   # creates tables, demo data, admin user
```

- App: http://localhost:8080
- API docs: http://localhost:8000/docs
- Default login: `admin` / `ChangeMe@123` (change it; set `SEED_ADMIN_PASSWORD` before seeding)

## Local development

```bash
# Database
docker compose up -d db

# Backend
cd backend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python -m app.seed
uvicorn app.main:app --reload

# Frontend
cd ../frontend
npm install
npm run dev      # http://localhost:5173 (proxies /api to :8000)
```

## API overview

| Method | Path                     | Description                          |
|--------|--------------------------|--------------------------------------|
| POST   | `/api/auth/login`        | Obtain JWT                           |
| GET    | `/api/auth/me`           | Current user                         |
| GET    | `/api/auth/groups`       | Groups visible to the user           |
| GET    | `/api/map/features`      | GeoJSON of assets + cables for a group |
| GET    | `/api/assets`            | List assets (filter by `asset_type`) |
| POST   | `/api/assets`            | Create asset (lat/lng)               |
| DELETE | `/api/assets/{id}`       | Delete asset (admin)                 |
| POST   | `/api/cables`            | Create cable route + cores           |
| GET    | `/api/search`            | Global search                        |

## Roadmap

- Dedicated screens for ports, cores, splice closures, customers and services
- Fiber trace (OLT → ONT path) and reports
- Photo capture and upload for field data
- Alembic migrations, tests, CI

## Security notes

Replace `SECRET_KEY` and the seeded admin password before any real deployment, and serve behind HTTPS.
