# Flashcard Trainer

Backend-проект для изучения английских слов с использованием карточек.
  
Backend project for learning English vocabulary using flashcards.

---

## Описание / Description

Проект реализует систему карточек для изучения слов с прогрессом обучения.
Каждое слово имеет уровень изученности (`score`), который изменяется в зависимости от правильности ответа.
  
The project implements a flashcard learning system with progress tracking.
Each word has a learning score that changes based on user answers.

---

## Текущий этап / Current Stage

```text
Python core → SQLite → SQLAlchemy ORM → FastAPI
```

* реализована работа с базой данных через ORM
* внедрён repository слой
* удалён старый sqlite3 подход
* реализован API слой (FastAPI)

---

## Основной функционал / Features

* Добавление слов / Add words
* Удаление слов / Delete words
* Получение всех слов / Get all words
* Обучение (learning):
  * выбор случайных слов со `score < 10`
  * обновление прогресса
* Повторение (review):
  * выбор слов со `score == 10`
* Обработка ответа пользователя:
  * проверка ответа
  * обновление `score`

---

## Архитектура / Architecture

```text
app
│
├ api           → FastAPI endpoints
├ models       → ORM модели и бизнес-логика
├ repositories → работа с базой данных
├ services     → логика обучения
├ database     → session и подключение к БД
```

**Layered architecture (EN)** — разделение на уровни ответственности.

---

## Технологии / Technologies

* Python
* SQLite
* SQLAlchemy (ORM)
* FastAPI

---

## Что реализовано / Implemented

* Word модель с бизнес-логикой (`score`, `is_learned`)
* Repository слой:
  * create / delete / update
  * batch выборка слов
* API слой (FastAPI):
  * POST /words
  * GET /words
  * GET /learning
  * POST /answer
* Работа с БД через SQLAlchemy
* Разделение на слои (models / services / repository / api)

---

## Что дальше / Next Steps

* pytest (автотесты)
* улучшение архитектуры

---

## Автор / Author

Roman Sivokhin
