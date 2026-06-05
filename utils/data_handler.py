"""
Data handling utilities for downloading and managing datasets
"""

import json
import os
import urllib.request
from pathlib import Path

import pandas as pd

from utils.logger import get_logger

logger = get_logger(__name__)


class DataHandler:
    """Handles data downloading, loading, and management"""

    def __init__(self, dataset_path, backup_urls=None):
        self.dataset_path = Path(dataset_path)
        self.backup_urls = backup_urls or []

    def download_dataset(self):
        """Download dataset from URL with fallback"""
        try:
            logger.info("Starting dataset download...")

            # Create sample dataset if download fails
            if not self._try_download():
                logger.warning("Download failed, creating sample dataset...")
                self._create_sample_dataset()

            logger.info(f"Dataset ready at {self.dataset_path}")
            return True

        except Exception as e:
            logger.error(f"Error in download_dataset: {e}")
            self._create_sample_dataset()
            return False

    def _try_download(self):
        """Attempt to download from primary URL"""
        try:
            url = "https://raw.githubusercontent.com/andrewng/cs294-112_data/master/emails.csv"
            logger.info(f"Downloading from {url}...")
            urllib.request.urlretrieve(url, self.dataset_path)
            return True
        except Exception as e:
            logger.warning(f"Primary download failed: {e}")
            return False

    def _create_sample_dataset(self):
        """Create a sample dataset for fallback"""
        try:
            sample_data = {
                "text": [
                    "Click here to claim your free prize",
                    "Meeting scheduled for tomorrow at 3 PM",
                    "Verify your account immediately",
                    "Project update: completed all tasks",
                    "Limited offer: get 50% off now",
                    "Thank you for your purchase",
                    "Urgent: confirm your payment details",
                    "Weekly report attached",
                ] * 125,
                "spam": [1, 0, 1, 0, 1, 0, 1, 0] * 125,
            }
            df = pd.DataFrame(sample_data)
            df.to_csv(self.dataset_path, index=False)
            logger.info(f"Sample dataset created at {self.dataset_path}")
        except Exception as e:
            logger.error(f"Error creating sample dataset: {e}")

    def load_dataset(self):
        """Load dataset with error handling"""
        try:
            if not self.dataset_path.exists():
                logger.warning("Dataset not found, downloading...")
                self.download_dataset()

            df = pd.read_csv(self.dataset_path)

            # Ensure required columns exist
            required_cols = ["text", "spam"]
            missing_cols = [col for col in required_cols if col not in df.columns]

            if missing_cols:
                logger.error(f"Missing columns: {missing_cols}")
                self._create_sample_dataset()
                df = pd.read_csv(self.dataset_path)

            # Clean data
            df = df.dropna(subset=["text"])
            df["text"] = df["text"].astype(str).str.strip()
            df = df[df["text"].str.len() > 0]

            if len(df) == 0:
                logger.warning("Dataset is empty, creating sample...")
                self._create_sample_dataset()
                df = pd.read_csv(self.dataset_path)

            logger.info(f"Dataset loaded: {len(df)} records")
            return df

        except Exception as e:
            logger.error(f"Error loading dataset: {e}")
            self._create_sample_dataset()
            return self.load_dataset()

    def save_history(self, history_path, predictions):
        """Save prediction history"""
        try:
            history_path = Path(history_path)
            history_path.parent.mkdir(parents=True, exist_ok=True)

            existing = []
            if history_path.exists():
                try:
                    with open(history_path, "r") as f:
                        existing = json.load(f)
                except Exception as e:
                    logger.warning(f"Could not load existing history: {e}")

            # Keep only the last MAX_HISTORY_RECORDS
            from config import MAX_HISTORY_RECORDS

            combined = existing + predictions
            combined = combined[-MAX_HISTORY_RECORDS:]

            with open(history_path, "w") as f:
                json.dump(combined, f, indent=2)

            return True
        except Exception as e:
            logger.error(f"Error saving history: {e}")
            return False

    def load_history(self, history_path):
        """Load prediction history"""
        try:
            history_path = Path(history_path)
            if history_path.exists():
                with open(history_path, "r") as f:
                    return json.load(f)
            return []
        except Exception as e:
            logger.error(f"Error loading history: {e}")
            return []
