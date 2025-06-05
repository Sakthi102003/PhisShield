"""
Database management utility for PhishShield
"""
import os
import sys
from datetime import datetime

# Add the parent directory to sys.path
sys.path.append(os.path.abspath(os.path.dirname(os.path.dirname(__file__))))

from flask import Flask

from backend.models import URLCheck, User, db

app = Flask(__name__)

# Ensure instance directory exists
instance_path = os.path.join(os.path.dirname(__file__), 'instance')
if not os.path.exists(instance_path):
    os.makedirs(instance_path)

# Configure database path
db_path = os.path.join(instance_path, 'phishshield.db')
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize database
db.init_app(app)
with app.app_context():
    db.create_all()  # Create tables if they don't exist

def list_users():
    """List all users in the database"""
    with app.app_context():
        users = User.query.all()
        print("\nRegistered Users:")
        print("-" * 80)
        print(f"{'ID':<5} {'Username':<20} {'Email':<30} {'Created At':<25}")
        print("-" * 80)
        for user in users:
            print(f"{user.id:<5} {user.username:<20} {user.email:<30} {user.created_at}")
        print("-" * 80)

def list_url_checks(username=None):
    """List URL checks, optionally filtered by username"""
    with app.app_context():
        query = URLCheck.query
        if username:
            query = query.join(User).filter(User.username == username)
        
        checks = query.order_by(URLCheck.checked_at.desc()).all()
        
        print("\nURL Checks:")
        print("-" * 100)
        print(f"{'ID':<5} {'User':<15} {'URL':<40} {'Result':<10} {'Confidence':<10} {'Checked At'}")
        print("-" * 100)
        for check in checks:
            result = "Phishing" if check.is_phishing else "Safe"
            confidence = f"{check.confidence*100:.1f}%"
            print(f"{check.id:<5} {check.user.username:<15} {check.url[:37]+'...':<40} {result:<10} {confidence:<10} {check.checked_at}")
        print("-" * 100)

def delete_user(username):
    """Delete a user and their URL checks"""
    with app.app_context():
        user = User.query.filter_by(username=username).first()
        if user:
            # Delete associated URL checks first
            URLCheck.query.filter_by(user_id=user.id).delete()
            db.session.delete(user)
            db.session.commit()
            print(f"\nUser '{username}' and their URL checks have been deleted.")
        else:
            print(f"\nUser '{username}' not found.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("\nUsage:")
        print("  python manage_db.py users              - List all users")
        print("  python manage_db.py checks             - List all URL checks")
        print("  python manage_db.py checks username    - List URL checks for specific user")
        print("  python manage_db.py delete username    - Delete user and their URL checks")
        sys.exit(1)

    command = sys.argv[1]
    if command == "users":
        list_users()
    elif command == "checks":
        username = sys.argv[2] if len(sys.argv) > 2 else None
        list_url_checks(username)
    elif command == "delete" and len(sys.argv) > 2:
        delete_user(sys.argv[2])
    else:
        print("\nInvalid command. Use python manage_db.py for usage instructions.")
