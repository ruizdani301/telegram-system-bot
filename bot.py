from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
from telegram.ext import CallbackQueryHandler
from finalizar import finish
from photo_download import handle_photo
import logging

sesiones = {}
token = 'key' 
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Envíame el nombre de la serie.")

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    texto = update.message.text

    sesiones[user_id] = {"serie": texto, "fotos": []}
     # Botones de confirmación
    keyboard = [
        [
            InlineKeyboardButton("✅ Sí", callback_data="confirmar_serie"),
            InlineKeyboardButton("❌ No", callback_data="rechazar_serie"),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(f"¿La serie es correcta?: *{texto}*", reply_markup=reply_markup, parse_mode="Markdown")

# async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     user_id = update.effective_user.id
#     logger.info(f"[{user_id}] Foto recibida")

#     if user_id not in sesiones:
#         await update.message.reply_text("Primero envíame el nombre de la serie.")
#         return

#     # Obtener la mejor calidad de foto
#     photo = update.message.photo[-1]
#     logger.info(f"referencia a la foto ->{photo}")
#     file = await context.bot.get_file(photo.file_id)

#     # Descargar el archivo localmente
#     file_path = f"{user_id}_{photo.file_id}.jpg"
#     await file.download_to_drive(f"/home/daniel/telegram_bot/{file_path}")

#     # Guardar el ID de la foto en la sesión
#     sesiones[user_id]["fotos"].append(file_path)

#     logger.info(f"[{user_id}] Foto descargada y guardada como {file_path}")
#     await update.message.reply_text("Foto guardada correctamente.")
    

async def confirmar_serie(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id

    if user_id not in sesiones:
        await query.edit_message_text("No se ha propuesto ninguna serie aún.")
        return

    if query.data == "confirmar_serie":
        sesiones[user_id]["confirmada"] = True
        await query.edit_message_text(f"✅ Serie confirmada: {sesiones[user_id]['serie']}. Ahora envíame las fotos.")
        logger.info(f"[{user_id}] Serie confirmada: {sesiones[user_id]['serie']}")
    else:
        del sesiones[user_id]  # Eliminamos la sesión si rechaza
        await query.edit_message_text("❌ Serie rechazada. Por favor, envíame el nombre correcto nuevamente.")
        logger.info(f"[{user_id}] Serie rechazada.")

# async def finish(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     user_id = update.effective_user.id
#     data = sesiones.get(user_id)
#     if not data:
#         await update.message.reply_text("No has iniciado ninguna serie.")
#         return

#     await update.message.reply_text(f"Serie: {data['serie']}, Fotos recibidas: {len(data['fotos'])}")
#     # Aquí podrías subir las fotos a un servidor, base de datos, etc.
#     del sesiones[user_id]
# async def pedir_especie(update, context):
#     keyboard = [
#         [InlineKeyboardButton("Perro", callback_data='especie_perro')],
#         [InlineKeyboardButton("Gato", callback_data='especie_gato')],
#         [InlineKeyboardButton("Pájaro", callback_data='especie_pajaro')]
#     ]
#     reply_markup = InlineKeyboardMarkup(keyboard)
#     await update.message.reply_text('Selecciona una especie:', reply_markup=reply_markup)

# async def manejar_seleccion(update, context):
#     query = update.callback_query
#     await query.answer()  # Responde al callback para que no quede el "reloj"
    
#     especie = query.data  # Ejemplo: 'especie_perro'
    
#     # Procesar selección
#     if especie == 'especie_perro':
#         texto = "Elegiste Perro 🐶"
#     elif especie == 'especie_gato':
#         texto = "Elegiste Gato 🐱"
#     else:
#         texto = "Elegiste Pájaro 🐦"
    
#     await query.edit_message_text(texto)

# En el setup del bot


app = ApplicationBuilder().token(token).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("finalizar", finish))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
app.add_handler(MessageHandler(filters.PHOTO, handle_photo))
app.add_handler(CallbackQueryHandler(confirmar_serie))
#--------------------
# app.add_handler(CommandHandler("especie", pedir_especie))
# app.add_handler(CallbackQueryHandler(manejar_seleccion, pattern="^especie_"))



if __name__ == "__main__":

    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO,
        handlers=[
            logging.FileHandler("bot_logs.log"),     # Guarda logs en un archivo
            #logging.StreamHandler()                  # Muestra logs en consola
        ]
    )

    logger = logging.getLogger(__name__)

    app.run_polling()

