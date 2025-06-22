import logging

def setup_logging():
    """Set up logging configuration."""

    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler()
        ]
    )

def get_logger(name: str = "api") -> logging.Logger:
    """Get a logger with the specified name."""
    return logging.getLogger(name)

setup_logging()

logger = get_logger()
