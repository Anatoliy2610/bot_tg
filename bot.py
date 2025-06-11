import os

from dotenv import load_dotenv
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (ApplicationBuilder, CallbackQueryHandler,
                          CommandHandler, ContextTypes)

from app.database import SessionLocal
from app.posts.models import PostModel

load_dotenv()
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Добро пожаловать!")
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Введите команду /posts, чтобы просмотреть список всех постов.")


async def get_posts(update: Update, context: ContextTypes.DEFAULT_TYPE):
    session = SessionLocal()
    posts = session.query(PostModel).all()
    session.close()
    keyboard = []
    for i in range(0, len(posts), 2):
        row = []
        row.append(InlineKeyboardButton(posts[i].title, callback_data=str(posts[i].id)))
        if i + 1 < len(posts):
            row.append(InlineKeyboardButton(posts[i + 1].title, callback_data=str(posts[i + 1].id)))
        keyboard.append(row)
    reply_markup = InlineKeyboardMarkup(keyboard)
    if update.message:
        await update.message.reply_text("Все посты:", reply_markup=reply_markup)
    else:
        await update.callback_query.answer()
        await update.callback_query.edit_message_text("Все посты:", reply_markup=reply_markup)


async def handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data
    if data != "back_to_posts":
        post_id = int(query.data)
        session = SessionLocal()
        post = session.query(PostModel).filter(PostModel.id == post_id).first()
        session.close()
        if post:
            back_button = InlineKeyboardButton("Вернуться к постам", callback_data="back_to_posts")
            reply_markup = InlineKeyboardMarkup([[back_button]])
            await query.edit_message_text(text=f"Название: {post.title}\n\nСодержание: {post.content}\n\nПост создан: {post.created_at}", reply_markup=reply_markup)
        else:
            await query.edit_message_text(text="Пост не найден")
    else:
        await get_posts(update, context)


if __name__ == '__main__':
    application = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('posts', get_posts))
    application.add_handler(CallbackQueryHandler(handler))
    application.run_polling()
