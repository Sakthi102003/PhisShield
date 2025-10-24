from datetime import datetime
from typing import Dict, Optional, Union

from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    display_name = db.Column(db.String(120), nullable=True)
    photo_url = db.Column(db.String(512), nullable=True)
    auth_provider = db.Column(db.String(20), default='local')  # 'local' or 'google'
    google_uid = db.Column(db.String(128), nullable=True)  # Unique constraint enforced at app level
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    url_checks = db.relationship('URLCheck', backref='user', lazy=True)

    def __init__(self, username: str, email: str, password_hash: str, 
                 display_name: Optional[str] = None, photo_url: Optional[str] = None, 
                 auth_provider: str = 'local', google_uid: Optional[str] = None) -> None:
        self.username = username
        self.email = email
        self.password_hash = password_hash
        self.display_name = display_name
        self.photo_url = photo_url
        self.auth_provider = auth_provider
        self.google_uid = google_uid

class URLCheck(db.Model):
    __tablename__ = 'url_checks'
    
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(2048), nullable=False)
    is_phishing = db.Column(db.Boolean, nullable=False)
    confidence = db.Column(db.Float, nullable=False)
    features = db.Column(db.JSON)
    checked_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    def __init__(self, url: str, is_phishing: bool, confidence: float, 
                 features: Dict[str, Union[int, float]], user_id: int) -> None:
        self.url = url
        self.is_phishing = is_phishing
        self.confidence = confidence
        self.features = features
        self.user_id = user_id
