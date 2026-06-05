"""
Logger utility for the application
"""

import logging
import sys
from pathlib import Path

# Create logs directory
log_dir = Path(__file__).resolve().parent.parent / "logs"
log_dir.mkdir(parents=True, exist_ok=True)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(log_dir / "app.log"),
        logging.StreamHandler(sys.stdout),
    ],
)


def get_logger(name):
    """Get a logger instance"""
    return logging.getLogger(name)
