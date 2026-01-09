"""
Flask приложение для лендинга "Здоровый Пар"
"""
from flask import Flask, render_template, request, jsonify, send_from_directory
from loguru import logger
import os
from typing import Dict, Any
from telegram_service import TelegramService

app = Flask(
    __name__,
    template_folder='templates',
    static_folder='static'
)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')

# Настройка логирования
logger.add(
    "logs/app.log",
    rotation="10 MB",
    retention="10 days",
    level="INFO",
    format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}"
)

# Инициализация Telegram сервиса
TELEGRAM_BOT_TOKEN = os.environ.get(
    'TELEGRAM_BOT_TOKEN', 
    '8494693569:AAF5j_0AdDktzqyptK2_lygLlN-dgQra-wY'
)
telegram_service = TelegramService(TELEGRAM_BOT_TOKEN)


@app.route('/')
def index():
    """Главная страница лендинга"""
    return render_template('index.html')


@app.route('/static/<path:filename>')
def static_files(filename):
    """Обработка статических файлов"""
    return send_from_directory(app.static_folder, filename)


@app.route('/api/order', methods=['POST'])
def create_order():
    """
    Обработка формы заказа
    
    Принимает данные заказа и отправляет их (например, в Telegram бот)
    """
    try:
        data: Dict[str, Any] = request.get_json()
        
        # Валидация данных
        required_fields = ['name', 'phone', 'product', 'quantity']
        for field in required_fields:
            if not data.get(field):
                return jsonify({
                    'success': False,
                    'error': f'Поле {field} обязательно для заполнения'
                }), 400
        
        # Логирование заказа
        logger.info(f"Новый заказ: {data}")
        
        # Отправка заявки в Telegram бот
        try:
            telegram_sent = telegram_service.send_order_notification(data)
            if telegram_sent:
                logger.info("Заявка успешно отправлена в Telegram")
            else:
                logger.warning("Не удалось отправить заявку в Telegram (нет подписчиков)")
        except Exception as e:
            logger.error(f"Ошибка при отправке заявки в Telegram: {e}")
            # Не прерываем выполнение, заявка все равно считается принятой
        
        return jsonify({
            'success': True,
            'message': 'Заявка успешно отправлена! Мы свяжемся с вами в ближайшее время.'
        }), 200
        
    except Exception as e:
        logger.error(f"Ошибка при обработке заказа: {e}")
        return jsonify({
            'success': False,
            'error': 'Произошла ошибка при отправке заявки. Попробуйте позже.'
        }), 500


if __name__ == '__main__':
    # Создаем папку для логов
    os.makedirs('logs', exist_ok=True)
    
    # Запуск приложения
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=os.environ.get('FLASK_ENV') == 'development'
    )

