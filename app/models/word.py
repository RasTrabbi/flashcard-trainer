class Word:
    # __init__ — конструктор класса, вызывается при создании объекта
    def __init__(self, en, ru, score=0.0, topic=None, id=None):
        self.id = id
        self.en = en
        self.ru = ru
        self.score = score  # значение проходит через setter score
        self.topic = topic

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

    # строковое представление объекта для print()
    def __str__(self):
        return f"{self.en} - {self.ru} (score={self.score})"

    # техническое представление объекта для отладки
    def __repr__(self):
        return f"Word(id={self.id}, en='{self.en}', ru='{self.ru}', score={self.score}, topic={self.topic!r})"