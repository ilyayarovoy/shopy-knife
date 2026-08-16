# Order (Checkout) System — Реализация

## ✅ Что было сделано

Добавлена полная система оформления заказов для Shopy Knife API.

## 📁 Созданные файлы

1. **`backend/repositories/order_repo.py`** — слой доступа к заказам
2. **`backend/services/order_service.py`** — бизнес-логика checkout
3. **`backend/api/schemas/order_schemas.py`** — Pydantic модели
4. **`backend/api/routers/orders.py`** — REST API эндпоинты
5. **`tests/test_orders.py`** — 10 тестов функциональности

## ✏️ Изменённые файлы

- **`main.py`** — добавлена регистрация Order Router
- **`tests/test_cart.py`** — исправлены пути в тестах (добавлен user_id)
- **`backend/requirements.txt`** — добавлены pytest, pytest-asyncio, httpx, aiosqlite

## 🎯 API Эндпоинты

### POST `/api/orders/user/{user_id}/checkout`
Оформить заказ из корзины пользователя.

**Алгоритм:**
1. Получить все товары из Cart
2. Проверить stock для каждого товара
3. Рассчитать total_price
4. Создать запись Order
5. Уменьшить stock товаров
6. Очистить корзину

**Response (201):**
```json
{
  "id": 1,
  "user_id": 123,
  "total_price": 299.97,
  "status": "new",
  "created_at": "2026-08-16T15:30:00"
}
```

**Ошибки:**
- 400: Cart is empty / Not enough stock

### GET `/api/orders/user/{user_id}`
Получить все заказы пользователя.

**Response (200):**
```json
{
  "items": [
    {
      "id": 1,
      "user_id": 123,
      "total_price": 299.97,
      "status": "new",
      "created_at": "2026-08-16T15:30:00"
    }
  ],
  "total_count": 1
}
```

### GET `/api/orders/{order_id}`
Получить заказ по ID.

**Response (200):** OrderResponseSchema

### PUT `/api/orders/{order_id}/user/{user_id}/status`
Обновить статус заказа (only owner).

**Request:**
```json
{
  "status": "processing"
}
```

**Response (200):** OrderResponseSchema

**Ошибки:**
- 403: Forbidden (не owner)
- 404: Order not found

## 🧪 Тесты

```bash
python -m pytest tests/test_orders.py -v
```

Покрытие:
- ✅ Успешное оформление заказа
- ✅ Пустая корзина (error)
- ✅ Недостаточно stock (error)
- ✅ Получение заказов пользователя
- ✅ Пустой список заказов
- ✅ Получение заказа по ID
- ✅ Заказ не найден (404)
- ✅ Обновление статуса
- ✅ Попытка обновить чужой заказ (403)
- ✅ Проверка что stock уменьшился после checkout

## 🔄 Frontend Integration

```javascript
// 1. Добавить товары в корзину (существует)
POST /api/cart/user/123/add
{ "product_id": 5, "quantity": 2 }

// 2. Оформить заказ
POST /api/orders/user/123/checkout
// Корзина автоматически очищается

// 3. Получить заказы
GET /api/orders/user/123

// 4. Отследить статус (опционально)
PUT /api/orders/1/user/123/status
{ "status": "processing" }
```

## 🏗️ Архитектура

**Слои:**
```
Router (API)
    ↓
Service (бизнес-логика)
    ├→ OrderRepository (CRUD)
    ├→ CartRepository (получение товаров)
    └→ ProductRepository (обновление stock)
    ↓
Repository (БД)
    ↓
Models (OrderModel)
```

**Зависимости:**
- OrderModel (существует в models.py)
- CartItemModel (существует)
- ProductModel (существует)

## 📝 Особенности

1. **Транзакционность** — все операции в одной БД транзакции
2. **Валидация** — проверка stock перед созданием Order
3. **Безопасность** — пользователь может изменить только свой заказ (403 Forbidden)
4. **Асинхронность** — полностью async для asyncpg
5. **Масштабируемость** — легко добавить новые статусы или поля

## 🚀 Запуск приложения

```bash
python main.py
```

Эндпоинты доступны:
- http://localhost:8000/api/orders/user/{user_id}/checkout
- http://localhost:8000/api/orders/user/{user_id}
- http://localhost:8000/api/orders/{order_id}
- И другие...

Swagger UI: http://localhost:8000/docs
