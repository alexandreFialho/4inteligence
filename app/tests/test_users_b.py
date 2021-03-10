def test_create(client):
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


def test_create_bad_token(client):
    response = client.post(
        "api/users",
        headers={"X-Token": "hailhydra"},
        json={"name": "Alexandre", "document": "123.456.789-10",
              "birth_date": "1995-10-05"},
    )
    assert response.status_code == 400
    assert response.json() == {"detail": "Invalid X-Token header"}


def test_create_existing(client):
    response = client.post(
        "api/users",
        headers={"X-Token": "coneofsilence"},
        json={"name": "Alexandre", "document": "123.456.789-10",
              "birth_date": "1995-10-05"},
    )
    assert response.status_code == 400
    assert response.json() == {"detail": "User already exists"}


def test_read(client):
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


def test_read_bad_token(client):
    response = client.get(
        "api/users/1",
        headers={"X-Token": "hailhydra"}
    )
    assert response.status_code == 400
    assert response.json() == {"detail": "Invalid X-Token header"}


def test_read_inexistent(client):
    response = client.get(
        "api/users/2", headers={"X-Token": "coneofsilence"})
    assert response.status_code == 404
    assert response.json() == {"detail": "User not found"}


def test_read_all(client):
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


def test_read_all_bad_token(client):
    response = client.get("/api/users/", headers={"X-Token": "hailhydra"})
    assert response.status_code == 400
    assert response.json() == {"detail": "Invalid X-Token header"}


def test_put(client):
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


def test_put_bad_token(client):
    response = client.put(
        "api/users/1", headers={"X-Token": "hailhydra"},
        json={"name": "Alexandre", "document": "321.456.789-10",
              "birth_date": "1995-10-05"})
    assert response.status_code == 400
    assert response.json() == {"detail": "Invalid X-Token header"}


def test_put_inexistent(client):
    response = client.put(
        "api/users/2", headers={"X-Token": "coneofsilence"},
        json={"name": "Alexandre", "document": "321.456.789-10",
              "birth_date": "1995-10-05"})
    assert response.status_code == 404
    assert response.json() == {"detail": "User not found"}


def test_delete(client):
    response = client.delete(
        "api/users/1", headers={"X-Token": "coneofsilence"}
    )
    assert response.status_code == 200
    assert response.json() == {"detail": "User deleted successfully"}


def test_delete_bad_token(client):
    response = client.delete(
        "api/users/1", headers={"X-Token": "hailhydra"}
    )
    assert response.status_code == 400
    assert response.json() == {"detail": "Invalid X-Token header"}


def test_delete_inexistent(client):
    response = client.delete(
        "api/users/32", headers={"X-Token": "coneofsilence"})
    assert response.status_code == 404
    assert response.json() == {"detail": "User not found"}
