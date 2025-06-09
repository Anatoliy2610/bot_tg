from dotenv import load_dotenv
import os

from telegram import Update
from telegram.ext import CommandHandler, CallbackQueryHandler

from app.posts.models import PostModel

from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

from app.database import SessionLocal
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup


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
    for post in posts:
        keyboard.append([
            InlineKeyboardButton(post.title, callback_data=str(post.id))
        ])
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Все посты:", reply_markup=reply_markup)


async def show_post_details(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    post_id = int(query.data)
    
    session = SessionLocal()
    post = session.query(PostModel).filter(PostModel.id == post_id).first()
    session.close()

    if post:
        await query.edit_message_text(text=f"Название: {post.title}\n\nСодержание: {post.content}\n\nПост создан: {post.created_at}")
    else:
        await query.edit_message_text(text="Пост не найден")


if __name__ == '__main__':
    application = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('posts', get_posts))
    application.add_handler(CallbackQueryHandler(show_post_details))
    application.run_polling()
