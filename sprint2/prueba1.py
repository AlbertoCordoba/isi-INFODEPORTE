import requests
from datetime import datetime, timedelta

API_URL = "https://v3.football.api-sports.io/fixtures"
API_KEY = "626a3c09150fe6934717af1b97e58b2f"

# Calcula la fecha de mañana
tomorrow_date = (datetime.utcnow() + timedelta(days=1)).strftime('%Y-%m-%d')

headers = {
    "x-apisports-key": API_KEY,
    "x-rapidapi-host": "v3.football.api-sports.io"
}

# Incluye el parámetro de fecha
params = {
    "date": tomorrow_date
}

response = requests.get(API_URL, headers=headers, params=params)

if response.status_code == 200:
    print("Conexión exitosa a la API de deportes")
    fixtures = response.json().get('response', [])
    for fixture in fixtures:
        league = fixture['league']['name']
        home_team = fixture['teams']['home']['name']
        away_team = fixture['teams']['away']['name']
        date = fixture['fixture']['date']
        venue = fixture['fixture']['venue']['name']
        print(f"🏆 {league}")
        print(f"⚽ {home_team} vs {away_team}")
        print(f"📅 Fecha: {date.split('T')[0]}")
        print(f"🏟️ Estadio: {venue}")
        print(f"⏰ Hora: {date.split('T')[1].split('+')[0]} (Hora Local)")
else:
    print("Error en la conexión a la API")