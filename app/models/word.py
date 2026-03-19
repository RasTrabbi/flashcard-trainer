class Word:
    def __init__(self, en, ru, score=0.0, topic=None, id=None):
        # __init__ — конструктор класса, вызывается при создании объекта
        self.id = id
        self.en = en
        self.ru = ru
        self.score = score  # значение проходит через setter score
        self.topic = topic

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

    def __str__(self):
        # строковое представление объекта для print()
        return f"{self.en} - {self.ru} (score={self.score})"

    def __repr__(self):
        # техническое представление объекта для отладки
        return f"Word(id={self.id}, en='{self.en}', ru='{self.ru}', score={self.score}, topic={self.topic!r})"