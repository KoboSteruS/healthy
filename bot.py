"""
Telegram бот для сбора заявок
Обрабатывает команду /start и сохраняет chat_id
"""
import json
import os
import time
from typing import List
from loguru import logger
import telebot
from dotenv import load_dotenv

# Загружаем переменные окружения
load_dotenv()

# Токен бота
BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN', '8494693569:AAF5j_0AdDktzqyptK2_lygLlN-dgQra-wY')
CHAT_IDS_FILE = 'chat_ids.json'

# Создаем экземпляр бота
bot = telebot.TeleBot(BOT_TOKEN)


def ensure_chat_ids_file():
    """Создает файл для хранения chat_id, если его нет"""
    if not os.path.exists(CHAT_IDS_FILE):
        with open(CHAT_IDS_FILE, 'w', encoding='utf-8') as f:
            json.dump([], f)


def get_chat_ids() -> List[int]:
    """Получает список всех сохраненных chat_id"""
    try:
        with open(CHAT_IDS_FILE, 'r', encoding='utf-8') as f:
            chat_ids = json.load(f)
            return list(set(chat_ids))
    except (FileNotFoundError, json.JSONDecodeError) as e:
        logger.error(f"Ошибка при чтении chat_ids: {e}")
        return []


def add_chat_id(chat_id: int):
    """Добавляет новый chat_id в список"""
    try:
        chat_ids = get_chat_ids()
        if chat_id not in chat_ids:
            chat_ids.append(chat_id)
            with open(CHAT_IDS_FILE, 'w', encoding='utf-8') as f:
                json.dump(chat_ids, f, indent=2)
            logger.info(f"Добавлен новый chat_id: {chat_id}")
            return True
        return False
    except Exception as e:
        logger.error(f"Ошибка при добавлении chat_id: {e}")
        return False


@bot.message_handler(commands=['start'])
def handle_start(message):
    """Обработчик команды /start"""
    chat_id = message.chat.id
    
    # Добавляем chat_id в список
    is_new = add_chat_id(chat_id)
    
    if is_new:
        response_text = (
            "✅ Вы успешно подписаны на получение заявок!\n\n"
            "Теперь все заявки с сайта будут приходить сюда."
        )
    else:
        response_text = (
            "✅ Вы уже подписаны на получение заявок.\n\n"
            "Все заявки с сайта будут приходить сюда."
        )
    
    bot.reply_to(message, response_text)
    logger.info(f"Обработана команда /start от chat_id: {chat_id}")


@bot.message_handler(commands=['status'])
def handle_status(message):
    """Проверка статуса подписки"""
    chat_id = message.chat.id
    chat_ids = get_chat_ids()
    
    if chat_id in chat_ids:
        response_text = f"✅ Вы подписаны на получение заявок.\n\nВаш chat_id: {chat_id}"
    else:
        response_text = (
            "❌ Вы не подписаны на получение заявок.\n\n"
            "Отправьте /start для подписки."
        )
    
    bot.reply_to(message, response_text)


@bot.message_handler(func=lambda message: True)
def handle_all_messages(message):
    """Обработчик всех остальных сообщений"""
    bot.reply_to(
        message,
        "Я бот для сбора заявок с сайта.\n\n"
        "Доступные команды:\n"
        "/start - подписаться на получение заявок\n"
        "/status - проверить статус подписки"
    )


def run_bot():
    """Запускает бота"""
    # Создаем папку для логов, если её нет
    os.makedirs('logs', exist_ok=True)
    
    # Настройка логирования
    logger.add(
        "logs/bot.log",
        rotation="10 MB",
        retention="10 days",
        level="INFO",
        format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}"
    )
    
    # Создаем файл для chat_id, если его нет
    ensure_chat_ids_file()
    
    logger.info("Запуск Telegram бота...")
    
    try:
        # Получаем информацию о боте
        bot_info = bot.get_me()
        logger.info(f"Бот запущен: @{bot_info.username}")
        
        # Запускаем бота
        bot.infinity_polling(timeout=10, long_polling_timeout=5)
    except Exception as e:
        logger.error(f"Ошибка при запуске бота: {e}")
        raise


if __name__ == '__main__':
    run_bot()
