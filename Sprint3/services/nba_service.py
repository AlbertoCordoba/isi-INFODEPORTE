import requests
from datetime import datetime, timedelta  # Importación corregida
from config import API_KEYS, API_URLS

BASE_URL = API_URLS["nba"]
PROJECTIONS_URL = "https://api.sportsdata.io/v3/nba/projections/json"

def get_nba_standings():
    """Obtiene la clasificación de la NBA"""
    current_year = datetime.now().year
    url = f"{BASE_URL}/Standings/{current_year}?key={API_KEYS['nba']}"
    
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            return response.json()
        return None
    except requests.exceptions.RequestException:
        return None

def get_next_nba_games(days_ahead=5):
    """Obtiene los próximos partidos de la NBA"""
    games = []
    today = datetime.now().date()
    
    for day_offset in range(days_ahead):
        current_date = today + timedelta(days=day_offset)  # Ahora timedelta está definido
        date_str = current_date.strftime("%Y-%m-%d")
        url = f"{BASE_URL}/GamesByDate/{date_str}?key={API_KEYS['nba']}"
        
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

def get_nba_injured_players():
    """Obtiene jugadores lesionados con manejo de errores mejorado"""
    url = f"{PROJECTIONS_URL}/InjuredPlayers?key={API_KEYS['nba']}"
    
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            # Filtramos posibles valores nulos
            players = response.json()
            return [p for p in players if p is not None]
        return []
    except requests.exceptions.RequestException:
        return []