# Database Setup Guide

## Overview
Your Django project is now configured to use either MySQL or SQLite as a fallback.

## Prerequisites

### Install Required Packages
```powershell
pip install -r requirements.txt
```

Or install individually:
```powershell
pip install python-dotenv pymysql cryptography
```

## Configuration

### 1. Set Your MySQL Password
Edit the `.env` file and replace `CLICK_TO_REVEAL_PASSWORD` with your actual password:
```
DB_PASSWORD=your_actual_password_here
```

### 2. Choose Your Database

#### Option A: Use MySQL (Default)
Keep `USE_MYSQL=True` in your `.env` file

#### Option B: Use SQLite (Fallback)
Set `USE_MYSQL=False` in your `.env` file

## Testing the Connection

### Test MySQL Connection
```powershell
python manage.py check
```

If MySQL connection fails, it will automatically fall back to SQLite.

### Run Migrations
```powershell
python manage.py makemigrations
python manage.py migrate
```

## How It Works

1. **Settings.py** loads environment variables from `.env`
2. If `USE_MYSQL=True`, it tries to connect to MySQL
3. If MySQL import fails or connection fails, it falls back to SQLite
4. You'll see console messages indicating which database is being used:
   - ✅ "Using MySQL database"
   - 🔄 "Falling back to SQLite"
   - ℹ️ "Using SQLite database"

## MySQL Connection Details

- **Host:** mysql-countries2-contries-currency1.d.aivencloud.com
- **Port:** 18360
- **Database:** defaultdb
- **User:** avnadmin
- **SSL Mode:** REQUIRED

## Troubleshooting

### If you see "pymysql not found":
```powershell
pip install pymysql cryptography
```

### If connection times out:
- Check your firewall settings
- Verify your password in `.env`
- Try setting `USE_MYSQL=False` to use SQLite temporarily

### To force SQLite usage:
Edit `.env` and change:
```
USE_MYSQL=False
```

## Security Notes

⚠️ **IMPORTANT:** Never commit `.env` file to git!

Add to `.gitignore`:
```
.env
db.sqlite3
*.pyc
__pycache__/
```
