import os

import joblib
from utils.url_features import ESSENTIAL_FEATURES, get_essential_features

# Load stored feature names
try:
    feature_names = joblib.load('model/feature_names.pkl')
    print("Stored features:", feature_names)
    print("Stored count:", len(feature_names))
except Exception as e:
    print("Error loading feature names:", e)

print("Current features:", ESSENTIAL_FEATURES)
print("Current count:", len(ESSENTIAL_FEATURES))

# Test feature extraction
try:
    features = get_essential_features('https://google.com')
    print("Feature extraction test successful")
    print("Extracted features:", list(features.keys()))
    print("Feature values:", features)
except Exception as e:
    print("Feature extraction error:", e)
    import traceback
    traceback.print_exc()
