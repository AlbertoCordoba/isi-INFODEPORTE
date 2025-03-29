import requests

# Reemplaza 'YOUR_TELEGRAM_BOT_TOKEN' con el token de tu bot de Telegram
TELEGRAM_BOT_TOKEN = "8062537403:AAE8JJRygu2BSM59v-kl_MbrzjwecmVPcR4"
# Reemplaza 'CHAT_ID' con el ID del chat al que quieres enviar el mensaje
CHAT_ID = "5761127653"
# El mensaje que quieres enviar
MESSAGE = "Hola, este es un mensaje de prueba desde la API de Telegram."

# URL de la API de Telegram para enviar mensajes
TELEGRAM_API_URL = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"

# Parámetros de la solicitud
params = {
    "chat_id": CHAT_ID,
    "text": MESSAGE
}

# Realiza la solicitud para enviar el mensaje
response = requests.get(TELEGRAM_API_URL, params=params)

if response.status_code == 200:
    print("Mensaje enviado exitosamente a través de la API de Telegram")
else:
    print("Error al enviar el mensaje a través de la API de Telegram")
    print(response.json())