"""
Machine Learning engine for model training and prediction
"""

import pickle
from pathlib import Path

import numpy as np
from sklearn.ensemble import GradientBoostingClassifier, RandomForestClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    f1_score,
    precision_score,
    recall_score,
    cross_val_score,
)
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC

from utils.logger import get_logger

logger = get_logger(__name__)


class MLEngine:
    """Machine Learning engine for training and prediction"""

    def __init__(self, model_path, vectorizer_path, scaler_path):
        self.model_path = Path(model_path)
        self.vectorizer_path = Path(vectorizer_path)
        self.scaler_path = Path(scaler_path)
        self.model = None
        self.vectorizer = None
        self.scaler = None
        self.best_model_name = None
        self.metrics = {}

    def train(self, X, y, feature_params=None):
        """Train multiple models and select the best one"""
        try:
            logger.info("Starting model training...")

            feature_params = feature_params or {}

            # Create TF-IDF vectorizer
            logger.info("Creating TF-IDF vectorizer...")
            self.vectorizer = TfidfVectorizer(**feature_params)
            X_tfidf = self.vectorizer.fit_transform(X)

            # Split data
            logger.info("Splitting data...")
            X_train, X_test, y_train, y_test = train_test_split(
                X_tfidf, y, test_size=0.2, random_state=42
            )

            # Train multiple models
            models = {
                "LogisticRegression": LogisticRegression(max_iter=1000, random_state=42),
                "RandomForest": RandomForestClassifier(n_estimators=100, random_state=42),
                "GradientBoosting": GradientBoostingClassifier(n_estimators=100, random_state=42),
                "SVM": SVC(kernel="rbf", probability=True, random_state=42),
            }

            best_score = 0
            best_model = None

            for name, model in models.items():
                try:
                    logger.info(f"Training {name}...")
                    model.fit(X_train, y_train)

                    # Evaluate
                    y_pred = model.predict(X_test)
                    score = accuracy_score(y_test, y_pred)
                    f1 = f1_score(y_test, y_pred, zero_division=0)

                    # Cross-validation
                    cv_scores = cross_val_score(model, X_train, y_train, cv=5)

                    self.metrics[name] = {
                        "accuracy": float(score),
                        "f1": float(f1),
                        "precision": float(precision_score(y_test, y_pred, zero_division=0)),
                        "recall": float(recall_score(y_test, y_pred, zero_division=0)),
                        "cv_mean": float(cv_scores.mean()),
                        "cv_std": float(cv_scores.std()),
                    }

                    logger.info(
                        f"{name} - Accuracy: {score:.4f}, F1: {f1:.4f}, CV: {cv_scores.mean():.4f}"
                    )

                    if score > best_score:
                        best_score = score
                        best_model = model
                        self.best_model_name = name

                except Exception as e:
                    logger.error(f"Error training {name}: {e}")

            if best_model is None:
                logger.error("No model trained successfully")
                return False

            self.model = best_model
            logger.info(f"Best model: {self.best_model_name} with accuracy {best_score:.4f}")

            # Save models
            self._save_models()
            return True

        except Exception as e:
            logger.error(f"Error in training: {e}")
            return False

    def predict(self, texts):
        """Predict on new texts"""
        try:
            if self.model is None or self.vectorizer is None:
                logger.error("Model or vectorizer not loaded")
                return None

            # Transform texts
            X = self.vectorizer.transform(texts)

            # Predict
            predictions = self.model.predict(X)
            probabilities = self.model.predict_proba(X)

            return predictions, probabilities

        except Exception as e:
            logger.error(f"Error in prediction: {e}")
            return None, None

    def load_models(self):
        """Load saved models"""
        try:
            if self.model_path.exists():
                logger.info("Loading model...")
                with open(self.model_path, "rb") as f:
                    self.model = pickle.load(f)

            if self.vectorizer_path.exists():
                logger.info("Loading vectorizer...")
                with open(self.vectorizer_path, "rb") as f:
                    self.vectorizer = pickle.load(f)

            if self.scaler_path.exists():
                logger.info("Loading scaler...")
                with open(self.scaler_path, "rb") as f:
                    self.scaler = pickle.load(f)

            if self.model and self.vectorizer:
                logger.info("Models loaded successfully")
                return True
            return False

        except Exception as e:
            logger.error(f"Error loading models: {e}")
            return False

    def _save_models(self):
        """Save models to disk"""
        try:
            self.model_path.parent.mkdir(parents=True, exist_ok=True)

            if self.model:
                logger.info("Saving model...")
                with open(self.model_path, "wb") as f:
                    pickle.dump(self.model, f)

            if self.vectorizer:
                logger.info("Saving vectorizer...")
                with open(self.vectorizer_path, "wb") as f:
                    pickle.dump(self.vectorizer, f)

            if self.scaler:
                logger.info("Saving scaler...")
                with open(self.scaler_path, "wb") as f:
                    pickle.dump(self.scaler, f)

            logger.info("Models saved successfully")
        except Exception as e:
            logger.error(f"Error saving models: {e}")

    def get_metrics(self):
        """Get training metrics"""
        return self.metrics

    def is_ready(self):
        """Check if model is ready for prediction"""
        return self.model is not None and self.vectorizer is not None
