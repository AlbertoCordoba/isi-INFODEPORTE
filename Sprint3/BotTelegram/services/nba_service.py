import requests
from datetime import datetime, timedelta
from config import API_KEYS, API_URLS
import pytz

BASE_URL = API_URLS["nba"]
PROJECTIONS_URL = "https://api.sportsdata.io/v3/nba/projections/json"

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

def get_next_nba_games(days_ahead=5):
    """Obtiene los próximos partidos de la NBA"""
    games = []
    today = datetime.now().date()
    
    for day_offset in range(days_ahead):
        current_date = today + timedelta(days=day_offset)
        date_str = current_date.strftime("%Y-%m-%d")
        url = f"{BASE_URL}/GamesByDate/{date_str}?key={API_KEYS['nba']}"
        
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


def get_nba_injured_players():
    """Obtiene jugadores lesionados"""
    url = f"{PROJECTIONS_URL}/InjuredPlayers?key={API_KEYS['nba']}"
    
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            players = response.json()
            return [p for p in players if p is not None]
        return []
    except requests.exceptions.RequestException:
        return []