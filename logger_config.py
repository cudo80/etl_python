import logging
import sys

def get_logger(name):
    logger = logging.getLogger(name)

    # Check if handlers are already configured to avoid duplicate logs
    if not logger.hasHandlers():
        logger.setLevel(logging.INFO)

        # Create formatter
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

        # Create file handler
        file_handler = logging.FileHandler('etl_pipeline.log')
        file_handler.setLevel(logging.INFO)
        file_handler.setFormatter(formatter)

        # Create console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(formatter)

        # Add handlers to logger
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

    return logger
