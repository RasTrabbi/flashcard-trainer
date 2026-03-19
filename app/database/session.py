from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from pathlib import Path
from app.models.db_models import Base

# __file__ — путь к текущему файлу (session.py)
# resolve() — превращает путь в абсолютный (полный путь в системе)
# parent — берет папку, в которой лежит файл (app/database)
BASE_DIR = Path(__file__).resolve().parent

# формируем путь к файлу базы данных внутри папки database
# оператор "/" в Path — безопасное объединение путей
db_path = BASE_DIR / "flashcard.db"

# подключение к базе
engine = create_engine(f"sqlite:///{db_path}")

# фабрика сессий
SessionLocal = sessionmaker(bind=engine)

# создание таблиц
Base.metadata.create_all(engine)
