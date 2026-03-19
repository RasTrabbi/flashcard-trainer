import random

from sqlalchemy.orm import Session
from sqlalchemy import select, delete

from app.models.db_models import WordDB

def get_word_by_id(session: Session, word_id: int):
    # Получаем одну запись по primary key.
    # Если записи нет, вернется None.
    return session.get(WordDB, word_id)

def create_word(session: Session, en: str, ru: str, topic: str | None = None):
    # создаем ORM объект WordDB
    # на этом этапе это обычный Python объект, в базе его еще нет
    word = WordDB(en=en, ru=ru, topic=topic, score=0)
    # Добавляем объект в session -> SQLAlchemy подготовит INSERT.
    session.add(word)

    session.commit()
    # Обновляем объект из БД, чтобы точно получить актуальные данные (сгенерированный id)
    session.refresh(word)

    return word

def delete_word_by_id(session: Session, word_id: int):
    word = session.get(WordDB, word_id)

    if word:
        session.delete(word)
        session.commit()

limit = 20

# Собираем список случайных слов, которые ещё не выучены (score < 10)
# Список случайный или по темам (topic)
def get_learning_words_batch(session: Session, limit: int, topic: str | None = None):
    # Защита от некорректного limit
    if limit <= 0:
        return []

    # Отбираем id, ещё невыученных слов
    stmt_ids = select(WordDB.id).where(WordDB._score < 10)
    # Фильтр по теме, если получил
    if topic is not None:
        stmt_ids = stmt_ids.where(WordDB.topic == topic)
    # Получаем список отобранных id
    candidate_ids = list(session.execute(stmt_ids).scalars().all())

    # Если нашли не нашли слов (не отобрали id), то возвращаем пустой список
    if not candidate_ids:
        return []

    # Слов < limit - берем все что есть
    # Иначе, берем слова по случайным id в пределах limit
    if len(candidate_ids) <= limit:
        selected_ids = candidate_ids
    else:
        selected_ids = random.sample(candidate_ids, limit)

    # По отобранным id подтягиваем полные объекты WordDB
    stmt_words = select(WordDB).where(WordDB.id.in_(selected_ids))
    words = list(session.execute(stmt_words).scalars().all())

    return words

# Аналогично get_learning_words_batch, но для уже выученных слов  (score == 10)
def get_review_words_batch(session: Session, limit: int, topic: str | None = None):
    if limit <= 0:
        return []

    stmt_ids = select(WordDB.id).where(WordDB._score == 10)
    if topic is not None:
        stmt_ids = stmt_ids.where(WordDB.topic == topic)
    candidate_ids = list(session.execute(stmt_ids).scalars().all())

    if not candidate_ids:
        return []

    if len(candidate_ids) <= limit:
        selected_ids = candidate_ids
    else:
        selected_ids = random.sample(candidate_ids, limit)

    stmt_words = select(WordDB).where(WordDB.id.in_(selected_ids))
    words = list(session.execute(stmt_words).scalars().all())

    return words

def get_all_words(session: Session):
    stmt_words = select(WordDB)
    words = list(session.execute(stmt_words).scalars().all())
    return words

# Удаление всех слов из БД
def delete_all_words(session: Session):
    stmt_words = delete(WordDB)
    session.execute(stmt_words)
    session.commit()

# Обновление score в БД при изучение слов
def update_word_score(session: Session, word_id: int, new_score: float):
    word = session.get(WordDB, word_id)

    if word is None:
        return None
    word.score = new_score
    session.commit()
    session.refresh(word)
    return word

