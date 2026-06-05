# Email Scam & Phishing Detection Platform

A production-ready AI-powered email security analysis system with advanced threat detection capabilities.

## 🚀 Features

### Core Functionality
- **Scam Detection**: Advanced ML models for identifying phishing and scam emails
- **Threat Classification**: Multi-class email classification (Phishing, Spam, Legitimate)
- **Confidence Scoring**: Probability-based confidence scores for predictions
- **Risk Assessment**: Multi-level risk evaluation (Critical, High, Medium, Low, Safe)
- **Threat Analysis**: Detailed threat summaries for each prediction

### Dashboard & Analytics
- **Real-time Analytics**: Live prediction statistics and trends
- **Prediction History**: Complete audit trail of all analyses
- **Risk Distribution**: Visual breakdown of threat levels
- **Model Metrics**: ML model performance metrics and comparison
- **Interactive Charts**: Chart.js-powered visualizations

### Reliability & Automation
- **Auto-initialization**: Automatic folder creation and configuration
- **Dataset Management**: Automatic dataset download and fallback
- **Model Training**: Automatic ML model training on startup
- **Model Persistence**: Saved models for instant loading
- **Error Recovery**: Comprehensive error handling and recovery
- **Health Checks**: Built-in system diagnostics

## 🛠️ Tech Stack

| Category | Technologies |
|----------|--------------|
| **Backend** | Python, Flask |
| **ML/Data** | Scikit-Learn, Pandas, NumPy, NLTK |
| **Frontend** | HTML5, CSS3, Vanilla JavaScript |
| **Visualization** | Chart.js |
| **Styling** | Premium Dark Theme with Glassmorphism |

## 📋 Requirements

- Python 3.8+
- pip (Python package manager)
- ~500MB disk space (for models and data)

## 🚀 Quick Start

### 1. Installation

```bash
# Clone or navigate to the project directory
cd Email-Scam-Classifier

# Install dependencies
pip install -r requirements.txt
```

### 2. Run the Application

```bash
# Start the Flask server
python app.py
```

The application will automatically:
- Create necessary directories
- Download the dataset (if not present)
- Train ML models (if not present)
- Initialize all components

### 3. Access the Application

Open your browser and navigate to:
```
http://localhost:5000
```

## 📱 User Interface

### Main Panel
- **Email Input**: Paste email content for analysis
- **Analyze Button**: Trigger real-time predictions
- **Result Display**: Comprehensive threat assessment

### Dashboard Sections
- **Statistics**: Total predictions, threats detected, average confidence
- **Model Info**: ML model performance metrics
- **Risk Distribution**: Visual breakdown of threat levels
- **Classification Overview**: Spam vs. Legitimate analysis
- **Prediction History**: Recent analysis records

## 🔌 API Endpoints

### Health & Status
```
GET /api/health          - System health check
GET /api/diagnostics     - Startup diagnostics
```

### Predictions
```
POST /api/predict        - Analyze email content
GET  /api/history        - Get prediction history
GET  /api/stats          - Get statistics
GET  /api/metrics        - Get model metrics
```

### Response Format

**Prediction Response:**
```json
{
  "classification": "LEGITIMATE",
  "confidence_score": 95.34,
  "risk_level": "SAFE",
  "threat_summary": "This email appears to be legitimate...",
  "timestamp": "2024-01-01T12:00:00",
  "email_preview": "Email content preview..."
}
```

## 🧠 Machine Learning

### Models Trained
- Logistic Regression
- Random Forest
- Gradient Boosting
- Support Vector Machine (SVM)

### Best Model Selection
Automatic selection based on:
- Accuracy
- F1-Score
- Precision & Recall
- Cross-validation scores

### Feature Engineering
- **TF-IDF Vectorization**: Text feature extraction
- **Text Cleaning**: URL and special character removal
- **Tokenization**: Word-level processing
- **Lemmatization**: Word normalization
- **Stopword Removal**: Noise reduction

## 🔒 Security Features

### Input Validation
- Email content length validation (5-50000 chars)
- Input sanitization
- Type checking
- Error message sanitization

### Error Handling
- Try-catch blocks in all critical functions
- Fallback mechanisms
- Graceful degradation
- Meaningful error messages

### Risk Management
- Multi-level threat assessment
- Confidence-based scoring
- Threat severity classification
- User warnings

## ⚙️ Configuration

All configuration is in `config.py`:

```python
# Dataset
DATASET_URL = "..."           # Primary dataset source
DATASET_BACKUP_URL = "..."    # Fallback source

# Model
TEST_SIZE = 0.2               # Train-test split
RANDOM_STATE = 42             # Reproducibility
N_FEATURES = 5000             # TF-IDF features

# Risk Levels (confidence thresholds)
RISK_THRESHOLDS = {
    "critical": 0.95,
    "high": 0.85,
    "medium": 0.65,
    "low": 0.40,
    "safe": 0.0,
}
```

## 📊 Data Flow

```
User Input (Email)
    ↓
Input Validation
    ↓
Text Processing (Clean, Tokenize, Lemmatize)
    ↓
TF-IDF Vectorization
    ↓
ML Model Prediction
    ↓
Risk Assessment & Scoring
    ↓
Result Display & Storage
```

## 🐛 Troubleshooting

### Port Already in Use
```bash
# Use different port
python app.py --port 5001
```

### Dataset Download Issues
The application automatically creates a sample dataset if download fails.

### Model Training Issues
Check `logs/app.log` for detailed error information.

### Frontend Not Loading
Clear browser cache and hard refresh (Ctrl+F5 or Cmd+Shift+R)

## 📈 Performance

- **Prediction Time**: <100ms per email
- **Model Training**: ~30-60 seconds (first run)
- **Memory Usage**: ~200-300MB
- **Scalability**: Multi-threaded Flask server

## 🔄 Auto-Recovery Features

| Issue | Recovery |
|-------|----------|
| Missing Dataset | Auto-download from URL or create sample |
| Missing Models | Auto-train from available dataset |
| Model Load Failure | Retrain models automatically |
| Empty Input | Validation error with guidance |
| API Crashes | Graceful error responses |

## 📝 Logging

Logs are saved to `logs/app.log`:
```
2024-01-01 12:00:00 - app - INFO - Application started
2024-01-01 12:00:05 - app - INFO - Model trained successfully
```

## 🎨 UI/UX Features

### Design
- **Dark Theme**: Professional cybersecurity aesthetic
- **Glassmorphism**: Modern frosted glass effect
- **Responsive Layout**: Mobile and desktop optimized
- **Smooth Animations**: Professional micro-interactions
- **Color Coding**: Risk-based visual feedback

### Accessibility
- High contrast text
- Readable font sizes
- Keyboard shortcuts (Ctrl+Enter to analyze)
- Semantic HTML structure

## 🚀 Deployment

### Production Checklist
- [ ] Set `DEBUG = False` in `config.py`
- [ ] Set strong `SECRET_KEY` in `config.py`
- [ ] Use production WSGI server (Gunicorn, uWSGI)
- [ ] Configure proper logging
- [ ] Set up regular backups
- [ ] Enable HTTPS/SSL

### Deployment with Gunicorn
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

## 📄 License

This project is provided as-is for educational and commercial use.

## 🙌 Support

For issues, questions, or suggestions, please check:
1. Application logs: `logs/app.log`
2. Browser console: F12 → Console tab
3. API diagnostics: `http://localhost:5000/api/diagnostics`

---

**Version**: 1.0  
**Last Updated**: 2024  
**Status**: Production Ready ✅
