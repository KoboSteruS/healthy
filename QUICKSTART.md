# Быстрый старт

## 1. Установка зависимостей

### Python
```bash
python -m venv venv
venv\Scripts\activate  # Windows
# или source venv/bin/activate  # Linux/Mac
pip install -r requirements.txt
```

## 2. Запуск приложения

```bash
python app.py
```

## 3. Откройте в браузере

- http://localhost:5000

## Структура проекта

```
├── app.py              # Flask приложение
├── templates/          # HTML шаблоны
├── static/            # CSS, JS, изображения
│   ├── css/
│   └── js/
└── logs/              # Логи приложения
```

## Проблемы?

1. **Порт занят**: Измените порт в `app.py`
2. **Модули не найдены**: Убедитесь, что виртуальное окружение активировано
3. **Статические файлы не загружаются**: Проверьте, что папка `static/` существует

