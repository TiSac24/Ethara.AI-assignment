# Quick Deployment Guide

## 🚀 Deploy to Render (Recommended)

### Step 1: Create Database
1. Go to [Render Dashboard](https://dashboard.render.com)
2. Click "New +" → "PostgreSQL"
3. Name it (e.g., `hrms-db`)
4. Copy the **Internal Database URL**

### Step 2: Deploy Backend
1. Click "New +" → "Web Service"
2. Connect your GitHub repository
3. Configure:
   - **Name**: `hrms-lite-api`
   - **Build Command**: `pip install -r backend/requirements.txt`
   - **Start Command**: `cd backend && uvicorn main:app --host 0.0.0.0 --port $PORT`
4. Add Environment Variables:
   - `DATABASE_URL` = (Internal Database URL from Step 1)
   - `ALLOWED_ORIGINS` = `https://your-frontend.vercel.app,http://localhost:5173`
5. Click "Create Web Service"

**Your API will be at**: `https://hrms-lite-api.onrender.com`

---

## ⚡ Deploy to Vercel

### Step 1: Install Vercel CLI
```bash
npm i -g vercel
```

### Step 2: Deploy
```bash
# From project root
vercel
```

### Step 3: Set Environment Variables
In Vercel Dashboard → Settings → Environment Variables:
- `DATABASE_URL` = Your PostgreSQL connection string
- `ALLOWED_ORIGINS` = Your frontend URLs

**Note**: Vercel requires PostgreSQL (SQLite won't work)

---

## 🔗 Connect Frontend

Update your frontend to use the deployed API:

```typescript
// In your frontend .env file
VITE_API_URL=https://hrms-lite-api.onrender.com
```

Or update your API client to use the production URL.

---

## ✅ Test Deployment

1. Visit: `https://your-api-url/docs`
2. Test the `/health` endpoint
3. Try creating an employee
4. Test marking attendance

---

## 📚 Full Documentation

See `backend/DEPLOYMENT.md` for detailed instructions and troubleshooting.

