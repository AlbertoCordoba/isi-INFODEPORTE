from datetime import datetime
from database import Database
from bot import format_football_matches, format_mlb_games, format_nba_games, format_nhl_games
import services.futbol_service as futbol_service
import services.mlb_service as mlb_service
import services.nba_service as nba_service
import services.nhl_service as nhl_service

db = Database()

def send_sport_updates(bot_instance, db_instance, sport):
    """Envía actualizaciones usando instancias recibidas"""
    conn, cursor = db_instance.get_connection()
    cursor.execute('SELECT chat_id FROM subscriptions WHERE sport = ?', (sport,))
    chat_ids = [row[0] for row in cursor.fetchall()]
    
    if not chat_ids:
        return

    try:
        if sport == 'football':
            matches = futbol_service.get_next_matches('EPL')
            message = "⚽ <b>Partidos de fútbol hoy:</b>\n\n"
            for match in matches[:3]:
                message += f"• {match['HomeTeamName']} vs {match['AwayTeamName']}\n"
        
        elif sport == 'mlb':
            games = mlb_service.get_next_mlb_games()
            message = "⚾ <b>Partidos de MLB hoy:</b>\n\n"
            for game in games[:3]:
                message += f"• {game['HomeTeam']} vs {game['AwayTeam']}\n"
        
        elif sport == 'nba':
            games = nba_service.get_next_nba_games()
            message = "🏀 <b>Partidos de NBA hoy:</b>\n\n"
            for game in games[:3]:
                message += f"• {game['HomeTeam']} vs {game['AwayTeam']}\n"
        
        elif sport == 'nhl':
            games = nhl_service.get_next_nhl_games()
            message = "🏒 <b>Partidos de NHL hoy:</b>\n\n"
            for game in games[:3]:
                message += f"• {game['HomeTeam']} vs {game['AwayTeam']}\n"

        for chat_id in chat_ids:
            bot_instance.send_message(chat_id, message, parse_mode='HTML')
            
    except Exception as e:
        print(f"Error al enviar actualizaciones de {sport}: {e}")

from services.futbol_service import get_competitions  # Importar las competiciones dinámicamente

def send_daily_updates(bot_instance, db_instance):
    """Envía actualizaciones diarias a los usuarios suscritos"""
    print("📨 Ejecutando send_daily_updates...")
    try:
        subscriptions = db_instance.cursor.execute('SELECT chat_id, sport FROM subscriptions').fetchall()
        print(f"📨 Preparando notificaciones para {len(subscriptions)} suscripciones...")

        for chat_id, sport in subscriptions:
            if sport == 'football':
                # Obtener dinámicamente las competiciones desde futbol_service
                competitions = get_competitions()
                message = "⚽ <b>Próximos partidos de fútbol:</b>\n\n"
                for competition_name, competition_data in competitions.items():
                    league_key = competition_data["scores_key"]
                    updates = futbol_service.get_next_matches(league_key)
                    if updates:
                        message += f"<b>{competition_name}:</b>\n"
                        for match in updates[:3]:  # Limitar a los primeros 3 partidos por liga
                            message += f"• {match['HomeTeamName']} vs {match['AwayTeamName']}\n"
                        message += "\n"
                if not message.strip():
                    message = "No hay partidos de fútbol disponibles hoy."
            elif sport == 'mlb':
                updates = mlb_service.get_next_mlb_games()
                message = format_mlb_games(updates)
            elif sport == 'nba':
                updates = nba_service.get_next_nba_games()
                message = format_nba_games(updates)
            elif sport == 'nhl':
                updates = nhl_service.get_next_nhl_games()
                message = format_nhl_games(updates)
            else:
                message = f"No hay actualizaciones disponibles para {sport}."

            # Envía el mensaje al usuario
            bot_instance.send_message(chat_id, message, parse_mode='HTML')

    except Exception as e:
        print(f"🔥 Error en notificaciones: {e}")