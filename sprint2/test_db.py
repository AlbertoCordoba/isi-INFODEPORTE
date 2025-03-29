import sqlite3
from datetime import datetime

# Conexión a la base de datos
conn = sqlite3.connect('sports.db')
cursor = conn.cursor()

# Añadir datos a la tabla sports
cursor.execute('''
INSERT INTO sports (name)
VALUES (?)
''', ('Fútbol',))

# Añadir datos a la tabla leagues
cursor.execute('''
INSERT INTO leagues (name, sport_id)
VALUES (?, ?)
''', ('Primera División', 1))

# Añadir datos a la tabla fixtures
cursor.execute('''
INSERT INTO fixtures (league_id, home_team, away_team, date)
VALUES (?, ?, ?, ?)
''', (1, 'Metropolitanos FC', 'Zamora FC', '2025-03-09T23:00:00+00:00'))

# Añadir datos a la tabla messages
cursor.execute('''
INSERT INTO messages (chat_id, message, timestamp)
VALUES (?, ?, ?)
''', ('5761127653', 'Hola, este es un mensaje de prueba desde la API de Telegram.', datetime.utcnow().isoformat()))

# Modificar datos en la tabla fixtures
cursor.execute('''
UPDATE fixtures
SET home_team = ?
WHERE id = ?
''', ('Caracas FC', 1))

# Eliminar datos de la tabla messages
cursor.execute('''
DELETE FROM messages
WHERE id = ?
''', (1,))

# Confirmar cambios y cerrar conexión
conn.commit()
conn.close()