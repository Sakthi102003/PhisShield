# Render Deployment with Firebase Guide

## 🚀 Deploying PhishShield to Render with Google Authentication

This guide covers deploying PhishShield to Render.com with Firebase Google Authentication enabled.

## Prerequisites

- Render.com account
- GitHub repository connected to Render
- Firebase project with Google Authentication enabled
- Firebase environment variables (from `.env` file)

## 📋 Step-by-Step Deployment

### 1. Backend Deployment

#### Create Backend Service
1. Go to [Render Dashboard](https://dashboard.render.com/)
2. Click **"New +"** → **"Web Service"**
3. Connect your GitHub repository
4. Configure:
   - **Name**: `phishshield-backend`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r backend/requirements.txt`
   - **Start Command**: `cd backend && gunicorn app:app`
   - **Plan**: Free

#### Set Backend Environment Variables
In the Render dashboard for backend service:
- `PYTHON_VERSION` = `3.11.0`
- `FLASK_ENV` = `production`
- `SECRET_KEY` = `your-secure-random-key-here` (generate a secure key)

### 2. Frontend Deployment

#### Create Frontend Static Site
1. Click **"New +"** → **"Static Site"**
2. Connect same GitHub repository
3. Configure:
   - **Name**: `phishshield-frontend`
   - **Build Command**: `cd frontend && npm install && npm run build`
   - **Publish Directory**: `frontend/dist`
   - **Plan**: Free

#### Set Frontend Environment Variables ⚠️ IMPORTANT
In the Render dashboard for frontend service, add these environment variables:

**Required for Build:**
```
NODE_VERSION = 20.11.1
```

**Firebase Configuration (from your .env file):**
```
VITE_API_URL = https://phishshield-backend.onrender.com/

VITE_FIREBASE_API_KEY = AIzaSyAnrUWm1EkKkVdSvG46xI60_WsgHtp0tKg
VITE_FIREBASE_AUTH_DOMAIN = phishshield-39b9a.firebaseapp.com
VITE_FIREBASE_PROJECT_ID = phishshield-39b9a
VITE_FIREBASE_STORAGE_BUCKET = phishshield-39b9a.firebasestorage.app
VITE_FIREBASE_MESSAGING_SENDER_ID = 225100436909
VITE_FIREBASE_APP_ID = 1:225100436909:web:894c384b2adfbdcecd7d24
VITE_FIREBASE_MEASUREMENT_ID = G-Z33H1R5H0C
```

**How to Add Environment Variables in Render:**
1. Go to your frontend service dashboard
2. Click **"Environment"** tab
3. Click **"Add Environment Variable"**
4. Add each variable one by one
5. Click **"Save Changes"**

### 3. Configure Custom Headers (Frontend)

Render should automatically pick up headers from `render.yaml`, but verify:

1. Go to frontend service → **"Settings"**
2. Scroll to **"Headers"**
3. Verify these headers exist:
   ```
   Cross-Origin-Opener-Policy: same-origin-allow-popups
   Cross-Origin-Embedder-Policy: unsafe-none
   ```

If not, add them manually:
- Click **"Add Header"**
- Path: `/*`
- Name: `Cross-Origin-Opener-Policy`
- Value: `same-origin-allow-popups`

### 4. Configure CORS (Backend)

The backend `app.py` already has CORS configured. Verify the origins include your Render URLs:

```python
CORS(app, 
     origins=['https://phishshield.onrender.com', 'http://localhost:5173'],
     ...)
```

Update if your Render URL is different.

### 5. Firebase Console Configuration

**Add Render Domains to Firebase:**

1. Go to [Firebase Console](https://console.firebase.google.com/)
2. Select your project: `phishshield-39b9a`
3. Navigate to **Authentication** → **Settings** → **Authorized Domains**
4. Add your Render domains:
   ```
   phishshield-frontend.onrender.com
   phishshield.onrender.com
   your-custom-domain.com (if you have one)
   ```

### 6. Deploy!

1. **Backend**: Should auto-deploy after configuration
2. **Frontend**: Should auto-deploy after environment variables are set

**Monitor Deployment:**
- Check **"Logs"** tab for any errors
- Backend should show: "Model loaded successfully"
- Frontend should build without errors

### 7. Test Deployment

1. Visit your frontend URL: `https://phishshield-frontend.onrender.com`
2. Try Google Sign-In
3. Test URL scanning
4. Check profile page

## 🔧 Troubleshooting

### Google Sign-In Not Working

**Error: "auth/unauthorized-domain"**
- Add your Render domain to Firebase Authorized Domains
- Wait a few minutes for changes to propagate

**Error: "COOP Policy Block"**
- Verify headers are set in Render
- Check browser console for specific errors
- Try redirect authentication (should work as fallback)

### Backend Connection Issues

**Error: "Network Error" or CORS**
- Check backend URL in frontend environment variables
- Verify CORS origins in `backend/app.py`
- Ensure backend is running (check backend logs)

### Environment Variables Not Applied

- Environment variables are only used during build
- After adding/changing env vars, trigger a **manual deploy**
- Go to **"Manual Deploy"** → **"Deploy latest commit"**

### Build Failures

**Frontend Build Error:**
- Check all VITE_ environment variables are set
- Verify Node version is 20.11.1
- Check build logs for specific errors

**Backend Build Error:**
- Check Python version is 3.11.0
- Verify requirements.txt path is correct
- Check build logs for missing dependencies

## 📝 Important Notes

### Firebase API Key Security
- ✅ Firebase API keys are **safe to expose** in frontend
- They're protected by Firebase Security Rules
- They're restricted to authorized domains
- Different from backend API keys (which should be secret)

### Free Tier Limitations
- Render free tier spins down after 15 minutes of inactivity
- First request after spin-down takes ~30-60 seconds
- Consider upgrading for production use

### Database
- SQLite database is ephemeral on Render free tier
- Database resets when service restarts
- For production, upgrade to paid plan with persistent disk
- Or switch to PostgreSQL

## 🔄 Automatic Deployments

Render automatically deploys when you push to GitHub:

1. **Auto-Deploy Enabled** (default)
   - Push to main branch → automatic deployment
   - Check **"Settings"** → **"Auto-Deploy"**

2. **Manual Deploy**
   - Go to service dashboard
   - Click **"Manual Deploy"** → **"Deploy latest commit"**

## 📊 Monitoring

**Check Service Health:**
- Backend: `https://your-backend.onrender.com/api/health`
- Frontend: Visit the URL in browser

**View Logs:**
- Dashboard → Select Service → **"Logs"** tab
- Real-time logs for debugging

## 🎯 Production Checklist

Before going live:
- [ ] All environment variables set correctly
- [ ] Firebase authorized domains configured
- [ ] CORS origins updated with production URLs
- [ ] Custom domain configured (optional)
- [ ] SSL certificate active (automatic on Render)
- [ ] Backend health endpoint responding
- [ ] Google authentication working
- [ ] Database migrations run
- [ ] Error logging configured
- [ ] Backup strategy in place

## 🌐 Custom Domain (Optional)

1. Go to frontend service → **"Settings"**
2. Scroll to **"Custom Domain"**
3. Click **"Add Custom Domain"**
4. Follow instructions to update DNS records
5. Add custom domain to Firebase Authorized Domains

## 💡 Tips

- **Faster Deploys**: Use `npm ci` instead of `npm install` in build command
- **Cache Dependencies**: Render caches node_modules automatically
- **Health Checks**: Backend includes `/api/health` endpoint
- **Logs**: Enable persistent logs for debugging
- **Notifications**: Set up Render notifications for deploy failures

## 📞 Support

If issues persist:
- Check Render [Status Page](https://status.render.com/)
- Review Render [Documentation](https://render.com/docs)
- Check Firebase [Status](https://status.firebase.google.com/)
- Review logs in both Render and Firebase Console

---

**Your PhishShield should now be live with Google Authentication! 🎉**
