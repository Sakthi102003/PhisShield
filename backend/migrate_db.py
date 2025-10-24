"""
Database Migration Script
Adds new columns to User table for Google authentication support
"""
import os
import sys

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.models import db
from flask import Flask

def migrate_database():
    """Add new columns to users table"""
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///phishshield.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    db.init_app(app)
    
    with app.app_context():
        # Get database engine
        engine = db.engine
        inspector = db.inspect(engine)
        
        # Check if columns exist
        columns = [col['name'] for col in inspector.get_columns('users')]
        
        print("Current columns:", columns)
        
        # Add new columns if they don't exist
        with engine.connect() as conn:
            if 'display_name' not in columns:
                print("Adding display_name column...")
                conn.execute(db.text('ALTER TABLE users ADD COLUMN display_name VARCHAR(120)'))
                conn.commit()
                print("✓ Added display_name column")
            
            if 'photo_url' not in columns:
                print("Adding photo_url column...")
                conn.execute(db.text('ALTER TABLE users ADD COLUMN photo_url VARCHAR(512)'))
                conn.commit()
                print("✓ Added photo_url column")
            
            if 'auth_provider' not in columns:
                print("Adding auth_provider column...")
                conn.execute(db.text('ALTER TABLE users ADD COLUMN auth_provider VARCHAR(20) DEFAULT "local"'))
                conn.commit()
                print("✓ Added auth_provider column")
            
            if 'google_uid' not in columns:
                print("Adding google_uid column...")
                conn.execute(db.text('ALTER TABLE users ADD COLUMN google_uid VARCHAR(128)'))
                conn.commit()
                print("✓ Added google_uid column")
                print("Note: UNIQUE constraint on google_uid will be enforced at application level")
        
        print("\n✅ Migration completed successfully!")
        print("New columns added: display_name, photo_url, auth_provider, google_uid")

if __name__ == '__main__':
    try:
        migrate_database()
    except Exception as e:
        print(f"\n❌ Migration failed: {e}")
        sys.exit(1)
