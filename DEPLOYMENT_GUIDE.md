# AGRIVERSE Deployment Guide

## Project Structure
- **Frontend**: React + Vite (Vercel)
- **Backend**: Flask + ML Models (Render/Railway/Fly.io)

---

## STEP 1: Frontend Deployment (Vercel)

### Prerequisites
- GitHub account with your code pushed
- Vercel account (free at vercel.com)

### Deploy Frontend

1. **Push your code to GitHub**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git push -u origin main
   ```

2. **Connect to Vercel**
   - Go to [vercel.com](https://vercel.com)
   - Click "New Project"
   - Import your GitHub repository
   - Select `FrontEnd` as the root directory

3. **Build Settings**
   - Framework Preset: Vite
   - Build Command: `npm run build`
   - Output Directory: `dist`
   - Install Command: `npm install`

4. **Environment Variables** (if needed)
   - Add `VITE_API_URL` pointing to your backend

5. **Deploy** - Click "Deploy"

**Result**: Your frontend will be live at `your-project.vercel.app`

---

## STEP 2: Backend Deployment (Render - Recommended)

### Option A: Deploy on Render (Easiest)

1. **Prepare Backend**
   ```bash
   cd Backend
   pip freeze > requirements.txt  # Update requirements
   ```

2. **Modify Flask app to accept environment variables**
   - Update `app_for_crop_recommendation.py`:
   ```python
   PORT = os.getenv('PORT', 5000)
   app.run(host='0.0.0.0', port=PORT, debug=False)
   ```

3. **Push to GitHub** with the Dockerfile included

4. **Deploy on Render**
   - Go to [render.com](https://render.com)
   - Click "New Web Service"
   - Connect your GitHub repo
   - Set name (e.g., `agriverse-backend`)
   - Environment: `Docker`
   - Plan: Free tier available
   - Deploy

**Result**: Backend available at `your-project.onrender.com`

---

## STEP 3: Connect Frontend to Backend

Update your frontend API calls in `FrontEnd/src/services/`:

```javascript
const API_URL = process.env.VITE_API_URL || 'http://localhost:5000';

// In your API calls:
axios.post(`${API_URL}/api/crop-recommendation`, data)
```

Add environment variable in Vercel:
- Go to Project Settings → Environment Variables
- Add: `VITE_API_URL=https://your-project.onrender.com`

---

## Alternative Backend Options

### Option B: Railway (railway.app)
- Similar to Render
- Better free tier limits
- Good documentation

### Option C: Fly.io (fly.io)
- Strong Docker support
- Global deployment
- Pay-as-you-go pricing

---

## Important Notes

⚠️ **CORS Configuration**
- Ensure your Flask app has CORS enabled for your Vercel domain
- Update `app_for_crop_recommendation.py`:
```python
from flask_cors import CORS
CORS(app, origins=['https://your-project.vercel.app'])
```

⚠️ **Database & Files**
- Large files (model.pkl, CSV files) should be:
  - Stored in cloud storage (AWS S3, etc.) or
  - Committed to git if < 50MB
  - Loaded on startup

⚠️ **Environment Variables**
- Never commit `.env` files
- Use platform-specific environment variable systems

---

## Quick Deploy Checklist

- [ ] Code pushed to GitHub
- [ ] requirements.txt updated with all dependencies
- [ ] Flask app uses PORT environment variable
- [ ] CORS configured for frontend domain
- [ ] Vercel project created for FrontEnd
- [ ] Backend deployed on Render/Railway
- [ ] Environment variables set in Vercel
- [ ] VITE_API_URL correctly configured
- [ ] Test API calls between frontend and backend

---

## Monitoring & Debugging

**Vercel Logs**: Dashboard → Deployments → Logs  
**Render Logs**: Dashboard → Services → Logs

---

For detailed help:
- Vercel Docs: https://vercel.com/docs
- Render Docs: https://render.com/docs
