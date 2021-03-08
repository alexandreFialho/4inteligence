from fastapi.testclient import TestClient

from api.main import app

client = TestClient(app=app)


def test_create():
    response = client.post(
        "api/users",
        headers={"X-Token": "coneofsilence"},
        json={"name": "Alexandre", "document": "123.456.789-10",
              "birth_date": "1995-10-05"},
    )
    assert response.status_code == 201
    assert response.json() == {
        "id": 1,
        "name": "Alexandre",
        "document": "123.456.789-10",
        "birth_date": "1995-10-05"
    }


def test_create_bad_token():
    response = client.post(
        "api/users",
        headers={"X-Token": "hailhydra"},
        json={"name": "Alexandre", "document": "123.456.789-10",
              "birth_date": "1995-10-05"},
    )
    assert response.status_code == 400
    assert response.json() == {"detail": "Invalid X-Token header"}


def test_create_existing():
    response = client.post(
        "api/users",
        headers={"X-Token": "coneofsilence"},
        json={"name": "Alexandre", "document": "123.456.789-10",
              "birth_date": "1995-10-05"},
    )
    assert response.status_code == 400
    assert response.json() == {"detail": "User already exists"}


def test_read():
    response = client.get(
        "api/users/1",
        headers={"X-Token": "coneofsilence"}
    )
    assert response.status_code == 200
    assert response.json() == {
        "id": 1,
        "name": "Alexandre",
        "document": "123.456.789-10",
        "birth_date": "1995-10-05"
    }


def test_read_bad_token():
    response = client.get(
        "api/users/0",
        headers={"X-Token": "hailhydra"}
    )
    assert response.status_code == 400
    assert response.json() == {"detail": "Invalid X-Token header"}


def test_read_inexistent():
    response = client.get(
        "api/users/2", headers={"X-Token": "coneofsilence"})
    assert response.status_code == 404
    assert response.json() == {"detail": "User not found"}


def test_read_all():
    response = client.get(
        "api/users/", headers={"X-Token": "coneofsilence"})
    assert response.status_code == 200
    assert response.json() == [
        {
            "id": 1,
            "name": "Alexandre",
            "document": "123.456.789-10",
            "birth_date": "1995-10-05"
        }
    ]


def test_read_all_bad_token():
    response = client.get("/api/users/", headers={"X-Token": "hailhydra"})
    assert response.status_code == 400
    assert response.json() == {"detail": "Invalid X-Token header"}


def test_put():
    response = client.put(
        "api/users/1", headers={"X-Token": "coneofsilence"},
        json={"name": "Alexandre", "document": "321.456.789-10",
              "birth_date": "1995-10-05"}
    )
    assert response.status_code == 200
    assert response.json() == {
        "id": 1,
        "name": "Alexandre",
        "document": "321.456.789-10",
        "birth_date": "1995-10-05"
    }


def test_put_bad_token():
    response = client.put(
        "api/users/1", headers={"X-Token": "hailhydra"},
        json={"name": "Alexandre", "document": "321.456.789-10",
              "birth_date": "1995-10-05"})
    assert response.status_code == 400
    assert response.json() == {"detail": "Invalid X-Token header"}


def test_put_inexistent():
    response = client.put(
        "api/users/2", headers={"X-Token": "coneofsilence"},
        json={"name": "Alexandre", "document": "321.456.789-10",
              "birth_date": "1995-10-05"})
    assert response.status_code == 404
    assert response.json() == {"detail": "User not found"}


def test_delete():
    response = client.delete(
        "api/users/1", headers={"X-Token": "coneofsilence"}
    )
    assert response.status_code == 200
    assert response.json() == {"detail": "User deleted successfully"}


def test_delete_bad_token():
    response = client.delete(
        "api/users/1", headers={"X-Token": "hailhydra"}
    )
    assert response.status_code == 400
    assert response.json() == {"detail": "Invalid X-Token header"}


def test_delete_inexistent():
    response = client.delete(
        "api/users/2", headers={"X-Token": "coneofsilence"})
    assert response.status_code == 404
    assert response.json() == {"detail": "User not found"}
