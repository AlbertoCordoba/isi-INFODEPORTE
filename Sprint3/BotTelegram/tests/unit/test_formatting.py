# tests/unit/test_formatting.py
import pytest
from unittest.mock import MagicMock
import sys

# Truco: Simula el módulo 'bot' sin importar realmente notifications
sys.modules['notifications'] = MagicMock()
from bot import format_date, format_nba_games  # Ahora esto funcionará

def test_format_date():
    date, time = format_date("2023-10-25 14:30:00")
    assert date == "25/10/2023"
    assert time == "14:30"

def test_format_nba_games():
    mock_games = [{"DateTime": "2023-10-25 14:30:00", "HomeTeam": "Lakers"}]
    formatted = format_nba_games(mock_games)
    assert "Lakers" in formatted