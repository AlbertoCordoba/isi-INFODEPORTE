import os

# Configuración común
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "8054312169:AAHDKStq52M_4h7DPmUlIclfsJHVxWs3Azg")

# Keys para las APIs deportivas
API_KEYS = {
    "futbol": "223bdfa7c34a47efb23a55f880ec8a8f",
    "mlb": "4ee1943370b7488e9ea1fccdd129bee4",
    "nba": "5dcf048503af49c781f692fb2058a057",
    "nhl": "7f046cd5ec974fa7a0baa6b332bb232d"
}

# URLs base de las APIs
API_URLS = {
    "futbol": "https://api.sportsdata.io/v4/soccer/scores/json",
    "mlb": "https://api.sportsdata.io/v3/mlb/scores/json",
    "nba": "https://api.sportsdata.io/v3/nba/scores/json",
    "nhl": "https://api.sportsdata.io/v3/nhl/scores/json"
}