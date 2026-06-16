from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_chart_response_shape():
    response = client.post(
        "/chart",
        json={
            "name": "Joana",
            "birth_date": "1990-08-15",
            "birth_time": "14:35",
            "birth_city": "São Paulo, Brasil",
            "timezone": "America/Sao_Paulo",
            "house_system": "equal",
        },
    )

    assert response.status_code == 200
    payload = response.json()

    assert payload["name"] == "Joana"
    assert payload["engine"] == "flatlib-swiss-ephemeris"
    assert payload["sun"]
    assert payload["moon"]
    assert payload["ascendant"]
    assert len(payload["houses"]) == 12
    assert "sun" in payload["planets"]
