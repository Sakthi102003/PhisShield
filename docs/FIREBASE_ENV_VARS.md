# Firebase Environment Variables - Quick Reference

## 📋 For Render Deployment

Add these environment variables in **Render Dashboard** → **Frontend Service** → **Environment Tab**:

### Required Variables

```bash
# API URL (Update with your actual backend URL)
VITE_API_URL=https://phishshield-backend.onrender.com/

# Firebase Configuration
VITE_FIREBASE_API_KEY=AIzaSyAnrUWm1EkKkVdSvG46xI60_WsgHtp0tKg
VITE_FIREBASE_AUTH_DOMAIN=phishshield-39b9a.firebaseapp.com
VITE_FIREBASE_PROJECT_ID=phishshield-39b9a
VITE_FIREBASE_STORAGE_BUCKET=phishshield-39b9a.firebasestorage.app
VITE_FIREBASE_MESSAGING_SENDER_ID=225100436909
VITE_FIREBASE_APP_ID=1:225100436909:web:894c384b2adfbdcecd7d24
VITE_FIREBASE_MEASUREMENT_ID=G-Z33H1R5H0C

# Node Version
NODE_VERSION=20.11.1
```

## ⚠️ Important Steps

### 1. Add to Render
Copy each variable above and add it in Render Dashboard:
- Navigate to your frontend service
- Click "Environment" tab
- Click "Add Environment Variable"
- Paste key and value
- Save changes

### 2. Trigger Rebuild
After adding environment variables:
- Go to "Manual Deploy"
- Click "Deploy latest commit"
- Wait for build to complete

### 3. Configure Firebase
In Firebase Console:
- Go to Authentication → Settings → Authorized Domains
- Add: `your-app.onrender.com`
- Add: `your-custom-domain.com` (if applicable)

## 🔍 Where Are These Used?

| Variable | Used For |
|----------|----------|
| `VITE_API_URL` | Backend API endpoint |
| `VITE_FIREBASE_API_KEY` | Firebase initialization |
| `VITE_FIREBASE_AUTH_DOMAIN` | Authentication domain |
| `VITE_FIREBASE_PROJECT_ID` | Firebase project identifier |
| `VITE_FIREBASE_STORAGE_BUCKET` | Firebase storage (future use) |
| `VITE_FIREBASE_MESSAGING_SENDER_ID` | Firebase messaging |
| `VITE_FIREBASE_APP_ID` | Firebase app identifier |
| `VITE_FIREBASE_MEASUREMENT_ID` | Google Analytics (optional) |

## 🔒 Security Notes

✅ **Safe to Commit to Git**: No (even though Firebase keys are client-safe)
✅ **Safe in Render Dashboard**: Yes
✅ **Safe in Frontend Code**: Yes (used by `vite.config.js`)
✅ **Protected By**: Firebase Security Rules + Authorized Domains

## 🚀 Quick Copy-Paste

For Render Dashboard (format: KEY=VALUE):

```
VITE_API_URL=https://phishshield-backend.onrender.com/
VITE_FIREBASE_API_KEY=AIzaSyAnrUWm1EkKkVdSvG46xI60_WsgHtp0tKg
VITE_FIREBASE_AUTH_DOMAIN=phishshield-39b9a.firebaseapp.com
VITE_FIREBASE_PROJECT_ID=phishshield-39b9a
VITE_FIREBASE_STORAGE_BUCKET=phishshield-39b9a.firebasestorage.app
VITE_FIREBASE_MESSAGING_SENDER_ID=225100436909
VITE_FIREBASE_APP_ID=1:225100436909:web:894c384b2adfbdcecd7d24
VITE_FIREBASE_MEASUREMENT_ID=G-Z33H1R5H0C
NODE_VERSION=20.11.1
```

## 📱 Local Development

For local development, these are in:
- `frontend/.env` (development)
- `frontend/.env.production` (production build)

**Never commit `.env` to Git!** ✋

## ✅ Verification

After deployment, verify:
1. Visit your site
2. Open browser DevTools → Console
3. Should see no Firebase errors
4. Try Google Sign-In
5. Should authenticate successfully

If you see errors:
- Check all variables are set in Render
- Verify Firebase Authorized Domains
- Check browser console for specific error messages
