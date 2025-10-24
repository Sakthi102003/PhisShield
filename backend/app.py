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
from flask import Flask, jsonify, make_response, request
from flask_cors import CORS

from backend.models import URLCheck, User, db
from backend.utils.auth import bcrypt, generate_token, token_required
from backend.utils.logger import log_error, logger
from backend.utils.url_features import (ESSENTIAL_FEATURES,
                                        get_essential_features)
from backend.utils.trusted_domains import is_trusted_domain

app = Flask(__name__)

# CORS Configuration - configure only once
app.config['CORS_HEADERS'] = 'Content-Type'
CORS(app, 
     origins=['https://phisshield.onrender.com', 'http://localhost:5173'],
     supports_credentials=True,
     allow_headers=['Content-Type', 'Authorization'],
     methods=['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'])

# Add COOP and COEP headers for Firebase popup authentication
@app.after_request
def add_security_headers(response):
    # Allow popups for Firebase authentication
    response.headers['Cross-Origin-Opener-Policy'] = 'same-origin-allow-popups'
    response.headers['Cross-Origin-Embedder-Policy'] = 'unsafe-none'
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

@app.route('/api/auth/google', methods=['POST'])
def google_auth():
    try:
        data = request.get_json()
        uid = data.get('uid')
        email = data.get('email')
        display_name = data.get('displayName')
        photo_url = data.get('photoURL')

        if not uid or not email:
            return jsonify({'error': 'Missing required fields'}), 400

        # Check if user already exists by email or google_uid
        user = User.query.filter(
            (User.email == email) | (User.google_uid == uid)
        ).first()

        if user:
            # Update user info if needed (photo might have changed)
            if not user.photo_url and photo_url:
                user.photo_url = photo_url
            if not user.display_name and display_name:
                user.display_name = display_name
            if not user.google_uid:
                user.google_uid = uid
                user.auth_provider = 'google'
            db.session.commit()
            
            # User exists, just log them in
            token = generate_token(user.id)
            return jsonify({
                'token': token,
                'username': user.username
            }), 200
        else:
            # Create new user with Google data
            # Use display_name or email prefix as username
            username = display_name if display_name else email.split('@')[0]
            
            # Make sure username is unique
            base_username = username
            counter = 1
            while User.query.filter_by(username=username).first():
                username = f"{base_username}{counter}"
                counter += 1

            # Create user without password (Google authenticated)
            # Use a random hash as placeholder since password is not needed
            import secrets
            random_password = secrets.token_urlsafe(32)
            hashed_password = bcrypt.generate_password_hash(random_password).decode('utf-8')
            
            new_user = User(
                username=username,
                email=email,
                password_hash=hashed_password,
                display_name=display_name,
                photo_url=photo_url,
                auth_provider='google',
                google_uid=uid
            )
            db.session.add(new_user)
            db.session.commit()

            # Generate token
            token = generate_token(new_user.id)
            return jsonify({
                'token': token,
                'username': new_user.username
            }), 201
    except Exception as e:
        log_error(e, "Google authentication failed")
        return jsonify({'error': 'Google authentication failed'}), 500

@app.route('/api/profile', methods=['GET'])
@token_required
def get_profile(current_user):
    try:
        return jsonify({
            'id': current_user.id,
            'username': current_user.username,
            'email': current_user.email,
            'display_name': current_user.display_name,
            'photo_url': current_user.photo_url,
            'auth_provider': current_user.auth_provider,
            'created_at': current_user.created_at.isoformat(),
            'total_scans': len(current_user.url_checks)
        }), 200
    except Exception as e:
        log_error(e, "Failed to fetch profile")
        return jsonify({'error': 'Failed to fetch profile'}), 500

@app.route('/api/profile', methods=['PUT'])
@token_required
def update_profile(current_user):
    try:
        data = request.get_json()
        
        # Update allowed fields
        if 'display_name' in data:
            current_user.display_name = data['display_name']
        
        if 'username' in data and data['username'] != current_user.username:
            # Check if username is already taken
            existing_user = User.query.filter_by(username=data['username']).first()
            if existing_user:
                return jsonify({'error': 'Username already taken'}), 400
            current_user.username = data['username']
        
        db.session.commit()
        
        return jsonify({
            'message': 'Profile updated successfully',
            'username': current_user.username,
            'display_name': current_user.display_name
        }), 200
    except Exception as e:
        log_error(e, "Failed to update profile")
        return jsonify({'error': 'Failed to update profile'}), 500

@app.route('/api/history', methods=['GET'])
@token_required
def get_history(current_user):
    try:
        # Get user's URL check history, ordered by most recent first
        history = URLCheck.query.filter_by(user_id=current_user.id)\
            .order_by(URLCheck.checked_at.desc()).all()
        
        return jsonify([{
            'url': check.url,
            'is_phishing': check.is_phishing,
            'confidence': check.confidence,
            'features': check.features,
            'checked_at': check.checked_at.isoformat()
        } for check in history]), 200
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
        
        # Check if domain is trusted first
        try:
            parsed_url = urlparse(url)
            domain = parsed_url.netloc.lower()
            if is_trusted_domain(domain):
                logger.info(f"URL from trusted domain: {domain}")
                # Store the check in history
                url_check = URLCheck(
                    url=url,
                    is_phishing=False,
                    confidence=0.99,  # High confidence for trusted domains
                    features={'domain_trusted': True, 'domain': domain},
                    user_id=current_user.id
                )
                db.session.add(url_check)
                db.session.commit()
                
                return jsonify({
                    "is_phishing": False,
                    "confidence": 0.99,
                    "features": {'domain_trusted': True, 'domain': domain},
                    "reason": "Trusted domain"
                }), 200
        except Exception as e:
            log_error(e, f"Error checking trusted domain for URL: {url}")
            # Continue with normal prediction if trust check fails
        
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

@app.route('/api/predict/bulk', methods=['POST'])
@token_required
def predict_bulk(current_user):
    try:
        data = request.get_json()
        urls = data.get('urls', [])
        
        if not urls or not isinstance(urls, list):
            return jsonify({"error": "URLs array is required"}), 400
        
        if len(urls) > 100:  # Limit to 100 URLs per request
            return jsonify({"error": "Maximum 100 URLs allowed per request"}), 400
        
        results = []
        
        for url in urls:
            try:
                # Check if domain is trusted first
                try:
                    parsed_url = urlparse(url)
                    domain = parsed_url.netloc.lower()
                    if is_trusted_domain(domain):
                        logger.info(f"Bulk scan: URL from trusted domain: {domain}")
                        # Store the check in history
                        url_check = URLCheck(
                            url=url,
                            is_phishing=False,
                            confidence=0.99,
                            features={'domain_trusted': True, 'domain': domain},
                            user_id=current_user.id
                        )
                        db.session.add(url_check)
                        
                        results.append({
                            'url': url,
                            'is_phishing': False,
                            'confidence': 0.99,
                            'features': {'domain_trusted': True, 'domain': domain}
                        })
                        continue  # Skip ML prediction for trusted domains
                except Exception as e:
                    log_error(e, f"Error checking trusted domain in bulk scan: {url}")
                    # Continue with normal prediction if trust check fails
                
                # Extract features
                features = get_essential_features(url)
                
                # Ensure all expected features are present
                for feature in ESSENTIAL_FEATURES:
                    if feature not in features:
                        features[feature] = -1
                        
                # Convert features to the expected format
                feature_vector = [features[feature] for feature in ESSENTIAL_FEATURES]
                
                if model is None or scaler is None:
                    results.append({
                        'url': url,
                        'error': 'Model not loaded'
                    })
                    continue
                
                # Convert feature vector to numpy array and scale
                feature_vector = np.array(feature_vector).reshape(1, -1)
                scaled_features = scaler.transform(feature_vector)
                
                # Make prediction
                prediction = model.predict(scaled_features)[0]
                probability = model.predict_proba(scaled_features)[0]
                
                is_phishing = bool(prediction)
                confidence = float(probability[1] if is_phishing else probability[0])
                
                # Adjust threshold
                if is_phishing and confidence < 0.6:
                    is_phishing = False
                    confidence = float(probability[0])
                
                # Store the check in history
                url_check = URLCheck(
                    url=url,
                    is_phishing=is_phishing,
                    confidence=confidence,
                    features=features,
                    user_id=current_user.id
                )
                db.session.add(url_check)
                
                results.append({
                    'url': url,
                    'is_phishing': is_phishing,
                    'confidence': confidence,
                    'features': features
                })
                
            except Exception as e:
                log_error(e, f"Error processing URL in bulk scan: {url}")
                results.append({
                    'url': url,
                    'error': str(e)
                })
        
        # Commit all URL checks at once
        db.session.commit()
        
        return jsonify({
            'results': results,
            'total': len(urls),
            'successful': len([r for r in results if 'error' not in r])
        }), 200
        
    except Exception as e:
        log_error(e, "Bulk scan failed")
        return jsonify({'error': str(e)}), 500

@app.route('/api/statistics', methods=['GET'])
@token_required
def get_statistics(current_user):
    try:
        # Get all URL checks for the current user
        checks = URLCheck.query.filter_by(user_id=current_user.id).all()
        
        if not checks:
            return jsonify({
                'total_scans': 0,
                'safe_count': 0,
                'phishing_count': 0,
                'average_confidence': 0,
                'recent_activity': [],
                'latest_scans': []
            }), 200
        
        total_scans = len(checks)
        phishing_count = sum(1 for check in checks if check.is_phishing)
        safe_count = total_scans - phishing_count
        
        # Calculate average confidence
        average_confidence = sum(check.confidence for check in checks) / total_scans * 100
        
        # Get recent activity (last 7 days)
        from datetime import datetime, timedelta
        from collections import defaultdict
        
        today = datetime.now().date()
        activity_data = defaultdict(int)
        
        for i in range(7):
            date = today - timedelta(days=6-i)
            activity_data[date.strftime('%m/%d')] = 0
        
        for check in checks:
            check_date = check.checked_at.date()
            if (today - check_date).days < 7:
                activity_data[check_date.strftime('%m/%d')] += 1
        
        recent_activity = [
            {'date': date, 'scans': count}
            for date, count in activity_data.items()
        ]
        
        # Get latest 5 scans
        latest_checks = sorted(checks, key=lambda x: x.checked_at, reverse=True)[:5]
        latest_scans = [{
            'url': check.url,
            'is_phishing': check.is_phishing,
            'confidence': check.confidence,
            'checked_at': check.checked_at.isoformat()
        } for check in latest_checks]
        
        return jsonify({
            'total_scans': total_scans,
            'safe_count': safe_count,
            'phishing_count': phishing_count,
            'average_confidence': average_confidence,
            'recent_activity': recent_activity,
            'latest_scans': latest_scans
        }), 200
        
    except Exception as e:
        log_error(e, "Failed to fetch statistics")
        return jsonify({'error': 'Failed to fetch statistics'}), 500

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