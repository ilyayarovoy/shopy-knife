FROM python:3.10-slim

WORKDIR /app

# Копируем сначала файлы зависимостей из папки backend
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем всё остальное содержимое репозитория
COPY . .

# Команда для запуска (указываем путь к твоему main.py)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "7860"]