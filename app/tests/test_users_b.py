from starlette.testclient import TestClient


def test_create(client: TestClient):
    response = client.post(
        "api/users",
        headers={"Authorization": "bearer "},
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
        headers={"Authorization": "bearer bad_token"},
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
        "api/users",
        headers={"Authorization": "bearer "},
        json={
            "name": "Alexandre",
            "document": "123.456.789-10",
            "birth_date": "1995-10-05",
        },
    )
    assert response.status_code == 400
    assert response.json() == {"detail": "User already exists"}


def test_read(client: TestClient):
    response = client.get("api/users/1", headers={"Authorization": "bearer "})
    assert response.status_code == 200
    assert response.json() == {
        "id": 1,
        "name": "Alexandre",
        "document": "123.456.789-10",
        "birth_date": "1995-10-05",
    }


def test_read_bad_token(client: TestClient):
    response = client.get("api/users/1", headers={"Authorization": "bearer "})
    assert response.status_code == 401
    assert response.json() == {"detail": "Could not validate credentials"}


def test_read_inexistent(client: TestClient):
    response = client.get("api/users/2", headers={"Authorization": "bearer "})
    assert response.status_code == 404
    assert response.json() == {"detail": "User not found"}


def test_read_all(client: TestClient):
    response = client.get("api/users/", headers={"Authorization": "bearer "})
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
    response = client.get("/api/users/", headers={"Authorization": "bearer "})
    assert response.status_code == 401
    assert response.json() == {"detail": "Could not validate credentials"}


def test_put(client: TestClient):
    response = client.put(
        "api/users/1",
        headers={"Authorization": "bearer "},
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
        headers={"Authorization": "bearer "},
        json={
            "name": "Alexandre",
            "document": "321.456.789-10",
            "birth_date": "1995-10-05",
        },
    )
    assert response.status_code == 401
    assert response.json() == {"detail": "Could not validate credentials"}


def test_put_inexistent(client: TestClient):
    response = client.put(
        "api/users/2",
        headers={"Authorization": "bearer "},
        json={
            "name": "Alexandre",
            "document": "321.456.789-10",
            "birth_date": "1995-10-05",
        },
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "User not found"}


def test_delete(client: TestClient):
    response = client.delete("api/users/1", headers={"Authorization": "bearer "})
    assert response.status_code == 200
    assert response.json() == {"detail": "User deleted successfully"}


def test_delete_bad_token(client: TestClient):
    response = client.delete("api/users/1", headers={"Authorization": "bearer "})
    assert response.status_code == 401
    assert response.json() == {"detail": "Could not validate credentials"}


def test_delete_inexistent(client: TestClient):
    response = client.delete("api/users/32", headers={"Authorization": "bearer "})
    assert response.status_code == 404
    assert response.json() == {"detail": "User not found"}
