#!/usr/bin/env python3

from utils.url_features import get_essential_features


def test_features():
    test_url = 'https://google.com'
    try:
        features = get_essential_features(test_url)
        print('Features extracted successfully:')
        for key, value in features.items():
            print(f'  {key}: {value}')
        print(f'Total features: {len(features)}')
        return features
    except Exception as e:
        print(f'Error: {e}')
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    test_features()
