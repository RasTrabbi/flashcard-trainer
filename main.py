from fastapi import FastAPI
from app.api.word import router

# создаём приложение
app = FastAPI()

# подключаем обработчики запросов
app.include_router(router)