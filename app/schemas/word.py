from pydantic import BaseModel, Field
from typing import Literal

# Pydantic модель для входящих данных (POST /words)
class WordCreate(BaseModel):
    # обязательные поля + защита от пустых строк
    en: str = Field(min_length=1)
    ru: str = Field(min_length=1)
    # необязательное поле
    topic: str | None = None

# Pydantic модель для ответа API
class WordRead(BaseModel):
    # поля, которые возвращаются клиенту
    id: int
    en: str
    ru: str
    score: float
    topic: str | None = None

    # позволяет конвертировать ORM (WordDB) → schema
    model_config = {"from_attributes": True}

# Pydantic модель с ответом пользователя
class AnswerRequest(BaseModel):
    word_id: int
    # какая сторона была показана ("ru" или "en"), Literal ограничивает допустимые значения
    prompt_side: Literal["ru", "en"]
    # Ответ пользователя + защита от пустой строки
    user_answer: str = Field(min_length=1)

# Pydantic модель для ответа после проверки слова
class AnswerResult(BaseModel):
    # результат проверки ответа (правильно / неправильно)
    is_correct: bool
    # обновлённый score после обработки ответа
    score: float
