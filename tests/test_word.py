from app.models.db_models import WordDB

def test_update_score_correct():
    # Arrange
    word = WordDB(en="apple", ru="яблоко", topic="food")
    word.score = 5

    # Act
    word.update_score(is_correct=True)

    #Assert
    assert word.score == 6

def test_update_score_incorrect():
    # Arrange
    word = WordDB(en="apple", ru="яблоко", topic="food")
    word.score = 5

    # Act
    word.update_score(is_correct=False)

    # Assert
    assert word.score == 4.5

def test_score_clamped():
    # Arrange
    word = WordDB(en="apple", ru="яблоко", topic="food")
    word.score = 10

    # Act
    word.update_score(is_correct=True)

    # Assert
    assert word.score == 10  # не растёт дальше