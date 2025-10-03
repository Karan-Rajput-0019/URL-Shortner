# Deployment Guide

## Quick Deploy to Railway (Recommended)

1. **Go to [railway.app](https://railway.app)**
2. **Sign up with GitHub**
3. **Click "New Project" → "Deploy from GitHub repo"**
4. **Select your URL-Shortner repository**
5. **Add Environment Variables:**
   - `FLASK_ENV` = `production`
   - `FLASK_SECRET_KEY` = `your-secure-secret-key`
   - `SUPABASE_URL` = `https://tejkxdfmuenlluyeptai.supabase.co`
   - `SUPABASE_KEY` = `eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InRlamt4ZGZtdWVubGx1eWVwdGFpIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTkzNDA0ODksImV4cCI6MjA3NDkxNjQ4OX0.t6lgUUoX2UfsxTXeUZ7YrKsVu3i8-HWfQIo3sSxyVm4`

6. **Deploy!** Railway will automatically build and deploy your app.

## Alternative: Heroku

1. **Install Heroku CLI**
2. **Login:** `heroku login`
3. **Create app:** `heroku create your-app-name`
4. **Set environment variables:**
   ```bash
   heroku config:set FLASK_ENV=production
   heroku config:set FLASK_SECRET_KEY=your-secret-key
   heroku config:set SUPABASE_URL=https://tejkxdfmuenlluyeptai.supabase.co
   heroku config:set SUPABASE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InRlamt4ZGZtdWVubGx1eWVwdGFpIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTkzNDA0ODksImV4cCI6MjA3NDkxNjQ4OX0.t6lgUUoX2UfsxTXeUZ7YrKsVu3i8-HWfQIo3sSxyVm4
   ```
5. **Deploy:** `git push heroku main`

## Your app is ready for deployment! 🚀
