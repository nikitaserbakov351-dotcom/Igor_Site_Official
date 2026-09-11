Multi-Service Platform: AI Agent & Media Web Hub

Интегрированный проект, объединяющий легковесный веб-сервис на Flask и асинхронного диалогового агента на Aiogram 3 с интеграцией Google Gemini LLM и поддержкой **Function Calling** (вызов внешних инструментов).
О проекте

Проект состоит из двух независимых модулей:

1. Интеллектуальный Telegram-бот (`main.py`)**:
   - Асинхронная архитектура на базе `aiogram 3` и `httpx`.
   - Интеграция с Large Language Model (Google Gemini) через прямой REST API.
   - Реализация механизма Tool Calling / Function Calling: модель самостоятельно определяет потребность во внешних данных и вызывает функцию получения текущей погоды (`OpenWeatherMap API`).
   - Управление контекстом диалога: скользящее окно памяти (Sliding Window Memory) с поддержанием корректных пар «запрос-ответ».
   - Поддержка сетевого проксирования для стабильной работы на ограниченных серверах.

2. Веб-сервис и мультимедийная визитка (`igor_site.py`):
   - Микрофреймворк `Flask` с динамическим рендерингом страниц.
   - Адаптивная верстка (CSS Grid, Flexbox, Mobile First, плавный скролл, динамическое меню).
   - Мультимедийная галерея (аудио- и видеоплееры HTML5) с обработкой ошибок загрузки статики (`fallback placeholders`).
   - Автоматическое определение локального IP-адреса хоста для тестирования с мобильных устройств в единой Wi-Fi сети.


Стек технологий

- Язык: Python 3.10+
- Бэкенд & Веб: Flask, Jinja2
- Telegram & Async**: Aiogram 3.x, Asyncio, Aiohttp, HTTPX
- Искусственный интеллект**: Google Gemini API (Function Calling, System Instructions)
- Сторонние API: OpenWeatherMap API
- Фронтенд: HTML5, CSS3 (Modern Responsive UI), FontAwesome


Структура проекта

```text
├── main.py              # Точка входа Telegram-бота с логикой LLM и Function Calling
├── igor_site.py         # Веб-сервер на Flask
├── static/              # Статические файлы (изображения, видео, аудио)
│   ├── images/
│   ├── videos/
│   └── music/
├── .env.example         # Шаблон переменных окружения
├── .gitignore           # Исключения системы контроля версий
└── requirements.txt     # Зависимости проекта
