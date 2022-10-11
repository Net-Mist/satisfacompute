import logging


class Formatter(logging.Formatter):
    def __init__(self) -> None:
        super().__init__("%(levelchar)s %(message)s")

    def formatMessage(self, record: logging.LogRecord) -> str:
        values = record.__dict__
        if values["levelname"] == "WARNING":
            values["levelchar"] = "\033[93mWarning\033[0m"
        return self._fmt % values


def get_logger(name: str) -> logging.Logger:
    handler = logging.StreamHandler()
    handler.setFormatter(Formatter())
    # logging.basicConfig(level=logging.WARNING, handlers=[handler])
    logger = logging.getLogger(name)
    logger.setLevel(logging.WARNING)
    logger.addHandler(handler)
    return logger
