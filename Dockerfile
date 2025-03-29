# filepath: c:\Users\User\Desktop\BotTelegramBaseDatos\Dockerfile
# Usa una imagen base de Python
FROM python:3.9-slim

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copia los archivos necesarios al contenedor
COPY . /app

# Instala las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Verifica que telebot esté instalado
RUN pip show pyTelegramBotAPI

# Comando para ejecutar el bot
CMD ["python", "BotTelegram/bot.py"]