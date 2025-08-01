import os
import logging
from logging.handlers import TimedRotatingFileHandler
from src.core.config import SETTINGS


class LevelFilter(logging.Filter):
    def __init__(self, level) -> None:
        super().__init__()
        self.__level = level

    def filter(self, record) -> bool:
        return record.levelno == self.__level


def flip_name(log_path) -> str:
    log_dir, log_filename = os.path.split(log_path)
    base_filename = os.path.splitext(log_filename)[0]
    timestamp = log_filename[len(base_filename) + 1 :]
    return os.path.join(log_dir, f"{timestamp}.{base_filename}")


def create_logger(
    console_log_level=logging.INFO,
    log_file_dir: str = None,
    logger_name: str = SETTINGS.SERVICE_NAME,
) -> logging.Logger:
    logger: logging.Logger = logging.getLogger(logger_name)
    logger.setLevel(logging.DEBUG)

    if logger.hasHandlers():
        logger.handlers.clear()

    log_formatter = logging.Formatter(
        "%(asctime)s - %(levelname)s - %(threadName)s - %(module)s.py - %(funcName)s() - %(lineno)d - %(message)s",
        datefmt="%Y-%m-%dT%H:%M:%S",
    )
    console_handler: logging.StreamHandler[logging.TextIO] = (
        logging.StreamHandler()
    )
    console_handler.setFormatter(log_formatter)
    console_handler.setLevel(console_log_level)
    logger.addHandler(console_handler)

    if log_file_dir:
        try:
            os.makedirs(log_file_dir, exist_ok=True)
        except Exception as e:
            logger.error(
                f"Creating log directory failed. Error: {e}", exc_info=True
            )
            return logger

        levels_to_log: dict[str, int] = {
            "debug": logging.DEBUG,
            "info": logging.INFO,
            "warning": logging.WARNING,
            "error": logging.ERROR,
            "critical": logging.CRITICAL,
        }

        for level_name, level_int in levels_to_log.items():
            log_filename: str = os.path.join(
                log_file_dir, f"{logger_name.lower()}_{level_name}.log"
            )
            file_handler = TimedRotatingFileHandler(
                log_filename, when="D", interval=1, backupCount=10
            )
            file_handler.setFormatter(log_formatter)
            file_handler.namer = flip_name
            file_handler.addFilter(LevelFilter(level_int))

            logger.addHandler(file_handler)

    return logger
