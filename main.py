import logging
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
import models
import database
from routers import users, games

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    filename="app.log",
    format="%(asctime)s - %(levelname)s - %(message)s",
)

logger = logging.getLogger(__name__)

# Создание таблиц в базе данных
models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

# Подключение роутеров
app.include_router(users.router)
app.include_router(games.router)

@app.get("/")
def read_root():
    logger.info("Root endpoint accessed")
    return {"message": "Welcome to the Casino API"}