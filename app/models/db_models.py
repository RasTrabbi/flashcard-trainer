from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import declarative_base

# создаем базовый класс ORM, все ORM модели должны наследоваться от него
Base = declarative_base()

class WordDB(Base):
    # words - имя таблицы в базе данных
    __tablename__ = "words"
    id = Column(Integer, primary_key=True)
    en = Column(String)
    ru = Column(String)
    _score = Column("score", Float)
    topic = Column(String)

    # property — позволяет обращаться к методу как к обычному полю объекта
    # используется чтобы контролировать чтение значения score
    @property
    def score(self):
        return self._score

    # setter — перехватывает присвоение значения свойству
    # здесь используется чтобы централизованно ограничить score диапазоном 0..10
    @score.setter
    def score(self, value):
        if value < 0:
            self._score = 0
        elif value > 10:
            self._score = 10
        else:
            self._score = value

    # метод инкапсулирует правила изменения score после ответа
    # изменение происходит через property → автоматически применяется setter
    def update_score(self, is_correct):
        if not self.is_learned:
            change = 1.0 if is_correct else -0.5
            self.score += change

    # вычисляемое свойство — значение рассчитывается на основе других полей
    @property
    def is_learned(self):
        return self.score >= 10

    # вспомогательный метод для сброса прогресса обучения
    def reset_score(self):
        self.score = 0

    # принудительно переводит слово в состояние "выучено"
    def mark_learned(self):
        self.score = 10.0