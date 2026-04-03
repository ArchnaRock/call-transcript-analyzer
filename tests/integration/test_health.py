from fastapi.testclient import TestClient


def test_health_check_returns_ok(test_client: TestClient) -> None:
    response = test_client.get("/health")
    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "ok"
    assert "db" in body


def test_health_check_db_status_when_no_db(test_client: TestClient) -> None:
    # With the in-memory SQLite override, db should respond
    response = test_client.get("/health")
    assert response.status_code == 200
    # Status is either "ok" or "unavailable" — never missing
    assert response.json()["db"] in ("ok", "unavailable")
