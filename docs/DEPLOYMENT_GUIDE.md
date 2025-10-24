# PhishShield - Deployment Guide

## 🚀 Quick Start (Development)

### Starting the Application

#### Backend
```bash
cd backend
python app.py
```
Backend will run on `http://localhost:5000`

#### Frontend
```bash
cd frontend
npm run dev
```
Frontend will run on `http://localhost:5173`

### Or use the batch files (Windows):
```bash
# Start backend
run_backend_admin.bat

# Start frontend  
run_frontend_admin.bat
```

---

## 📦 Production Build

### Frontend Build
```bash
cd frontend
npm run build
```
This creates optimized production files in `frontend/dist/`

### Backend Production
For production, use a WSGI server like Gunicorn:
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 backend.app:app
```

---

## 🌐 Environment Variables

### Backend (.env)
```env
SECRET_KEY=your-secret-key-here-change-in-production
FLASK_ENV=production
DATABASE_URL=sqlite:///phishshield.db
ALLOWED_ORIGINS=https://yourdomain.com
```

### Frontend (.env)
```env
VITE_API_URL=https://your-backend-url.com
```

---

## 📋 Pre-Deployment Checklist

### Backend
- [ ] Update `SECRET_KEY` in production
- [ ] Configure CORS with production domain
- [ ] Set up production database
- [ ] Enable rate limiting
- [ ] Configure logging
- [ ] Set up error monitoring
- [ ] Enable HTTPS
- [ ] Configure backup strategy

### Frontend
- [ ] Update API URL in `config.js`
- [ ] Run `npm run build`
- [ ] Test production build locally
- [ ] Verify all assets load
- [ ] Check bundle size
- [ ] Optimize images if any
- [ ] Test on multiple browsers
- [ ] Verify mobile responsiveness

### Security
- [ ] Change default secret keys
- [ ] Enable HTTPS
- [ ] Configure CSP headers
- [ ] Set up rate limiting
- [ ] Enable CORS properly
- [ ] Validate all inputs
- [ ] Sanitize outputs
- [ ] Set secure cookie flags

---

## 🔧 Configuration Updates

### Update Backend CORS (backend/app.py)
```python
CORS(app, 
     origins=['https://your-production-domain.com'],
     supports_credentials=True,
     allow_headers=['Content-Type', 'Authorization'],
     methods=['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'])
```

### Update Frontend API URL (frontend/src/config.js)
Create this file if it doesn't exist:
```javascript
export const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:5000';
```

Update `frontend/src/services/api.js`:
```javascript
import axios from 'axios';
import { API_BASE_URL } from '../config';

const api = axios.create({
  baseURL: API_BASE_URL,
  // ... rest of config
});
```

---

## 🌍 Deployment Options

### Option 1: Render.com (Current)

#### Backend on Render
1. Connect your GitHub repository
2. Create new Web Service
3. Configure:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn backend.app:app`
   - Environment: Python 3.12
4. Add environment variables
5. Deploy

#### Frontend on Render
1. Create new Static Site
2. Configure:
   - Build Command: `cd frontend && npm install && npm run build`
   - Publish Directory: `frontend/dist`
3. Add environment variables
4. Deploy

### Option 2: Vercel (Frontend) + Render (Backend)

#### Backend on Render
Same as above

#### Frontend on Vercel
1. Install Vercel CLI: `npm i -g vercel`
2. Run: `vercel`
3. Follow prompts
4. Set environment variables in Vercel dashboard

### Option 3: AWS (Advanced)

#### Frontend on S3 + CloudFront
1. Build frontend: `npm run build`
2. Upload `dist/` to S3 bucket
3. Configure CloudFront distribution
4. Enable HTTPS with ACM certificate

#### Backend on EC2 or ECS
1. Set up EC2 instance
2. Install dependencies
3. Configure Nginx reverse proxy
4. Set up SSL with Let's Encrypt
5. Deploy application

### Option 4: Docker (Any Platform)

#### Dockerfile (Backend)
```dockerfile
FROM python:3.12-slim
WORKDIR /app
COPY backend/requirements.txt .
RUN pip install -r requirements.txt
COPY backend/ .
EXPOSE 5000
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
```

#### Dockerfile (Frontend)
```dockerfile
FROM node:18-alpine as build
WORKDIR /app
COPY frontend/package*.json .
RUN npm ci
COPY frontend/ .
RUN npm run build

FROM nginx:alpine
COPY --from=build /app/dist /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

#### docker-compose.yml
```yaml
version: '3.8'
services:
  backend:
    build: 
      context: .
      dockerfile: Dockerfile.backend
    ports:
      - "5000:5000"
    environment:
      - SECRET_KEY=${SECRET_KEY}
      - DATABASE_URL=${DATABASE_URL}
    volumes:
      - ./backend/instance:/app/instance
  
  frontend:
    build:
      context: .
      dockerfile: Dockerfile.frontend
    ports:
      - "80:80"
    depends_on:
      - backend
```

---

## 📊 Database Setup

### Development (SQLite)
Already configured in `app.py`

### Production (PostgreSQL)
1. Install psycopg2: `pip install psycopg2-binary`
2. Update `app.py`:
```python
import os
database_url = os.environ.get('DATABASE_URL', 'sqlite:///phishshield.db')
if database_url.startswith("postgres://"):
    database_url = database_url.replace("postgres://", "postgresql://", 1)
app.config['SQLALCHEMY_DATABASE_URI'] = database_url
```
3. Set `DATABASE_URL` environment variable

### Migrations (Optional)
```bash
pip install flask-migrate
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

---

## 🔐 SSL/HTTPS Setup

### Let's Encrypt (Nginx)
```bash
sudo apt-get install certbot python3-certbot-nginx
sudo certbot --nginx -d yourdomain.com
```

### Nginx Configuration
```nginx
server {
    listen 80;
    server_name yourdomain.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name yourdomain.com;
    
    ssl_certificate /etc/letsencrypt/live/yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/yourdomain.com/privkey.pem;
    
    location / {
        root /var/www/phishshield/frontend/dist;
        try_files $uri $uri/ /index.html;
    }
    
    location /api {
        proxy_pass http://localhost:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

---

## 📈 Monitoring & Logging

### Backend Logging
Already configured in `backend/utils/logger.py`
Logs are stored in `backend/logs/`

### Frontend Monitoring
Add error tracking:
```bash
npm install @sentry/react
```

Configure in `main.jsx`:
```javascript
import * as Sentry from "@sentry/react";

Sentry.init({
  dsn: "your-sentry-dsn",
  environment: "production",
});
```

### Application Monitoring
- Set up uptime monitoring (e.g., UptimeRobot)
- Configure log aggregation (e.g., Papertrail)
- Set up alerts for errors

---

## 🔄 CI/CD Pipeline

### GitHub Actions (.github/workflows/deploy.yml)
```yaml
name: Deploy

on:
  push:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Test Backend
        run: |
          cd backend
          pip install -r requirements.txt
          python -m pytest
      
      - name: Test Frontend
        run: |
          cd frontend
          npm ci
          npm run build

  deploy:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - name: Deploy to production
        # Add deployment steps
```

---

## 🧪 Post-Deployment Testing

### Smoke Tests
- [ ] Homepage loads
- [ ] Login works
- [ ] Single URL scan works
- [ ] Bulk scan works
- [ ] History loads
- [ ] Dashboard displays
- [ ] Theme toggle works
- [ ] PDF download works
- [ ] CSV export works

### Performance Tests
- [ ] Page load time < 3s
- [ ] API response time < 1s
- [ ] No console errors
- [ ] No memory leaks

### Security Tests
- [ ] HTTPS enabled
- [ ] Secure headers set
- [ ] CORS configured
- [ ] Authentication works
- [ ] SQL injection prevented
- [ ] XSS prevented

---

## 📞 Support & Maintenance

### Regular Maintenance Tasks
- [ ] Update dependencies monthly
- [ ] Review logs weekly
- [ ] Backup database daily
- [ ] Monitor uptime
- [ ] Check error rates
- [ ] Review security alerts

### Scaling Considerations
- Add load balancer
- Use Redis for session management
- Implement caching
- Use CDN for static assets
- Horizontal scaling with multiple instances

---

## 🆘 Troubleshooting

### Common Issues

#### "CORS Error"
- Check CORS configuration in `app.py`
- Verify frontend URL is in allowed origins

#### "Database locked"
- Switch to PostgreSQL for production
- Check concurrent access

#### "Module not found"
- Verify all dependencies installed
- Check Python/Node versions

#### "Build failed"
- Clear node_modules: `rm -rf node_modules && npm install`
- Clear Python cache: `find . -type d -name __pycache__ -exec rm -r {} +`

---

## 📝 Rollback Plan

If deployment fails:

1. **Immediate Rollback**
   ```bash
   git revert HEAD
   git push
   ```

2. **Database Rollback**
   ```bash
   flask db downgrade
   ```

3. **Restore from Backup**
   - Restore database backup
   - Redeploy previous version

---

## ✅ Deployment Complete

After successful deployment:

1. **Verify all features work**
2. **Monitor for 24 hours**
3. **Update documentation**
4. **Notify users of new features**
5. **Create release notes**

---

## 📚 Additional Resources

- [Flask Deployment](https://flask.palletsprojects.com/en/2.3.x/deploying/)
- [Vite Production Build](https://vitejs.dev/guide/build.html)
- [Render Documentation](https://render.com/docs)
- [Docker Documentation](https://docs.docker.com/)

---

**Questions?** Check ENHANCEMENTS.md or QUICK_START_GUIDE.md
