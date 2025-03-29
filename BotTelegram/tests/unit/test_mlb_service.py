import pytest
from datetime import datetime

def test_get_mlb_standings(requests_mock):
    from services.mlb_service import get_mlb_standings
    test_data = [{
        "Name": "Yankees",
        "League": "AL",
        "Wins": 99
    }]
    current_year = datetime.now().year
    requests_mock.get(
        f"https://api.sportsdata.io/v3/mlb/scores/json/Standings/{current_year}?key=4ee1943370b7488e9ea1fccdd129bee4",
        json=test_data
    )
    standings = get_mlb_standings()
    assert standings[0]["Name"] == "Yankees"

def test_get_mlb_injured_players(requests_mock):
    from services.mlb_service import get_mlb_injured_players
    test_data = [{"FirstName": "Aaron", "LastName": "Judge"}]
    requests_mock.get(
        "https://api.sportsdata.io/v3/mlb/projections/json/InjuredPlayers?key=4ee1943370b7488e9ea1fccdd129bee4",
        json=test_data
    )
    injured = get_mlb_injured_players()
    assert injured[0]["FirstName"] == "Aaron"

def test_api_error_handling(requests_mock):
    from services.mlb_service import get_next_mlb_games
    today = datetime.now().strftime("%Y-%m-%d")
    requests_mock.get(
        f"https://api.sportsdata.io/v3/mlb/scores/json/GamesByDate/{today}?key=4ee1943370b7488e9ea1fccdd129bee4",
        status_code=500
    )
    assert get_next_mlb_games(days_ahead=1) == []