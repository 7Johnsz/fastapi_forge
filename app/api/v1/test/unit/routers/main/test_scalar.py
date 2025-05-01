def test_scalar_with_valid_auth(client, valid_auth_headers):
    response = client.get("/scalar", headers=valid_auth_headers)
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]

def test_scalar_with_invalid_auth(client, invalid_auth_headers):
    response = client.get("/scalar", headers=invalid_auth_headers)
    assert response.status_code == 401
    data = response.json()["detail"]
    assert data["message"] == "You don't have permission to access this resource"
    assert data["status"] == "error"

def test_scalar_without_auth(client):
    response = client.get("/scalar")
    assert response.status_code == 401
    data = response.json()["detail"]
    assert data["message"] == "You don't have permission to access this resource"
    assert data["status"] == "error"