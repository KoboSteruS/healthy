"""
Сервис для работы с Telegram ботом
Отправка заявок в сохраненные chat_id
"""
import json
import os
from typing import List, Dict, Any
from loguru import logger
import requests


class TelegramService:
    """Сервис для отправки заявок в Telegram"""
    
    def __init__(self, bot_token: str, chat_ids_file: str = 'chat_ids.json'):
        self.bot_token = bot_token
        self.chat_ids_file = chat_ids_file
        self.api_url = f"https://api.telegram.org/bot{bot_token}"
        self._ensure_chat_ids_file()
    
    def _ensure_chat_ids_file(self):
        """Создает файл для хранения chat_id, если его нет"""
        if not os.path.exists(self.chat_ids_file):
            with open(self.chat_ids_file, 'w', encoding='utf-8') as f:
                json.dump([], f)
    
    def get_chat_ids(self) -> List[int]:
        """Получает список всех сохраненных chat_id"""
        try:
            with open(self.chat_ids_file, 'r', encoding='utf-8') as f:
                chat_ids = json.load(f)
                # Убираем дубликаты и возвращаем список
                return list(set(chat_ids))
        except (FileNotFoundError, json.JSONDecodeError) as e:
            logger.error(f"Ошибка при чтении chat_ids: {e}")
            return []
    
    def add_chat_id(self, chat_id: int):
        """Добавляет новый chat_id в список"""
        try:
            chat_ids = self.get_chat_ids()
            if chat_id not in chat_ids:
                chat_ids.append(chat_id)
                with open(self.chat_ids_file, 'w', encoding='utf-8') as f:
                    json.dump(chat_ids, f, indent=2)
                logger.info(f"Добавлен новый chat_id: {chat_id}")
        except Exception as e:
            logger.error(f"Ошибка при добавлении chat_id: {e}")
    
    def send_order_notification(self, order_data: Dict[str, Any]) -> bool:
        """
        Отправляет уведомление о заказе во все сохраненные chat_id
        
        Args:
            order_data: Словарь с данными заказа
            
        Returns:
            True если хотя бы одно сообщение отправлено успешно
        """
        chat_ids = self.get_chat_ids()
        
        if not chat_ids:
            logger.warning("Нет сохраненных chat_id для отправки заявок")
            return False
        
        # Формируем сообщение о заказе
        message = self._format_order_message(order_data)
        
        success_count = 0
        for chat_id in chat_ids:
            try:
                response = requests.post(
                    f"{self.api_url}/sendMessage",
                    json={
                        'chat_id': chat_id,
                        'text': message,
                        'parse_mode': 'HTML'
                    },
                    timeout=10
                )
                
                if response.status_code == 200:
                    success_count += 1
                    logger.info(f"Заявка отправлена в chat_id: {chat_id}")
                else:
                    error_data = response.json()
                    logger.warning(
                        f"Не удалось отправить в chat_id {chat_id}: "
                        f"{error_data.get('description', 'Unknown error')}"
                    )
                    
            except Exception as e:
                logger.error(f"Ошибка при отправке в chat_id {chat_id}: {e}")
        
        return success_count > 0
    
    def _format_order_message(self, order_data: Dict[str, Any]) -> str:
        """Форматирует данные заказа в сообщение для Telegram"""
        product_names = {
            'birch': 'Берёзовый веник',
            'juniper': 'Можжевеловый веник',
            'canadian_oak': 'Канадский дубовый веник',
            'oak': 'Дуб классический веник'
        }
        
        product_name = product_names.get(
            order_data.get('product', ''), 
            order_data.get('product', 'Неизвестный товар')
        )
        
        message = (
            "🆕 <b>Новая заявка с сайта</b>\n\n"
            f"👤 <b>Имя:</b> {order_data.get('name', 'Не указано')}\n"
            f"📞 <b>Телефон:</b> {order_data.get('phone', 'Не указан')}\n"
            f"📦 <b>Товар:</b> {product_name}\n"
            f"🔢 <b>Количество:</b> {order_data.get('quantity', 'Не указано')} шт.\n"
        )
        
        if order_data.get('comment'):
            message += f"💬 <b>Комментарий:</b> {order_data.get('comment')}\n"
        
        return message
