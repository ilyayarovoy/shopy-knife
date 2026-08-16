# Функциональность избранного (Favorites)

## Обзор

Добавлена полная система управления избранными товарами. Пользователи могут добавлять товары в избранное, удалять их, просматривать список и проверять, находится ли товар в избранном.

## Созданные компоненты

### 1. База данных

**Модель `FavoriteModel`** (`backend/database/models.py`):
- `id` - первичный ключ
- `user_id` - внешний ключ на таблицу users (CASCADE delete)
- `product_id` - внешний ключ на таблицу products (CASCADE delete)
- `created_at` - временная метка создания
- **Уникальное ограничение** на пару (user_id, product_id) — предотвращает дубли

**Миграция** (`alembic/versions/2026_08_16_add_favorites.py`):
- Создает таблицу `favorites` с нужной структурой
- Поддерживает откат (`downgrade`)

### 2. Слой данных

**Репозиторий** (`backend/repositories/favorite_repo.py`):
- `get_user_favorites(user_id)` - получить все избранные товары пользователя
- `get_favorite_by_id(favorite_id)` - получить элемент по ID
- `get_favorite_by_user_and_product(user_id, product_id)` - проверка существования
- `add_to_favorites(user_id, product_id)` - добавить в избранное (обрабатывает дубли)
- `remove_from_favorites(item)` - удалить из избранного
- `is_favorite(user_id, product_id)` - boolean проверка

Все методы асинхронные и используют `selectinload` для оптимизации запросов.

### 3. Бизнес-логика

**Сервис** (`backend/services/favorite_service.py`):
- `get_user_favorites_service(user_id)` - получить с полной информацией о товарах
- `add_to_favorites_service(user_id, product_id)` - добавить с проверкой существования товара
- `remove_from_favorites_service(item_id, user_id)` - удалить с проверкой прав доступа
- `is_favorite_service(user_id, product_id)` - проверить наличие

### 4. API схемы

**Pydantic модели** (`backend/api/schemas/favorite_schemas.py`):
- `AddToFavoritesSchema` - input для добавления (только product_id)
- `FavoriteItemResponseSchema` - single item response
- `FavoritesResponseSchema` - list response с total_count
- `IsFavoriteResponseSchema` - boolean response

### 5. REST API эндпоинты

**Роутер** (`backend/api/routers/favorites.py`, регистрация в `main.py`):

#### GET /api/favorites/user/{user_id}
Получить все избранные товары пользователя.

**Response (200):**
```json
{
  "items": [
    {
      "id": 1,
      "user_id": 123,
      "product_id": 5,
      "product": {
        "id": 5,
        "category_id": 2,
        "title": "Kitchen Knife",
        "price": 99.99,
        "description": "Professional knife",
        "images": ["url1", "url2"]
      },
      "created_at": "2026-08-16T10:30:00"
    }
  ],
  "total_count": 1
}
```

#### POST /api/favorites/user/{user_id}/add
Добавить товар в избранное.

**Request:**
```json
{
  "product_id": 5
}
```

**Response (201):**
```json
{
  "id": 1,
  "user_id": 123,
  "product_id": 5,
  "product": { ... },
  "created_at": "2026-08-16T10:30:00"
}
```

**Ошибки:**
- 404: Товар не найден

#### DELETE /api/favorites/user/{user_id}/item/{item_id}
Удалить товар из избранного.

**Response (204):** No Content

**Ошибки:**
- 404: Элемент избранного не найден
- 403: Элемент не принадлежит пользователю

#### GET /api/favorites/user/{user_id}/check/{product_id}
Проверить, находится ли товар в избранном пользователя.

**Response (200):**
```json
{
  "is_favorite": true
}
```

## Тесты

**Файл** (`tests/test_favorites.py`) содержит 10 тестов:

1. `test_add_to_favorites` - добавление товара
2. `test_add_to_favorites_product_not_found` - обработка несуществующего товара
3. `test_add_duplicate_to_favorites` - добавление одного товара дважды
4. `test_get_user_favorites` - получение списка
5. `test_get_user_favorites_empty` - пустой список
6. `test_remove_from_favorites` - удаление товара
7. `test_remove_from_favorites_item_not_found` - обработка несуществующего элемента
8. `test_is_product_favorite` - проверка наличия товара
9. `test_is_product_favorite_not_added` - проверка отсутствия
10. `test_remove_favorite_wrong_user` - защита от удаления чужого элемента

## Особенности реализации

1. **Уникальность** - уникальное ограничение на пару (user_id, product_id) предотвращает дубли
2. **Асинхронность** - всё асинхронное, совместимо с asyncpg
3. **Оптимизация** - используется `selectinload` для подгрузки related данных
4. **Защита** - проверка прав доступа при удалении (403 если не owner)
5. **Симметрия** - архитектура аналогична корзине для легкой поддержки
6. **Валидация** - Pydantic валидирует все входные данные

## Использование в фронтенде

```javascript
// Получить избранные товары
GET /api/favorites/user/123

// Добавить в избранное
POST /api/favorites/user/123/add
Body: { "product_id": 5 }

// Проверить, в избранном ли
GET /api/favorites/user/123/check/5

// Удалить из избранного
DELETE /api/favorites/user/123/item/1
```

## Миграция БД

Миграция запустится автоматически при старте приложения (через Alembic в lifespan).

Если нужно откатить:
```bash
alembic downgrade -1
```

Если нужно применить все миграции:
```bash
alembic upgrade head
```
