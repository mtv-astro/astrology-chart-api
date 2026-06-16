from fastapi import FastAPI

from app.schemas import ChartRequest, ChartResponse
from app.services.chart import build_chart_response

app = FastAPI(
    title="Astrology Chart API",
    description="FastAPI service that calculates real astrological chart data from birth information using Flatlib.",
    version="1.0.0",
)


@app.get("/health")
def health_check() -> dict[str, bool | str]:
    return {"ok": True, "service": "astrology-chart-api"}


@app.post("/chart", response_model=ChartResponse)
def create_chart(payload: ChartRequest) -> ChartResponse:
    return build_chart_response(payload)
