"""
Main Flask Application - Email Scam & Phishing Detection Platform
Production-ready with fault tolerance and error prevention
"""

import json
import time
from datetime import datetime
from pathlib import Path

from flask import Flask, jsonify, render_template, request

import config
from utils.data_handler import DataHandler
from utils.logger import get_logger
from utils.ml_engine import MLEngine
from utils.text_processor import TextProcessor

logger = get_logger(__name__)

# Initialize Flask app
app = Flask(__name__, template_folder="templates", static_folder="static")
app.config.from_object(config)

# Global components
ml_engine = None
text_processor = None
data_handler = None
app_ready = False
startup_diagnostics = {}


def init_components():
    """Initialize all application components"""
    global ml_engine, text_processor, data_handler, app_ready, startup_diagnostics

    startup_time = time.time()
    diagnostics = {"timestamp": datetime.now().isoformat(), "checks": {}}

    try:
        logger.info("=" * 50)
        logger.info("INITIALIZING EMAIL SCAM DETECTOR")
        logger.info("=" * 50)

        # Initialize text processor
        try:
            logger.info("Initializing text processor...")
            text_processor = TextProcessor()
            diagnostics["checks"]["text_processor"] = {"status": "success"}
            logger.info("✓ Text processor initialized")
        except Exception as e:
            logger.error(f"✗ Text processor initialization failed: {e}")
            diagnostics["checks"]["text_processor"] = {"status": "failed", "error": str(e)}

        # Initialize data handler
        try:
            logger.info("Initializing data handler...")
            data_handler = DataHandler(
                config.DATASET_PATH, [config.DATASET_URL, config.DATASET_BACKUP_URL]
            )
            diagnostics["checks"]["data_handler"] = {"status": "success"}
            logger.info("✓ Data handler initialized")
        except Exception as e:
            logger.error(f"✗ Data handler initialization failed: {e}")
            diagnostics["checks"]["data_handler"] = {"status": "failed", "error": str(e)}

        # Initialize ML engine
        try:
            logger.info("Initializing ML engine...")
            ml_engine = MLEngine(config.MODEL_PATH, config.VECTORIZER_PATH, config.SCALER_PATH)
            diagnostics["checks"]["ml_engine"] = {"status": "success"}
            logger.info("✓ ML engine initialized")
        except Exception as e:
            logger.error(f"✗ ML engine initialization failed: {e}")
            diagnostics["checks"]["ml_engine"] = {"status": "failed", "error": str(e)}

        # Load or train model
        try:
            logger.info("Checking for saved models...")
            if config.MODEL_PATH.exists() and config.VECTORIZER_PATH.exists():
                logger.info("Loading saved models...")
                if ml_engine.load_models():
                    diagnostics["checks"]["model_loading"] = {"status": "success"}
                    logger.info("✓ Models loaded successfully")
                else:
                    raise Exception("Failed to load models")
            else:
                logger.info("No saved models found, training new models...")
                if data_handler and ml_engine:
                    df = data_handler.load_dataset()
                    if df is not None and len(df) > 0:
                        logger.info(f"Training on {len(df)} samples...")
                        if ml_engine.train(df["text"], df["spam"], config.FEATURE_PARAMS):
                            diagnostics["checks"]["model_training"] = {"status": "success"}
                            logger.info("✓ Models trained successfully")
                        else:
                            raise Exception("Model training failed")
                    else:
                        raise Exception("No valid dataset available")
                else:
                    raise Exception("Dependencies not initialized")
        except Exception as e:
            logger.error(f"✗ Model initialization failed: {e}")
            diagnostics["checks"]["model_loading"] = {"status": "failed", "error": str(e)}

        # Verify model readiness
        if ml_engine and ml_engine.is_ready():
            app_ready = True
            diagnostics["checks"]["model_readiness"] = {"status": "success"}
            logger.info("✓ Model is ready for predictions")
        else:
            logger.warning("⚠ Model is not ready for predictions")
            diagnostics["checks"]["model_readiness"] = {"status": "warning"}

        diagnostics["startup_time_ms"] = round((time.time() - startup_time) * 1000)
        diagnostics["status"] = "healthy" if app_ready else "degraded"

        logger.info("=" * 50)
        logger.info(f"STARTUP STATUS: {diagnostics['status'].upper()}")
        logger.info("=" * 50)

        startup_diagnostics.update(diagnostics)
        return app_ready

    except Exception as e:
        logger.error(f"Critical initialization error: {e}")
        startup_diagnostics.update(
            {
                "status": "failed",
                "error": str(e),
                "timestamp": datetime.now().isoformat(),
            }
        )
        return False


def get_risk_level(confidence):
    """Determine risk level based on confidence score"""
    try:
        from config import RISK_THRESHOLDS

        if confidence >= RISK_THRESHOLDS["critical"]:
            return "CRITICAL"
        elif confidence >= RISK_THRESHOLDS["high"]:
            return "HIGH"
        elif confidence >= RISK_THRESHOLDS["medium"]:
            return "MEDIUM"
        elif confidence >= RISK_THRESHOLDS["low"]:
            return "LOW"
        else:
            return "SAFE"
    except Exception as e:
        logger.error(f"Error determining risk level: {e}")
        return "UNKNOWN"


def get_threat_summary(prediction, confidence, email_text):
    """Generate threat summary"""
    try:
        threat_type = "Phishing/Scam" if prediction == 1 else "Legitimate"
        risk_level = get_risk_level(confidence)

        summaries = {
            "CRITICAL": f"CRITICAL THREAT: High-confidence {threat_type} email detected. DO NOT click links or provide information.",
            "HIGH": f"HIGH RISK: This email shows strong signs of being {threat_type.lower()}. Exercise caution.",
            "MEDIUM": f"MEDIUM RISK: This email contains some suspicious characteristics typical of {threat_type.lower()} attempts.",
            "LOW": f"LOW RISK: Some minor suspicious indicators detected, but likely {threat_type.lower()}.",
            "SAFE": "SAFE: This email appears to be legitimate with very low risk indicators.",
        }

        return summaries.get(risk_level, "Unable to assess threat level")
    except Exception as e:
        logger.error(f"Error generating threat summary: {e}")
        return "Error generating summary"


def validate_input(text):
    """Validate user input"""
    try:
        if not text or not isinstance(text, str):
            return False, "Input must be a non-empty string"

        text = text.strip()
        if len(text) < 5:
            return False, "Input must be at least 5 characters long"

        if len(text) > 50000:
            return False, "Input must not exceed 50000 characters"

        return True, text
    except Exception as e:
        logger.error(f"Error validating input: {e}")
        return False, "Input validation error"


# ============================================================================
# API ROUTES
# ============================================================================


@app.route("/", methods=["GET"])
def index():
    """Serve main page"""
    try:
        return render_template("index.html")
    except Exception as e:
        logger.error(f"Error serving index: {e}")
        return jsonify({"error": "Could not load application"}), 500


@app.route("/api/health", methods=["GET"])
def health():
    """Health check endpoint"""
    try:
        return jsonify(
            {
                "status": "healthy" if app_ready else "degraded",
                "model_ready": ml_engine.is_ready() if ml_engine else False,
                "timestamp": datetime.now().isoformat(),
            }
        )
    except Exception as e:
        logger.error(f"Error in health check: {e}")
        return jsonify({"status": "error", "error": str(e)}), 500


@app.route("/api/diagnostics", methods=["GET"])
def diagnostics():
    """Get startup diagnostics"""
    try:
        return jsonify(startup_diagnostics)
    except Exception as e:
        logger.error(f"Error getting diagnostics: {e}")
        return jsonify({"error": "Could not retrieve diagnostics"}), 500


@app.route("/api/predict", methods=["POST"])
def predict():
    """Predict if email is spam/phishing"""
    try:
        # Validate app readiness
        if not app_ready or not ml_engine or not ml_engine.is_ready():
            return (
                jsonify({"error": "Model not ready. Please wait for system initialization."}),
                503,
            )

        # Get input
        data = request.get_json()
        if not data or "email" not in data:
            return jsonify({"error": "Missing 'email' field in request"}), 400

        email_text = data.get("email", "").strip()

        # Validate input
        is_valid, result = validate_input(email_text)
        if not is_valid:
            return jsonify({"error": result}), 400

        email_text = result

        # Process text
        try:
            processed_text = text_processor.process(email_text)
            if not processed_text:
                processed_text = email_text.lower()
        except Exception as e:
            logger.warning(f"Error processing text: {e}")
            processed_text = email_text.lower()

        # Predict
        try:
            prediction, probabilities = ml_engine.predict([processed_text])

            if prediction is None or probabilities is None:
                return jsonify({"error": "Prediction failed"}), 500

            pred = int(prediction[0])
            probs = probabilities[0]

            # Get confidence
            confidence = float(max(probs))

            # Determine classification
            if pred == 1:
                classification = "PHISHING/SCAM"
                confidence_pct = float(probs[1]) * 100
            else:
                classification = "LEGITIMATE"
                confidence_pct = float(probs[0]) * 100

            risk_level = get_risk_level(confidence)
            threat_summary = get_threat_summary(pred, confidence, email_text)

            response = {
                "classification": classification,
                "confidence_score": round(confidence_pct, 2),
                "risk_level": risk_level,
                "threat_summary": threat_summary,
                "timestamp": datetime.now().isoformat(),
                "email_preview": email_text[:100] + ("..." if len(email_text) > 100 else ""),
            }

            # Save to history
            try:
                if data_handler:
                    data_handler.save_history(config.HISTORY_PATH, [response])
            except Exception as e:
                logger.warning(f"Could not save prediction to history: {e}")

            return jsonify(response)

        except Exception as e:
            logger.error(f"Error in prediction: {e}")
            return jsonify({"error": "Prediction failed", "details": str(e)}), 500

    except Exception as e:
        logger.error(f"Error in /api/predict: {e}")
        return jsonify({"error": "Request processing failed"}), 500


@app.route("/api/history", methods=["GET"])
def get_history():
    """Get prediction history"""
    try:
        if not data_handler:
            return jsonify({"history": []})

        history = data_handler.load_history(config.HISTORY_PATH)
        return jsonify({"history": history[-50:]})  # Return last 50

    except Exception as e:
        logger.error(f"Error getting history: {e}")
        return jsonify({"history": [], "error": str(e)})


@app.route("/api/stats", methods=["GET"])
def get_stats():
    """Get prediction statistics"""
    try:
        if not data_handler:
            return jsonify({"stats": {}})

        history = data_handler.load_history(config.HISTORY_PATH)

        if not history:
            return jsonify(
                {
                    "stats": {
                        "total_predictions": 0,
                        "scam_detected": 0,
                        "legitimate": 0,
                        "average_confidence": 0,
                    }
                }
            )

        total = len(history)
        scam = sum(
            1 for h in history if "classification" in h and "PHISHING" in h["classification"]
        )
        legit = total - scam

        avg_confidence = (
            sum(h.get("confidence_score", 0) for h in history) / total if total > 0 else 0
        )

        risk_counts = {}
        for h in history:
            risk = h.get("risk_level", "UNKNOWN")
            risk_counts[risk] = risk_counts.get(risk, 0) + 1

        return jsonify(
            {
                "stats": {
                    "total_predictions": total,
                    "scam_detected": scam,
                    "legitimate": legit,
                    "average_confidence": round(avg_confidence, 2),
                    "risk_distribution": risk_counts,
                }
            }
        )

    except Exception as e:
        logger.error(f"Error getting stats: {e}")
        return jsonify({"stats": {}, "error": str(e)})


@app.route("/api/metrics", methods=["GET"])
def get_metrics():
    """Get model training metrics"""
    try:
        if not ml_engine:
            return jsonify({"metrics": {}})

        metrics = ml_engine.get_metrics()
        best_model = ml_engine.best_model_name

        return jsonify({"metrics": metrics, "best_model": best_model})

    except Exception as e:
        logger.error(f"Error getting metrics: {e}")
        return jsonify({"metrics": {}, "error": str(e)})


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({"error": "Endpoint not found"}), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    logger.error(f"Internal server error: {error}")
    return jsonify({"error": "Internal server error"}), 500


# ============================================================================
# APP STARTUP
# ============================================================================


if __name__ == "__main__":
    try:
        logger.info("Starting Email Scam Detection Platform...")

        # Initialize components
        if init_components():
            logger.info("✓ Application initialized successfully")
        else:
            logger.warning("⚠ Application initialized with warnings")

        # Start Flask server
        logger.info(f"Starting Flask server on {config.HOST}:{config.PORT}")
        app.run(
            host=config.HOST, port=config.PORT, debug=config.DEBUG, threaded=True, use_reloader=False
        )

    except Exception as e:
        logger.error(f"Critical error starting application: {e}")
        raise
