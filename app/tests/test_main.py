from fastapi.testclient import TestClient

from main import app

client = TestClient(app)

def test_get_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"msg": "ok"}

def test_get_user():
    user_id = 'admin'
    response = client.get(
        f"/user/{user_id}"
    )
    assert response.status_code == 200
    assert response.json()["user_id"] == user_id

def test_query_user():
    q = 'hoge'
    response = client.get(
        f"/query/user",
        params={"q": q},
    )
    assert response.status_code == 200
    assert response.json() == {'q': q } 