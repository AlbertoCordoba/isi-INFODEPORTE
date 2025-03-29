from datetime import datetime
from database import Database
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

def send_daily_updates(bot_instance, db_instance):
    """Envía actualizaciones usando la instancia de db"""
    try:
        subs = db_instance.get_all_subscriptions()
        print(f"📨 Preparando notificaciones para {len(subs)} suscripciones...")
        
        for chat_id, sport in subs:
            try:
                # Tu lógica de envío aquí
                print(f"Enviando a {chat_id} - {sport}")
            except Exception as e:
                print(f"Error enviando a {chat_id}: {e}")
                
    except Exception as e:
        print(f"🔥 Error en notificaciones: {e}")