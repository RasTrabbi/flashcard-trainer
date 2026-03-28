import random

from sqlalchemy.orm import Session
from sqlalchemy import select, delete

from app.models.db_models import WordDB

# Получаем слово по id
def get_word_by_id(session: Session, word_id: int):
    # session.get(...) ищет запись по primary key
    # если запись не найдена, вернётся None
    return session.get(WordDB, word_id)

# Добавляем слово в БД
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

# Ищем слово по id и удаляем если нашли
def delete_word_by_id(session: Session, word_id: int):
    word = session.get(WordDB, word_id)

    if word is not None:
        session.delete(word)
        session.commit()

def _get_words_batch(session: Session, limit: int, topic: str | None, score_filter):
    # Защита от некорректного Limit
    if limit <= 0:
        return []

    # Фильтр по score_filter, который получаем снаружи
    stmt_ids = select(WordDB.id).where(score_filter)

    # Фильтр по Теме, если передали
    if topic is not None:
        stmt_ids = stmt_ids.where(WordDB.topic == topic)

    # execute(stmt_ids) — запускает запрос к БД
    # scalars() — забирает только значения первого столбца (id)
    # all() — собирает результат в обычный Python список
    candidate_ids = list(session.execute(stmt_ids).scalars().all())

    # Возвращаем пустой список, если после фильтров не смогли отобрать ни одного слова
    if not candidate_ids:
        return []

    if len(candidate_ids) <= limit:
        selected_ids = candidate_ids
    else:
        selected_ids = random.sample(candidate_ids, limit)

    # По отобранным id загружаем полные объекты WordDB
    stmt_words = select(WordDB).where(WordDB.id.in_(selected_ids))
    words = list(session.execute(stmt_words).scalars().all())

    return words

# Передаем правило "только выученные слова"
def get_review_words_batch(session: Session, limit: int, topic: str | None = None):
    return _get_words_batch(
        session,
        limit,
        topic,
        WordDB._score == 10
    )
# Передаем правило "слова, которые ещё не выучены"
def get_learning_words_batch(session: Session, limit: int, topic: str | None = None):
    return _get_words_batch(
        session,
        limit,
        topic,
        WordDB._score < 10
    )

# Возвращаем все слова из БД
def get_all_words(session: Session):
    # формируем SELECT * FROM words
    stmt_words = select(WordDB)

    # выполняем запрос и получаем список всех объектов WordDB
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

