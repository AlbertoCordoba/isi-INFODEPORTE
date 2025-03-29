import requests
from datetime import datetime, timedelta
from config import API_KEYS, API_URLS
import pytz

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
# Zona horaria local
LOCAL_TIMEZONE = pytz.timezone("Europe/Madrid")

def convert_utc_to_local(utc_time_str):
    """Convierte una hora en formato UTC a la hora local"""
    try:
        utc_time = datetime.strptime(utc_time_str, "%Y-%m-%dT%H:%M:%S")
        utc_time = pytz.utc.localize(utc_time)
        local_time = utc_time.astimezone(LOCAL_TIMEZONE)
        return local_time.strftime("%Y-%m-%d %H:%M:%S")
    except Exception as e:
        print(f"Error al convertir la hora: {e}")
        return utc_time_str
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
                for match in daily_matches:
                    # Usar DateTimeUTC si está disponible
                    if "DateTimeUTC" in match:
                        match["DateTime"] = convert_utc_to_local(match["DateTimeUTC"])
                    elif "DateTime" in match:
                        match["DateTime"] = convert_utc_to_local(match["DateTime"])
                    matches.append(match)
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