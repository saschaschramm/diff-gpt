import logging
from logging import Logger, StreamHandler

class CustomFormatter(logging.Formatter):

    grey: str = "\x1b[38;20m"
    green: str = "\x1b[32;1m"
    yellow: str = "\x1b[33;20m"
    red: str = "\x1b[31;20m"
    bold_red: str = "\x1b[31;1m"
    reset: str = "\x1b[0m"

    _FORMAT: str = "%(asctime)s - (%(filename)s:%(lineno)s) - %(levelname)s: %(message)s"

    def _format_with_level(self, level: int, format_str: str) -> str:
        FORMATS = {
            logging.DEBUG: self.grey + format_str + self.reset,
            logging.INFO: self.green + format_str + self.reset,
            logging.WARNING: self.yellow + format_str + self.reset,
            logging.ERROR: self.red + format_str + self.reset,
            logging.CRITICAL: self.bold_red + format_str + self.reset,
        }
        return FORMATS[level]

    def format(self, record: logging.LogRecord) -> str:
        format: str = self._format_with_level(record.levelno, self._FORMAT)
        formatter: logging.Formatter = logging.Formatter(format)
        return formatter.format(record)


def get_logger() -> Logger:
    logger: Logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    logger.handlers = []
    streaming_handler: StreamHandler = logging.StreamHandler()
    streaming_handler.setFormatter(CustomFormatter())
    logger.addHandler(streaming_handler)
    return logger
