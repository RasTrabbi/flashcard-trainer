from app.models.db_models import WordDB
from app.repositories.word_repository import  get_learning_words_batch, get_review_words_batch

def test_get_learning_words_only_not_learned(session):
    # Arrange
    w1 = WordDB(en="a", ru="a", topic="t")
    w1.score = 5

    w2 = WordDB(en="b", ru="b", topic="t")
    w2.score = 10

    session.add_all([w1, w2])
    session.commit()

    # Act
    result = get_learning_words_batch(session, limit=10)

    # Assert
    # должны быть только слова со score < 10
    assert len(result) == 1
    assert result[0].score < 10

def test_get_review_words_only_learned(session):
    # Arrange
    w1 = WordDB(en="a", ru="a", topic="t")
    w1.score = 5

    w2 = WordDB(en="b", ru="b", topic="t")
    w2.score = 10

    session.add_all([w1, w2])
    session.commit()

    # Act
    result = get_review_words_batch(session, limit=10)

    # Assert — только score == 10
    assert len(result) == 1
    assert result[0].score == 10

def test_get_learning_words_respects_limit(session):
    # Arrange — создаём 5 слов
    words = []
    for i in range(5):
        w = WordDB(en=str(i), ru=str(i), topic="t")
        w.score = 5
        words.append(w)

    session.add_all(words)
    session.commit()

    # Act
    result = get_learning_words_batch(session, limit=2)

    # Assert — должно вернуть ровно 2
    assert len(result) == 2

def test_get_learning_words_by_topic(session):
    # Arrange
    w1 = WordDB(en="a", ru="a", topic="food")
    w1.score = 5

    w2 = WordDB(en="b", ru="b", topic="tech")
    w2.score = 5

    session.add_all([w1, w2])
    session.commit()

    # Act — фильтр по topic
    result = get_learning_words_batch(session, limit=10, topic="food")

    # Assert — только нужная тема
    assert len(result) == 1
    assert result[0].topic == "food"

def test_get_learning_words_empty(session):
    # Arrange
    w = WordDB(en="a", ru="a", topic="t")
    w.score = 10

    session.add(w)
    session.commit()

    # Act
    result = get_learning_words_batch(session, limit=10)

    # Assert — ничего не найдено
    assert result == []