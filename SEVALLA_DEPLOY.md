# Deploy to Sevalla - Step by Step Guide

This guide walks you through deploying the Country Currency Django app to Sevalla hosting platform with Kinsta MySQL database.

## Prerequisites

- GitHub repository with your code pushed to `main` branch
- Kinsta MySQL database credentials (you already have these)
- Sevalla account (sign up at https://sevalla.com if needed)

## Database Setup

Your Kinsta MySQL database is already configured:
- **Host**: `europe-west4-001.proxy.kinsta.app`
- **Port**: `30156`
- **Database**: `country-currency`
- **User**: `Olaitan34`
- **Password**: `hA4=qI2+vV8=gI4=bT6_`
- **Connection URL**: `mysql://Olaitan34:hA4=qI2+vV8=gI4=bT6_@europe-west4-001.proxy.kinsta.app:30156/country-currency`

✅ No SSL certificate required for this database connection.

## Step 1: Prepare Your Repository

Make sure these files are committed and pushed to GitHub:
- `Dockerfile` - Production container configuration
- `.dockerignore` - Excludes unnecessary files from image
- `start.sh` - Startup script (migrations, static files, gunicorn)
- `requirements.txt` - Python dependencies
- `countries_project/settings.py` - Updated for Kinsta MySQL

### Generate a Strong SECRET_KEY

Run this command locally to generate a secure secret key:

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

Save this key - you'll need it in Step 3.

## Step 2: Push Your Code to GitHub

Commit and push all changes:

```bash
git add .
git commit -m "Configure for Sevalla deployment with Kinsta MySQL"
git push origin main
```

## Step 3: Create App on Sevalla

1. **Log in to Sevalla** and create a new application
2. **Connect GitHub Repository**:
   - Select your GitHub account
   - Choose the `country-currency` repository
   - Select the `main` branch

3. **Configure Build Settings**:
   - **Build Method**: Docker
   - **Dockerfile Path**: `./Dockerfile` (or just `Dockerfile`)
   - **Build Context**: `.` (root of repository)
   - Sevalla will automatically detect and use your Dockerfile

4. **Set Environment Variables** (CRITICAL):
   
   Add these environment variables in Sevalla's dashboard:

   ```
   DATABASE_URL=mysql://Olaitan34:hA4=qI2+vV8=gI4=bT6_@europe-west4-001.proxy.kinsta.app:30156/country-currency
   USE_MYSQL=True
   SECRET_KEY=<paste-your-generated-secret-key-here>
   DEBUG=False
   ALLOWED_HOSTS=<your-sevalla-app-domain>.sevalla.com,localhost
   ```

   **Important Notes**:
   - Replace `<paste-your-generated-secret-key-here>` with the key from Step 1
   - Replace `<your-sevalla-app-domain>` with your actual Sevalla app URL
   - You can add multiple domains to `ALLOWED_HOSTS` separated by commas

## Step 4: Deploy

1. **Trigger Deployment**:
   - Click "Deploy" or "Create Application" in Sevalla
   - Sevalla will build the Docker image and deploy your app

2. **Monitor Build Logs**:
   - Watch the build logs for any errors
   - The build should complete in 3-5 minutes
   - Look for messages like:
     - `Successfully built <image-id>`
     - `Successfully tagged <image-name>`

3. **Check Application Logs**:
   After deployment, monitor logs for startup messages:
   ```
   Starting startup script...
   Using Python: Python 3.12.x
   Running migrations...
   Collecting static files...
   Starting gunicorn on port 8080...
   ✅ Using MySQL database (from DATABASE_URL)
   ```

## Step 5: Verify Deployment

### Test the Status Endpoint

```bash
curl https://<your-sevalla-app-domain>.sevalla.com/status/
```

Expected response:
```json
{
  "status": "ok",
  "database": "connected"
}
```

### Test Country List Endpoint

```bash
curl https://<your-sevalla-app-domain>.sevalla.com/api/countries/
```

### Refresh Countries Data

Populate your database with country data from RestCountries API:

```bash
curl -X POST https://<your-sevalla-app-domain>.sevalla.com/api/countries/refresh/
```

This will fetch all countries and their currency exchange rates.

## Step 6: Run Initial Data Load (Optional)

If you want to pre-populate the database, you can use the Django admin or make a POST request to `/api/countries/refresh/` as shown above.

## Troubleshooting

### Build Fails

**Problem**: Docker build fails or times out

**Solutions**:
- Check build logs for specific error messages
- Verify `requirements.txt` has all dependencies with correct versions
- Ensure `start.sh` has Unix line endings (LF, not CRLF)

### Database Connection Fails

**Problem**: App logs show MySQL connection errors

**Solutions**:
1. Verify `DATABASE_URL` is correctly set in Sevalla environment variables
2. Check that Kinsta MySQL allows connections from Sevalla's IP range
3. Verify credentials are correct (no typos in password)
4. Check Kinsta MySQL dashboard for connection limits or firewall rules

### Migrations Don't Run

**Problem**: Database tables not created

**Solutions**:
- Check application logs for migration errors
- The `start.sh` script runs migrations automatically on startup
- If needed, you can SSH into the container and run `python manage.py migrate` manually

### Static Files Not Loading

**Problem**: CSS/JS/images return 404

**Solutions**:
- Verify `collectstatic` ran successfully in startup logs
- Check that `STATIC_ROOT` is set correctly in `settings.py`
- WhiteNoise is configured to serve static files automatically

### App Crashes on Startup

**Problem**: Container exits immediately after starting

**Solutions**:
1. Check application logs in Sevalla dashboard
2. Verify all required environment variables are set
3. Test locally with Docker:
   ```bash
   docker build -t country-currency .
   docker run -e DATABASE_URL="..." -e SECRET_KEY="..." -p 8080:8080 country-currency
   ```

## Environment Variables Reference

| Variable | Required | Description | Example |
|----------|----------|-------------|---------|
| `DATABASE_URL` | Yes | Full MySQL connection URL | `mysql://user:pass@host:port/db` |
| `USE_MYSQL` | Yes | Enable MySQL (set to True) | `True` |
| `SECRET_KEY` | Yes | Django secret key (50+ chars) | Generate with Django command |
| `DEBUG` | Yes | Debug mode (False in production) | `False` |
| `ALLOWED_HOSTS` | Yes | Comma-separated domain list | `app.sevalla.com,localhost` |
| `PORT` | No | Port to bind (Sevalla sets this) | `8080` |

## Post-Deployment Checklist

- [ ] App is accessible via HTTPS
- [ ] `/status/` endpoint returns 200 OK
- [ ] Database migrations ran successfully
- [ ] Static files are loading correctly
- [ ] Country refresh endpoint works
- [ ] Set up monitoring/uptime checks (optional)
- [ ] Configure custom domain (optional)
- [ ] Enable automatic deployments on push (optional)

## Updating Your App

To deploy updates:

1. Make code changes locally
2. Test locally
3. Commit and push to GitHub:
   ```bash
   git add .
   git commit -m "Your update message"
   git push origin main
   ```
4. Sevalla will automatically rebuild and redeploy (if auto-deploy is enabled)
5. Or manually trigger a redeploy from Sevalla dashboard

## Support

- **Sevalla Documentation**: Check Sevalla's official docs for platform-specific features
- **Django Docs**: https://docs.djangoproject.com/
- **Kinsta MySQL Support**: Contact Kinsta support for database issues

## Security Best Practices

✅ **Implemented**:
- `DEBUG=False` in production
- Strong `SECRET_KEY` generation
- WhiteNoise for static file serving with compression
- CSRF protection enabled
- Database credentials in environment variables (not in code)

🔒 **Recommended Additional Steps**:
- Set up HTTPS (usually automatic with Sevalla)
- Enable HSTS headers (add to `settings.py`)
- Configure database backups via Kinsta
- Set up error monitoring (Sentry, etc.)
- Rotate `SECRET_KEY` periodically
- Use separate staging and production environments

---

**Your deployment is ready!** 🚀

Visit your app at: `https://<your-sevalla-app-domain>.sevalla.com`
