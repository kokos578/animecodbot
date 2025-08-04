import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes, MessageHandler, filters

# Логирование
logging.basicConfig(level=logging.INFO)

# Получаем токен из переменной окружения
import os
TOKEN = os.getenv("TELEGRAM_TOKEN")

# Каналы (обязательно публичные)
CHANNELS = [
    {"id": "@hotlentaa", "url": "https://t.me/+O2MCfpvdcb1lOTli"},
    {"id": "@rrreportt", "url": "https://t.me/+QvVBN6D7zHI4M2My"},
    {"id": "@gamelivenew", "url": "https://t.me/+In753IkOfJMwNGYy"},
    {"id": "@perezagryzska", "url": "https://t.me/+HJnx3PMd0xM5YTk6"},
    {"id": "@focustgg", "url": "https://t.me/+0xkYGnZLk5sxZGVi"},
]

# Коды → фильмы
CODES = {
    "501": "Криминальное чтиво",
    "502": "Начало",
    "503": "Матрица",
    "504": "Титаник",
    "505": "Аватар",
    "506": "Джокер",
    "507": "Начало",
    "508": "Интерстеллар"
}

# /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    keyboard = [[{"text": "🔍 Найти аниме", "callback_data": "check_sub"}]]
    reply_markup = {"inline_keyboard": keyboard}
    await update.message.reply_text(
        f"🎬 Привет, {user.first_name}!\n\n"
        "Увидел фрагмент в TikTok?\n"
        "Введи **код из видео**, чтобы найти аниме.\n\n"
        "Но сначала необходимо подписаться на несколько каналов 😉",
        reply_markup=reply_markup
    )

# Проверка подписки
async def check_subscription(user_id: int, context: ContextTypes.DEFAULT_TYPE) -> bool:
    for channel in CHANNELS:
        try:
            member = await context.bot.get_chat_member(chat_id=channel["id"], user_id=user_id)
            if member.status not in ['member', 'administrator', 'creator']:
                return False
        except:
            return False
    return True

# Обработка кнопки
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id

    if await check_subscription(user_id, context):
        await query.edit_message_text(
            "✅ Отлично! Ты подписан.\n\n"
            "Теперь введи **код из TikTok-видео**, чтобы найти аниме."
        )
        context.user_data['allowed'] = True
    else:
        buttons = [
            [{"text": "📌 Подписаться", "url": ch["url"]}] for ch in CHANNELS
        ]
        buttons.append([{"text": "✅ Проверить подписку", "callback_data": "check_sub"}])
        reply_markup = {"inline_keyboard": buttons}
        await query.edit_message_text(
            "❌ Подпишись на все каналы, чтобы получить доступ.",
            reply_markup=reply_markup
        )

# Обработка сообщения
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.user_data.get('allowed', False):
        await update.message.reply_text(
            "Сначала подпишись на каналы! Нажми /start"
        )
        return

    code = update.message.text.strip().upper()
    if code in CODES:
        film = CODES[code]
        await update.message.reply_text(
            f"🎉 Поздравляю!\n\n"
            f"🎬 Название аниме по коду `{code}` — это:\n\n"
            f"📌 *{film}*\n\n"
            parse_mode="Markdown"
        )
    else:
        await update.message.reply_text(
            "❌ Неверный код. Проверь, правильно ли ты его переписал из видео."
        )

# Запуск
def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("✅ Бот запущен")
    app.run_polling()

if __name__ == '__main__':
    main()
