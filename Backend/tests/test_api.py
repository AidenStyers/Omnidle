import requests

# Litterally just tests if the backend is up
def test_backend_health():
    # 'backend' is the service name in docker-compose.
    # Note: Use the internal port (e.g., 8000)
    url = "http://backend:8000/health" 
    
    response = requests.get(url)
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


# Checks if game-results returns anything
def test_game_results_returns():
    url = "http://backend:8000/game-results?guesses=3&table_name=buildings" 
    response = requests.post(url)

    assert response.status_code == 200
