import os
import sys
from datetime import datetime
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup

# Add the parent directory to sys.path to allow absolute imports
sys.path.append(os.path.abspath(os.path.dirname(os.path.dirname(__file__))))

import joblib
import numpy as np
from flask import Flask, jsonify, request
from flask_cors import CORS

from backend.models import URLCheck, User, db
from backend.utils.auth import bcrypt, generate_token, token_required
from backend.utils.logger import log_error, logger
from backend.utils.url_features import (ESSENTIAL_FEATURES,
                                        get_essential_features)

app = Flask(__name__)
CORS(app, resources={
    r"/*": {
        "origins": ["https://phisshield.onrender.com", "http://localhost:5173"],
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"],
        "expose_headers": ["Content-Type", "Authorization"],
        "supports_credentials": True,
        "allow_credentials": True
    }
})

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', request.headers.get('Origin', '*'))
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    response.headers.add('Access-Control-Allow-Credentials', 'true')
    return response

# Configuration
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your-secret-key-here')  # Change in production
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///phishshield.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize extensions
db.init_app(app)
bcrypt.init_app(app)

# Create database tables
with app.app_context():
    db.create_all()

# Get the absolute path to the model directory (use root model directory)
current_dir = os.path.dirname(os.path.abspath(__file__))
model_dir = os.path.join(os.path.dirname(current_dir), 'model')  # Use root model directory

# Load the model and scaler with absolute paths
model_path = os.path.join(model_dir, 'phishing_model.pkl')
scaler_path = os.path.join(model_dir, 'scaler.pkl')
feature_names_path = os.path.join(model_dir, 'feature_names.pkl')

logger.info(f"Loading model from: {model_dir}")  # Debug print

try:
    model = joblib.load(model_path)
    scaler = joblib.load(scaler_path)
    feature_names = joblib.load(feature_names_path)
    logger.info("Model loaded successfully")
    logger.debug(f"Loaded feature names: {feature_names}")  # Debug print
    logger.debug(f"Current ESSENTIAL_FEATURES: {ESSENTIAL_FEATURES}")  # Debug print
except Exception as e:
    log_error(e, f"Failed to load model from {model_dir}")
    model = None
    scaler = None
    feature_names = None

@app.errorhandler(404)
def not_found(error):
    log_error(error, f"Route not found: {request.url}")
    return jsonify({"error": "Not found"}), 404

@app.errorhandler(500)
def internal_error(error):
    log_error(error, f"Internal server error on {request.url}")
    return jsonify({"error": "Internal server error"}), 500

@app.route('/', methods=['GET'])
def home():
    return jsonify({"message": "PhishShield API is running"}), 200

@app.route('/api/health', methods=['GET'])
def health_check():
    if model is None or scaler is None:
        log_error("Health check failed - model not loaded")
        return jsonify({"status": "unhealthy", "reason": "Model not loaded"}), 503
    return jsonify({"status": "healthy"}), 200

@app.route('/api/auth/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')

        if User.query.filter_by(username=username).first():
            return jsonify({'error': 'Username already exists'}), 400
        if User.query.filter_by(email=email).first():
            return jsonify({'error': 'Email already exists'}), 400

        # Create new user
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        new_user = User(username=username, email=email, password_hash=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        # Generate token
        token = generate_token(new_user.id)
        return jsonify({
            'token': token,
            'username': new_user.username
        }), 201
    except Exception as e:
        log_error(e, "Registration failed")
        return jsonify({'error': 'Registration failed'}), 500

@app.route('/api/auth/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        logger.info(f"Login attempt for username: {data.get('username')}")
        username = data.get('username')
        password = data.get('password')

        # Find user by username
        user = User.query.filter_by(username=username).first()
        if not user:
            return jsonify({'error': 'Invalid username or password'}), 401

        # Check password
        if not bcrypt.check_password_hash(user.password_hash, password):
            return jsonify({'error': 'Invalid username or password'}), 401

        # Generate token
        token = generate_token(user.id)
        return jsonify({
            'token': token,
            'username': user.username
        }), 200
    except Exception as e:
        log_error(e, "Login failed")
        return jsonify({'error': 'Login failed'}), 500

@app.route('/api/history', methods=['GET'])
@token_required
def get_history(current_user):
    try:
        checks = URLCheck.query.filter_by(user_id=current_user.id).order_by(URLCheck.checked_at.desc()).all()
        history = [{
            'url': check.url,
            'is_phishing': check.is_phishing,
            'confidence': check.confidence,
            'checked_at': check.checked_at.isoformat()
        } for check in checks]
        return jsonify(history)
    except Exception as e:
        log_error(e, "Failed to fetch history")
        return jsonify({'error': 'Failed to fetch history'}), 500

@app.route('/api/predict', methods=['POST'])
@token_required
def predict(current_user):
    try:
        data = request.get_json()
        url = data.get('url')
        
        if not url:
            logger.warning("Prediction attempt with missing URL")
            return jsonify({"error": "URL is required"}), 400
        
        # Extract essential features from URL
        try:
            features = get_essential_features(url)
            logger.debug(f"Extracted features for URL {url}: {features}")
        except Exception as e:
            log_error(e, f"Feature extraction failed for URL: {url}")
            return jsonify({"error": f"Error extracting features: {str(e)}"}), 500
        
        # Ensure all expected features are present
        for feature in ESSENTIAL_FEATURES:
            if feature not in features:
                features[feature] = -1  # Use -1 as default for missing features
                
        # Convert features to the expected format
        feature_vector = [features[feature] for feature in ESSENTIAL_FEATURES]
        logger.debug(f"Feature vector: {feature_vector}")
        
        if model is None or scaler is None:
            logger.error("Model or scaler is None")
            return jsonify({"error": "Model not loaded"}), 500
        
        # Check feature names match
        try:
            if feature_names is not None:
                if len(feature_names) != len(ESSENTIAL_FEATURES):
                    log_error("Feature mismatch", 
                             f"stored={len(feature_names)}, current={len(ESSENTIAL_FEATURES)}")
                    return jsonify({"error": "Model feature mismatch - retrain model"}), 500
        except Exception as e:
            log_error(e, "Error checking feature names")
        
        # Convert feature vector to numpy array and scale
        try:
            feature_vector = np.array(feature_vector).reshape(1, -1)
            scaled_features = scaler.transform(feature_vector)
        except Exception as e:
            log_error(e, "Error processing features")
            return jsonify({"error": "Error processing URL features"}), 500
        
        # Make prediction
        try:
            prediction = model.predict(scaled_features)[0]
            probability = model.predict_proba(scaled_features)[0]
            
            # Calculate confidence based on the prediction
            # probability[0] is confidence of being legitimate
            # probability[1] is confidence of being phishing
            is_phishing = bool(prediction)
            confidence = float(probability[1] if is_phishing else probability[0])
            
            # Adjust threshold based on prediction
            # For phishing predictions, we want higher confidence (0.6)
            # For legitimate predictions, we can be less strict (0.5)
            if is_phishing and confidence < 0.6:
                is_phishing = False
                confidence = float(probability[0])  # Use legitimate confidence
            
            logger.debug(f"Prediction probabilities: legitimate={probability[0]:.3f}, phishing={probability[1]:.3f}")
            logger.debug(f"Final prediction: is_phishing={is_phishing}, confidence={confidence:.3f}")
            
        except Exception as e:
            log_error(e, "Error making prediction")
            return jsonify({"error": "Error making prediction"}), 500
        
        # Store the check in history
        url_check = URLCheck(
            url=url,
            is_phishing=is_phishing,
            confidence=confidence,
            features=features,
            user_id=current_user.id
        )
        db.session.add(url_check)
        db.session.commit()
        
        response = {
            "is_phishing": is_phishing,
            "confidence": confidence,
            "features": features
        }
        
        logger.info(f"Prediction complete for {url}: {'phishing' if is_phishing else 'legitimate'}")
        return jsonify(response), 200
        
    except Exception as e:
        log_error(e, f"Unexpected error during prediction: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/url-info', methods=['GET'])
@token_required
def get_url_info(current_user):
    url = request.args.get('url')
    if not url:
        return jsonify({'error': 'URL is required'}), 400

    try:
        logger.info(f"Fetching URL info for: {url}")
        
        # Add headers to mimic a browser request
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        # Extract domain first in case request fails
        domain = urlparse(url).netloc
        
        # Make request with a timeout, first try with verification
        try:
            logger.debug("Attempting request with SSL verification")
            response = requests.get(url, headers=headers, timeout=5, verify=True)
        except requests.exceptions.SSLError:
            logger.debug("SSL verification failed, retrying without verification")
            response = requests.get(url, headers=headers, timeout=5, verify=False)
        except requests.exceptions.RequestException as e:
            logger.error(f"Request failed: {str(e)}")
            # Return minimal info if request fails
            return jsonify({
                'title': None,
                'description': None,
                'type': None,
                'domain': domain,
                'error': 'Could not connect to website'
            })
        
        logger.debug(f"Request successful, status code: {response.status_code}")
        
        if not response.text:
            logger.warning("Empty response received")
            return jsonify({
                'title': None,
                'description': None,
                'type': response.headers.get('content-type', '').split(';')[0],
                'domain': domain,
                'error': 'Empty response'
            })
            
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract information with error handling
        try:
            title = soup.title.string.strip() if soup.title else None
            logger.debug(f"Extracted title: {title}")
        except Exception as e:
            logger.warning(f"Failed to extract title: {str(e)}")
            title = None

        # Try to get meta description
        try:
            meta_desc = soup.find('meta', attrs={'name': 'description'})
            if not meta_desc:
                meta_desc = soup.find('meta', attrs={'property': 'og:description'})
            description = meta_desc.get('content', '').strip() if meta_desc else None
            logger.debug(f"Extracted description: {description}")
        except Exception as e:
            logger.warning(f"Failed to extract description: {str(e)}")
            description = None

        content_type = response.headers.get('content-type', '').split(';')[0]
        
        info = {
            'title': title,
            'description': description,
            'type': content_type,
            'domain': domain,
            'status': response.status_code
        }

        # Try to get meta description
        meta_desc = soup.find('meta', attrs={'name': 'description'}) or \
                   soup.find('meta', attrs={'property': 'og:description'})
        if meta_desc:
            info['description'] = meta_desc.get('content', '').strip()

        return jsonify(info)

    except requests.RequestException as e:
        log_error(f"Error fetching URL info: {str(e)}")
        return jsonify({'error': 'Could not fetch URL information'}), 400
    except Exception as e:
        log_error(f"Unexpected error while fetching URL info: {str(e)}")
        return jsonify({'error': 'An unexpected error occurred'}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)