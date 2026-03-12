# Brokerage API

Backend API for an AI-powered inbound carrier sales agent. Handles carrier verification (FMCSA), load search, call logging, and a metrics dashboard.

## Tech Stack

Python, FastAPI, PostgreSQL, Nginx (SSL), Docker Compose

## Quick Start

```bash
cp .env.example .env        # configure API keys
bash scripts/generate_certs.sh
docker compose up --build
```

API available at `https://localhost/docs` (accept self-signed cert).

## Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/health` | Health check (no auth) |
| GET | `/carrier/verify/{mc_number}` | FMCSA carrier verification |
| POST | `/loads/search` | Search available loads (fuzzy match) |
| POST | `/calls/log` | Log a carrier call |
| GET | `/dashboard` | Aggregated call metrics |

All endpoints except `/health` require an `x-api-key` header.

## Environment Variables

See `.env.example` for required configuration including `API_KEY`, `FMCSA_API_KEY`, and Postgres credentials.
