import logging

LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"


def setup_logger(log_file="crawler.log"):
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler(log_file)
        ]
    )
    logger = logging.getLogger(__name__)
    return logger
