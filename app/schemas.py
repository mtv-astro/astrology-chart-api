from pydantic import BaseModel, Field


class ChartRequest(BaseModel):
    name: str = Field(..., examples=["Joana"])
    birth_date: str = Field(..., examples=["1990-08-15"], description="Format: YYYY-MM-DD")
    birth_time: str = Field(..., examples=["14:35"], description="Format: HH:MM")
    birth_city: str = Field(..., examples=["São Paulo, Brasil"])
    timezone: str = Field("America/Sao_Paulo", examples=["America/Sao_Paulo"])
    house_system: str = Field("equal", examples=["equal"])


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
