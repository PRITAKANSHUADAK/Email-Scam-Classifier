"""
Text processing utilities for NLP tasks
"""

import re
import string

import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize

from utils.logger import get_logger

logger = get_logger(__name__)

# Download required NLTK data
try:
    nltk.data.find("tokenizers/punkt")
except LookupError:
    nltk.download("punkt", quiet=True)

try:
    nltk.data.find("corpora/stopwords")
except LookupError:
    nltk.download("stopwords", quiet=True)

try:
    nltk.data.find("corpora/wordnet")
except LookupError:
    nltk.download("wordnet", quiet=True)


class TextProcessor:
    """Handles text preprocessing and cleaning"""

    def __init__(self):
        try:
            self.stop_words = set(stopwords.words("english"))
            self.lemmatizer = WordNetLemmatizer()
        except Exception as e:
            logger.warning(f"Error loading NLTK resources: {e}")
            self.stop_words = set()
            self.lemmatizer = None

    def clean_text(self, text):
        """Clean and normalize text"""
        try:
            if not isinstance(text, str):
                return ""

            # Convert to lowercase
            text = text.lower()

            # Remove URLs
            text = re.sub(r"http\S+|www\S+|https\S+", "", text, flags=re.MULTILINE)

            # Remove email addresses
            text = re.sub(r"\S+@\S+", "", text)

            # Remove special characters but keep spaces
            text = re.sub(r"[^a-zA-Z0-9\s]", "", text)

            # Remove extra whitespace
            text = re.sub(r"\s+", " ", text).strip()

            return text
        except Exception as e:
            logger.error(f"Error cleaning text: {e}")
            return ""

    def tokenize(self, text):
        """Tokenize text"""
        try:
            text = self.clean_text(text)
            if not text:
                return []
            return text.split()
        except Exception as e:
            logger.error(f"Error tokenizing text: {e}")
            return []

    def remove_stopwords(self, tokens):
        """Remove stopwords from tokens"""
        try:
            if not self.stop_words:
                return tokens
            return [token for token in tokens if token not in self.stop_words]
        except Exception as e:
            logger.error(f"Error removing stopwords: {e}")
            return tokens

    def lemmatize(self, tokens):
        """Lemmatize tokens"""
        try:
            if not self.lemmatizer:
                return tokens
            return [self.lemmatizer.lemmatize(token) for token in tokens]
        except Exception as e:
            logger.error(f"Error lemmatizing tokens: {e}")
            return tokens

    def process(self, text):
        """Complete text processing pipeline"""
        try:
            tokens = self.tokenize(text)
            tokens = self.remove_stopwords(tokens)
            tokens = self.lemmatize(tokens)
            return " ".join(tokens)
        except Exception as e:
            logger.error(f"Error in text processing pipeline: {e}")
            return ""
