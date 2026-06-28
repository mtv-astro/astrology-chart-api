from typing import Literal

from pydantic import BaseModel, Field


class ChartRequest(BaseModel):
    name: str = Field(..., examples=["Demo User"], min_length=1)
    birth_date: str = Field(
        ...,
        examples=["1990-08-15"],
        description="Format: YYYY-MM-DD",
        pattern=r"^\d{4}-\d{2}-\d{2}$",
    )
    birth_time: str = Field(
        ...,
        examples=["14:35"],
        description="Format: HH:MM",
        pattern=r"^([01]\d|2[0-3]):[0-5]\d$",
    )
    birth_city: str = Field(..., examples=["São Paulo, Brasil"], min_length=1)
    timezone: str = Field("America/Sao_Paulo", examples=["America/Sao_Paulo"], min_length=1)
    house_system: Literal["equal"] = Field("equal", examples=["equal"])


class PlanetPosition(BaseModel):
    sign: str
    longitude: float
    sign_degree: float
    is_retrograde: bool


class ChartResponse(BaseModel):
    name: str
    birth_city: str
    timezone: str
    latitude: float
    longitude: float
    house_system: str
    sun: str
    moon: str
    ascendant: str
    houses: dict[str, str]
    planets: dict[str, PlanetPosition]
    engine: str
