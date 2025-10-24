"""
Test script to verify that trusted domains are correctly identified
and bypass the ML model prediction.
"""
import sys
from urllib.parse import urlparse

sys.path.append('.')

from utils.trusted_domains import is_trusted_domain

# Test URLs - mix of trusted and untrusted
test_cases = [
    # Google services
    ("https://aistudio.google.com/app/api-keys", True, "Google AI Studio"),
    ("https://console.cloud.google.com/", True, "Google Cloud Console"),
    ("https://mail.google.com", True, "Gmail"),
    
    # Microsoft services
    ("https://portal.azure.com", True, "Azure Portal"),
    ("https://github.com/microsoft/vscode", True, "GitHub"),
    
    # Amazon
    ("https://console.aws.amazon.com", True, "AWS Console"),
    
    # Other trusted
    ("https://stackoverflow.com/questions", True, "Stack Overflow"),
    ("https://www.netflix.com", True, "Netflix"),
    
    # Suspicious/Unknown sites
    ("https://secure-login-bank-verify.com", False, "Suspicious phishing-like domain"),
    ("https://free-amazon-gift-cards.xyz", False, "Suspicious domain"),
    ("https://my-random-site.com", False, "Unknown domain"),
]

print("=" * 80)
print("TRUSTED DOMAIN VERIFICATION TEST")
print("=" * 80)
print()

passed = 0
failed = 0

for url, expected_trusted, description in test_cases:
    parsed_url = urlparse(url)
    domain = parsed_url.netloc.lower()
    is_trusted = is_trusted_domain(domain)
    
    status = "✓ PASS" if is_trusted == expected_trusted else "✗ FAIL"
    result = "TRUSTED" if is_trusted else "NOT TRUSTED"
    
    if is_trusted == expected_trusted:
        passed += 1
    else:
        failed += 1
    
    print(f"{status}")
    print(f"  URL: {url}")
    print(f"  Description: {description}")
    print(f"  Domain: {domain}")
    print(f"  Expected: {'TRUSTED' if expected_trusted else 'NOT TRUSTED'}")
    print(f"  Got: {result}")
    print()

print("=" * 80)
print(f"RESULTS: {passed} passed, {failed} failed out of {len(test_cases)} tests")
print("=" * 80)

if failed == 0:
    print("\n✓ All tests passed! Trusted domain checking is working correctly.")
    print("  Google AI Studio and other legitimate domains will no longer be flagged.")
else:
    print(f"\n✗ {failed} test(s) failed. Please review the results above.")
