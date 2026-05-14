import asyncio
import os
import uvicorn
from fastapi import FastAPI
from aiogram import Bot, Dispatcher

app = FastAPI()


@app.get("/")
async def root():
    return {"status": "ok", "message": "Knife Shop API is running"}



# 3. Главная функция запуска
async def main():
    # Берем порт, который дает Render
    port = int(os.environ.get("PORT", 8000))

    # Настройка сервера
    config = uvicorn.Config(app, host="0.0.0.0", port=port)
    server = uvicorn.Server(config)

    # Запускаем сервер и бота одновременно
    await asyncio.gather(
        server.serve()
    )


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        print("Приложение остановлено")