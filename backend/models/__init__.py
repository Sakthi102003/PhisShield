from datetime import datetime
from typing import Dict, Union

from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    url_checks = db.relationship('URLCheck', backref='user', lazy=True)

    def __init__(self, username: str, email: str, password_hash: str) -> None:
        self.username = username
        self.email = email
        self.password_hash = password_hash

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
