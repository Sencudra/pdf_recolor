import logging


class Formatter(logging.Formatter):

    grey = "\x1b[38;20m"
    yellow = "\x1b[33;20m"
    red = "\x1b[31;20m"
    bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"
    message_format = "%(asctime)s [%(levelname)s] %(filename)s:%(lineno)d - %(message)s"
    asctime_format = "%H:%M:%S"

    FORMATS = {
        logging.DEBUG: "⚪️ " + message_format,
        logging.INFO: "🟢 " + message_format,
        logging.WARNING: "🟡 " + message_format,
        logging.ERROR: "🔴 " + message_format,
        logging.CRITICAL: "🟣 " + message_format
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt, self.asctime_format)
        return formatter.format(record)
