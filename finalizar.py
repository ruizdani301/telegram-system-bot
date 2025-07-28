from telegram import Update
from telegram.ext import ContextTypes
import logging

sesiones = {}

async def finish(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    data = sesiones.get(user_id)
    if not data:
        await update.message.reply_text("No has iniciado ninguna serie.")
        return
    await update.message.reply_text(f"Serie: {data['serie']}, Fotos recibidas: {len(data['fotos'])}")
#Aquí podrías subir las fotos a un servidor, base de datos, etc.
    del sesiones[user_id]
