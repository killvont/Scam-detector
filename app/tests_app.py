import sys
import os
from pathlib import Path

# Add the parent directory to sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from scam_detector.app import app  # Adjusted import path for the app

def test_ping():
    with app.test_client() as client:
        response = client.get('/ping')
        assert response.status_code == 200
        assert response.json == {"message": "pong"}
