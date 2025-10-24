# Google Authentication Setup Guide

## Overview
PhishShield now supports Google authentication using Firebase. Users can sign in or sign up using their Google accounts.

## Environment Variables

The following Firebase environment variables have been configured:

### Frontend (.env and .env.production)
```
VITE_FIREBASE_API_KEY=AIzaSyAnrUWm1EkKkVdSvG46xI60_WsgHtp0tKg
VITE_FIREBASE_AUTH_DOMAIN=phishshield-39b9a.firebaseapp.com
VITE_FIREBASE_PROJECT_ID=phishshield-39b9a
VITE_FIREBASE_STORAGE_BUCKET=phishshield-39b9a.firebasestorage.app
VITE_FIREBASE_MESSAGING_SENDER_ID=225100436909
VITE_FIREBASE_APP_ID=1:225100436909:web:894c384b2adfbdcecd7d24
VITE_FIREBASE_MEASUREMENT_ID=G-Z33H1R5H0C
```

## Files Added/Modified

### New Files
1. **frontend/src/config/firebase.js** - Firebase configuration and initialization
2. **frontend/.env** - Development environment variables (DO NOT COMMIT)

### Modified Files
1. **frontend/src/components/Auth.jsx** - Added Google Sign-In button and logic
2. **backend/app.py** - Added `/api/auth/google` endpoint
3. **frontend/.env.production** - Added Firebase environment variables

## How It Works

### Frontend Flow
1. User clicks "Sign in/up with Google" button
2. Firebase popup opens for Google authentication
3. User selects/authorizes their Google account
4. Frontend receives user data (uid, email, displayName, photoURL)
5. Frontend sends this data to backend `/api/auth/google` endpoint
6. Backend returns JWT token
7. User is logged in

### Backend Flow
1. Receives Google user data from frontend
2. Checks if user exists by email
3. If exists: generates token and logs in
4. If new: creates account with Google info and generates token
5. Returns token and username to frontend

## Security Notes

⚠️ **Important Security Considerations:**

1. **Never commit .env files** - They contain sensitive API keys
2. **Firebase API Key** - While visible in frontend, it's restricted by Firebase security rules
3. **Backend Validation** - Backend validates all Google auth requests
4. **JWT Tokens** - Tokens expire after 24 hours for security

## Firebase Console Setup

To enable Google authentication in Firebase Console:

1. Go to [Firebase Console](https://console.firebase.google.com/)
2. Select project: **phishshield-39b9a**
3. Navigate to **Authentication** → **Sign-in method**
4. Enable **Google** provider
5. Add authorized domains:
   - `localhost` (for development)
   - `phishshield.onrender.com` (for production)
   - Your custom domain (if any)

## Testing

### Development
```bash
cd frontend
npm run dev
```

### Production Build
```bash
cd frontend
npm run build
```

## Troubleshooting

### "Firebase: Error (auth/unauthorized-domain)"
- Add your domain to Firebase authorized domains
- Check Firebase Console → Authentication → Settings → Authorized domains

### "Google authentication failed"
- Check browser console for detailed error
- Verify Firebase configuration in .env files
- Ensure backend `/api/auth/google` endpoint is accessible

### "Popup blocked"
- Some browsers block popups by default
- User needs to allow popups for your domain

## Dependencies

### Frontend
- `firebase` (v10.x+) - Firebase SDK

### Backend
- No additional dependencies needed (uses existing Flask + SQLAlchemy)

## API Endpoint

### POST /api/auth/google
**Request Body:**
```json
{
  "uid": "google-user-id",
  "email": "user@gmail.com",
  "displayName": "John Doe",
  "photoURL": "https://..."
}
```

**Response (Success):**
```json
{
  "token": "jwt-token-here",
  "username": "john.doe"
}
```

**Response (Error):**
```json
{
  "error": "Error message"
}
```

## User Experience

- **New Users**: Automatically creates account with Google email and display name
- **Existing Users**: Logs in if email already exists in database
- **Username Generation**: Uses Google display name, or email prefix if name unavailable
- **Username Conflicts**: Automatically appends numbers to ensure uniqueness

## Future Enhancements

- [ ] Link Google account to existing username/password account
- [ ] Profile picture integration using photoURL
- [ ] Additional OAuth providers (GitHub, Microsoft, etc.)
- [ ] Two-factor authentication
