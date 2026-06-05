"""
Configuration module for Email Scam & Phishing Detection Platform
"""

import os
from pathlib import Path

# Base paths
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
MODELS_DIR = BASE_DIR / "models"
STATIC_DIR = BASE_DIR / "static"
TEMPLATES_DIR = BASE_DIR / "templates"

# Create directories if they don't exist
for directory in [DATA_DIR, MODELS_DIR, STATIC_DIR, TEMPLATES_DIR]:
    directory.mkdir(parents=True, exist_ok=True)

# File paths
DATASET_PATH = DATA_DIR / "emails.csv"
MODEL_PATH = MODELS_DIR / "model.pkl"
VECTORIZER_PATH = MODELS_DIR / "vectorizer.pkl"
SCALER_PATH = MODELS_DIR / "scaler.pkl"
CONFIG_PATH = DATA_DIR / "config.json"
HISTORY_PATH = DATA_DIR / "prediction_history.json"

# Dataset configuration
DATASET_URL = "https://raw.githubusercontent.com/andrewng/cs294-112_data/master/emails.csv"
DATASET_BACKUP_URL = "https://www.kaggle.com/api/v1/datasets/download/balakrishnakuppusamy/spam-or-not-spam-dataset"

# Model configuration
TEST_SIZE = 0.2
RANDOM_STATE = 42
N_FEATURES = 5000
MAX_DF = 0.8
MIN_DF = 2

# Flask configuration
SECRET_KEY = os.getenv("SECRET_KEY", "production-secret-key-change-in-production")
DEBUG = False
TESTING = False
JSON_SORT_KEYS = False

# Feature extraction
FEATURE_PARAMS = {
    "max_features": N_FEATURES,
    "max_df": MAX_DF,
    "min_df": MIN_DF,
    "ngram_range": (1, 2),
}

# Model names
MODELS_TO_TRAIN = ["LogisticRegression", "RandomForest", "GradientBoosting", "SVM"]

# Risk level thresholds
RISK_THRESHOLDS = {
    "critical": 0.95,
    "high": 0.85,
    "medium": 0.65,
    "low": 0.40,
    "safe": 0.0,
}

# Prediction history max records
MAX_HISTORY_RECORDS = 1000

# App settings
HOST = "0.0.0.0"
PORT = 5000
THREADS = 4
