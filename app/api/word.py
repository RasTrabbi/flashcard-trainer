from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.repositories.word_repository import create_word, get_all_words, get_learning_words_batch, get_word_by_id
from app.schemas.word import WordCreate, WordRead, AnswerRequest, AnswerResult
from app.services.learning import process_answer

# router хранит обработчики запросов
router = APIRouter()

# если придёт POST /words → вызвать эту функцию, результат привести к WordRead
@router.post("/words", response_model=WordRead)
def create_word_endpoint(word: WordCreate, db: Session = Depends(get_db)):
    # вызываем repository (сохраняем в БД)
    created_word = create_word(db, word.en, word.ru, word.topic)

    # FastAPI сам преобразует WordDB → WordRead
    return created_word

# получаем все слова из БД
@router.get("/words", response_model=List[WordRead])
def read_words_endpoint(db: Session = Depends(get_db)):
    words = get_all_words(db)

    # FastAPI сам преобразует список WordDB → список WordRead
    return words

# Получаем batch слов для обучения (score < 10)
@router.get("/learning", response_model=List[WordRead])
def get_learning_words_endpoint(db: Session = Depends(get_db), limit: int = 20, topic: str | None = None):
    # вызываем repository → получаем список WordDB по фильтру learning
    words = get_learning_words_batch(db, limit, topic)

    # вызываем repository → получаем список WordDB по фильтру learning
    return words

@router.post("/answer", response_model=AnswerResult)
def process_answer_endpoint(answer: AnswerRequest, db: Session = Depends(get_db)):
    word = get_word_by_id(db, answer.word_id)

    # Возвращаем 404, если слово не найдено
    if word is None:
        raise HTTPException(status_code=404, detail="Answer not found")

    # Проверяем ответ и обновляем score
    is_correct = process_answer(db, word, answer.prompt_side, answer.user_answer)

    return AnswerResult(
        is_correct=is_correct,
        score=word.score
    )