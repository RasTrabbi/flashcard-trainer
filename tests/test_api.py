from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from main import app
from app.database.session import get_db
from app.models.db_models import Base, WordDB


# тестовая SQLite в памяти
# StaticPool нужен, чтобы одна и та же in-memory БД жила во всех запросах TestClient
engine = create_engine(
    "sqlite://",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestSessionLocal = sessionmaker(bind=engine)


# подменяем get_db для FastAPI
def override_get_db():
    db = TestSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


def setup_function():
    # создаём чистые таблицы перед каждым тестом
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)


def test_create_word_endpoint():
    # Arrange — данные для создания слова
    payload = {
        "en": "apple",
        "ru": "яблоко",
        "topic": "food"
    }

    # Act — отправляем POST /words
    response = client.post("/words", json=payload)

    # Assert — проверяем статус и тело ответа
    assert response.status_code == 200

    data = response.json()
    assert data["en"] == "apple"
    assert data["ru"] == "яблоко"
    assert data["topic"] == "food"
    assert data["score"] == 0


def test_get_all_words_endpoint():
    # Arrange — создаём слово напрямую в тестовой БД
    db = TestSessionLocal()
    word = WordDB(en="apple", ru="яблоко", topic="food", score=0)
    db.add(word)
    db.commit()
    db.close()

    # Act — запрашиваем все слова
    response = client.get("/words")

    # Assert — должен вернуться список с одним словом
    assert response.status_code == 200

    data = response.json()
    assert len(data) == 1
    assert data[0]["en"] == "apple"


def test_get_word_by_id_endpoint():
    # Arrange — создаём слово
    db = TestSessionLocal()
    word = WordDB(en="apple", ru="яблоко", topic="food", score=0)
    db.add(word)
    db.commit()
    db.refresh(word)
    word_id = word.id
    db.close()

    # Act — запрашиваем слово по id
    response = client.get(f"/words/{word_id}")

    # Assert — должно вернуться нужное слово
    assert response.status_code == 200

    data = response.json()
    assert data["id"] == word_id
    assert data["en"] == "apple"


def test_get_word_by_id_not_found():
    # Act — запрашиваем несуществующее слово
    response = client.get("/words/999")

    # Assert — должен быть 404
    assert response.status_code == 404
    assert response.json()["detail"] == "Word not found"


def test_get_learning_words_endpoint():
    # Arrange — одно слово learning, одно review
    db = TestSessionLocal()

    w1 = WordDB(en="apple", ru="яблоко", topic="food", score=5)
    w2 = WordDB(en="table", ru="стол", topic="home", score=10)

    db.add_all([w1, w2])
    db.commit()
    db.close()

    # Act — запрашиваем learning batch
    response = client.get("/learning")

    # Assert — должны прийти только слова со score < 10
    assert response.status_code == 200

    data = response.json()
    assert len(data) == 1
    assert data[0]["score"] < 10
    assert data[0]["en"] == "apple"


def test_get_review_words_endpoint():
    # Arrange — одно слово learning, одно review
    db = TestSessionLocal()

    w1 = WordDB(en="apple", ru="яблоко", topic="food", score=5)
    w2 = WordDB(en="table", ru="стол", topic="home", score=10)

    db.add_all([w1, w2])
    db.commit()
    db.close()

    # Act — запрашиваем review batch
    response = client.get("/review")

    # Assert — должны прийти только слова со score == 10
    assert response.status_code == 200

    data = response.json()
    assert len(data) == 1
    assert data[0]["score"] == 10
    assert data[0]["en"] == "table"


def test_get_learning_words_by_topic():
    # Arrange — слова одной группы score, но разных topic
    db = TestSessionLocal()

    w1 = WordDB(en="apple", ru="яблоко", topic="food", score=5)
    w2 = WordDB(en="mouse", ru="мышь", topic="tech", score=5)

    db.add_all([w1, w2])
    db.commit()
    db.close()

    # Act — фильтруем по topic
    response = client.get("/learning", params={"topic": "food"})

    # Assert — должно вернуться только слово с нужной темой
    assert response.status_code == 200

    data = response.json()
    assert len(data) == 1
    assert data[0]["topic"] == "food"


def test_process_answer_endpoint_correct():
    # Arrange — создаём слово
    db = TestSessionLocal()
    word = WordDB(en="apple", ru="яблоко", topic="food", score=5)
    db.add(word)
    db.commit()
    db.refresh(word)
    word_id = word.id
    db.close()

    payload = {
        "word_id": word_id,
        "prompt_side": "ru",
        "user_answer": "apple"
    }

    # Act — отправляем ответ
    response = client.post("/answer", json=payload)

    # Assert — ответ правильный, score увеличен
    assert response.status_code == 200

    data = response.json()
    assert data["is_correct"] is True
    assert data["score"] == 6


def test_process_answer_endpoint_incorrect():
    # Arrange — создаём слово
    db = TestSessionLocal()
    word = WordDB(en="apple", ru="яблоко", topic="food", score=5)
    db.add(word)
    db.commit()
    db.refresh(word)
    word_id = word.id
    db.close()

    payload = {
        "word_id": word_id,
        "prompt_side": "ru",
        "user_answer": "banana"
    }

    # Act — отправляем неправильный ответ
    response = client.post("/answer", json=payload)

    # Assert — ответ неправильный, score уменьшен
    assert response.status_code == 200

    data = response.json()
    assert data["is_correct"] is False
    assert data["score"] == 4.5


def test_process_answer_endpoint_not_found():
    # Arrange — несуществующий word_id
    payload = {
        "word_id": 999,
        "prompt_side": "ru",
        "user_answer": "apple"
    }

    # Act — отправляем ответ
    response = client.post("/answer", json=payload)

    # Assert — слово не найдено
    assert response.status_code == 404
    assert response.json()["detail"] == "Word not found"


def test_delete_word_endpoint():
    # Arrange — создаём слово
    db = TestSessionLocal()
    word = WordDB(en="apple", ru="яблоко", topic="food", score=0)
    db.add(word)
    db.commit()
    db.refresh(word)
    word_id = word.id
    db.close()

    # Act — удаляем слово
    response = client.delete(f"/words/{word_id}")

    # Assert — 204 и слово реально удалено
    assert response.status_code == 204

    check_response = client.get(f"/words/{word_id}")
    assert check_response.status_code == 404


def test_delete_word_endpoint_not_found():
    # Act — удаляем несуществующее слово
    response = client.delete("/words/999")

    # Assert — должен быть 404
    assert response.status_code == 404
    assert response.json()["detail"] == "Word not found"