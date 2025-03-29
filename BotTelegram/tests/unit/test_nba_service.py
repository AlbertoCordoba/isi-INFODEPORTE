import pytest
from datetime import datetime

def test_get_nba_standings(requests_mock):
    from services.nba_service import get_nba_standings
    test_data = [{
        "Name": "Lakers",
        "Conference": "Western",
        "Wins": 5
    }]
    current_year = datetime.now().year
    requests_mock.get(
        f"https://api.sportsdata.io/v3/nba/scores/json/Standings/{current_year}?key=5dcf048503af49c781f692fb2058a057",
        json=test_data
    )
    standings = get_nba_standings()
    assert standings[0]["Name"] == "Lakers"

def test_get_nba_injured_players(requests_mock):
    from services.nba_service import get_nba_injured_players
    test_data = [{"FirstName": "LeBron", "LastName": "James"}]
    requests_mock.get(
        "https://api.sportsdata.io/v3/nba/projections/json/InjuredPlayers?key=5dcf048503af49c781f692fb2058a057",
        json=test_data
    )
    injured = get_nba_injured_players()
    assert injured[0]["FirstName"] == "LeBron"

def test_empty_response(requests_mock):
    from services.nba_service import get_next_nba_games
    today = datetime.now().strftime("%Y-%m-%d")
    requests_mock.get(
        f"https://api.sportsdata.io/v3/nba/scores/json/GamesByDate/{today}?key=5dcf048503af49c781f692fb2058a057",
        json=[]
    )
    assert get_next_nba_games(days_ahead=1) == []