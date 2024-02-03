import logging
from logging.handlers import RotatingFileHandler
from logging import Filter
from app.context import ctx


class ContextualFilter(Filter):
    """Contextual filter for logging."""

    def filter(self, message: object) -> bool:
        """Customize the contextual filter."""
        message.trace_request_uuid = ctx.trace_request_uuid
        message.pid = ctx.pid
        return True


class LoggerCreator:
    def __init__(self, config):
        self.config = config

    def create_logger(self):
        handler = RotatingFileHandler(filename=self.config.LOG_FILENAME, maxBytes=self.config.LOG_FILESIZE,
                                      backupCount=self.config.LOG_FILES_LIMIT)
        handler.setFormatter(logging.Formatter(self.config.LOG_FORMAT))

        log = logging.getLogger(__name__)
        log.addHandler(handler)
        log.addFilter(ContextualFilter())
        log.setLevel(logging.getLevelName(self.config.LOG_LEVEL))
        return log
