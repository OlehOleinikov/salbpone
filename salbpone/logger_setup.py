"""
Модуль налаштувань логера.
"""

from loguru import logger
import sys

# Форматування повідомлень
log_format = (
    "<green>{time:DD.MM.YYYY HH:mm:ss}</green> | "
    "<level>{level}</level> | "
    "<level>{message}</level>"
)

# Налаштування логера
logger.remove()
logger.add(
    sys.stdout,
    format=log_format,
    level="DEBUG",
    colorize=True
)
logger.add(
    "logs/logfile.log",
    format=log_format,
    level="DEBUG",
    rotation="1 MB",
    compression="zip"
)

# Встановлення кольорів для рівнів логування
logger.level("SUCCESS", color="<green>")
logger.level("ERROR", color="<red>")
logger.level("DEBUG", color="<yellow>")


# Логування у разі крашу програми
def log_exception(exc_type, exc_value, exc_traceback):
    logger.error(f"{exc_type.__name__} - {exc_value}",
                 exc_info=(exc_type, exc_value, exc_traceback))


# Налаштування покращеного відображення Traceback
sys.excepthook = log_exception
