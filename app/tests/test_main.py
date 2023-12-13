from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_read_root():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"msg": "ok"}

def test_read_item():
    q = 'hoge'
    item_id = 1
    response = client.get(
        f"/items/{item_id}",
        params={"q": q},
    )
    assert response.status_code == 200
    assert response.json() == {"item_id": item_id, 'q': q } 