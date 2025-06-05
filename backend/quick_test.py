#!/usr/bin/env python3
"""
Simple test to verify the Flask app can start without errors
"""

try:
    # Test imports
    from utils.url_features import ESSENTIAL_FEATURES, get_essential_features
    print("✅ url_features imports successful")
    
    # Test feature extraction
    test_url = "https://google.com"
    features = get_essential_features(test_url)
    print(f"✅ Feature extraction successful: {len(features)} features")
    
    # Test Flask app imports
    from app import app
    print("✅ Flask app imports successful")
    
    print(f"✅ All tests passed! Essential features: {len(ESSENTIAL_FEATURES)}")
    print("The phishing detector is ready to use!")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
