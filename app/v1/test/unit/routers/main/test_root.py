def test_root_with_valid_auth(client, valid_auth_headers):
    response = client.get("/", headers=valid_auth_headers)
    assert response.status_code == 200
    assert response.json() == "Hello World!"

def test_root_with_invalid_auth(client, invalid_auth_headers):
    response = client.get("/", headers=invalid_auth_headers)
    assert response.status_code == 401
    data = response.json()["detail"]
    assert data["message"] == "You don't have permission to access this resource"
    assert data["status"] == "error"

def test_root_without_auth(client):
    response = client.get("/")
    assert response.status_code == 401
    data = response.json()["detail"]
    assert data["message"] == "You don't have permission to access this resource"
    assert data["status"] == "error"