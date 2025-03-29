import requests

API_URL = "https://v3.football.api-sports.io/fixtures"
API_KEY = "626a3c09150fe6934717af1b97e58b2f"

headers = {
    "X-RapidAPI-Key": API_KEY,
    "X-RapidAPI-Host": "api-football-v1.p.rapidapi.com"
}

response = requests.get(API_URL, headers=headers)
if response.status_code == 200:
    print("Conexión exitosa a la API de deportes")
    print(response.json())
else:
    print("Error en la conexión a la API")