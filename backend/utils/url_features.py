import re
from typing import Any, Dict, Optional, Union
from urllib.parse import urlparse

import requests
import tldextract
from bs4 import BeautifulSoup, PageElement, Tag

from backend.utils.trusted_domains import is_trusted_domain

# Essential features for optimized phishing detection
ESSENTIAL_FEATURES = [
    'url_length', 'num_directories', 'query_length', 'num_dots', 'num_hyphens', 
    'num_underscores', 'num_slashes', 'num_parameters', 'has_ip', 'has_suspicious_words'
]


def extract_features(url: str) -> Dict[str, Union[int, float]]:
    """
    Extract features from a URL for phishing detection.
    Returns a dictionary of optimized features for phishing detection.
    Also includes domain trust information.
    """
    features = get_essential_features(url)
    
    # Add domain trust check
    try:
        parsed_url = urlparse(url)
        domain = parsed_url.netloc.lower()
        features['is_trusted_domain'] = is_trusted_domain(domain)
    except Exception:
        features['is_trusted_domain'] = False
    
    return features
def get_website_content(url: str) -> Optional[Dict[str, Any]]:
    """
    Attempt to fetch website content and extract additional features.
    Returns None if the request fails.
    """
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers, timeout=5, verify=True)
        if response.status_code == 200:
            # Get security headers (case-insensitive)
            security_headers = {
                'content-security-policy': response.headers.get('Content-Security-Policy') or 
                                         response.headers.get('content-security-policy'),
                'x-frame-options': response.headers.get('X-Frame-Options') or 
                                 response.headers.get('x-frame-options'),
                'strict-transport-security': response.headers.get('Strict-Transport-Security') or 
                                          response.headers.get('strict-transport-security'),
                'x-content-type-options': response.headers.get('X-Content-Type-Options') or 
                                        response.headers.get('x-content-type-options'),
                'x-xss-protection': response.headers.get('X-XSS-Protection') or 
                                  response.headers.get('x-xss-protection')
            }
            
            return {
                'content': response.text,
                'headers': security_headers,
                'status_code': response.status_code
            }
    except requests.RequestException:
        return None
    return None

def get_essential_features(url: str) -> Dict[str, Union[int, float]]:
    """
    Extract only the essential features that match the trained model.
    This function extracts the exact features that the model was trained on.
    
    Returns a dictionary of features matching the stored model.
    """
    features: Dict[str, Union[int, float]] = {}
    
    # Parse URL with error handling
    try:
        parsed_url = urlparse(url)
        extracted = tldextract.extract(url)
    except Exception:
        # Return safe defaults if URL parsing fails
        return {
            'url_length': len(url) if url else 0,
            'num_directories': 0,
            'query_length': 0,
            'num_dots': 0,
            'num_hyphens': 0,
            'num_underscores': 0,
            'num_slashes': 0,
            'num_parameters': 0,
            'has_ip': 0,
            'has_suspicious_words': 0
        }
    
    # Basic URL features
    features['url_length'] = len(url)
    
    # Path analysis
    path = parsed_url.path or ""
    directories = [d for d in path.split('/') if d]
    features['num_directories'] = len(directories)
    
    # Query parameters
    query = parsed_url.query or ""
    features['query_length'] = len(query)
    features['num_parameters'] = len(query.split('&')) if query else 0
    
    # Character counting
    features['num_dots'] = url.count('.')
    features['num_hyphens'] = url.count('-')
    features['num_underscores'] = url.count('_')
    features['num_slashes'] = url.count('/')
    
    # IP address detection
    ip_pattern = r'(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)'
    features['has_ip'] = 1 if re.search(ip_pattern, url) else 0
    
    # Suspicious words detection
    suspicious_words = [
        'login', 'signin', 'auth', 'bank', 'account', 'payment', 'transfer',
        'credit', 'debit', 'password', 'secure', 'verify', 'confirm', 'update',
        'click', 'download', 'free', 'winner', 'prize', 'urgent', 'expire'
    ]
    
    url_lower = url.lower()
    features['has_suspicious_words'] = 1 if any(word in url_lower for word in suspicious_words) else 0
    
    return features