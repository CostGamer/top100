import logging
from logging.handlers import RotatingFileHandler

from src.backend.DB.settings import all_settings


def setup_logger(name: str) -> logging.Logger:
    log_level = all_settings.LOG_LEVEL.upper()
    log_file = all_settings.LOG_FILE
    log_encoding = all_settings.LOG_ENCODING

    log_format = (
        "[%(asctime)s] %(filename)20s:%(lineno)3d - %(levelname)7s - %(message)s"
    )
    log_date_format = "%Y-%m-%d %H:%M:%S"

    logging.basicConfig(
        level=log_level,
        datefmt=log_date_format,
        format=log_format,
        handlers=[logging.StreamHandler()],  # Обработчик для вывода в консоль
    )

    file_handler = RotatingFileHandler(
        log_file, maxBytes=5 * 1024 * 1024, backupCount=3, encoding=log_encoding
    )
    file_handler.setFormatter(logging.Formatter(log_format, datefmt=log_date_format))

    logger = logging.getLogger(name)
    logger.addHandler(file_handler)

    return logger
