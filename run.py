"""
Скрипт для запуска Flask приложения и Telegram бота одновременно
"""
import os
import threading
import time
from loguru import logger

# Импортируем Flask приложение
from app import app

# Импортируем бота
from bot import run_bot


def run_flask():
    """Запускает Flask приложение"""
    os.makedirs('logs', exist_ok=True)
    logger.info("Запуск Flask приложения...")
    app.run(
        host='0.0.0.0',
        port=5001,
        debug=os.environ.get('FLASK_ENV') == 'development',
        use_reloader=False  # Отключаем автоперезагрузку, чтобы не конфликтовать с ботом
    )


def run_telegram_bot():
    """Запускает Telegram бота"""
    time.sleep(2)  # Небольшая задержка перед запуском бота
    run_bot()


if __name__ == '__main__':
    # Настройка логирования
    logger.add(
        "logs/run.log",
        rotation="10 MB",
        retention="10 days",
        level="INFO",
        format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}"
    )
    
    # Запускаем бота в отдельном потоке
    bot_thread = threading.Thread(target=run_telegram_bot, daemon=True)
    bot_thread.start()
    
    # Запускаем Flask приложение в основном потоке
    run_flask()
