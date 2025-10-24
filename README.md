# PhishShield - Advanced Phishing Website Detection Tool

## Overview
PhishShield is a sophisticated web application that uses machine learning to detect potential phishing websites in real-time. It provides instant website analysis, security information, and comprehensive reporting features. The application offers an intuitive interface for both casual users and security professionals.

## 🌟 Key Features
- **Real-time Phishing Detection** - Instant website analysis using ML
- **Google Authentication** - Sign in with Google OAuth (Firebase)
- **User Profile** - Personalized profile with Google photo integration
- **Interactive Dashboard** - Visual statistics and analytics with charts
- **Bulk URL Scanning** - Scan multiple URLs at once (CSV/TXT support)
- **Advanced Search & Filters** - Filter history by date, type, and confidence
- **Toast Notifications** - Real-time feedback for all user actions
- **Dark/Light Theme** - Toggle between themes with persistent preferences
- **User Authentication** - Secure login and registration system
- **Scan History Tracking** - Track all your scans with detailed information
- **PDF Report Generation** - Download professional analysis reports
- **CSV Export** - Export scan history and bulk results
- **URL Information Display** - Automatic website metadata retrieval
- **Security Status Indicators** - HTTPS verification and connection status
- **Professional UI** - Modern cyberpunk-inspired design
- **Mobile-Responsive** - Works seamlessly on all devices

## 🛠️ Tech Stack

### Frontend
- React.js with Hooks and Context API
- Firebase Authentication (Google OAuth)
- Tailwind CSS for styling
- ShadCN UI components
- Recharts for data visualization
- React Toastify for notifications
- Axios for API communication
- jsPDF for report generation
- Lucide React for icons

### Backend
- Python 3.12
- Flask
- Scikit-learn
- Pandas & NumPy

## 🎯 Project Need
Phishing attacks continue to be one of the most prevalent cyber threats, with attackers becoming increasingly sophisticated. PhishShield addresses this challenge by:
- Providing automated detection of potential phishing websites
- Analyzing multiple URL and website features
- Offering real-time risk assessment
- Presenting results in an intuitive, user-friendly interface

## ✨ Latest Features

### 🔐 Google Authentication (Firebase)
- Sign in/up with Google account
- Automatic profile population from Google
- Profile photo integration
- Secure OAuth 2.0 authentication
- Fallback to redirect for popup blockers

### 👤 User Profile
- View and edit profile information
- Display name customization
- Google profile photo display
- Account type indicators (Google/Local)
- Total scans statistics
- Member since information

### 📊 Interactive Dashboard
- Visual statistics with real-time data
- Pie chart showing safe vs phishing distribution
- Line chart displaying scan activity over the last 7 days
- Quick access to latest scan results
- Summary cards for key metrics

### 📤 Bulk URL Scanner
- Upload CSV or TXT files with multiple URLs
- Manual paste support for quick batch scanning
- Process up to 100 URLs simultaneously
- Detailed results with export functionality
- Individual error handling per URL

### 🔍 Enhanced History
- Real-time search across all scans
- Filter by result type (safe/phishing/all)
- Date range filtering
- Multiple sort options (date, confidence)
- Export filtered results to CSV

### 🔔 Toast Notifications
- Success, warning, error, and info notifications
- Non-intrusive, auto-dismissible alerts
- Theme-aware styling
- Real-time feedback for all actions

### 🌓 Dark/Light Theme Toggle
- Smooth theme transitions
- Persistent theme preferences
- Fully styled components for both themes
- Professional cyberpunk dark mode
- Clean modern light mode

## 🚀 Installation & Setup

### Prerequisites
- Node.js (v20 or higher)
- Python 3.11+
- Git
- Firebase account (for Google Auth)

### Quick Start

**Windows Users:**
```cmd
# Setup backend
scripts\setup_backend.bat

# Run backend (in one terminal)
scripts\run_backend_admin.bat

# Run frontend (in another terminal)
scripts\run_frontend_admin.bat
```

**Linux/Mac Users:**
```bash
# Setup backend
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Run backend
python app.py

# Run frontend (in new terminal)
cd frontend
npm install
npm run dev
```

### Detailed Setup

For detailed setup instructions including Firebase configuration, see:
- 📖 [Quick Start Guide](docs/QUICK_START_GUIDE.md)
- 🔐 [Google Auth Setup](docs/GOOGLE_AUTH_SETUP.md)
- 🚀 [Deployment Guide](docs/DEPLOYMENT_GUIDE.md)

## 📁 Project Structure
```
PhisShield/
├── backend/
│   ├── app.py                  # Main Flask application
│   ├── migrate_db.py          # Database migration script
│   ├── models/                # Database models
│   ├── utils/                 # Utility functions
│   │   ├── auth.py           # Authentication utilities
│   │   ├── logger.py         # Logging configuration
│   │   ├── trusted_domains.py
│   │   └── url_features.py   # Feature extraction
│   ├── instance/             # Database files
│   └── requirements.txt      # Python dependencies
├── frontend/
│   ├── src/
│   │   ├── components/       # React components
│   │   │   ├── Auth.jsx     # Login/Register with Google
│   │   │   ├── Profile.jsx  # User profile page
│   │   │   ├── Dashboard.jsx
│   │   │   ├── History.jsx
│   │   │   ├── BulkScanner.jsx
│   │   │   ├── ThemeToggle.jsx
│   │   │   └── ErrorBoundary.jsx
│   │   ├── contexts/        # React contexts
│   │   │   └── ThemeContext.jsx
│   │   ├── services/        # API services
│   │   │   └── api.js
│   │   ├── config/          # Configuration
│   │   │   └── firebase.js  # Firebase config
│   │   ├── App.jsx          # Main app component
│   │   ├── index.css        # Global styles
│   │   └── main.jsx         # Entry point
│   ├── public/              # Static assets
│   ├── .env                 # Environment variables (local)
│   ├── .env.production      # Production env vars
│   ├── tailwind.config.js
│   ├── vite.config.js
│   └── package.json
├── model/                   # ML model files
│   ├── phishing_model.pkl
│   ├── scaler.pkl
│   └── feature_names.pkl
├── docs/                    # Documentation
│   ├── README.md
│   ├── QUICK_START_GUIDE.md
│   ├── DEPLOYMENT_GUIDE.md
│   ├── GOOGLE_AUTH_SETUP.md
│   ├── PROFILE_FEATURE.md
│   ├── FIREBASE_COOP_FIX.md
│   └── TESTING_CHECKLIST.md
├── scripts/                 # Utility scripts
│   ├── README.md
│   ├── build.sh
│   ├── run_backend_admin.bat
│   ├── run_frontend_admin.bat
│   └── setup_backend.bat
├── exports/                 # Export files (PDFs, CSVs)
├── .gitignore
├── LICENSE
├── README.md               # This file
├── pyrightconfig.json
└── render.yaml            # Render deployment config
```

## 🔐 Security Features
- SSL/HTTPS verification
- Domain analysis
- URL structure validation
- Website content inspection
- Security status indicators
- Connection security monitoring

## 🔮 Future Improvements
- Browser extension development
- Integration with threat databases
- Enhanced feature extraction
- API rate limiting and caching
- Multi-language support
- Mobile app development
- Real-time collaboration features
- Scheduled automated scans
- Email notifications for threats
- Account linking (add Google to existing account)
- Two-factor authentication
- ~~Dark/Light theme toggle~~ ✅ **Implemented**
- ~~Google Authentication~~ ✅ **Implemented**
- ~~User Profile~~ ✅ **Implemented**

## 📝 License
This project is licensed under the MIT License - see the LICENSE file for details.

## 👥 Authors
Sakthimurugan S

## 🤝 Contributing
Contributions, issues, and feature requests are welcome! Feel free to check the issues page. 
