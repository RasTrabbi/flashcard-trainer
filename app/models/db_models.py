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

    @property
    # property — позволяет обращаться к методу как к обычному полю объекта
    # используется чтобы контролировать чтение значения score
    def score(self):
        return self._score

    @score.setter
    # setter — перехватывает присвоение значения свойству
    # здесь используется чтобы централизованно ограничить score диапазоном 0..10
    def score(self, value):
        if value < 0:
            self._score = 0
        elif value > 10:
            self._score = 10
        else:
            self._score = value

    def update_score(self, is_correct):
        # метод инкапсулирует правила изменения score после ответа
        # изменение происходит через property → автоматически применяется setter
        if not self.is_learned:
            change = 1.0 if is_correct else -0.5
            self.score += change

    @property
    # вычисляемое свойство — значение рассчитывается на основе других полей
    def is_learned(self):
        return self.score >= 10

    def reset_score(self):
        # вспомогательный метод для сброса прогресса обучения
        self.score = 0

    def mark_learned(self):
        # принудительно переводит слово в состояние "выучено"
        self.score = 10.0