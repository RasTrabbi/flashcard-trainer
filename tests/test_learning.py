from app.models.db_models import  WordDB
from app.services.learning import process_answer, check_answer

def test_check_answer_correct_ru_to_en():
    # Arrange
    word = WordDB(en="apple", ru="яблоко", topic="food")

    # Act
    result = check_answer("ru", word, "apple")

    # Assert
    assert result is True

def test_check_answer_correct_en_to_ru():
    # Arrange
    word = WordDB(en="apple", ru="яблоко", topic="food")

    # Act
    result = check_answer("en", word, "яблоко")

    # Assert
    assert result is True

def test_check_answer_ignores_case_and_spaces():
    # Arrange
    word = WordDB(en="apple", ru="яблоко", topic="food")

    # Act
    result = check_answer("ru", word, "  Apple  ")

    # Assert
    assert result is True

def test_check_answer_wrong():
    # Arrange
    word = WordDB(en="apple", ru="яблоко", topic="food")

    # Act
    result = check_answer("ru", word, "banana")

    # Assert
    assert result is False

def test_check_answer_invalid_prompt_side():
    # Arrange
    word = WordDB(en="apple", ru="яблоко", topic="food")

    # Act / Assert
    import pytest
    # pytest.raises — проверяет, что внутри блока возникает исключение
    with pytest.raises(ValueError):
        # передаём неправильный prompt_side → должна быть ошибка
        check_answer("de", word, "apple")

def test_process_answer_correct(session):
    # Arrange
    word = WordDB(en="apple", ru="яблоко", topic="food")
    word.score = 5

    session.add(word)
    session.commit()
    session.refresh(word)

    # Act
    result = process_answer(session, word, "ru", "apple")

    # Assert
    assert result is True

    updated_word = session.get(WordDB, word.id)
    assert updated_word.score == 6

def test_process_answer_incorrect(session):
    # Arrange
    word = WordDB(en="apple", ru="яблоко", topic="food")
    word.score = 5

    session.add(word)
    session.commit()
    session.refresh(word)

    # Act
    result = process_answer(session, word, "ru", "banana")

    # Assert
    assert result is False

    updated_word = session.get(WordDB, word.id)
    assert updated_word.score == 4.5

def test_process_answer_does_not_go_above_ten(session):
    # Arrange
    word = WordDB(en="apple", ru="яблоко", topic="food")
    word.score = 10

    session.add(word)
    session.commit()
    session.refresh(word)

    # Act
    result = process_answer(session, word, "ru", "apple")

    # Assert
    assert result is True

    updated_word = session.get(WordDB, word.id)
    assert updated_word.score == 10