from starlette.testclient import TestClient
from core.controllers.auth import create_access_token


def test_create_auth(client: TestClient):
    response = client.post(
        "api/auth",
        json={"username": "test", "password": "123teste"},
    )

    assert response.status_code == 201
    content = response.json()
    assert content["username"] == "test"


def test_create(client: TestClient):
    token = create_access_token(
        data={"sub": "test", "scopes": ["default"]})
    response = client.post(
        "api/users",
        headers={"Authorization": f"bearer {token}"},
        json={
            "name": "Alexandre Fialho",
            "document": "390.430.138-11",
            "birth_date": "1995-10-05",
            "address": {
                "postal_code": "08412-070"
            }
        },
    )
    assert response.status_code == 201
    assert response.json() == {
        "name": "Alexandre Fialho",
        "document": "390.430.138-11",
        "birth_date": "1995-10-05",
        "id": 1,
        "address": {
            "city": "São Paulo",
            "postal_code": "08412-070",
            "street": "Rua Antônio Silvestre Ferreira",
            "neighborhoods": "Vila Cruzeiro",
            "state": "Sp",
            "id": 1,
        }
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
    token = create_access_token(
        data={"sub": "test", "scopes": ["default"]})
    response = client.post(
        "api/users",
        headers={"Authorization": f"bearer {token}"},
        json={
            "name": "Alexandre Fialho",
            "document": "390.430.138-11",
            "birth_date": "1995-10-05",
        },
    )
    assert response.status_code == 400
    assert response.json() == {"detail": "User already exists"}


def test_read(client: TestClient):
    token = create_access_token(
        data={"sub": "test", "scopes": ["default"]})
    response = client.get("api/users/1", headers={"Authorization": f"bearer {token}"})
    assert response.status_code == 200
    assert response.json() == {
        "id": 1,
        "name": "Alexandre Fialho",
        "document": "390.430.138-11",
        "birth_date": "1995-10-05",
        "address": {
            "postal_code": "08412-070",
            "street": "Rua Antônio Silvestre Ferreira",
            "neighborhoods": "Vila Cruzeiro",
            "city": "São Paulo",
            "state": "Sp",
            "id": 1
        }
    }


def test_read_bad_token(client: TestClient):
    response = client.get(
        "api/users/1", headers={"Authorization": "bearer dhasudlajkn"}
    )
    assert response.status_code == 401
    assert response.json() == {"detail": "Could not validate credentials"}


def test_read_inexistent(client: TestClient):
    token = create_access_token(
        data={"sub": "test", "scopes": ["default"]})
    response = client.get("api/users/2", headers={"Authorization": f"bearer {token}"})
    assert response.status_code == 404
    assert response.json() == {"detail": "User not found"}


def test_read_all(client: TestClient):
    token = create_access_token(
        data={"sub": "test", "scopes": ["default"]})
    response = client.get("api/users/", headers={"Authorization": f"bearer {token}"})
    assert response.status_code == 200
    assert response.json() == [
        {
            "id": 1,
            "name": "Alexandre Fialho",
            "document": "390.430.138-11",
            "birth_date": "1995-10-05",
            "address": {
                "postal_code": "08412-070",
                "street": "Rua Antônio Silvestre Ferreira",
                "neighborhoods": "Vila Cruzeiro",
                "city": "São Paulo",
                "state": "Sp",
                "id": 1
            }
        }
    ]


def test_read_all_bad_token(client: TestClient):
    response = client.get(
        "/api/users/", headers={"Authorization": "bearer jdlasjhfgsfkah"}
    )
    assert response.status_code == 401
    assert response.json() == {"detail": "Could not validate credentials"}


def test_put(client: TestClient):
    token = create_access_token(
        data={"sub": "test", "scopes": ["default"]})
    response = client.put(
        "api/users/1",
        headers={"Authorization": f"bearer {token}"},
        json={
            "name": "Alexandre Fialho de Araujo",
        },
    )
    assert response.status_code == 200
    assert response.json() == {
        "id": 1,
        "name": "Alexandre Fialho De Araujo",
        "document": "390.430.138-11",
        "birth_date": "1995-10-05",
        "address": {
            "id": 1,
            "postal_code": "08412-070",
            "street": "Rua Antônio Silvestre Ferreira",
            "neighborhoods": "Vila Cruzeiro",
            "city": "São Paulo",
            "state": "Sp"
        }
    }


def test_put_bad_token(client: TestClient):
    response = client.put(
        "api/users/1",
        headers={"Authorization": "bearer dasjhdkjfd"},
        json={
            "name": "Alexandre Fialho de Araujo",
        },
    )
    assert response.status_code == 401
    assert response.json() == {"detail": "Could not validate credentials"}


def test_put_inexistent(client: TestClient):
    token = create_access_token(
        data={"sub": "test", "scopes": ["default"]})
    response = client.put(
        "api/users/2",
        headers={"Authorization": f"bearer {token}"},
        json={
            "name": "Alexandre Fialho de Araujo",
        },
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "User not found"}


def test_delete(client: TestClient):
    token = create_access_token(
        data={"sub": "test", "scopes": ["default"]})
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
    token = create_access_token(
        data={"sub": "test", "scopes": ["default"]})
    response = client.delete(
        "api/users/32", headers={"Authorization": f"bearer {token}"}
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "User not found"}
