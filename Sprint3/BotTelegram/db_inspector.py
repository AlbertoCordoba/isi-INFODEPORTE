import sqlite3
from tabulate import tabulate
from datetime import datetime

def print_db_status(db_path='sports_bot.db'):
    """Muestra un reporte completo de la base de datos"""
    conn = None
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        print("\n" + "="*60)
        print("🔍 INSPECCIÓN COMPLETA DE LA BASE DE DATOS".center(60))
        print("="*60)
        print(f"📅 Fecha de verificación: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"📌 Ubicación: {db_path}")

        # 1. Verificar tablas existentes
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        print("\n📊 TABLAS DISPONIBLES:")
        print(tabulate(tables, headers=['Tabla'], tablefmt='fancy_grid'))

        # 2. Estadísticas generales
        print("\n📈 ESTADÍSTICAS GLOBALES:")
        
        cursor.execute("SELECT COUNT(*) FROM users")
        total_users = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM subscriptions")
        total_subs = cursor.fetchone()[0]
        
        print(f"• 👥 Usuarios registrados: {total_users}")
        print(f"• 🔔 Suscripciones totales: {total_subs}")

        # 3. Detalle por tablas
        for table in [t[0] for t in tables]:
            print(f"\n🔎 CONTENIDO DE '{table.upper()}':")
            
            # Obtener columnas
            cursor.execute(f"PRAGMA table_info({table})")
            columns = [col[1] for col in cursor.fetchall()]
            
            # Obtener datos (limitado a 10 registros para no saturar)
            cursor.execute(f"SELECT * FROM {table} LIMIT 10")
            data = cursor.fetchall()
            
            if data:
                print(tabulate(data, headers=columns, tablefmt='fancy_grid'))
                if len(data) == 10:
                    cursor.execute(f"SELECT COUNT(*) FROM {table}")
                    total = cursor.fetchone()[0]
                    print(f"\nMostrando 10 de {total} registros. Usa DB Browser para ver el resto.")
            else:
                print("~ Tabla vacía ~")

        # 4. Suscripciones por deporte
        print("\n🏆 SUSCRIPCIONES POR DEPORTE:")
        cursor.execute('''
            SELECT sport, COUNT(*) as total 
            FROM subscriptions 
            GROUP BY sport 
            ORDER BY total DESC
        ''')
        print(tabulate(cursor.fetchall(), headers=['Deporte', 'Suscripciones'], tablefmt='fancy_grid'))

        # 5. Últimos usuarios registrados
        print("\n🆕 ÚLTIMOS USUARIOS REGISTRADOS:")
        cursor.execute('''
            SELECT chat_id, username, first_name, last_name, register_date 
            FROM users 
            ORDER BY register_date DESC 
            LIMIT 5
        ''')
        print(tabulate(cursor.fetchall(), 
                      headers=['ID', 'Username', 'Nombre', 'Apellido', 'Fecha Registro'], 
                      tablefmt='fancy_grid'))

    except sqlite3.Error as e:
        print(f"\n❌ ERROR DE SQLITE: {str(e)}")
    except Exception as e:
        print(f"\n❌ ERROR INESPERADO: {str(e)}")
    finally:
        if conn:
            conn.close()
        print("\n" + "="*60)
        print("🔍 Inspección completada".center(60))
        print("="*60)

if __name__ == '__main__':
    print_db_status()