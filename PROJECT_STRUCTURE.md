# PhishShield - Project Structure

## 📂 Directory Organization

```
PhisShield/
│
├── 📁 backend/              # Flask Backend Application
│   ├── app.py              # Main Flask server
│   ├── migrate_db.py       # Database migration script
│   ├── requirements.txt    # Python dependencies
│   │
│   ├── 📁 instance/        # SQLite database files
│   ├── 📁 logs/            # Application logs
│   ├── 📁 models/          # Database models
│   │   └── __init__.py     # User & URLCheck models
│   │
│   └── 📁 utils/           # Utility modules
│       ├── auth.py         # JWT & authentication
│       ├── logger.py       # Logging configuration
│       ├── trusted_domains.py
│       └── url_features.py # ML feature extraction
│
├── 📁 frontend/            # React Frontend Application
│   ├── index.html          # HTML entry point
│   ├── package.json        # Node dependencies
│   ├── vite.config.js      # Vite configuration
│   ├── tailwind.config.js  # Tailwind CSS config
│   ├── .env                # Development environment
│   ├── .env.production     # Production environment
│   │
│   ├── 📁 public/          # Static assets
│   │   ├── _headers        # Render headers config
│   │   └── icons/          # App icons
│   │
│   └── 📁 src/             # Source code
│       ├── main.jsx        # React entry point
│       ├── App.jsx         # Main app component
│       ├── index.css       # Global styles
│       │
│       ├── 📁 components/  # React components
│       │   ├── Auth.jsx    # Login/Register (Google)
│       │   ├── Profile.jsx # User profile page
│       │   ├── Dashboard.jsx
│       │   ├── History.jsx
│       │   ├── BulkScanner.jsx
│       │   ├── ThemeToggle.jsx
│       │   └── ErrorBoundary.jsx
│       │
│       ├── 📁 contexts/    # React contexts
│       │   └── ThemeContext.jsx
│       │
│       ├── 📁 config/      # Configuration
│       │   └── firebase.js # Firebase setup
│       │
│       └── 📁 services/    # API services
│           └── api.js      # Axios configuration
│
├── 📁 model/               # Machine Learning Models
│   ├── phishing_model.pkl  # Trained XGBoost model
│   ├── scaler.pkl          # Feature scaler
│   └── feature_names.pkl   # Feature column names
│
├── 📁 docs/                # 📚 Documentation
│   ├── README.md           # Docs index
│   ├── QUICK_START_GUIDE.md
│   ├── DEPLOYMENT_GUIDE.md
│   ├── GOOGLE_AUTH_SETUP.md
│   ├── PROFILE_FEATURE.md
│   ├── FIREBASE_COOP_FIX.md
│   ├── FALSE_POSITIVE_FIX.md
│   ├── ENHANCEMENTS.md
│   └── TESTING_CHECKLIST.md
│
├── 📁 scripts/             # 🔧 Utility Scripts
│   ├── README.md           # Scripts documentation
│   ├── build.sh            # Build script (Unix)
│   ├── setup_backend.bat   # Backend setup (Windows)
│   ├── run_backend_admin.bat
│   └── run_frontend_admin.bat
│
├── 📁 exports/             # 📊 Generated Exports
│   ├── .gitignore          # Ignore export files
│   └── *.pdf, *.csv        # User-generated exports
│
├── .gitignore              # Git ignore rules
├── LICENSE                 # MIT License
├── README.md               # 📖 Main documentation
├── pyrightconfig.json      # Python type checking
└── render.yaml             # Render deployment config
```

## 🎯 Key Directories

### Backend (`/backend`)
Contains the Flask API server with:
- REST API endpoints
- ML model integration
- Database management
- Authentication & authorization

### Frontend (`/frontend`)
React application with:
- Modern UI components
- Firebase authentication
- Theme management
- API integration

### Model (`/model`)
Pre-trained ML models:
- XGBoost classifier
- Feature scaler
- Feature definitions

### Docs (`/docs`)
Comprehensive documentation:
- Setup guides
- Feature documentation
- Troubleshooting
- Deployment instructions

### Scripts (`/scripts`)
Automation scripts:
- Build scripts
- Setup scripts
- Run scripts

### Exports (`/exports`)
User-generated files:
- PDF reports
- CSV exports
- Scan results

## 📝 Configuration Files

| File | Purpose |
|------|---------|
| `pyrightconfig.json` | Python type checking configuration |
| `render.yaml` | Render.com deployment configuration |
| `.gitignore` | Git ignore patterns |
| `frontend/.env` | Development environment variables |
| `frontend/.env.production` | Production environment variables |
| `frontend/vite.config.js` | Vite build configuration |
| `frontend/tailwind.config.js` | Tailwind CSS configuration |
| `backend/requirements.txt` | Python dependencies |
| `frontend/package.json` | Node.js dependencies |

## 🔄 File Flow

### User Scan Request Flow
```
User Browser
    ↓
frontend/src/App.jsx
    ↓
frontend/src/services/api.js
    ↓
backend/app.py (/api/predict)
    ↓
backend/utils/url_features.py
    ↓
model/phishing_model.pkl
    ↓
backend/models/__init__.py (save to DB)
    ↓
Response → User
```

### Authentication Flow
```
User → Auth.jsx
    ↓
Firebase (Google Auth) OR
    ↓
backend/app.py (/api/auth/*)
    ↓
backend/utils/auth.py (JWT)
    ↓
backend/models/__init__.py (User model)
    ↓
Token → Stored in localStorage
```

## 🎨 Clean Organization Benefits

✅ **Separation of Concerns**: Backend, frontend, docs, and scripts are clearly separated

✅ **Easy Navigation**: Find what you need quickly with logical folder structure

✅ **Better Git Management**: Cleaner commit history and easier to review changes

✅ **Scalability**: Easy to add new features without cluttering root directory

✅ **Professional**: Industry-standard project organization

✅ **Documentation**: All docs in one place, easy to maintain and update

✅ **Scripts**: Utility scripts organized separately for easy access

✅ **Exports**: User-generated files don't clutter the project

## 🚀 Quick Access

| Task | Location |
|------|----------|
| Start backend | `scripts/run_backend_admin.bat` |
| Start frontend | `scripts/run_frontend_admin.bat` |
| Setup guide | `docs/QUICK_START_GUIDE.md` |
| API documentation | `backend/app.py` |
| React components | `frontend/src/components/` |
| ML models | `model/` |
| User exports | `exports/` |
