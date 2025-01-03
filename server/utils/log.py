import logging
import argparse

# ANSI escape codes for colored output
RESET = "\033[0m"
DIM = "\033[2m"
RED = "\033[31m"
INTENSE_YELLOW = "\033[33;1m"
LIGHT_CYAN = "\033[36;1m"
LIGHT_YELLOW = "\033[93m"

class CustomFormatter(logging.Formatter):
    """
    Custom logging formatter for consistent, colored logs.
    """

    def format(self, record):
        now = self.formatTime(record, "%d/%m/%Y-%H:%M:%S")
        if record.levelno == logging.ERROR:
            level = f"{RED}[ERROR]{RESET} {DIM}"
        elif record.levelno == logging.WARNING:
            level = f"{INTENSE_YELLOW}[WARN]{RESET} {DIM}"
        elif record.levelno == logging.INFO:
            level = f"{LIGHT_CYAN}[INFO]{RESET} {DIM}"
        elif record.levelno == logging.DEBUG:
            level = f"{LIGHT_YELLOW}[DEBUG]{RESET} {DIM}"
        else:
            level = f"{RESET}[{record.levelname}]{RESET} {DIM}"

        message = super().format(record)
        return f"{now} {level} {message}{RESET}"


def get_logger(name: str = None, log_level: str = "INFO") -> logging.Logger:
    """
    Returns a configured logger instance.

    Args:
        name (str): Name of the logger (typically the module's __name__).
        log_level (str): Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL).

    Returns:
        logging.Logger: Configured logger instance.
    """
    logger = logging.getLogger(name or __name__)
    if not logger.hasHandlers():
        # Set log level dynamically
        level = getattr(logging, log_level.upper(), logging.INFO)
        logger.setLevel(level)

        # Stream handler for console logs
        handler = logging.StreamHandler()
        handler.setFormatter(CustomFormatter())
        logger.addHandler(handler)

        # Optional: File handler for logs
        file_handler = logging.FileHandler("/tmp/application.log")
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(message)s"))
        logger.addHandler(file_handler)
    return logger

