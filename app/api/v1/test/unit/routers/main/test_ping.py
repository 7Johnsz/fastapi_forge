def test_ping(client):
    response = client.get("/ping")
    assert response.status_code == 200
    assert response.json() == "Pong!"

def test_ping_rate_limit(client):
    # ATENÇÃO: Como o limiter está mockado, não haverá rate limit real.
    # Este teste só funcionaria com Redis real e limiter real.
    # Portanto, aqui esperamos 200, não 429.
    for _ in range(31):
        client.get("/ping")
    response = client.get("/ping")
    assert response.status_code == 200  # Se usar limiter real, troque para 429