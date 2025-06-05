#!/usr/bin/env python3
"""
Debug script to check model compatibility issues
"""

import os

import joblib
import numpy as np
from utils.url_features import ESSENTIAL_FEATURES, get_essential_features


def debug_model_compatibility():
    """Debug model compatibility with current feature extraction"""
    
    print("🔍 DEBUGGING MODEL COMPATIBILITY")
    print("=" * 50)
    
    # Get model paths
    current_dir = os.path.dirname(os.path.abspath(__file__))
    model_dir = os.path.join(current_dir, 'model')
    
    model_path = os.path.join(model_dir, 'phishing_model.pkl')
    scaler_path = os.path.join(model_dir, 'scaler.pkl')
    feature_names_path = os.path.join(model_dir, 'feature_names.pkl')
    
    # Check if model files exist
    print("📁 Checking model files:")
    print(f"  Model exists: {os.path.exists(model_path)}")
    print(f"  Scaler exists: {os.path.exists(scaler_path)}")
    print(f"  Feature names exists: {os.path.exists(feature_names_path)}")
    
    if not all([os.path.exists(model_path), os.path.exists(scaler_path), os.path.exists(feature_names_path)]):
        print("❌ Some model files are missing!")
        print("🔧 Solution: Run 'python model/train_model.py' to retrain the model")
        return False
    
    # Load model files
    try:
        model = joblib.load(model_path)
        scaler = joblib.load(scaler_path)
        stored_feature_names = joblib.load(feature_names_path)
        print("✅ Model files loaded successfully")
    except Exception as e:
        print(f"❌ Error loading model files: {e}")
        return False
    
    # Check current features vs stored features
    print(f"\n📊 Feature comparison:")
    print(f"  Current essential features: {len(ESSENTIAL_FEATURES)}")
    print(f"  Stored feature names: {len(stored_feature_names)}")
    print(f"  Current features: {ESSENTIAL_FEATURES}")
    print(f"  Stored features: {stored_feature_names}")
    
    # Check for differences
    current_set = set(ESSENTIAL_FEATURES)
    stored_set = set(stored_feature_names)
    
    missing_in_current = stored_set - current_set
    missing_in_stored = current_set - stored_set
    
    if missing_in_current:
        print(f"⚠️  Features in model but not in current extraction: {missing_in_current}")
    if missing_in_stored:
        print(f"⚠️  Features in current extraction but not in model: {missing_in_stored}")
    
    if missing_in_current or missing_in_stored:
        print("❌ Feature mismatch detected!")
        print("🔧 Solution: Retrain the model with current features")
        return False
    
    # Test feature extraction
    print(f"\n🧪 Testing feature extraction:")
    test_url = "https://google.com"
    
    try:
        features = get_essential_features(test_url)
        print(f"  ✅ Feature extraction successful")
        print(f"  Features extracted: {len(features)}")
        print(f"  Feature keys: {list(features.keys())}")
        
        # Create feature vector in the same order as stored features
        feature_vector = [features[feature] for feature in stored_feature_names]
        print(f"  ✅ Feature vector created: length={len(feature_vector)}")
        print(f"  Feature vector: {feature_vector}")
        
        # Test array conversion
        feature_array = np.array(feature_vector).reshape(1, -1)
        print(f"  ✅ Array conversion successful: shape={feature_array.shape}")
        
        # Test scaling
        scaled_features = scaler.transform(feature_array)
        print(f"  ✅ Feature scaling successful: shape={scaled_features.shape}")
        
        # Test prediction
        prediction = model.predict(scaled_features)[0]
        probability = model.predict_proba(scaled_features)[0]
        print(f"  ✅ Prediction successful: prediction={prediction}, probability={probability}")
        
        return True
        
    except Exception as e:
        print(f"  ❌ Error in feature processing: {e}")
        import traceback
        traceback.print_exc()
        return False

def suggested_fixes():
    """Print suggested fixes for common issues"""
    print(f"\n🔧 SUGGESTED FIXES:")
    print("-" * 20)
    print("1. If model files are missing:")
    print("   - Run: python model/train_model.py")
    print("\n2. If feature mismatch:")
    print("   - Update ESSENTIAL_FEATURES to match stored features")
    print("   - OR retrain model with current features")
    print("\n3. If scaling errors:")
    print("   - Check for NaN or infinite values in features")
    print("   - Ensure feature types are numeric")
    print("\n4. If prediction errors:")
    print("   - Check model compatibility with scikit-learn version")
    print("   - Retrain model if necessary")

if __name__ == "__main__":
    success = debug_model_compatibility()
    suggested_fixes()
    
    if success:
        print("\n🎉 All checks passed! The model should work correctly.")
    else:
        print("\n❌ Issues detected. Follow the suggested fixes above.")
