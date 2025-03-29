import pytest
import requests_mock
import requests
from unittest.mock import patch
from datetime import datetime

def test_get_standings(requests_mock):
    from services.futbol_service import get_standings
    test_data = [{
        "Standings": [{"Name": "Barcelona", "Points": 10}]
    }]
    current_year = datetime.now().year
    requests_mock.get(
        f"https://api.sportsdata.io/v4/soccer/scores/json/Standings/ESP/{current_year}?key=223bdfa7c34a47efb23a55f880ec8a8f",
        json=test_data
    )
    standings = get_standings("ESP")
    assert standings[0]["Standings"][0]["Name"] == "Barcelona"

def test_get_injured_players(requests_mock):
    from services.futbol_service import get_injured_players
    test_data = [{"CommonName": "Messi", "InjuryStartDate": "2023-10-01"}]
    requests_mock.get(
        "https://api.sportsdata.io/v4/soccer/projections/json/InjuredPlayers/ESP?key=223bdfa7c34a47efb23a55f880ec8a8f",
        json=test_data
    )
    injured = get_injured_players("ESP")
    assert injured[0]["CommonName"] == "Messi"

def test_api_timeout(requests_mock):
    from services.futbol_service import get_next_matches
    today = datetime.now().strftime("%Y-%m-%d")
    requests_mock.get(
        f"https://api.sportsdata.io/v4/soccer/scores/json/ScoresBasicFinal/ESP/{today}?key=223bdfa7c34a47efb23a55f880ec8a8f",
        exc=requests.exceptions.Timeout
    )
    assert get_next_matches("ESP") == []