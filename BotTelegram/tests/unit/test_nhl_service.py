import pytest
from datetime import datetime

def test_get_nhl_standings(requests_mock):
    from services.nhl_service import get_nhl_standings
    test_data = [{
        "Name": "Maple Leafs",
        "Conference": "Eastern",
        "Wins": 7
    }]
    current_year = datetime.now().year
    requests_mock.get(
        f"https://api.sportsdata.io/v3/nhl/scores/json/Standings/{current_year}?key=7f046cd5ec974fa7a0baa6b332bb232d",
        json=test_data
    )
    standings = get_nhl_standings()
    assert standings[0]["Name"] == "Maple Leafs"

def test_get_player_stats(requests_mock):
    from services.nhl_service import get_player_stats
    test_data = {"PlayerID": 8478483, "Name": "Auston Matthews"}
    requests_mock.get(
        "https://api.sportsdata.io/v3/nhl/scores/json/Player/8478483?key=7f046cd5ec974fa7a0baa6b332bb232d",
        json=test_data
    )
    player = get_player_stats(8478483)
    assert player["Name"] == "Auston Matthews"

def test_timezone_conversion_edge_cases():
    from services.nhl_service import convert_utc_to_local
    # Test horario de invierno (CET)
    assert convert_utc_to_local("2023-01-25T14:30:00") == "2023-01-25 15:30:00"
    # Test horario de verano (CEST)
    assert convert_utc_to_local("2023-06-25T14:30:00") == "2023-06-25 16:30:00"