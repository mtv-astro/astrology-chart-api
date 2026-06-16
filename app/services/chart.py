from datetime import datetime

import pytz
from fastapi import HTTPException
from flatlib import const
from flatlib.chart import Chart
from flatlib.datetime import Datetime
from flatlib.geopos import GeoPos

from app.schemas import ChartRequest, ChartResponse
from app.services.geocoding import get_coordinates

PLANETS = [
    const.SUN,
    const.MOON,
    const.MERCURY,
    const.VENUS,
    const.MARS,
    const.JUPITER,
    const.SATURN,
    const.URANUS,
    const.NEPTUNE,
    const.PLUTO,
    const.NORTH_NODE,
    const.SOUTH_NODE,
    const.PARS_FORTUNA,
    const.SYZYGY,
]

HOUSE_SYSTEMS = {
    "equal": const.HOUSES_EQUAL,
}


def _sign_degree(longitude: float) -> float:
    return round(longitude % 30, 2)


def build_chart_response(payload: ChartRequest) -> ChartResponse:
    try:
        house_system = HOUSE_SYSTEMS.get(payload.house_system.lower())
        if not house_system:
            raise HTTPException(
                status_code=400,
                detail=f"Unsupported house system: {payload.house_system}. Supported: {', '.join(HOUSE_SYSTEMS)}",
            )

        latitude, longitude = get_coordinates(payload.birth_city)

        local_tz = pytz.timezone(payload.timezone)
        local_dt = datetime.strptime(
            f"{payload.birth_date} {payload.birth_time}",
            "%Y-%m-%d %H:%M",
        )

        localized_dt = local_tz.localize(local_dt)
        utc_dt = localized_dt.astimezone(pytz.utc)

        date = Datetime(
            utc_dt.strftime("%Y/%m/%d"),
            utc_dt.strftime("%H:%M"),
            "+00:00",
        )

        chart = Chart(
            date,
            GeoPos(latitude, longitude),
            hsys=house_system,
            IDs=PLANETS,
        )

        sun = chart.get(const.SUN)
        moon = chart.get(const.MOON)
        ascendant = chart.get(const.ASC)

        houses = {
            f"house_{index}": chart.get(f"House{index}").sign
            for index in range(1, 13)
        }

        planets = {}
        for obj in PLANETS:
            body = chart.get(obj)
            if body:
                planets[body.id.lower()] = {
                    "sign": body.sign,
                    "longitude": round(body.lon, 2),
                    "sign_degree": _sign_degree(body.lon),
                    "is_retrograde": body.isRetrograde(),
                }

        return ChartResponse(
            name=payload.name,
            birth_city=payload.birth_city,
            timezone=payload.timezone,
            latitude=round(latitude, 6),
            longitude=round(longitude, 6),
            house_system=payload.house_system.lower(),
            sun=f"{sun.sign} {_sign_degree(sun.lon):.2f}",
            moon=f"{moon.sign} {_sign_degree(moon.lon):.2f}",
            ascendant=ascendant.sign,
            houses=houses,
            planets=planets,
            engine="flatlib-swiss-ephemeris",
        )

    except HTTPException:
        raise
    except pytz.UnknownTimeZoneError as error:
        raise HTTPException(status_code=400, detail=f"Unknown timezone: {payload.timezone}") from error
    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail="Invalid date or time format. Use birth_date=YYYY-MM-DD and birth_time=HH:MM.",
        ) from error
    except Exception as error:
        raise HTTPException(status_code=500, detail=str(error)) from error
