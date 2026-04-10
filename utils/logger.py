import os
import logging
from logging.handlers import RotatingFileHandler
from config.settings import LOG_LEVEL, LOG_DIR, LOG_FILE


# Create logs directory if missing

os.makedirs(LOG_DIR, exist_ok=True)



# Logger Formatter

LOG_FORMAT = "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"



# Main Logger Function

def get_logger(name="enterprise_kb_app"):
    """
    Create and return a reusable logger instance.

    Args:
        name (str): Logger name

    Returns:
        logging.Logger: Configured logger
    """
    logger = logging.getLogger(name)

    # Prevent duplicate handlers
    if logger.handlers:
        return logger

    logger.setLevel(getattr(logging, LOG_LEVEL.upper(), logging.INFO))
    logger.propagate = False

    formatter = logging.Formatter(LOG_FORMAT, datefmt=DATE_FORMAT)

    
    # Console Handler
    
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    
    # File Handler (Rotating)
    
    log_path = os.path.join(LOG_DIR, LOG_FILE)

    file_handler = RotatingFileHandler(
        log_path,
        maxBytes=2 * 1024 * 1024,   # 2 MB
        backupCount=3,
        encoding="utf-8"
    )
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    return logger