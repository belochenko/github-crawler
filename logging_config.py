import logging

LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"

def setup_logger(log_file="crawler.log"):
    # Configure logging
    logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)

    # Create file handler
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(logging.Formatter(LOG_FORMAT))

    # Create console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(logging.Formatter(LOG_FORMAT))

    # Get root logger and add handlers
    logger = logging.getLogger()
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger
