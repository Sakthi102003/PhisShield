"""
Trusted domains whitelist for PhishShield.
This module contains lists of known legitimate domains to reduce false positives.
"""

# Major tech companies and cloud providers
TRUSTED_DOMAINS = {
    # Google services
    'google.com', 'gmail.com', 'youtube.com', 'google.co.in', 'google.co.uk',
    'googleapis.com', 'googleusercontent.com', 'gstatic.com', 'googlesource.com',
    'google-analytics.com', 'googleadservices.com', 'googlevideo.com',
    'googletagmanager.com', 'googledomains.com', 'blogger.com', 'blogspot.com',
    'aistudio.google.com', 'console.cloud.google.com', 'firebase.google.com',
    
    # Microsoft services
    'microsoft.com', 'office.com', 'outlook.com', 'live.com', 'hotmail.com',
    'azure.com', 'windows.com', 'xbox.com', 'onedrive.com', 'microsoftonline.com',
    'office365.com', 'visualstudio.com', 'github.com', 'linkedin.com',
    
    # Apple
    'apple.com', 'icloud.com', 'itunes.com', 'appstore.com', 'me.com',
    
    # Amazon
    'amazon.com', 'aws.amazon.com', 'amazonaws.com', 'amazon.co.uk', 'amazon.in',
    'amazon.de', 'amazon.fr', 'amazon.ca', 'cloudfront.net',
    
    # Social media
    'facebook.com', 'instagram.com', 'twitter.com', 'x.com', 'tiktok.com',
    'snapchat.com', 'reddit.com', 'pinterest.com', 'whatsapp.com',
    
    # Development platforms
    'stackoverflow.com', 'stackexchange.com', 'npmjs.com', 'pypi.org',
    'gitlab.com', 'bitbucket.org', 'sourceforge.net', 'codepen.io',
    
    # Cloud & hosting
    'cloudflare.com', 'netlify.com', 'vercel.com', 'heroku.com',
    'digitalocean.com', 'linode.com', 'render.com',
    
    # Financial institutions (major ones)
    'paypal.com', 'stripe.com', 'square.com', 'venmo.com',
    
    # Education
    'coursera.org', 'udemy.com', 'edx.org', 'khanacademy.org',
    'mit.edu', 'stanford.edu', 'harvard.edu', 'berkeley.edu',
    
    # E-commerce
    'ebay.com', 'etsy.com', 'shopify.com', 'walmart.com', 'bestbuy.com',
    
    # Media & entertainment
    'netflix.com', 'spotify.com', 'hulu.com', 'disney.com', 'twitch.tv',
    
    # Other popular services
    'dropbox.com', 'zoom.us', 'slack.com', 'discord.com', 'telegram.org',
    'wikipedia.org', 'wikimedia.org', 'mozilla.org', 'w3.org',
}


def is_trusted_domain(domain: str) -> bool:
    """
    Check if a domain is in the trusted domains list.
    Supports subdomain matching (e.g., mail.google.com matches google.com).
    
    Args:
        domain: The domain to check (e.g., 'mail.google.com')
        
    Returns:
        True if the domain is trusted, False otherwise
    """
    if not domain:
        return False
    
    domain = domain.lower().strip()
    
    # Direct match
    if domain in TRUSTED_DOMAINS:
        return True
    
    # Check if it's a subdomain of any trusted domain
    # e.g., mail.google.com should match google.com
    parts = domain.split('.')
    for i in range(len(parts)):
        potential_root = '.'.join(parts[i:])
        if potential_root in TRUSTED_DOMAINS:
            return True
    
    return False


def get_domain_trust_score(domain: str) -> float:
    """
    Get a trust score for a domain (0.0 to 1.0).
    1.0 means fully trusted, 0.0 means unknown/untrusted.
    
    Args:
        domain: The domain to score
        
    Returns:
        A trust score between 0.0 and 1.0
    """
    if is_trusted_domain(domain):
        return 1.0
    
    # Could be extended with additional scoring logic
    # (e.g., checking domain age, SSL certificate, etc.)
    return 0.0
