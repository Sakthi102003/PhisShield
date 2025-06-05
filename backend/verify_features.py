#!/usr/bin/env python3
"""
Quick verification script to test the fixed feature extraction
"""

import os
import sys

# Add the backend directory to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from utils.url_features import ESSENTIAL_FEATURES, get_essential_features


def test_feature_extraction():
    """Test the feature extraction with multiple URLs"""
    test_urls = [
        'https://google.com',
        'https://github.com', 
        'http://phishing-example.com',
        'https://192.168.1.1',
        'https://bit.ly/test'
    ]
    
    print(f"Testing feature extraction with {len(ESSENTIAL_FEATURES)} essential features:")
    print(f"Features: {ESSENTIAL_FEATURES}")
    print("-" * 60)
    
    all_passed = True
    
    for url in test_urls:
        try:
            print(f"\nTesting URL: {url}")
            features = get_essential_features(url)
            
            # Check if all essential features are present
            missing_features = set(ESSENTIAL_FEATURES) - set(features.keys())
            extra_features = set(features.keys()) - set(ESSENTIAL_FEATURES)
            
            if missing_features:
                print(f"  ❌ Missing features: {missing_features}")
                all_passed = False
            elif extra_features:
                print(f"  ⚠️  Extra features: {extra_features}")
            else:
                print(f"  ✅ All {len(features)} features extracted correctly")
            
            print(f"  Features: {list(features.keys())}")
            
        except Exception as e:
            print(f"  ❌ Error: {e}")
            all_passed = False
    
    print("-" * 60)
    if all_passed:
        print("🎉 All tests passed! Feature extraction is working correctly.")
        return True
    else:
        print("❌ Some tests failed. Please check the errors above.")
        return False

if __name__ == "__main__":
    test_feature_extraction()
