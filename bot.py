from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters

TOKEN = "8448868303:AAGk7SH8ZnyTk9P42WV0CQlxGZuA1qj32Wk"

async def reply_private(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.chat.type == "private":
        await update.message.reply_text(
            "أهلًا بيك 👋\nتم استلام رسالتك وهرد عليك في أقرب وقت ✅"
        )

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, reply_private))

print("Bot is running...")
app.run_polling()
