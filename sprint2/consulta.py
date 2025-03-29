import sqlite3

# Conectar a la base de datos
conn = sqlite3.connect('sports.db')

# Crear un cursor
cursor = conn.cursor()

# Ejecutar una consulta
cursor.execute("SELECT * FROM leagues")

# Obtener los resultados
rows = cursor.fetchall()

# Imprimir los resultados
for row in rows:
    print(row)

# Cerrar la conexión
conn.close()