from app.models.word import Word
from app.repositories.word_repository import update_word_score

def check_answer(prompt_side, word, user_answer):
    # "ru" → показали русский, ожидаем английский
    if prompt_side == "ru":
        expected = word.en
    # "en" → показали английский, ожидаем русский
    elif prompt_side == "en":
        expected = word.ru

    else:
        raise ValueError("prompt_side must be 'ru' or 'en'") # raise вызывает исключение и останавливает выполнение функции

    # нормируем строки
    expected = expected.strip().lower()
    user_answer = user_answer.strip().lower()

    return expected == user_answer

# Проверяем ответ и изменяем "прогресс" обучения
def process_answer(session, word, prompt_side, user_answer):
    is_correct = check_answer(prompt_side, word, user_answer)
    word.update_score(is_correct)
    update_word_score(session, word.id, word.score)
    return is_correct