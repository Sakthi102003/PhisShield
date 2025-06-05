import json
import os
import sys  # Add sys import
from datetime import datetime, timedelta

# Add the parent directory (backend) to sys.path
# os.path.dirname(__file__) is the 'model' directory
# os.path.abspath(os.path.join(os.path.dirname(__file__), '..')) is the 'backend' directory
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import joblib
import numpy as np
import pandas as pd
import requests
import xgboost as xgb
from sklearn.metrics import accuracy_score, classification_report
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from tqdm import tqdm
from utils.url_features import ESSENTIAL_FEATURES  # Moved import to top
from utils.url_features import get_essential_features


def fetch_phishtank_data():
    """
    Fetch recent phishing data from PhishTank API.
    Returns a DataFrame with URLs and their status.
    """
    print("Fetching data from PhishTank...")
    
    # PhishTank API endpoint
    url = "https://data.phishtank.com/data/online-valid.json"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        
        # Convert to DataFrame
        df = pd.DataFrame(data)
        
        # Filter for verified phishing URLs
        df = df[df['verified'] == True]
        
        # Get only the last 30 days of data
        df['submission_time'] = pd.to_datetime(df['submission_time'])
        cutoff_date = datetime.now() - timedelta(days=30)
        df = df[df['submission_time'] >= cutoff_date]
        
        print(f"Fetched {len(df)} recent phishing URLs")
        return df
        
    except Exception as e:
        print(f"Error fetching PhishTank data: {e}")
        print("Using fallback phishing dataset...")
        return get_fallback_phishing_data()

def get_fallback_phishing_data():
    """
    Fallback phishing dataset when PhishTank is unavailable.
    """
    phishing_urls = [
        "http://phishing-example1.com/login",
        "https://fake-bank.net/secure",
        "http://suspicious-site.org/verify",
        "https://scam-paypal.com/signin",
        "http://fake-amazon.net/account",
        "https://phish-google.org/login",
        "http://malicious-ebay.com/signin",
        "https://fake-microsoft.net/office",
        "http://scam-apple.org/icloud",
        "https://phishing-netflix.com/login",
        "http://fake-facebook.net/login",
        "https://suspicious-instagram.org/auth",
        "http://scam-twitter.com/signin",
        "https://fake-linkedin.net/login",
        "http://phishing-github.org/signin",
        "https://malicious-dropbox.com/login",
        "http://fake-spotify.net/account",
        "https://scam-uber.org/signin",
        "http://phishing-zoom.com/signin",
        "https://fake-whatsapp.net/web"
    ]
    
    data = []
    for url in phishing_urls:
        data.append({
            'url': url,
            'phish_id': f"fallback_{hash(url) % 100000}",
            'verified': True,
            'submission_time': datetime.now()
        })
    
    df = pd.DataFrame(data)
    print(f"Using fallback dataset with {len(df)} phishing URLs")
    return df

def fetch_legitimate_urls():
    """
    Fetch legitimate URLs from various sources.
    Returns a DataFrame with legitimate URLs.
    """
    print("Fetching legitimate URLs...")
    
    # List of legitimate domains to sample from
    legitimate_domains = [
        'google.com', 'microsoft.com', 'apple.com', 'amazon.com',
        'facebook.com', 'twitter.com', 'linkedin.com', 'github.com',
        'netflix.com', 'spotify.com', 'youtube.com', 'wikipedia.org',
        'reddit.com', 'instagram.com', 'yahoo.com', 'bing.com',
        'wordpress.com', 'medium.com', 'quora.com', 'stackoverflow.com'
    ]
    
    # Generate URLs with various paths and parameters
    legitimate_urls = []
    for domain in legitimate_domains:
        # Add some common paths
        paths = ['', '/about', '/contact', '/products', '/services', 
                '/blog', '/news', '/support', '/help', '/login']
        
        # Add some common parameters
        params = ['', '?ref=home', '?source=main', '?lang=en', 
                 '?utm_source=direct', '?page=1']
        
        for path in paths:
            for param in params:
                url = f"https://{domain}{path}{param}"
                legitimate_urls.append({
                    'url': url,
                    'verified': True,
                    'submission_time': datetime.now()
                })
    
    df = pd.DataFrame(legitimate_urls)
    print(f"Generated {len(df)} legitimate URLs")
    return df

def prepare_dataset():
    """
    Prepare the dataset by combining phishing and legitimate URLs.
    Returns features and labels.
    """
    # Fetch phishing URLs
    phishing_df = fetch_phishtank_data()
    if phishing_df is None or phishing_df.empty:
        print("No phishing data available, using fallback dataset")
        phishing_df = get_fallback_phishing_data()
    
    # Fetch legitimate URLs
    legitimate_df = fetch_legitimate_urls()
    
    # Combine datasets
    df = pd.concat([phishing_df, legitimate_df], ignore_index=True)
    
    # Create labels (1 for phishing, 0 for legitimate)
    df['label'] = df['url'].isin(phishing_df['url']).astype(int)
    
    # Extract features using the optimized essential features function
    print("Extracting essential features...")
    features_list = []
    
    for url in tqdm(df['url']):
        features = get_essential_features(url)
        # Ensure all expected features are present
        for feature in ESSENTIAL_FEATURES:
            if feature not in features:
                features[feature] = -1  # Use -1 as default for missing features
        features_list.append({k: features[k] for k in ESSENTIAL_FEATURES})
    
    # Convert features to DataFrame
    X = pd.DataFrame(features_list)
    y = df['label']
    
    return X, y

def train_model():
    """
    Train the phishing detection model using recent data.
    """
    print("Preparing dataset...")
    X, y = prepare_dataset()
    
    # Split the data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    
    # Scale the features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # Train XGBoost model
    print("Training model...")
    model = xgb.XGBClassifier(
        n_estimators=100,
        learning_rate=0.1,
        max_depth=5,
        random_state=42
    )
    
    model.fit(X_train_scaled, y_train)
    
    # Evaluate the model
    y_pred = model.predict(X_test_scaled)
    accuracy = accuracy_score(y_test, y_pred)
    print(f"\nModel Accuracy: {accuracy:.2f}")
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred))
    
    # Save the model and scaler
    os.makedirs('model', exist_ok=True)
    joblib.dump(model, 'model/phishing_model.pkl')
    joblib.dump(scaler, 'model/scaler.pkl')
    
    # Save feature names using ESSENTIAL_FEATURES to ensure consistency
    joblib.dump(ESSENTIAL_FEATURES, 'model/feature_names.pkl')
    print(f"Saved feature names: {ESSENTIAL_FEATURES}") # Added print statement for verification
    
    return model, scaler, ESSENTIAL_FEATURES # Return ESSENTIAL_FEATURES

if __name__ == "__main__":
    train_model()