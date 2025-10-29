# 🚂 Railway Deployment Guide - Country Currency API

## 📋 Prerequisites Checklist

Before deploying, ensure you have:
- ✅ GitHub repository with your code pushed
- ✅ Railway account (sign up at https://railway.app)
- ✅ All configuration files created (see below)

---

## 📦 Configuration Files Created

Your project now has these files for Railway deployment:

1. ✅ **`railway.json`** - Railway configuration
2. ✅ **`Procfile`** - Process commands
3. ✅ **`requirements.txt`** - Updated with production dependencies
4. ✅ **`settings.py`** - Updated with production settings

---

## 🚀 Step-by-Step Deployment

### **Step 1: Push to GitHub**

Make sure all changes are committed and pushed:

```bash
git add .
git commit -m "Configure for Railway deployment"
git push origin main
```

---

### **Step 2: Sign Up / Login to Railway**

1. Go to https://railway.app
2. Click **"Start a New Project"**
3. Sign in with GitHub

---

### **Step 3: Create New Project**

1. Click **"New Project"**
2. Select **"Deploy from GitHub repo"**
3. Choose your repository: **`Olaitan34/country-currency`**
4. Railway will auto-detect Django and start deploying

---

### **Step 4: Add MySQL Database**

1. In your Railway project dashboard, click **"+ New"**
2. Select **"Database"**
3. Choose **"Add MySQL"**
4. Railway will provision a MySQL database instantly
5. MySQL credentials will be automatically available as environment variables

---

### **Step 5: Configure Environment Variables**

Click on your **Django service** → **Variables** tab, and add these:

#### **Required Variables:**

```env
DEBUG=False
SECRET_KEY=your-super-secret-key-here-change-this-in-production
ALLOWED_HOSTS=.railway.app
USE_MYSQL=True
```

#### **Database Variables (Auto-configured by Railway MySQL):**

These are automatically set when you add MySQL database:
- `MYSQL_HOST`
- `MYSQL_PORT`
- `MYSQL_DATABASE`
- `MYSQL_USER`
- `MYSQL_PASSWORD`
- `MYSQL_URL`

#### **Optional: Use DATABASE_URL**

If you want to use the `DATABASE_URL` format, add:

```env
DATABASE_URL=${{MySQL.DATABASE_URL}}
```

This references the MySQL service's DATABASE_URL automatically.

---

### **Step 6: Update Database Configuration (if needed)**

Railway automatically provides `MYSQLHOST`, `MYSQLPORT`, `MYSQLDATABASE`, `MYSQLUSER`, `MYSQLPASSWORD`.

Update your `.env` or Railway variables to use Railway's format:

```env
DB_HOST=${{MySQL.MYSQLHOST}}
DB_PORT=${{MySQL.MYSQLPORT}}
DB_NAME=${{MySQL.MYSQLDATABASE}}
DB_USER=${{MySQL.MYSQLUSER}}
DB_PASSWORD=${{MySQL.MYSQLPASSWORD}}
```

Or simpler, just use:
```env
DATABASE_URL=${{MySQL.DATABASE_URL}}
```

---

### **Step 7: Deploy!**

1. Railway will automatically deploy after you add variables
2. Wait for build to complete (2-5 minutes)
3. Watch the deployment logs in the **"Deployments"** tab

---

### **Step 8: Run Database Migrations**

Railway runs migrations automatically via `Procfile`, but you can also run them manually:

1. Go to your Django service
2. Click on the **"..."** menu → **"Run Command"**
3. Enter: `python manage.py migrate`

---

### **Step 9: Create Superuser (Optional)**

To access Django admin:

1. Click **"..."** menu → **"Run Command"**
2. Enter: `python manage.py createsuperuser`
3. Follow the prompts (note: this is interactive, might be tricky)

Or, use Railway CLI (see below)

---

### **Step 10: Get Your Deployment URL**

1. Go to your Django service **"Settings"** tab
2. Look for **"Domains"** section
3. Copy your Railway domain: `https://your-app-name.railway.app`
4. Test your API!

---

## 🧪 Testing Your Deployed API

Replace `localhost:8000` with your Railway URL:

```bash
# Test refresh endpoint
curl -X POST https://your-app.railway.app/countries/refresh

# Test status
curl https://your-app.railway.app/status

# Test countries list
curl https://your-app.railway.app/countries
```

---

## 🔧 Railway CLI (Advanced)

For better control, install Railway CLI:

### **Install Railway CLI:**

```bash
# Windows (PowerShell)
iwr https://railway.app/install.ps1 | iex

# Mac/Linux
curl -fsSL https://railway.app/install.sh | sh
```

### **Login and Link:**

```bash
railway login
railway link
```

### **Run Commands:**

```bash
# Run migrations
railway run python manage.py migrate

# Create superuser
railway run python manage.py createsuperuser

# Open Django shell
railway run python manage.py shell
```

### **View Logs:**

```bash
railway logs
```

---

## 📊 Environment Variables Summary

Here's the complete list you need in Railway:

```env
# Django Settings
DEBUG=False
SECRET_KEY=generate-a-new-secret-key-here
ALLOWED_HOSTS=.railway.app

# Database
USE_MYSQL=True
DATABASE_URL=${{MySQL.DATABASE_URL}}

# Or use individual credentials
DB_HOST=${{MySQL.MYSQLHOST}}
DB_PORT=${{MySQL.MYSQLPORT}}
DB_NAME=${{MySQL.MYSQLDATABASE}}
DB_USER=${{MySQL.MYSQLUSER}}
DB_PASSWORD=${{MySQL.MYSQLPASSWORD}}
```

---

## 🔒 Generate a New SECRET_KEY

Run this in your local terminal:

```python
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

Copy the output and use it as your `SECRET_KEY` in Railway.

---

## 🐛 Troubleshooting

### **Issue: Build Failed**

**Check:**
- `requirements.txt` has all dependencies
- No syntax errors in code
- Check build logs in Railway

**Fix:**
```bash
# Locally test requirements
pip install -r requirements.txt
```

### **Issue: Database Connection Failed**

**Check:**
- MySQL service is running in Railway
- Environment variables are set correctly
- `USE_MYSQL=True` is set

**Fix:**
- Verify `DATABASE_URL` or individual DB credentials in Variables tab

### **Issue: Static Files Not Loading**

**Check:**
- `whitenoise` is in `requirements.txt`
- `STATIC_ROOT` is set in `settings.py`

**Fix:**
```bash
railway run python manage.py collectstatic --noinput
```

### **Issue: 503 Service Unavailable**

**Check:**
- App is fully deployed (check Deployments tab)
- No errors in logs
- Correct `PORT` binding (Railway provides this automatically)

### **Issue: ALLOWED_HOSTS Error**

**Fix:** Add your Railway domain to `ALLOWED_HOSTS`:
```env
ALLOWED_HOSTS=.railway.app,your-app-name.railway.app
```

---

## 📝 Deployment Checklist

Before submitting:

- [ ] Code pushed to GitHub
- [ ] Railway project created
- [ ] MySQL database added
- [ ] Environment variables configured
- [ ] Deployment successful (no errors)
- [ ] Database migrations run
- [ ] Test POST `/countries/refresh` endpoint
- [ ] Test GET `/countries` endpoint
- [ ] Test all other endpoints
- [ ] API accessible from external network
- [ ] Take note of your deployment URL

---

## 🌐 Your Deployment URLs

Once deployed, your endpoints will be:

```
Base URL: https://your-app.railway.app

POST   https://your-app.railway.app/countries/refresh
GET    https://your-app.railway.app/countries
GET    https://your-app.railway.app/countries?region=Africa
GET    https://your-app.railway.app/countries/Nigeria
DELETE https://your-app.railway.app/countries/Nigeria
GET    https://your-app.railway.app/status
GET    https://your-app.railway.app/countries/image
```

---

## 💰 Railway Pricing

**Free Tier:**
- $5 monthly credit (enough for this project)
- No credit card required initially
- Automatic sleeping after inactivity

**Usage Tips:**
- Monitor usage in Railway dashboard
- App sleeps after 5 minutes of inactivity (good for free tier)
- First request after sleep takes ~10 seconds (cold start)

---

## 📤 Submission Checklist

Before submitting to `/stage-two-backend`:

1. ✅ API deployed and accessible
2. ✅ Test all endpoints with Postman
3. ✅ GitHub repo is public and up-to-date
4. ✅ README.md has setup instructions
5. ✅ `.env.example` included (not `.env`)
6. ✅ Test from multiple networks (not just localhost)

---

## 🆘 Need Help?

**Railway Documentation:** https://docs.railway.app  
**Railway Discord:** https://discord.gg/railway  
**Django on Railway:** https://docs.railway.app/guides/django

---

## 🎉 Next Steps

1. **Deploy to Railway** (follow steps above)
2. **Test your deployed API**
3. **Update your Postman collection** with Railway URL
4. **Create/Update README.md** with deployment instructions
5. **Submit to `/stage-two-backend` command** in Slack

---

**Good luck with your deployment! 🚀**

Your Railway URL: `https://________.railway.app`  
Your GitHub Repo: `https://github.com/Olaitan34/country-currency`
