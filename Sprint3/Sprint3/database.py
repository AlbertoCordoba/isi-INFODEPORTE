import sqlite3
from datetime import datetime

class Database:
    def __init__(self, db_path='sports_bot.db'):
        """Inicializa la conexión a la base de datos y crea las tablas"""
        self.db_path = db_path
        self.connection = None
        self.cursor = None
        self._initialize_db()

    def _initialize_db(self):
        """Conexión segura a la base de datos con manejo de errores"""
        try:
            self.connection = sqlite3.connect(self.db_path, check_same_thread=False)
            self.cursor = self.connection.cursor()
            self._create_tables()
            print(f"✅ Base de datos inicializada en {self.db_path}")
        except Exception as e:
            print(f"❌ Error al inicializar DB: {e}")
            raise

    def _create_tables(self):
        """Crea las tablas necesarias con estructura mejorada"""
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                chat_id INTEGER PRIMARY KEY,
                username TEXT,
                first_name TEXT,
                last_name TEXT,
                register_date TEXT DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS subscriptions (
                chat_id INTEGER,
                sport TEXT,
                FOREIGN KEY (chat_id) REFERENCES users (chat_id),
                PRIMARY KEY (chat_id, sport)
            )
        ''')
        self.connection.commit()

    def get_connection(self):
        """Devuelve una conexión activa, reconectando si es necesario"""
        if self.connection is None:
            self._initialize_db()
        return self.connection

    # ================== OPERACIONES DE USUARIO ==================
    def add_user(self, chat_id, username, first_name, last_name):
        """Registra un nuevo usuario o actualiza uno existente"""
        try:
            self.cursor.execute('''
                INSERT OR REPLACE INTO users 
                (chat_id, username, first_name, last_name) 
                VALUES (?, ?, ?, ?)
            ''', (chat_id, username, first_name, last_name))
            self.connection.commit()
            print(f"👤 Usuario {chat_id} registrado/actualizado")
        except Exception as e:
            print(f"❌ Error al añadir usuario: {e}")
            raise

    # ================== OPERACIONES DE SUSCRIPCIÓN ==================
    def subscribe_user(self, chat_id, sport):
        """Agrega una suscripción con verificación de usuario"""
        try:
            # Verifica que el usuario exista
            self.cursor.execute('SELECT 1 FROM users WHERE chat_id = ?', (chat_id,))
            if not self.cursor.fetchone():
                raise ValueError(f"Usuario {chat_id} no registrado")
                
            self.cursor.execute('''
                INSERT OR IGNORE INTO subscriptions (chat_id, sport)
                VALUES (?, ?)
            ''', (chat_id, sport))
            self.connection.commit()
            print(f"🔔 Suscrito: {chat_id} a {sport}")
        except Exception as e:
            print(f"❌ Error al suscribir: {e}")
            raise

    def unsubscribe_user(self, chat_id, sport):
        """Elimina una suscripción específica"""
        try:
            self.cursor.execute('''
                DELETE FROM subscriptions 
                WHERE chat_id = ? AND sport = ?
            ''', (chat_id, sport))
            self.connection.commit()
            print(f"🔕 Desuscrito: {chat_id} de {sport}")
        except Exception as e:
            print(f"❌ Error al desuscribir: {e}")
            raise

    def get_user_subscriptions(self, chat_id):
        """Obtiene todas las suscripciones de un usuario"""
        try:
            self.cursor.execute('''
                SELECT sport FROM subscriptions 
                WHERE chat_id = ?
                ORDER BY sport
            ''', (chat_id,))
            return [row[0] for row in self.cursor.fetchall()]
        except Exception as e:
            print(f"❌ Error obteniendo suscripciones: {e}")
            return []

    def is_user_subscribed(self, chat_id, sport):
        """Verifica si un usuario está suscrito a un deporte específico"""
        try:
            self.cursor.execute('''
                SELECT 1 FROM subscriptions 
                WHERE chat_id = ? AND sport = ?
            ''', (chat_id, sport))
            return self.cursor.fetchone() is not None
        except Exception as e:
            print(f"❌ Error verificando suscripción: {e}")
            return False

    # ================== FUNCIONES PARA NOTIFICACIONES ==================
    def get_all_subscriptions(self):
        """Obtiene todas las suscripciones activas (para notificaciones)"""
        try:
            self.cursor.execute('''
                SELECT u.chat_id, u.first_name, s.sport 
                FROM subscriptions s
                JOIN users u ON s.chat_id = u.chat_id
            ''')
            return self.cursor.fetchall()
        except Exception as e:
            print(f"❌ Error obteniendo todas las suscripciones: {e}")
            return []

    # ================== MÉTODOS DE MANTENIMIENTO ==================
    def close(self):
        """Cierra la conexión de manera segura"""
        if self.connection:
            self.connection.close()
            print("🔌 Conexión a DB cerrada")
            
    def __del__(self):
        """Destructor que asegura el cierre de la conexión"""
        self.close()

    def backup_database(self):
        """Crea una copia de seguridad de la base de datos"""
        import shutil
        backup_file = f"{self.db_path}.backup_{datetime.now().strftime('%Y%m%d_%H%M')}"
        shutil.copy2(self.db_path, backup_file)
        print(f"💾 Copia de seguridad creada: {backup_file}")