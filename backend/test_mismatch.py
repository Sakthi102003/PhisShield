#!/usr/bin/env python3
"""
Simple test to check for feature mismatch
"""

import joblib
import numpy as np
from utils.url_features import ESSENTIAL_FEATURES, get_essential_features


def main():
    print("=== FEATURE MISMATCH DIAGNOSTIC ===")
    
    # Load stored feature names
    try:
        stored_features = joblib.load('model/feature_names.pkl')
        print(f"✅ Loaded stored features: {len(stored_features)} features")
        print(f"Stored: {stored_features}")
    except Exception as e:
        print(f"❌ Error loading stored features: {e}")
        return
    
    print(f"Current: {ESSENTIAL_FEATURES}")
    print(f"Current count: {len(ESSENTIAL_FEATURES)}")
    
    # Check for differences
    if set(stored_features) != set(ESSENTIAL_FEATURES):
        print("\n❌ FEATURE MISMATCH DETECTED!")
        missing_in_current = set(stored_features) - set(ESSENTIAL_FEATURES)
        extra_in_current = set(ESSENTIAL_FEATURES) - set(stored_features)
        
        if missing_in_current:
            print(f"Missing in current: {missing_in_current}")
        if extra_in_current:
            print(f"Extra in current: {extra_in_current}")
            
        print("\n🔧 FIXING THE ISSUE...")
        
        # Option 1: Update ESSENTIAL_FEATURES to match stored features
        print("Option 1: Update current features to match model")
        print(f"Update ESSENTIAL_FEATURES to: {stored_features}")
        
        # Let's fix this by updating the current features
        return stored_features
    else:
        print("✅ Features match!")
        
        # Test actual feature extraction
        try:
            features = get_essential_features('https://google.com')
            print(f"✅ Feature extraction works: {len(features)} features")
            
            # Create feature vector
            feature_vector = [features[feature] for feature in stored_features]
            print(f"✅ Feature vector: {feature_vector}")
            
            # Test scaling
            scaler = joblib.load('model/scaler.pkl')
            scaled = scaler.transform(np.array(feature_vector).reshape(1, -1))
            print(f"✅ Scaling works: {scaled.shape}")
            
        except Exception as e:
            print(f"❌ Error in feature processing: {e}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    main()
