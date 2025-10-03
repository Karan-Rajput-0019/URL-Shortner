# Render Deployment Guide

## 🚀 Deploy to Render (Free Tier Available)

### Step 1: Prepare Your Repository
1. **Commit all changes to Git:**
   ```bash
   git add .
   git commit -m "Ready for Render deployment"
   git push origin main
   ```

### Step 2: Deploy on Render
1. **Go to [render.com](https://render.com)**
2. **Sign up/Login** (free account)
3. **Click "New +" → "Web Service"**
4. **Connect your GitHub repository**
5. **Select your URL-Shortner repository**

### Step 3: Configure Your Service
**Service Settings:**
- **Name:** `url-shortener` (or any name you prefer)
- **Environment:** `Python 3`
- **Region:** Choose closest to your users
- **Branch:** `main`
- **Root Directory:** Leave empty (uses root)
- **Build Command:** `pip install -r requirements.txt`
- **Start Command:** `gunicorn wsgi:app`

### Step 4: Set Environment Variables
Click "Advanced" and add these environment variables:

```
FLASK_ENV = production
FLASK_SECRET_KEY = your-secure-secret-key-here
SUPABASE_URL = https://tejkxdfmuenlluyeptai.supabase.co
SUPABASE_KEY = eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InRlamt4ZGZtdWVubGx1eWVwdGFpIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTkzNDA0ODksImV4cCI6MjA3NDkxNjQ4OX0.t6lgUUoX2UfsxTXeUZ7YrKsVu3i8-HWfQIo3sSxyVm4
```

### Step 5: Deploy!
1. **Click "Create Web Service"**
2. **Wait for build to complete** (2-3 minutes)
3. **Your app will be live at:** `https://your-app-name.onrender.com`

## ✅ Your app is ready!

**Features included:**
- ✅ Automatic HTTPS
- ✅ Custom domain support
- ✅ Auto-deploy on Git push
- ✅ Free tier: 750 hours/month
- ✅ Sleeps after 15 minutes of inactivity (free tier)

## 🔧 Troubleshooting
- If build fails, check the logs in Render dashboard
- Make sure all environment variables are set correctly
- Ensure your Supabase database is accessible

**Ready to deploy? Let's go! 🚀**
