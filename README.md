# Создать файл .env в корне проекта и заполните его по шаблону:

* DOMAIN=http://localhost:8000      # Домен API (для локальной разработки)
* LOG_LEVEL=INFO                    # Уровень логирования
* DATABASE_URL=sqlite+aiosqlite:///./complaints.db  # Путь к SQLite 

# API-ключи
* SENTIMENT_API_KEY=your_sentiment_api_key_here       # Ключ для анализа тональности
* OPENAI_API_KEY=your_openai_api_key_here             # Ключ OpenAI API
* TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here     # Токен бота Telegram
* HUGGINGFACE_API_KEY=your_huggingface_api_key_here   # Ключ Hugging Face API
* SPAM_API_KEY=your_spam_api_key_here                 # Для фильтра

### Начало 

* git clone https://github.com/sskywwalkerr/complaint_handling

* Создать .env файл в директории complaint-api


### Установка зависимостей
* pip install -r requirements.txt

### Запуск сервера

* uvicorn app.main:app --host 0.0.0.0 --port 8000

### После запуска API будет доступен по адресу: http://localhost:8000/docs


