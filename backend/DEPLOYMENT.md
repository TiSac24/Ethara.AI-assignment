# Deployment Guide - HRMS Lite Backend

This guide covers deploying the FastAPI backend to **Render** and **Vercel**.

---

## 🚀 Deployment Options

### Option 1: Render (Recommended for Python Backends)

Render is ideal for Python/FastAPI applications as it supports long-running processes and databases.

#### Prerequisites
- A Render account (free tier available)
- A PostgreSQL database (Render provides free PostgreSQL)

#### Steps

1. **Create a PostgreSQL Database on Render**
   - Go to [Render Dashboard](https://dashboard.render.com)
   - Click "New +" → "PostgreSQL"
   - Choose a name and region
   - Copy the **Internal Database URL** (for use in your service)
   - Copy the **External Database URL** (for local development)

2. **Deploy the Web Service**
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Configure the service:
     - **Name**: `hrms-lite-api` (or your preferred name)
     - **Environment**: `Python 3`
     - **Build Command**: `pip install -r backend/requirements.txt`
     - **Start Command**: `cd backend && uvicorn main:app --host 0.0.0.0 --port $PORT`
     - **Plan**: Free (or paid for better performance)

3. **Set Environment Variables**
   - Go to your service → Environment
   - Add the following:
     ```
     DATABASE_URL=postgresql://user:password@host:port/dbname
     ALLOWED_ORIGINS=https://your-frontend.vercel.app,https://your-frontend.netlify.app
     ```
   - **Note**: Use the Internal Database URL from step 1

4. **Deploy**
   - Render will automatically deploy on every push to your main branch
   - Or click "Manual Deploy" → "Deploy latest commit"

5. **Access Your API**
   - Your API will be available at: `https://your-service-name.onrender.com`
   - API Docs: `https://your-service-name.onrender.com/docs`

#### Using render.yaml (Alternative)

If you prefer configuration as code:

1. The `render.yaml` file is already created in the root
2. In Render Dashboard, go to "New +" → "Blueprint"
3. Connect your repository
4. Render will automatically detect and use `render.yaml`

---

### Option 2: Vercel (Serverless Functions)

Vercel supports Python but works best with serverless functions. Note: SQLite won't work on Vercel (use PostgreSQL).

#### Prerequisites
- A Vercel account
- A PostgreSQL database (Vercel Postgres, Supabase, or any PostgreSQL provider)

#### Steps

1. **Install Vercel CLI** (optional, you can also use the web interface)
   ```bash
   npm i -g vercel
   ```

2. **Deploy from Root Directory**
   ```bash
   # From project root
   vercel
   ```
   - Follow the prompts
   - Or use the Vercel web interface and connect your GitHub repo

3. **Configure Environment Variables**
   - Go to your project on Vercel Dashboard
   - Settings → Environment Variables
   - Add:
     ```
     DATABASE_URL=postgresql://user:password@host:port/dbname
     ALLOWED_ORIGINS=https://your-frontend.vercel.app
     ```

4. **Important Notes for Vercel**
   - The `vercel.json` configuration is already set up
   - Vercel uses serverless functions, so cold starts may occur
   - Database connections should use connection pooling
   - SQLite files are read-only on Vercel - **must use PostgreSQL**

5. **Access Your API**
   - Your API will be available at: `https://your-project.vercel.app`
   - API Docs: `https://your-project.vercel.app/docs`

---

## 🗄️ Database Setup

### PostgreSQL on Render (Recommended)

1. Create a PostgreSQL database in Render Dashboard
2. Use the **Internal Database URL** for your web service
3. The database will be automatically available to your service

### Other PostgreSQL Options

- **Supabase**: Free PostgreSQL with great features
- **Neon**: Serverless PostgreSQL
- **Railway**: PostgreSQL hosting
- **AWS RDS**: For production workloads

### Database Migration

The tables are created automatically when the app starts. For manual migration:

```bash
# Connect to your database and run the SQL from:
supabase/migrations/20260208071112_create_hrms_tables.sql
```

Or use the Python script:
```bash
cd backend
python init_db.py
```

---

## 🔧 Environment Variables

### Required Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `DATABASE_URL` | PostgreSQL connection string | `postgresql://user:pass@host:5432/dbname` |
| `ALLOWED_ORIGINS` | Comma-separated list of allowed CORS origins | `https://app.vercel.app,https://app.netlify.app` |

### Optional Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `PYTHON_VERSION` | Python version (Vercel) | `3.11` |

### Setting Environment Variables

**Render:**
- Dashboard → Your Service → Environment → Add Environment Variable

**Vercel:**
- Dashboard → Your Project → Settings → Environment Variables

---

## 🌐 CORS Configuration

Update `ALLOWED_ORIGINS` to include your frontend domains:

```
ALLOWED_ORIGINS=https://your-frontend.vercel.app,https://your-frontend.netlify.app,http://localhost:5173
```

The backend automatically reads this and configures CORS.

---

## 📝 Deployment Checklist

### Before Deploying

- [ ] Database is set up (PostgreSQL)
- [ ] Environment variables are configured
- [ ] CORS origins are set correctly
- [ ] `requirements.txt` is up to date
- [ ] Database tables will be created (or migration script is ready)

### After Deploying

- [ ] API is accessible at the deployment URL
- [ ] `/health` endpoint returns `{"status": "healthy"}`
- [ ] `/docs` shows the API documentation
- [ ] Test creating an employee
- [ ] Test marking attendance
- [ ] Frontend can connect to the API

---

## 🐛 Troubleshooting

### Common Issues

#### 1. Database Connection Error
```
Error: could not connect to server
```
**Solution**: 
- Verify `DATABASE_URL` is correct
- Check if database allows connections from your deployment IP
- For Render: Use Internal Database URL
- For Vercel: Ensure database allows external connections

#### 2. CORS Errors
```
Access to fetch at '...' from origin '...' has been blocked by CORS policy
```
**Solution**:
- Add your frontend URL to `ALLOWED_ORIGINS`
- Ensure no trailing slashes in URLs
- Restart the service after updating environment variables

#### 3. Module Not Found
```
ModuleNotFoundError: No module named '...'
```
**Solution**:
- Verify `requirements.txt` includes all dependencies
- Check build logs for installation errors
- Ensure Python version is compatible

#### 4. Port Issues (Render)
```
Error: Port already in use
```
**Solution**:
- Use `$PORT` environment variable (already configured)
- Render automatically sets this

#### 5. Cold Starts (Vercel)
- First request may be slow (10-30 seconds)
- Subsequent requests are fast
- Consider upgrading to Pro plan for better performance

---

## 🔄 Continuous Deployment

Both platforms support automatic deployments:

- **Render**: Auto-deploys on push to main branch
- **Vercel**: Auto-deploys on push to main branch (if connected to GitHub)

To disable auto-deploy:
- **Render**: Settings → Auto-Deploy → Disable
- **Vercel**: Settings → Git → Disable automatic deployments

---

## 📊 Monitoring

### Render
- View logs in Dashboard → Logs
- Monitor metrics in Dashboard → Metrics

### Vercel
- View logs in Dashboard → Deployments → Click deployment → View Function Logs
- Monitor in Dashboard → Analytics

---

## 🔐 Security Best Practices

1. **Never commit `.env` files** (already in `.gitignore`)
2. **Use strong database passwords**
3. **Limit CORS origins** to only your frontend domains
4. **Use HTTPS** (automatic on both platforms)
5. **Keep dependencies updated** (`pip list --outdated`)
6. **Use environment variables** for all secrets

---

## 💰 Cost Comparison

### Render Free Tier
- ✅ 750 hours/month (enough for 24/7)
- ✅ 512 MB RAM
- ✅ PostgreSQL database included
- ⚠️ Spins down after 15 minutes of inactivity

### Vercel Free Tier
- ✅ Unlimited serverless function invocations
- ✅ 100 GB bandwidth
- ⚠️ 10-second function execution limit (Hobby plan)
- ⚠️ Cold starts can be slow

**Recommendation**: Use **Render** for Python backends, **Vercel** for frontend.

---

## 🚀 Quick Deploy Commands

### Render
```bash
# Using Render CLI (if installed)
render deploy
```

### Vercel
```bash
# From project root
vercel --prod
```

---

## 📚 Additional Resources

- [Render Python Documentation](https://render.com/docs/deploy-python)
- [Vercel Python Documentation](https://vercel.com/docs/functions/serverless-functions/runtimes/python)
- [FastAPI Deployment](https://fastapi.tiangolo.com/deployment/)
- [SQLAlchemy Connection Pooling](https://docs.sqlalchemy.org/en/14/core/pooling.html)

---

## 🆘 Need Help?

If you encounter issues:
1. Check the deployment logs
2. Verify environment variables
3. Test the API endpoints using `/docs`
4. Check database connectivity
5. Review this troubleshooting section

