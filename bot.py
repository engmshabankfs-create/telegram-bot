from telegram import Update, Bot, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, CallbackQueryHandler, CommandHandler, filters

# ====== إعدادات البوت ======
TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = 834202099

bot_instance = Bot(token=TOKEN)

# تخزين الرسائل مؤقتًا
messages = {}

# ====== الرد على /start ======
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "مرحبا بك 🌹\nاترك رسالتك هنا وسوف يتم الرد عليك في أقرب وقت، شكرا لك ❤️"
    )

# ====== التعامل مع أي رسالة واردة ======
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.chat.type == "private":
        user = update.message.from_user
        text = update.message.text

        # رد تلقائي للمرسل
        await update.message.reply_text(
            "أهلاً بيك 👋\nتم استلام رسالتك، وهنتواصل معاك في أقرب وقت ✅"
        )

        # تسجيل الرسالة للإدارة
        msg_id = update.message.message_id
        messages[msg_id] = {"user_id": user.id, "name": user.first_name, "text": text}

        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("رد على الرسالة", callback_data=str(msg_id))]
        ])

        await context.bot.send_message(
            chat_id=ADMIN_ID,
            text=(
                f"📩 رسالة جديدة للبوت\n\n"
                f"👤 الاسم: {user.first_name}\n"
                f"🔗 اليوزر: @{user.username if user.username else 'لا يوجد'}\n"
                f"🆔 ID: {user.id}\n\n"
                f"💬 الرسالة:\n{text}"
            ),
            reply_markup=keyboard
        )

# ====== التعامل مع أزرار الرد ======
async def handle_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    msg_id = int(query.data)
    
    user_data = messages.get(msg_id)
    if user_data:
        user_id = user_data["user_id"]
        name = user_data["name"]
        await context.bot.send_message(
            chat_id=ADMIN_ID,
            text=f"✅ هتبعث رسالة لـ {name} دلوقتي. اكتب النص اللي تحب تبعته:"
        )
        context.user_data["reply_to"] = user_id

# ====== الرد على المستخدم من ADMIN ======
async def reply_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if "reply_to" in context.user_data:
        user_id = context.user_data["reply_to"]
        await bot_instance.send_message(chat_id=user_id, text=update.message.text)
        await update.message.reply_text("✅ الرسالة اتبعتت بنجاح!")
        del context.user_data["reply_to"]

# ====== تشغيل البوت ======
app = ApplicationBuilder().token(TOKEN).build()

# إضافة Handlers
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
app.add_handler(CallbackQueryHandler(handle_button))
app.add_handler(MessageHandler(filters.TEXT & filters.Chat(ADMIN_ID), reply_text))

print("Bot is running...")
app.run_polling()
