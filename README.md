# Astrology Chart API

![Python](https://img.shields.io/badge/Python-3.11%2B-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115-green)
![Flatlib](https://img.shields.io/badge/Flatlib-Swiss%20Ephemeris-purple)
![Docker](https://img.shields.io/badge/Docker-recommended-blue)
![License](https://img.shields.io/badge/License-MIT-lightgrey)

FastAPI service for calculating structured astrological chart data from birth information using Flatlib, Swiss Ephemeris and Docker.

![Swagger Execution](docs/swagger-execution.png)

---

## Overview

Astrology Chart API is a backend service that receives birth data and returns a structured JSON representation of an astrological chart.

The project was designed as a reusable calculation layer for astrology-based applications, dashboards, automation workflows and AI-assisted interpretation systems.

It focuses on **calculation and data structure**, not on textual astrological interpretation.

## What the API does

The service receives:

- Birth date
- Birth time
- Birth city
- Timezone
- House system

And returns:

- Sun sign and degree
- Moon sign and degree
- Ascendant sign
- 12 house signs
- Planetary positions
- Retrograde status
- Calculation engine metadata

The calculation engine is powered by **Flatlib** and **Swiss Ephemeris**.

---

## Why this project exists

Astrology products often mix interface, interpretation text, user data and chart calculation in the same codebase.

This project separates the calculation layer into a small HTTP service so it can be reused by:

- Web applications
- Member platforms
- Admin dashboards
- Personal astrology tools
- Automation workflows
- AI-powered interpretation systems

This makes the astrology calculation layer easier to test, replace, deploy and integrate with different frontends.

---

## Architecture

```txt
Client
  ↓
FastAPI Route
  ↓
Pydantic Validation
  ↓
Geocoding Service
  ↓
Timezone Conversion
  ↓
Flatlib / Swiss Ephemeris
  ↓
Structured JSON Response
```

### Main responsibilities

| Layer | Responsibility |
| --- | --- |
| FastAPI | HTTP routes and OpenAPI/Swagger documentation |
| Pydantic | Request and response validation |
| Geocoding | Converts city names into latitude/longitude |
| Timezone handling | Converts local birth time to UTC |
| Flatlib / Swiss Ephemeris | Calculates chart objects and positions |
| Tests | Validate endpoint behavior and response shape |

---

## Technology stack

- Python 3.11+
- FastAPI
- Pydantic
- Flatlib
- Swiss Ephemeris
- OpenCage Geocoding API
- Docker / Docker Compose
- Pytest
- GitHub Actions

---

## API

### Health check

```http
GET /health
```

Response:

```json
{
  "ok": true,
  "service": "astrology-chart-api"
}
```

### Generate chart

```http
POST /chart
```

Request:

```json
{
  "name": "Demo User",
  "birth_date": "1990-08-15",
  "birth_time": "14:35",
  "birth_city": "São Paulo, Brasil",
  "timezone": "America/Sao_Paulo",
  "house_system": "equal"
}
```

Response excerpt:

```json
{
  "name": "Demo User",
  "birth_city": "São Paulo, Brasil",
  "timezone": "America/Sao_Paulo",
  "latitude": -23.5505,
  "longitude": -46.6333,
  "house_system": "equal",
  "sun": "Leo 22.41",
  "moon": "Cancer 18.31",
  "ascendant": "Sagittarius",
  "houses": {
    "house_1": "Sagittarius"
  },
  "planets": {
    "sun": {
      "sign": "Leo",
      "longitude": 142.41,
      "sign_degree": 22.41,
      "is_retrograde": false
    }
  },
  "engine": "flatlib-swiss-ephemeris"
}
```

---

## Running with Docker

Docker is the recommended runtime because Flatlib and Swiss Ephemeris depend on native packages.

```bash
cp .env.example .env
docker compose up --build
```

Open:

```txt
http://localhost:8000/docs
```

Run tests:

```bash
docker compose run --rm astrology-chart-api pytest
```

---

## Local development

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
pytest
uvicorn app.main:app --reload
```

On Unix-like shells, activate the virtual environment with:

```bash
source .venv/bin/activate
```

---

## Environment variables

```env
OPENCAGE_API_KEY=your_key_here
```

For local testing without an API key, the project includes fallback coordinates for a small set of Brazilian cities.

Fallback cities currently include São Paulo, Florianópolis, Rio de Janeiro, Curitiba, Belo Horizonte, Porto Alegre and Brasília.

---

## Automated testing

Run tests locally:

```bash
pytest
```

Or through Docker:

```bash
docker compose run --rm astrology-chart-api pytest
```

The current automated test suite validates the `/chart` endpoint response shape and the expected chart fields.

---

## Known limitations

- Only the `equal` house system is currently exposed.
- Geocoding depends on OpenCage when the requested city is not available in the local fallback list.
- The service returns structured chart data only; it does not generate astrological interpretation text.
- The project is intended as a reusable calculation service, not as a complete user-facing astrology product.
- The fallback city list is intentionally small and intended for local demos/tests.

---

## Roadmap

Potential next improvements:

- Add support for additional house systems.
- Expand automated tests for validation errors and geocoding fallbacks.
- Add example client requests with `curl` and Python.
- Add optional deployment guide for a hosted API environment.
- Add versioned API routes if the service becomes public-facing.

---

## What this project demonstrates

- API design with FastAPI
- Domain-specific calculation workflows
- Pydantic request/response modeling
- External geocoding integration
- Timezone conversion for user-submitted birth data
- Dockerized Python service deployment
- Automated API testing
- Service-oriented architecture for astrology applications

---

## License

MIT. See [`LICENSE`](LICENSE).
