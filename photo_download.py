from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
from telegram.ext import CallbackQueryHandler
from finalizar import finish
import logging
sesiones = {}

async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    #logger.info(f"[{user_id}] Foto recibida")

    if user_id not in sesiones:
        await update.message.reply_text("Primero envíame el nombre de la serie.")
        return

    # Obtener la mejor calidad de foto
    photo = update.message.photo[-1]
    #logger.info(f"referencia a la foto ->{photo}")
    file = await context.bot.get_file(photo.file_id)

    # Descargar el archivo localmente
    file_path = f"{user_id}_{photo.file_id}.jpg"
    await file.download_to_drive(f"/home/daniel/telegram_bot/{file_path}")

    # Guardar el ID de la foto en la sesión
    sesiones[user_id]["fotos"].append(file_path)

    #logger.info(f"[{user_id}] Foto descargada y guardada como {file_path}")
    await update.message.reply_text("Foto guardada correctamente.")