import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from datetime import datetime
from config import TELEGRAM_BOT_TOKEN
from services import futbol_service, mlb_service, nba_service, nhl_service
from database import Database
from apscheduler.schedulers.background import BackgroundScheduler
import notifications

# Inicialización
bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)
print("⚡ Bot Deportivo iniciado...")
db = Database()
# Estados del usuario
user_states = {}

# Programar tareas
scheduler = BackgroundScheduler()
scheduler.add_job(
    lambda: notifications.send_daily_updates(bot, db),  # Pasa db como parámetro
    'cron', 
    hour=9, 
    minute=0
)
# =============================================
# FUNCIONES AUXILIARES
# =============================================

def format_date(date_str):
    """Formatea una fecha ISO a dd/mm/yyyy HH:MM"""
    try:
        return datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%S').strftime('%d/%m/%Y %H:%M')
    except:
        return "Fecha no disponible"

# =============================================
# FUNCIONES DE FORMATEO PARA CADA DEPORTE
# =============================================

# --- FÚTBOL ---
def format_football_matches(matches, competition_name):
    if not matches:
        return f"⚽ <b>{competition_name}</b>\n\nNo hay partidos programados."
    
    message = f"⚽ <b>{competition_name} - Próximos Partidos</b>\n\n"
    for match in matches[:10]:
        message += (
            f"🏠 <b>{match.get('HomeTeamName', 'Desconocido')}</b> vs <b>{match.get('AwayTeamName', 'Desconocido')}</b>\n"
            f"📅 {format_date(match.get('DateTime'))}\n"
            f"🏟 {match.get('StadiumDetails', {}).get('Name', 'Estadio no disponible')}\n"
            f"────────────────────\n"
        )
    return message

def format_football_standings(standings, competition_name):
    if not standings:
        return f"⚽ <b>{competition_name}</b>\n\nNo hay datos de clasificación."
    
    message = f"⚽ <b>{competition_name} - Clasificación</b>\n<code>\n"
    message += "Pos | Equipo           | PTS | PJ | G | E | P | DG\n"
    message += "──────────────────────────────────────────────────\n"
    
    for team in standings[0]['Standings'][:20]:  # Top 20
        if team.get('Scope') == "Total":
            message += (
                f"{team.get('Order', 0):<3} | "
                f"{team.get('Name', 'Desconocido')[:15]:<15} | "
                f"{team.get('Points', 0):<3} | "
                f"{team.get('Games', 0):<3} | "
                f"{team.get('Wins', 0):<2} | "
                f"{team.get('Draws', 0):<2} | "
                f"{team.get('Losses', 0):<2} | "
                f"{team.get('GoalsDifferential', 0):<3}\n"
            )
    return message + "</code>"

def format_football_injuries(players, competition_name):
    if not players:
        return f"⚽ <b>{competition_name}</b>\n\nNo hay jugadores lesionados."
    
    message = f"⚽ <b>{competition_name} - Lesionados</b>\n<code>\n"
    message += "Jugador           | Equipo  | Posición | Desde\n"
    message += "──────────────────────────────────────────────\n"
    
    for player in players[:15]:
        name = player.get('CommonName') or f"{player.get('FirstName', '')} {player.get('LastName', '')}"
        message += (
            f"{name[:15]:<15} | "
            f"{player.get('Team', 'N/A')[:6]:<6} | "
            f"{player.get('Position', 'N/A')[:8]:<8} | "
            f"{player.get('InjuryStartDate', 'N/A')[:10]}\n"
        )
    return message + "</code>"

# --- MLB ---
def format_mlb_games(games):
    if not games:
        return "⚾ <b>MLB</b>\n\nNo hay partidos próximos."
    
    message = "⚾ <b>MLB - Próximos Partidos</b>\n\n"
    for game in games[:10]:
        message += (
            f"🏟 <b>{game.get('HomeTeam', 'Desconocido')}</b> vs <b>{game.get('AwayTeam', 'Desconocido')}</b>\n"
            f"📅 {format_date(game.get('DateTime'))}\n"
            f"📍 {game.get('Stadium', 'Estadio no disponible')}\n"
            f"────────────────────\n"
        )
    return message

def format_mlb_standings(standings):
    if not standings:
        return "⚾ <b>MLB</b>\n\nNo hay datos de clasificación."
    
    message = "⚾ <b>MLB - Clasificación</b>\n"
    
    for league in ["AL", "NL"]:
        message += f"\n<b>{league} League</b>\n<code>\n"
        message += "Div | Equipo      | G | P | %    | GB\n"
        message += "──────────────────────────────────────\n"
        
        for team in standings:
            if team['League'] == league:
                message += (
                    f"{team.get('DivisionRank', 0):<3} | "
                    f"{team.get('Name', 'Desconocido')[:10]:<10} | "
                    f"{team.get('Wins', 0):<2} | "
                    f"{team.get('Losses', 0):<2} | "
                    f"{team.get('Percentage', 0):<5.3f} | "
                    f"{team.get('GamesBack', 0):<4.1f}\n"
                )
        message += "</code>"
    return message

def format_mlb_injuries(players):
    if not players:
        return "⚾ <b>MLB</b>\n\nNo hay jugadores lesionados."
    
    message = "⚾ <b>MLB - Lesionados</b>\n<code>\n"
    message += "Jugador         | Posición | Desde     | Status\n"
    message += "───────────────────────────────────────────────\n"
    
    for player in players[:15]:
        name = f"{player.get('FirstName', '')} {player.get('LastName', '')}"
        message += (
            f"{name[:12]:<12} | "
            f"{player.get('Position', 'N/A')[:8]:<8} | "
            f"{player.get('InjuryStartDate', 'N/A')[:10]:<10} | "
            f"{player.get('Status', 'N/A')[:10]}\n"
        )
    return message + "</code>"

# --- NBA ---
def format_nba_games(games):
    if not games:
        return "🏀 <b>NBA</b>\n\nNo hay partidos próximos."
    
    message = "🏀 <b>NBA - Próximos Partidos</b>\n\n"
    for game in games[:10]:
        message += (
            f"🏟 <b>{game.get('HomeTeam', 'Desconocido')}</b> vs <b>{game.get('AwayTeam', 'Desconocido')}</b>\n"
            f"📅 {format_date(game.get('DateTime'))}\n"
            f"📍 {game.get('Stadium', 'Estadio no disponible')}\n"
            f"────────────────────\n"
        )
    return message

def format_nba_standings(standings):
    if not standings:
        return "🏀 <b>NBA</b>\n\nNo hay datos de clasificación."
    
    message = "🏀 <b>NBA - Clasificación</b>\n"
    
    for conference in ["Eastern", "Western"]:
        message += f"\n<b>{conference} Conference</b>\n<code>\n"
        message += "Pos | Equipo      | G | P | %    | Streak\n"
        message += "──────────────────────────────────────────\n"
        
        for team in standings:
            if team['Conference'] == conference:
                message += (
                    f"{team.get('ConferenceRank', 0):<3} | "
                    f"{team.get('Name', 'Desconocido')[:10]:<10} | "
                    f"{team.get('Wins', 0):<2} | "
                    f"{team.get('Losses', 0):<2} | "
                    f"{team.get('Percentage', 0):<5.3f} | "
                    f"{team.get('StreakDescription', '-')[:6]}\n"
                )
        message += "</code>"
    return message

def format_nba_injuries(players):
    if not players:
        return "🏀 <b>NBA</b>\n\nNo hay jugadores lesionados reportados."
    
    message = "🏀 <b>NBA - Jugadores Lesionados</b>\n<code>\n"
    message += "Jugador         | Equipo  | Posición | Desde\n"
    message += "────────────────────────────────────────────\n"
    
    for player in players[:15]:
        if player is None:  # Verificación adicional
            continue
            
        name = f"{player.get('FirstName', '')} {player.get('LastName', '')}"
        team = player.get('Team', 'N/A')
        position = player.get('Position', 'N/A')
        injury_date = player.get('InjuryStartDate', 'N/A')[:10] if player.get('InjuryStartDate') else 'N/A'
        
        message += (
            f"{name[:12]:<12} | "
            f"{str(team)[:6]:<6} | "  # Aseguramos que sea string
            f"{str(position)[:8]:<8} | "
            f"{injury_date}\n"
        )
    return message + "</code>"

# --- NHL ---
def format_nhl_games(games):
    if not games:
        return "🏒 <b>NHL</b>\n\nNo hay partidos próximos."
    
    message = "🏒 <b>NHL - Próximos Partidos</b>\n\n"
    for game in games[:10]:
        message += (
            f"🏟 <b>{game.get('HomeTeam', 'Desconocido')}</b> vs <b>{game.get('AwayTeam', 'Desconocido')}</b>\n"
            f"📅 {format_date(game.get('DateTime'))}\n"
            f"📍 {game.get('Stadium', 'Estadio no disponible')}\n"
            f"────────────────────\n"
        )
    return message

def format_nhl_standings(standings):
    if not standings:
        return "🏒 <b>NHL</b>\n\nNo hay datos de clasificación."
    
    message = "🏒 <b>NHL - Clasificación</b>\n"
    
    for conference in ["Eastern", "Western"]:
        message += f"\n<b>{conference} Conference</b>\n<code>\n"
        message += "Pos | Equipo      | G | P | OT | PTS\n"
        message += "────────────────────────────────────\n"
        
        for team in standings:
            if team['Conference'] == conference:
                points = (team.get('Wins', 0) * 2) + team.get('OvertimeLosses', 0)
                message += (
                    f"{team.get('ConferenceRank', 0):<3} | "
                    f"{team.get('Name', 'Desconocido')[:10]:<10} | "
                    f"{team.get('Wins', 0):<2} | "
                    f"{team.get('Losses', 0):<2} | "
                    f"{team.get('OvertimeLosses', 0):<2} | "
                    f"{points:<3}\n"
                )
        message += "</code>"
    return message

def format_nhl_injuries(players):
    if not players:
        return "🏒 <b>NHL</b>\n\nNo hay jugadores lesionados."
    
    message = "🏒 <b>NHL - Lesionados</b>\n<code>\n"
    message += "Jugador         | Equipo  | Posición | Desde\n"
    message += "────────────────────────────────────────────\n"
    
    for player in players[:15]:
        name = f"{player.get('FirstName', '')} {player.get('LastName', '')}"
        message += (
            f"{name[:12]:<12} | "
            f"{player.get('Team', 'N/A')[:6]:<6} | "
            f"{player.get('Position', 'N/A')[:8]:<8} | "
            f"{player.get('InjuryStartDate', 'N/A')[:10]}\n"
        )
    return message + "</code>"

# =============================================
# HANDLERS PRINCIPALES
# =============================================

@bot.message_handler(commands=['start', 'help', 'menu'])
def send_welcome(message):
    """Handler inicial que registra al usuario"""
    db.add_user(
        chat_id=message.chat.id,
        username=message.chat.username,
        first_name=message.chat.first_name,
        last_name=message.chat.last_name
    )
    show_main_menu(message.chat.id, "🏆 <b>Bot Deportivo Multiliga</b>\n\nSelecciona un deporte:")

@bot.message_handler(commands=['mis_suscripciones'])
def show_subscriptions(message):
    """Muestra las suscripciones activas del usuario"""
    chat_id = message.chat.id
    subs = db.get_user_subscriptions(chat_id)
    
    if not subs:
        bot.send_message(chat_id, "❌ No estás suscrito a ningún deporte.")
        return
    
    markup = InlineKeyboardMarkup()
    for sport in subs:
        markup.add(InlineKeyboardButton(
            f"❌ Desuscribirse de {sport.upper()}",
            callback_data=f"unsubscribe_{sport}"
        ))
    
    bot.send_message(
        chat_id,
        "📋 <b>Tus suscripciones activas:</b>\n\n" + "\n• ".join([s.upper() for s in subs]),
        reply_markup=markup,
        parse_mode='HTML'
    )

@bot.callback_query_handler(func=lambda call: call.data == 'my_subscriptions')
def handle_my_subscriptions(call):
    show_subscriptions(call.message)

@bot.callback_query_handler(func=lambda call: call.data.startswith(('subscribe_', 'unsubscribe_')))
def handle_subscription(call):
    """Gestiona suscripciones/desuscripciones"""
    chat_id = call.message.chat.id
    action, sport = call.data.split('_')
    
    if action == 'subscribe':
        db.subscribe_user(chat_id, sport)
        bot.answer_callback_query(call.id, f"✅ Suscrito a {sport.upper()}!")
    else:
        db.unsubscribe_user(chat_id, sport)
        bot.answer_callback_query(call.id, f"❌ Desuscrito de {sport.upper()}")
    
    # Actualizar menú correspondiente
    if sport == 'football':
        show_football_menu(chat_id)
    elif sport == 'mlb':
        show_mlb_menu(chat_id)
    elif sport == 'nba':
        show_nba_menu(chat_id)
    elif sport == 'nhl':
        show_nhl_menu(chat_id)

@bot.callback_query_handler(func=lambda call: call.data == 'back_to_sports')
def back_to_sports(call):
    show_main_menu(call.message.chat.id, "🏆 <b>Menú Principal</b>\n\nSelecciona un deporte:")
    bot.answer_callback_query(call.id)

# =============================================
# MENÚS CON SUSCRIPCIONES
# =============================================

def show_main_menu(chat_id, text="🏆 Bot Deportivo Multiliga"):
    markup = InlineKeyboardMarkup(row_width=2)
    
    # Botones principales
    markup.add(
        InlineKeyboardButton("⚽ Fútbol", callback_data="sport_football"),
        InlineKeyboardButton("⚾ MLB", callback_data="sport_mlb"),
        InlineKeyboardButton("🏀 NBA", callback_data="sport_nba"),
        InlineKeyboardButton("🏒 NHL", callback_data="sport_nhl")
    )
    
    # Nuevo: Botón destacado de suscripciones
    subs_count = len(db.get_user_subscriptions(chat_id))
    markup.add(
        InlineKeyboardButton(
            f"🔔 Suscripciones ({subs_count})", 
            callback_data="subscription_manager"
        ),
        InlineKeyboardButton("📋 Mis Susc.", callback_data="my_subscriptions")
    )
    
    bot.send_message(chat_id, text, reply_markup=markup, parse_mode='HTML')

@bot.callback_query_handler(func=lambda call: call.data == 'subscription_manager')
def show_sports_subscriptions(call):
    chat_id = call.message.chat.id
    markup = InlineKeyboardMarkup(row_width=2)
    
    sports = [
        ("⚽ Fútbol", "football"),
        ("⚾ MLB", "mlb"),
        ("🏀 NBA", "nba"),
        ("🏒 NHL", "nhl")
    ]
    
    # Crea botones dinámicos
    for sport_name, sport_code in sports:
        is_subscribed = db.is_user_subscribed(chat_id, sport_code)
        icon = "🔕" if is_subscribed else "🔔"
        markup.add(InlineKeyboardButton(
            f"{icon} {sport_name}", 
            callback_data=f"toggle_{sport_code}"
        ))
    
    markup.add(InlineKeyboardButton("« Volver", callback_data="back_to_main"))
    
    bot.edit_message_text(
        "🔔 Gestión de Suscripciones\n\nSelecciona un deporte para suscribirte/desuscribirte:",
        chat_id,
        call.message.message_id,
        reply_markup=markup
    )
@bot.callback_query_handler(func=lambda call: call.data.startswith('toggle_'))
def toggle_subscription(call):
    chat_id = call.message.chat.id
    sport_code = call.data.split('_')[1]
    
    if db.is_user_subscribed(chat_id, sport_code):
        db.unsubscribe_user(chat_id, sport_code)
        action = "❌ Desuscrito de"
    else:
        db.subscribe_user(chat_id, sport_code)
        action = "✅ Suscrito a"
    
    bot.answer_callback_query(call.id, f"{action} {sport_code.upper()}")
    show_sports_subscriptions(call)  # Actualiza el menú
    
def show_football_menu(chat_id):
    markup = InlineKeyboardMarkup(row_width=2)
    competitions = [
        ("Premier League", "EPL"),
        ("La Liga", "ESP"),
        ("Serie A", "ITSA"),
        ("Bundesliga", "DEB"),
        ("Ligue 1", "FRL1"),
        ("Champions League", "UCL")
    ]
    
    buttons = [InlineKeyboardButton(name, callback_data=f"fb_comp_{key}") for name, key in competitions]
    markup.add(*buttons)
    
    # Botón de suscripción dinámico
    is_subscribed = db.is_user_subscribed(chat_id, 'football')
    sub_button = InlineKeyboardButton(
        text="🔕 Desuscribirse de Fútbol" if is_subscribed else "🔔 Suscribirse a Fútbol",
        callback_data="unsubscribe_football" if is_subscribed else "subscribe_football"
    )
    markup.add(sub_button)
    markup.add(InlineKeyboardButton("🔙 Menú Principal", callback_data="back_to_sports"))
    
    bot.send_message(chat_id, "⚽ <b>Selecciona una competición:</b>", reply_markup=markup, parse_mode='HTML')

def show_mlb_menu(chat_id):
    markup = InlineKeyboardMarkup(row_width=2)
    is_subscribed = db.is_user_subscribed(chat_id, 'mlb')
    sub_button_text = "🔔 Suscribirse a MLB" if not is_subscribed else "🔕 Desuscribirse de MLB"
    sub_button_data = "subscribe_mlb" if not is_subscribed else "unsubscribe_mlb"
    
    markup.add(
        InlineKeyboardButton("📅 Próximos Partidos", callback_data="mlb_matches"),
        InlineKeyboardButton("🏆 Clasificación", callback_data="mlb_standings"),
        InlineKeyboardButton("🏥 Jugadores Lesionados", callback_data="mlb_injuries"),
        InlineKeyboardButton(sub_button_text, callback_data=sub_button_data),
        InlineKeyboardButton("🔙 Menú Principal", callback_data="back_to_sports")
    )
    bot.send_message(chat_id, "⚾ <b>MLB - Menú Principal</b>\n\nSelecciona una opción:", reply_markup=markup, parse_mode='HTML')

def show_nba_menu(chat_id):
    markup = InlineKeyboardMarkup(row_width=2)
    is_subscribed = db.is_user_subscribed(chat_id, 'nba')
    sub_button_text = "🔔 Suscribirse a NBA" if not is_subscribed else "🔕 Desuscribirse de NBA"
    sub_button_data = "subscribe_nba" if not is_subscribed else "unsubscribe_nba"
    
    markup.add(
        InlineKeyboardButton("📅 Próximos Partidos", callback_data="nba_matches"),
        InlineKeyboardButton("🏆 Clasificación", callback_data="nba_standings"),
        InlineKeyboardButton("🏥 Jugadores Lesionados", callback_data="nba_injuries"),
        InlineKeyboardButton(sub_button_text, callback_data=sub_button_data),
        InlineKeyboardButton("🔙 Menú Principal", callback_data="back_to_sports")
    )
    bot.send_message(chat_id, "🏀 <b>NBA - Menú Principal</b>\n\nSelecciona una opción:", reply_markup=markup, parse_mode='HTML')

def show_nhl_menu(chat_id):
    markup = InlineKeyboardMarkup(row_width=2)
    is_subscribed = db.is_user_subscribed(chat_id, 'nhl')
    sub_button_text = "🔔 Suscribirse a NHL" if not is_subscribed else "🔕 Desuscribirse de NHL"
    sub_button_data = "subscribe_nhl" if not is_subscribed else "unsubscribe_nhl"
    
    markup.add(
        InlineKeyboardButton("📅 Próximos Partidos", callback_data="nhl_matches"),
        InlineKeyboardButton("🏆 Clasificación", callback_data="nhl_standings"),
        InlineKeyboardButton("🏥 Jugadores Lesionados", callback_data="nhl_injuries"),
        InlineKeyboardButton(sub_button_text, callback_data=sub_button_data),
        InlineKeyboardButton("🔙 Menú Principal", callback_data="back_to_sports")
    )
    bot.send_message(chat_id, "🏒 <b>NHL - Menú Principal</b>\n\nSelecciona una opción:", reply_markup=markup, parse_mode='HTML')

# =============================================
# HANDLERS PARA CADA DEPORTE
# =============================================

# --- FÚTBOL ---
@bot.callback_query_handler(func=lambda call: call.data == 'sport_football')
def handle_football_selection(call):
    chat_id = call.message.chat.id
    user_states[chat_id] = {'sport': 'football'}
    show_football_menu(chat_id)
    bot.answer_callback_query(call.id)

def show_football_menu(chat_id):
    markup = InlineKeyboardMarkup(row_width=2)
    competitions = [
        ("Premier League", "EPL"),
        ("La Liga", "ESP"),
        ("Serie A", "ITSA"),
        ("Bundesliga", "DEB"),
        ("Ligue 1", "FRL1"),
        ("Champions League", "UCL")
    ]
    
    buttons = [InlineKeyboardButton(name, callback_data=f"fb_comp_{key}") for name, key in competitions]
    markup.add(*buttons)
    markup.add(InlineKeyboardButton("🔙 Menú Principal", callback_data="back_to_sports"))
    
    bot.send_message(
        chat_id,
        "⚽ <b>Selecciona una competición:</b>",
        reply_markup=markup,
        parse_mode='HTML'
    )

@bot.callback_query_handler(func=lambda call: call.data.startswith('fb_comp_'))
def handle_football_competition(call):
    chat_id = call.message.chat.id
    comp_key = call.data.split('_')[2]
    comp_name = next(name for name, key in [
        ("Premier League", "EPL"),
        ("La Liga", "ESP"),
        ("Serie A", "ITSA"),
        ("Bundesliga", "DEB"),
        ("Ligue 1", "FRL1"),
        ("Champions League", "UCL")
    ] if key == comp_key)
    
    user_states[chat_id].update({
        'competition': comp_name,
        'comp_key': comp_key
    })
    
    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(
        InlineKeyboardButton("📅 Próximos Partidos", callback_data="fb_matches"),
        InlineKeyboardButton("🏆 Clasificación", callback_data="fb_standings"),
        InlineKeyboardButton("🏥 Jugadores Lesionados", callback_data="fb_injuries"),
        InlineKeyboardButton("🔙 Atrás", callback_data="sport_football")
    )
    
    bot.edit_message_text(
        f"⚽ <b>{comp_name}</b>\n\nSelecciona qué información deseas ver:",
        chat_id,
        call.message.message_id,
        reply_markup=markup,
        parse_mode='HTML'
    )
    bot.answer_callback_query(call.id)

@bot.callback_query_handler(func=lambda call: call.data.startswith('fb_'))
def handle_football_action(call):
    chat_id = call.message.chat.id
    action = call.data.split('_')[1]
    comp_name = user_states[chat_id]['competition']
    comp_key = user_states[chat_id]['comp_key']
    
    if action == 'matches':
        matches = futbol_service.get_next_matches(comp_key)
        response = format_football_matches(matches, comp_name)
    elif action == 'standings':
        standings = futbol_service.get_standings(comp_key)
        response = format_football_standings(standings, comp_name)
    elif action == 'injuries':
        injuries = futbol_service.get_injured_players(comp_key)
        response = format_football_injuries(injuries, comp_name)
    
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton(
        "↩️ Volver a opciones",
        callback_data=f"fb_comp_{comp_key}"
    ))
    markup.add(InlineKeyboardButton(
        "🔙 Menú Principal",
        callback_data="back_to_sports"
    ))
    
    bot.send_message(chat_id, response, reply_markup=markup, parse_mode='HTML')
    bot.answer_callback_query(call.id)

# --- MLB ---
@bot.callback_query_handler(func=lambda call: call.data == 'sport_mlb')
def handle_mlb_selection(call):
    chat_id = call.message.chat.id
    user_states[chat_id] = {'sport': 'mlb'}
    show_mlb_menu(chat_id)
    bot.answer_callback_query(call.id)

def show_mlb_menu(chat_id):
    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(
        InlineKeyboardButton("📅 Próximos Partidos", callback_data="mlb_matches"),
        InlineKeyboardButton("🏆 Clasificación", callback_data="mlb_standings"),
        InlineKeyboardButton("🏥 Jugadores Lesionados", callback_data="mlb_injuries"),
        InlineKeyboardButton("🔙 Menú Principal", callback_data="back_to_sports")
    )
    bot.send_message(
        chat_id,
        "⚾ <b>MLB - Menú Principal</b>\n\nSelecciona una opción:",
        reply_markup=markup,
        parse_mode='HTML'
    )

@bot.callback_query_handler(func=lambda call: call.data.startswith('mlb_'))
def handle_mlb_action(call):
    chat_id = call.message.chat.id
    action = call.data.split('_')[1]
    
    if action == 'matches':
        games = mlb_service.get_next_mlb_games()
        response = format_mlb_games(games)
    elif action == 'standings':
        standings = mlb_service.get_mlb_standings()
        response = format_mlb_standings(standings)
    elif action == 'injuries':
        injuries = mlb_service.get_mlb_injured_players()
        response = format_mlb_injuries(injuries)
    
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("↩️ Volver a MLB", callback_data="sport_mlb"))
    markup.add(InlineKeyboardButton("🔙 Menú Principal", callback_data="back_to_sports"))
    
    bot.send_message(chat_id, response, reply_markup=markup, parse_mode='HTML')
    bot.answer_callback_query(call.id)

# --- NBA ---
@bot.callback_query_handler(func=lambda call: call.data == 'sport_nba')
def handle_nba_selection(call):
    chat_id = call.message.chat.id
    user_states[chat_id] = {'sport': 'nba'}
    show_nba_menu(chat_id)
    bot.answer_callback_query(call.id)

def show_nba_menu(chat_id):
    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(
        InlineKeyboardButton("📅 Próximos Partidos", callback_data="nba_matches"),
        InlineKeyboardButton("🏆 Clasificación", callback_data="nba_standings"),
        InlineKeyboardButton("🏥 Jugadores Lesionados", callback_data="nba_injuries"),
        InlineKeyboardButton("🔙 Menú Principal", callback_data="back_to_sports")
    )
    bot.send_message(
        chat_id,
        "🏀 <b>NBA - Menú Principal</b>\n\nSelecciona una opción:",
        reply_markup=markup,
        parse_mode='HTML'
    )

@bot.callback_query_handler(func=lambda call: call.data.startswith('nba_'))
def handle_nba_action(call):
    chat_id = call.message.chat.id
    action = call.data.split('_')[1]
    
    if action == 'matches':
        games = nba_service.get_next_nba_games()
        response = format_nba_games(games)
    elif action == 'standings':
        standings = nba_service.get_nba_standings()
        response = format_nba_standings(standings)
    elif action == 'injuries':
        injuries = nba_service.get_nba_injured_players()
        response = format_nba_injuries(injuries)
    
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("↩️ Volver a NBA", callback_data="sport_nba"))
    markup.add(InlineKeyboardButton("🔙 Menú Principal", callback_data="back_to_sports"))
    
    bot.send_message(chat_id, response, reply_markup=markup, parse_mode='HTML')
    bot.answer_callback_query(call.id)

# --- NHL ---
@bot.callback_query_handler(func=lambda call: call.data == 'sport_nhl')
def handle_nhl_selection(call):
    chat_id = call.message.chat.id
    user_states[chat_id] = {'sport': 'nhl'}
    show_nhl_menu(chat_id)
    bot.answer_callback_query(call.id)

def show_nhl_menu(chat_id):
    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(
        InlineKeyboardButton("📅 Próximos Partidos", callback_data="nhl_matches"),
        InlineKeyboardButton("🏆 Clasificación", callback_data="nhl_standings"),
        InlineKeyboardButton("🏥 Jugadores Lesionados", callback_data="nhl_injuries"),
        InlineKeyboardButton("🔙 Menú Principal", callback_data="back_to_sports")
    )
    bot.send_message(
        chat_id,
        "🏒 <b>NHL - Menú Principal</b>\n\nSelecciona una opción:",
        reply_markup=markup,
        parse_mode='HTML'
    )

@bot.callback_query_handler(func=lambda call: call.data.startswith('nhl_'))
def handle_nhl_action(call):
    chat_id = call.message.chat.id
    action = call.data.split('_')[1]
    
    if action == 'matches':
        games = nhl_service.get_next_nhl_games()
        response = format_nhl_games(games)
    elif action == 'standings':
        standings = nhl_service.get_nhl_standings()
        response = format_nhl_standings(standings)
    elif action == 'injuries':
        injuries = nhl_service.get_nhl_injured_players()
        response = format_nhl_injuries(injuries)
    
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("↩️ Volver a NHL", callback_data="sport_nhl"))
    markup.add(InlineKeyboardButton("🔙 Menú Principal", callback_data="back_to_sports"))
    
    bot.send_message(chat_id, response, reply_markup=markup, parse_mode='HTML')
    bot.answer_callback_query(call.id)

# =============================================
# MANEJO DE ERRORES
# =============================================

@bot.callback_query_handler(func=lambda call: call.data == 'my_subscriptions')
def handle_my_subscriptions(call):
    show_subscriptions(call.message)

@bot.callback_query_handler(func=lambda call: True)
def handle_unmatched_callback(call):
    bot.answer_callback_query(call.id, "⚠️ Opción no reconocida")
    show_main_menu(call.message.chat.id, "Selecciona una opción válida:")
@bot.message_handler(commands=['test_notif'])
def test_notification(message):
    try:
        chat_id = message.chat.id
        
        # Mensaje de prueba (personalízalo)
        test_msg = (
            "🔔 *NOTIFICACIÓN DE PRUEBA*\n\n"
            "¡Funciona correctamente!\n"
            f"• Hora: {datetime.now().strftime('%H:%M:%S')}\n"
            f"• Chat ID: {chat_id}"
        )
        
        bot.send_message(chat_id, test_msg, parse_mode='Markdown')
        bot.reply_to(message, "✅ Notificación enviada correctamente")
        
    except Exception as e:
        bot.reply_to(message, f"❌ Error: {str(e)}")
@bot.message_handler(func=lambda message: True)
def handle_unrecognized_message(message):
    show_main_menu(message.chat.id, "No entendí tu mensaje. Por favor selecciona una opción del menú:")

if __name__ == '__main__':
    try:
        print("⚡ Inicializando base de datos...")
        db.get_connection()  # Fuerza la inicialización
        
        # Debug: Mostrar estado inicial
        print(f"📊 Usuarios registrados: {len(db.get_all_subscriptions())}")
        
        print("🤖 Bot deportivo + Notificaciones activado...")
        bot.infinity_polling()
    except Exception as e:
        print(f"❌ Error crítico: {e}")
    finally:
        scheduler.shutdown()
        db.close()  # Asegura cierre limpio