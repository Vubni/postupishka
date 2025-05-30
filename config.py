from dotenv import load_dotenv
import os

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

API_KEY = os.getenv("API_KEY")

PROXY_IP = os.getenv("PROXY_IP")
PROXY_PORT = os.getenv("PROXY_PORT")
PROXY_USER = os.getenv("PROXY_USER")
PROXY_PASS = os.getenv("PROXY_PASS")

SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")

DATE_BASE_CONNECT = {"host": "45.89.190.44", 
             "user": "user", 
             "password": os.getenv("DB_PASSWORD"), 
             "database": "postupishka"}

bot_url = "https://t.me/postupishka_bot"





import logging
from logging.handlers import RotatingFileHandler

# Создаем логгер
logger = logging.getLogger()
logger.setLevel(logging.INFO)


# Форматтер с единой структурой
formatter = logging.Formatter(
    '%(asctime)s - %(levelname)s - %(name)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

# Основной обработчик для всех логов
all_logs_handler = RotatingFileHandler(
    'logs/all_logs.log',
    maxBytes=5*1024*1024,  # 5 MB
    backupCount=3,
    encoding='utf-8'
)
all_logs_handler.setFormatter(formatter)

# Обработчик только для ошибок
error_handler = RotatingFileHandler(
    'logs/errors.log',
    maxBytes=5*1024*1024,
    backupCount=3,
    encoding='utf-8'
)
error_handler.setLevel(logging.ERROR)
error_handler.setFormatter(formatter)

# Консольный обработчик (опционально)
console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)

# Добавляем все обработчики
logger.addHandler(all_logs_handler)
logger.addHandler(error_handler)
logger.addHandler(console_handler)
