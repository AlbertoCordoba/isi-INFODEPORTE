import requests
from datetime import datetime, timedelta
from config import API_KEYS, API_URLS
import pytz

BASE_URL = API_URLS["mlb"]
PROJECTIONS_URL = "https://api.sportsdata.io/v3/mlb/projections/json"

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
                for game in daily_games:
                    if "DateTimeUTC" in game:
                        game["DateTime"] = convert_utc_to_local(game["DateTimeUTC"])
                games.extend(daily_games)
                if len(games) >= 5:
                    break
        except requests.exceptions.RequestException as e:
            print(f"Error al obtener datos de la API: {e}")
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