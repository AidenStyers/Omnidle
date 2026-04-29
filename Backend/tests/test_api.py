import pytest
import requests
from tenacity import retry, stop_after_attempt, wait_fixed

# This decorator tells the test to try 10 times, 
# waiting 2 seconds between each, before finally giving up.
@retry(stop=stop_after_attempt(10), wait=wait_fixed(2))
def wait_for_api():
    response = requests.get("http://backend:8000/health")
    response.raise_for_status()
    return response


def test_backend_health():
    # 'backend' is the service name in docker-compose.
    # Note: Use the internal port (e.g., 8000)
    url = "http://backend:8000/health" 
    
    # 1. Wait for the server to be 'Live'
    wait_for_api()
    
    # 2. Perform actual assertions
    response = requests.get(url)
    assert response.status_code == 200
    assert response.json()["status"] == "ok"