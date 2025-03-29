import requests
from datetime import datetime, timedelta
from config import API_KEYS, API_URLS

BASE_URL = API_URLS["futbol"]
INJURIES_URL = "https://api.sportsdata.io/v4/soccer/projections/json/InjuredPlayers"

COMPETITIONS = {
    "Premier League": {"scores_key": "EPL", "injuries_key": "ENG"},
    "Bundesliga": {"scores_key": "DEB", "injuries_key": "GER"},
    "La Liga": {"scores_key": "ESP", "injuries_key": "ESP"},
    "Serie A": {"scores_key": "ITSA", "injuries_key": "ITA"},
    "Ligue 1": {"scores_key": "FRL1", "injuries_key": "FRA"},
    "Champions League": {"scores_key": "UCL", "injuries_key": "UCL"}
}

def get_competitions():
    """Devuelve el diccionario de competiciones disponibles"""
    return COMPETITIONS

def get_next_matches(competition_key):
    """Obtiene los próximos 5 partidos"""
    matches = []
    current_date = datetime.now()
    
    while len(matches) < 5:
        url = f"{BASE_URL}/ScoresBasicFinal/{competition_key}/{current_date.strftime('%Y-%m-%d')}?key={API_KEYS['futbol']}"
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                daily_matches = response.json()
                matches.extend(daily_matches)
        except requests.exceptions.RequestException:
            break
        
        current_date += timedelta(days=1)
        if (current_date - datetime.now()).days > 30:
            break
    
    return matches[:5]

def get_standings(competition_key):
    """Obtiene la clasificación"""
    current_year = datetime.now().year
    url = f"{BASE_URL}/Standings/{competition_key}/{current_year}?key={API_KEYS['futbol']}"
    
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            return response.json()
        return None
    except requests.exceptions.RequestException:
        return None

def get_injured_players(competition_key):
    """Obtiene jugadores lesionados"""
    url = f"{INJURIES_URL}/{competition_key}?key={API_KEYS['futbol']}"
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            return response.json()
        return None
    except requests.exceptions.RequestException:
        return None