import requests
from datetime import datetime, timedelta
from config import API_KEYS, API_URLS

BASE_URL = API_URLS["mlb"]
PROJECTIONS_URL = "https://api.sportsdata.io/v3/mlb/projections/json"

def get_mlb_standings(season=datetime.now().year):
    """Obtiene la clasificación de la MLB"""
    url = f"{BASE_URL}/Standings/{season}?key={API_KEYS['mlb']}"
    
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            return response.json()
        return None
    except requests.exceptions.RequestException:
        return None

def get_next_mlb_games(days_ahead=7):
    """Obtiene los próximos 5 partidos de la MLB"""
    games = []
    today = datetime.now().date()
    
    for day_offset in range(days_ahead):
        current_date = today + timedelta(days=day_offset)
        url = f"{BASE_URL}/GamesByDate/{current_date.strftime('%Y-%m-%d')}?key={API_KEYS['mlb']}"
        
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                daily_games = response.json()
                games.extend(daily_games)
                if len(games) >= 5:
                    break
        except requests.exceptions.RequestException:
            continue
    
    return games[:5]

def get_mlb_injured_players():
    """Obtiene jugadores lesionados"""
    url = f"{PROJECTIONS_URL}/InjuredPlayers?key={API_KEYS['mlb']}"
    
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            return response.json()
        return None
    except requests.exceptions.RequestException:
        return None