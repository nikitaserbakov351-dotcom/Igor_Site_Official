# Персональный сайт-визитка на Flask

![Python](https://img.shields.io/badge/Python-3.11+-3776AB?logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-3.x-000000?logo=flask&logoColor=white)
![Tests](https://github.com/nikitaserbakov351-dotcom/Igor_Site_Official/actions/workflows/tests.yml/badge.svg)
![pytest](https://img.shields.io/badge/pytest-passed-0A9EDC?logo=pytest&logoColor=white)

Адаптивный мультимедийный сайт-визитка с встроенным аудиоплеером. Бэкенд на Flask, фронтенд — чистый HTML5/CSS/JS без тяжёлых фреймворков. Проект отрабатывает адаптивную вёрстку, работу со статикой и потоковое воспроизведение медиа; покрыт автотестами с запуском через GitHub Actions.

## Ключевые возможности

- **Одностраничный лендинг** — секции «Обо мне», галерея, медиа и контакты с плавной прокруткой.
- **Аудиоплеер на HTML5 Audio** — воспроизведение локальных mp3-треков из каталога `static/music`, без внешних библиотек.
- **Полная адаптивность** — Flexbox и CSS Grid, мобильное бургер-меню на ванильном JS.
- **Локальная сетевая отладка** — при старте скрипт определяет локальный IP машины в Wi-Fi сети и печатает адрес в консоль: вёрстку можно сразу проверить со смартфона.
- **Автотесты и CI** — pytest-проверки главной страницы и ключевых секций, workflow GitHub Actions запускается на каждый push.

## Технологический стек

| Слой | Технологии |
|---|---|
| Бэкенд | Python 3.11+, Flask 3 |
| Фронтенд | HTML5, CSS (Flexbox/Grid), ванильный JavaScript |
| Медиа | HTML5 Audio API |
| Тестирование | pytest, GitHub Actions |

## Быстрый старт

```bash
git clone https://github.com/nikitaserbakov351-dotcom/Igor_Site_Official.git
cd Igor_Site_Official

python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt

python igor_site.py              # адрес сервера появится в консоли
```

Для запуска тестов:

```bash
pytest -v
```

## Приватность и медиафайлы

Все оригинальные фотографии, видеозаписи и реальные контакты намеренно удалены из публичной ветки репозитория ради конфиденциальности. В соответствующих блоках (галерея и видео) оставлены информационные заглушки, чтобы не ломать разметку и логику навигации. Аудиотреки размещаются в `static/music/` и в репозиторий не входят.

## Структура проекта

```
├── igor_site.py                   # приложение Flask и встроенный шаблон
├── test_site.py                   # pytest-тесты (статус, ключевые секции)
├── .github/workflows/tests.yml    # CI: прогон pytest на каждый push
├── static/music/                  # локальные mp3-треки для плеера
└── requirements.txt               # зависимости
```

## Развитие проекта

- [ ] Плейлист с переключением треков и обложками
- [ ] Поддержка видео-секции (сейчас — заглушка)
- [ ] Тесты мобильного меню через Playwright
- [ ] Деплой на VPS с gunicorn + nginx

## Автор

Проект подготовлен **[@TheSheinAir](https://github.com/TheSheinAir)** — другие работы смотрите в [профиле GitHub](https://github.com/TheSheinAir?tab=repositories).
