# Telegram Notifications — Реализация

## ✅ Что было сделано

Добавлена система отправки Telegram-уведомлений при создании заказа через прямые HTTP-запросы к Telegram Bot API (без использования aiogram в этом проекте).

## 📁 Созданные файлы

1. **`backend/config.py`** — конфигурация для загрузки TELEGRAM_BOT_TOKEN из .env
2. **`backend/services/telegram_service.py`** — сервис отправки сообщений через Telegram Bot API

## ✏️ Изменённые файлы

1. **`.env`** — добавлена переменная TELEGRAM_BOT_TOKEN
2. **`backend/repositories/user_repo.py`** — добавлен метод `get_user_by_id(user_id)`
3. **`backend/api/routers/orders.py`** — добавлена отправка уведомления при checkout через BackgroundTasks
4. **`backend/services/order_service.py`** — изменён `update_order_status_service()` для поддержки bot callback без проверки владельца

## 🎯 Новый функционал

### 1. Отправка уведомления при создании заказа

**POST `/api/orders/user/{user_id}/checkout`** теперь:
1. Создаёт заказ в БД
2. Отправляет Telegram-уведомление пользователю в фоне (через BackgroundTasks)
3. Уведомление содержит:
   - Номер заказа
   - Сумму заказа
   - Inline-кнопку "Подтвердить"

**Пример сообщения:**
```
Вы оформили заказ №123 на сумму 1499.99 ₽
[Кнопка: Подтвердить]
```

**Inline-клавиатура:**
```json
{
  "inline_keyboard": [
    [
      {
        "text": "Подтвердить",
        "callback_data": "confirm_order:123"
      }
    ]
  ]
}
```

### 2. Эндпоинт подтверждения заказа

**PATCH `/api/orders/{order_id}/confirm`** — подтверждает заказ (меняет статус на "confirmed").

Этот эндпоинт предназначен для вызова из отдельного aiogram-проекта при нажатии кнопки "Подтвердить".

**Response (200):**
```json
{
  "id": 123,
  "user_id": 456,
  "total_price": 1499.99,
  "status": "confirmed",
  "created_at": "2026-08-17T18:00:00"
}
```

**Ошибки:**
- 404: Order not found
- 400: Ошибка обновления статуса

## 🔧 Технические детали

### Telegram Service

**Функция `send_telegram_message(chat_id, text, reply_markup)`:**
- Использует `httpx.AsyncClient` для HTTP-запросов
- URL: `https://api.telegram.org/bot{TOKEN}/sendMessage`
- Таймаут: 10 секунд
- Обработка ошибок:
  - 403 Forbidden → пользователь заблокировал бота (логируется warning)
  - Другие HTTP ошибки → логируются как error
  - Сетевые ошибки → логируются как error
- **Не роняет создание заказа** — все ошибки ловятся через try/except

### BackgroundTasks

Отправка сообщения происходит в фоне через FastAPI BackgroundTasks:
- Ответ клиенту приходит сразу после создания заказа
- Telegram-запрос выполняется асинхронно после отправки ответа
- Задержка для клиента: 0ms (неблокирующий режим)

### Использование tg_id как chat_id

В модели `UserModel` есть поле `tg_id` (Telegram user ID). Для личных чатов `tg_id == chat_id`, поэтому используется напрямую без миграции БД.

### Безопасность

**Проверка владельца заказа:**
- Обычное обновление статуса (`PUT /orders/{order_id}/user/{user_id}/status`) — проверяет `user_id`
- Подтверждение из бота (`PATCH /orders/{order_id}/confirm`) — пропускает проверку (`user_id=None`)

## 📝 Конфигурация

### .env
```env
DATABASE_URL=postgresql://...
TELEGRAM_BOT_TOKEN=your_bot_token_here
```

Замените `your_bot_token_here` на реальный токен от @BotFather.

### requirements.txt
```
httpx  # уже было в проекте
```

## 🚀 Интеграция с aiogram-ботом

В отдельном aiogram-проекте нужно добавить обработчик callback:

```python
@dp.callback_query(lambda c: c.data.startswith("confirm_order:"))
async def confirm_order_callback(callback: CallbackQuery):
    order_id = callback.data.split(":")[1]
    
    # Вызвать API бэкенда
    async with httpx.AsyncClient() as client:
        response = await client.patch(f"http://backend:8000/api/orders/{order_id}/confirm")
    
    if response.status_code == 200:
        await callback.answer("Заказ подтверждён!")
        await callback.message.edit_text(
            callback.message.text + "\n\n✅ Заказ подтверждён"
        )
    else:
        await callback.answer("Ошибка подтверждения", show_alert=True)
```

## 🧪 Тестирование

### Ручное тестирование

1. Запустить backend:
```bash
python main.py
```

2. Добавить товары в корзину:
```bash
POST /api/cart/user/123/add
{"product_id": 5, "quantity": 2}
```

3. Оформить заказ:
```bash
POST /api/orders/user/123/checkout
```

4. Проверить Telegram — должно прийти сообщение с кнопкой "Подтвердить"

### Логирование

Все ошибки отправки логируются:
```python
logger.error(f"Failed to send Telegram message to {chat_id}: {error}")
```

Проверить логи можно в консоли приложения.

## ⚠️ Важные замечания

1. **Не импортировать aiogram** — весь Telegram функционал через httpx
2. **Не делать polling** — отправка синхронная в момент checkout
3. **BackgroundTasks** — отправка не блокирует ответ клиенту
4. **Обработка ошибок** — если пользователь заблокировал бота, заказ всё равно создаётся
5. **chat_id = tg_id** — для личных чатов они равны

## 🎯 Статусы заказов

- `new` — создан, ожидает подтверждения
- `confirmed` — подтверждён через Telegram
- `processing` — в обработке
- (другие статусы можно добавить по необходимости)

## 📊 Архитектура

```
Next.js Frontend
    ↓ POST /checkout
FastAPI Backend (orders.py)
    ↓ await checkout_service()
Order created in DB
    ↓ background_tasks.add_task()
Telegram Bot API (sendMessage)
    ↓
User's Telegram
    [Click "Подтвердить"]
    ↓ callback_data
Aiogram Bot (отдельный проект)
    ↓ PATCH /orders/{id}/confirm
FastAPI Backend
    ↓ update_order_status_service(status="confirmed")
Order status updated
```

Реализация завершена и готова к использованию!
