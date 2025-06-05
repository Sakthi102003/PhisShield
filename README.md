# PhishShield - Advanced Phishing Website Detection Tool

## Overview
PhishShield is a sophisticated web application that uses machine learning to detect potential phishing websites in real-time. It provides instant website analysis, security information, and comprehensive reporting features. The application offers an intuitive interface for both casual users and security professionals.

## 🌟 Key Features
- Real-time website analysis and phishing detection
- Automatic URL validation and formatting
- Instant website information display
- Comprehensive security status indicators
- Detailed PDF report generation
- User authentication and history tracking
- Professional UI with cyberpunk theme
- Mobile-responsive design

## 🛠️ Tech Stack

### Frontend
- React.js
- Tailwind CSS
- ShadCN UI
- Axios for API communication

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

## 🚀 Installation & Setup

### Prerequisites
- Node.js (v16 or higher)
- Python 3.12
- Git

### Backend Setup
1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Start the Flask server:
   ```bash
   python app.py
   ```

### Frontend Setup
1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Start the development server:
   ```bash
   npm run dev
   ```

## 📁 Project Structure
```
phishshield/
├── backend/
│   ├── app.py
│   ├── model/
│   │   └── train_model.py
│   ├── utils/
│   │   └── url_features.py
│   ├── check_features.py
│   ├── test_mismatch.py
│   ├── verify_features.py
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── App.jsx
│   │   ├── index.css
│   │   └── main.jsx
│   ├── tailwind.config.js
│   ├── postcss.config.js
│   ├── index.html
│   ├── package.json
│   └── vite.config.js
├── model/
│   ├── feature_names.pkl
│   ├── phishing_model.pkl
│   └── scaler.pkl
├── run_backend_admin.bat
├── run_frontend_admin.bat
└── README.md
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
- Dark/Light theme toggle
- Mobile app development

## 📝 License
This project is licensed under the MIT License - see the LICENSE file for details.

## 👥 Authors
Sakthimurugan S

## 🤝 Contributing
Contributions, issues, and feature requests are welcome! Feel free to check the issues page. 
