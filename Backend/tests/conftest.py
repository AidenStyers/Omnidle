# This file contains the parts of pytest that should run before everything else

import pytest
import requests
from tenacity import retry, stop_after_attempt, wait_fixed

# Adds parent directory to python search paths so that db_management can be imported
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import db_management as db


@pytest.fixture(scope="session", autouse=True)
def ensure_api_is_ready():
    """
    This runs ONCE per test session.
    scope="session": Run only once, not for every test function.
    autouse=True: Every test automatically waits for this without being told.
    """
    url = "http://localhost:8000/health"
    
    print(f"\n⏳ Checking API health at {url}...")
    
    @retry(stop=stop_after_attempt(15), wait=wait_fixed(2))
    def check():
        response = requests.get(url)
        response.raise_for_status()
        return True

    try:
        check()
        print("✅ API is up and running!")

        # Reset / Initialize tables
        db.initialize()
        db.reset_tables()

    except Exception as e:
        pytest.exit(f"❌ API failed to become ready: {e}", returncode=1)