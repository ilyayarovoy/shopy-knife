import logging
import httpx
from backend.config import TELEGRAM_BOT_TOKEN

logger = logging.getLogger(__name__)


def format_order_message(order_data: dict) -> str:
    """
    Форматирует детальное сообщение о заказе для Telegram.

    Args:
        order_data: Данные заказа с items

    Returns:
        Отформатированный текст сообщения
    """
    order_id = order_data['id']
    total_price = float(order_data['total_price'])
    items = order_data.get('items', [])

    # Заголовок
    message = f"🛍 <b>Новый заказ #{order_id}</b>\n\n"

    # Список товаров
    if items:
        message += "<b>Состав заказа:</b>\n"
        for item in items:
            product = item['product']
            quantity = item['quantity']
            price = float(item['price_at_order'])
            item_total = price * quantity

            message += f"• {product['title']}\n"
            message += f"  {quantity} шт. × {price:.2f} ₽ = {item_total:.2f} ₽\n"
        message += "\n"

    # Итого
    message += f"<b>Итого:</b> {total_price:.2f} ₽\n\n"
    message += "Для подтверждения заказа нажмите кнопку ниже 👇"

    return message


async def send_telegram_message(
    chat_id: int,
    text: str,
    reply_markup: dict | None = None
):
    """
    Отправляет сообщение в Telegram через Bot API.

    Args:
        chat_id: Telegram chat ID пользователя
        text: Текст сообщения
        reply_markup: Inline-клавиатура (опционально)
    """
    if not TELEGRAM_BOT_TOKEN:
        logger.error("TELEGRAM_BOT_TOKEN not configured")
        return

    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"

    payload = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "HTML"
    }

    if reply_markup:
        payload["reply_markup"] = reply_markup

    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.post(url, json=payload)
            response.raise_for_status()
            logger.info(f"Telegram message sent successfully to chat_id={chat_id}")
    except httpx.HTTPStatusError as e:
        if e.response.status_code == 403:
            logger.warning(f"User {chat_id} blocked the bot or chat not found")
        else:
            logger.error(f"Failed to send Telegram message to {chat_id}: {e.response.status_code} - {e.response.text}")
    except httpx.RequestError as e:
        logger.error(f"Network error sending Telegram message to {chat_id}: {e}")
    except Exception as e:
        logger.error(f"Unexpected error sending Telegram message to {chat_id}: {e}")
