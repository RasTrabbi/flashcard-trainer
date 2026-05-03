import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models.db_models import Base

# TEST DB (in-memory - база в RAM, исчезает после тестов)
engine = create_engine('sqlite:///:memory:')

TestingSessionLocal = sessionmaker(bind=engine)

@pytest.fixture
def session():
    # создаём таблицы перед тестом
    Base.metadata.create_all(engine)

    db = TestingSessionLocal()

    yield db # отдаём session в тест

    db.close()

    # Отчищаем после теста
    Base.metadata.drop_all(engine)