import json

from starlette.testclient import TestClient


def test_create_auth(client: TestClient):
    response = client.post(
        "api/auth",
        json={"username": "test", "password": "123teste"},
    )

    assert response.status_code == 201
    content = response.json()
    assert content["username"] == "test"


def test_create(client: TestClient):
    response = client.post(
        "token",
        data={"username": "test", "password": "123teste"},
    )
    token = json.loads(response.content).get("access_token")
    response = client.post(
        "api/users",
        headers={"Authorization": f"bearer {token}"},
        json={
            "name": "Alexandre",
            "document": "123.456.789-10",
            "birth_date": "1995-10-05",
        },
    )
    assert response.status_code == 201
    assert response.json() == {
        "id": 1,
        "name": "Alexandre",
        "document": "123.456.789-10",
        "birth_date": "1995-10-05",
    }


def test_create_bad_token(client: TestClient):
    response = client.post(
        "api/users",
        headers={"Authorization": "bearer jdsailfiuhksaf"},
        json={
            "name": "Alexandre",
            "document": "123.456.789-10",
            "birth_date": "1995-10-05",
        },
    )
    assert response.status_code == 401
    assert response.json() == {"detail": "Could not validate credentials"}


def test_create_existing(client: TestClient):
    response = client.post(
        "token",
        data={"username": "test", "password": "123teste"},
    )
    token = json.loads(response.content).get("access_token")
    response = client.post(
        "api/users",
        headers={"Authorization": f"bearer {token}"},
        json={
            "name": "Alexandre",
            "document": "123.456.789-10",
            "birth_date": "1995-10-05",
        },
    )
    assert response.status_code == 400
    assert response.json() == {"detail": "User already exists"}


def test_read(client: TestClient):
    response = client.post(
        "token",
        data={"username": "test", "password": "123teste"},
    )
    token = json.loads(response.content).get("access_token")
    response = client.get("api/users/1", headers={"Authorization": f"bearer {token}"})
    assert response.status_code == 200
    assert response.json() == {
        "id": 1,
        "name": "Alexandre",
        "document": "123.456.789-10",
        "birth_date": "1995-10-05",
    }


def test_read_bad_token(client: TestClient):
    response = client.get(
        "api/users/1", headers={"Authorization": "bearer dhasudlajkn"}
    )
    assert response.status_code == 401
    assert response.json() == {"detail": "Could not validate credentials"}


def test_read_inexistent(client: TestClient):
    response = client.post(
        "token",
        data={"username": "test", "password": "123teste"},
    )
    token = json.loads(response.content).get("access_token")
    response = client.get("api/users/2", headers={"Authorization": f"bearer {token}"})
    assert response.status_code == 404
    assert response.json() == {"detail": "User not found"}


def test_read_all(client: TestClient):
    response = client.post(
        "token",
        data={"username": "test", "password": "123teste"},
    )
    token = json.loads(response.content).get("access_token")
    response = client.get("api/users/", headers={"Authorization": f"bearer {token}"})
    assert response.status_code == 200
    assert response.json() == [
        {
            "id": 1,
            "name": "Alexandre",
            "document": "123.456.789-10",
            "birth_date": "1995-10-05",
        }
    ]


def test_read_all_bad_token(client: TestClient):
    response = client.get(
        "/api/users/", headers={"Authorization": "bearer jdlasjhfgsfkah"}
    )
    assert response.status_code == 401
    assert response.json() == {"detail": "Could not validate credentials"}


def test_put(client: TestClient):
    response = client.post(
        "token",
        data={"username": "test", "password": "123teste"},
    )
    token = json.loads(response.content).get("access_token")
    response = client.put(
        "api/users/1",
        headers={"Authorization": f"bearer {token}"},
        json={
            "name": "Alexandre",
            "document": "321.456.789-10",
            "birth_date": "1995-10-05",
        },
    )
    assert response.status_code == 200
    assert response.json() == {
        "id": 1,
        "name": "Alexandre",
        "document": "321.456.789-10",
        "birth_date": "1995-10-05",
    }


def test_put_bad_token(client: TestClient):
    response = client.put(
        "api/users/1",
        headers={"Authorization": "bearer dasjhdkjfd"},
        json={
            "name": "Alexandre",
            "document": "321.456.789-10",
            "birth_date": "1995-10-05",
        },
    )
    assert response.status_code == 401
    assert response.json() == {"detail": "Could not validate credentials"}


def test_put_inexistent(client: TestClient):
    response = client.post(
        "token",
        data={"username": "test", "password": "123teste"},
    )
    token = json.loads(response.content).get("access_token")
    response = client.put(
        "api/users/2",
        headers={"Authorization": f"bearer {token}"},
        json={
            "name": "Alexandre",
            "document": "321.456.789-10",
            "birth_date": "1995-10-05",
        },
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "User not found"}


def test_delete(client: TestClient):
    response = client.post(
        "token",
        data={"username": "test", "password": "123teste"},
    )
    token = json.loads(response.content).get("access_token")
    response = client.delete(
        "api/users/1", headers={"Authorization": f"bearer {token}"}
    )
    assert response.status_code == 204


def test_delete_bad_token(client: TestClient):
    response = client.delete(
        "api/users/1", headers={"Authorization": "bearer hfhajlfdjslhf"}
    )
    assert response.status_code == 401
    assert response.json() == {"detail": "Could not validate credentials"}


def test_delete_inexistent(client: TestClient):
    response = client.post(
        "token",
        data={"username": "test", "password": "123teste"},
    )
    token = json.loads(response.content).get("access_token")
    response = client.delete(
        "api/users/32", headers={"Authorization": f"bearer {token}"}
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "User not found"}
