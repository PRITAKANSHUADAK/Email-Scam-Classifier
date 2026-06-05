"""
Logger utility for the application
"""

import logging
import os
import sys
from pathlib import Path


def _get_writable_log_dir(default_dir: Path) -> Path:
    try:
        default_dir.mkdir(parents=True, exist_ok=True)
        test_file = default_dir / ".write_test"
        with open(test_file, "w") as test:
            test.write("ok")
        test_file.unlink()
        return default_dir
    except OSError:
        fallback = Path(os.getenv("EMAIL_SCAM_LOG_DIR", "/tmp/logs"))
        fallback.mkdir(parents=True, exist_ok=True)
        return fallback

# Create logs directory
log_dir = _get_writable_log_dir(Path(__file__).resolve().parent.parent / "logs")

# Configure logging
handlers = [logging.StreamHandler(sys.stdout)]
try:
    handlers.insert(0, logging.FileHandler(log_dir / "app.log"))
except OSError:
    # Fall back to console-only logging in read-only environments
    pass

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=handlers,
)


def get_logger(name):
    """Get a logger instance"""
    return logging.getLogger(name)
