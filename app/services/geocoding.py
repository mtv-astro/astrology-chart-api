import os
from functools import lru_cache

import requests
from fastapi import HTTPException


FALLBACK_COORDINATES: dict[str, tuple[float, float]] = {
    "sao paulo": (-23.5505, -46.6333),
    "são paulo": (-23.5505, -46.6333),
    "florianopolis": (-27.5949, -48.5482),
    "florianópolis": (-27.5949, -48.5482),
    "rio de janeiro": (-22.9068, -43.1729),
    "curitiba": (-25.4284, -49.2733),
    "belo horizonte": (-19.9167, -43.9345),
    "porto alegre": (-30.0346, -51.2177),
    "brasilia": (-15.7939, -47.8828),
    "brasília": (-15.7939, -47.8828),
}


def _normalize_city(city: str) -> str:
    return city.strip().lower().split(",")[0]


@lru_cache(maxsize=256)
def get_coordinates(city: str) -> tuple[float, float]:
    api_key = os.getenv("OPENCAGE_API_KEY")
    normalized_city = _normalize_city(city)

    if not api_key:
        if normalized_city in FALLBACK_COORDINATES:
            return FALLBACK_COORDINATES[normalized_city]

        raise HTTPException(
            status_code=500,
            detail=(
                "Missing OPENCAGE_API_KEY environment variable. "
                "For demo without an API key, use one of the fallback cities: "
                + ", ".join(sorted(FALLBACK_COORDINATES.keys()))
            ),
        )

    response = requests.get(
        "https://api.opencagedata.com/geocode/v1/json",
        params={"q": city, "key": api_key, "limit": 1},
        timeout=10,
    )

    if response.status_code >= 400:
        raise HTTPException(
            status_code=502,
            detail="Geocoding provider returned an error.",
        )

    data = response.json()
    results = data.get("results", [])

    if not results:
        raise HTTPException(status_code=400, detail="Location not found.")

    geometry = results[0]["geometry"]
    return float(geometry["lat"]), float(geometry["lng"])
