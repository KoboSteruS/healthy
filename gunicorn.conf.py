"""
Конфигурация Gunicorn для запуска Flask приложения
"""
import multiprocessing
import os

# Создаем папку для логов, если её нет
os.makedirs('logs', exist_ok=True)

# Количество воркеров (рекомендуется: количество CPU * 2 + 1)
workers = multiprocessing.cpu_count() * 2 + 1

# Класс воркера
worker_class = 'sync'

# Таймауты
timeout = 120
keepalive = 5

# Биндинг
bind = f"0.0.0.0:{os.environ.get('PORT', '5000')}"

# Логирование
accesslog = 'logs/gunicorn_access.log'
errorlog = 'logs/gunicorn_error.log'
loglevel = os.environ.get('LOG_LEVEL', 'info')

# Перезагрузка при изменении кода (только для разработки)
reload = os.environ.get('FLASK_ENV') == 'development'

# Имя приложения
proc_name = 'zdoroviy_par'

# Предзагрузка приложения для лучшей производительности
preload_app = True

# Максимальное количество запросов на воркер перед перезапуском
max_requests = 1000
max_requests_jitter = 50

