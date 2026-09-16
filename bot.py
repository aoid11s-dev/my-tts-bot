import os
import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import edge_tts

TOKEN = "8551348467:AAGL1opX9tUsovfocKHpX2F2mZmJ_sBEHSQ"
VOICE = "ar-SA-HamedNeural"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("أهلاً بك! أرسل لي أي نص وسأقوم بتحويله إلى صوت وثائقي فخم.")

async def convert_text_to_audio(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    chat_id = update.message.chat_id
    file_name = f"audio_{chat_id}.mp3"

    status_msg = await update.message.reply_text("جاري تحويل النص إلى صوت...")

    try:
        communicate = edge_tts.Communicate(text, VOICE)
        await communicate.save(file_name)

        with open(file_name, 'rb') as audio:
            await update.message.reply_audio(audio=audio, title="التعليق الصوتي")

    except Exception as e:
        await update.message.reply_text("حدث خطأ أثناء تحويل الصوت.")
    finally:
        if os.path.exists(file_name):
            os.remove(file_name)
        await status_msg.delete()

if __name__ == '__main__':
    print("البوت يعمل الآن بالصوت الوثائقي...")
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, convert_text_to_audio))
    app.run_polling()
