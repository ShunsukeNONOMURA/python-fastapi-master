from fastapi.testclient import TestClient

from main import app

client = TestClient(app)

def test_get_user():
    user_id = "admin"
    response = client.get(
        f"/users/{user_id}",
    )
    assert response.status_code == 200
    assert response.json()["user_id"] == user_id

def test_query_user():
    q = "hoge"
    response = client.get(
        "/query/users",
        params={"q": q},
    )
    assert response.status_code == 200
    # assert response.json() == {'q': q }

def test_create_user():
    user = {
        "user_id": "test",
        "user_name": "test",
        "user_password": "test",
        "user_role_code": "99",
    }
    response = client.post(
        "/users",
        params={"user": user},
    )
    assert response.status_code == 200

    user_id = user["user_id"]
    response = client.get(
        f"/users/{user_id}",
    )
    assert response.status_code == 200
    assert response.json()["user_id"] == user_id
