import sqlite3

# Conexión a la base de datos (se creará si no existe)
conn = sqlite3.connect('sports.db')
cursor = conn.cursor()

# Crear tabla sports
cursor.execute('''
CREATE TABLE IF NOT EXISTS sports (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL
)
''')

# Crear tabla leagues
cursor.execute('''
CREATE TABLE IF NOT EXISTS leagues (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    sport_id INTEGER NOT NULL,
    FOREIGN KEY (sport_id) REFERENCES sports (id)
)
''')

# Crear tabla fixtures
cursor.execute('''
CREATE TABLE IF NOT EXISTS fixtures (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    league_id INTEGER NOT NULL,
    home_team TEXT NOT NULL,
    away_team TEXT NOT NULL,
    date TEXT NOT NULL,
    FOREIGN KEY (league_id) REFERENCES leagues (id)
)
''')

# Crear tabla messages
cursor.execute('''
CREATE TABLE IF NOT EXISTS messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    chat_id TEXT NOT NULL,
    message TEXT NOT NULL,
    timestamp TEXT NOT NULL
)
''')

# Confirmar cambios y cerrar conexión
conn.commit()
conn.close()