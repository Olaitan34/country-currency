# 🌍 Country Currency & Exchange Rate API

A RESTful API that fetches country data from external sources, stores it in a MySQL database, and provides CRUD operations with filtering and sorting capabilities.

## 🚀 Live Demo

**API Base URL:** `https://your-app.railway.app` _(Update after deployment)_

**GitHub Repository:** [https://github.com/Olaitan34/country-currency](https://github.com/Olaitan34/country-currency)

---

## 📋 Features

- ✅ Fetch and cache country data from external APIs
- ✅ Calculate estimated GDP based on population and exchange rates
- ✅ Filter countries by region and currency
- ✅ Sort countries by GDP
- ✅ Generate summary images with top countries
- ✅ Full CRUD operations
- ✅ MySQL database with Railway hosting
- ✅ Proper error handling and validation

---

## 🔗 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/countries/refresh` | Fetch all countries and cache in database |
| `GET` | `/countries` | List all countries (supports filters) |
| `GET` | `/countries/:name` | Get specific country by name |
| `DELETE` | `/countries/:name` | Delete a country record |
| `GET` | `/status` | Get total countries and last refresh time |
| `GET` | `/countries/image` | Get generated summary image |

### Query Parameters

- `?region=Africa` - Filter by region
- `?currency=NGN` - Filter by currency code
- `?sort=gdp_desc` - Sort by GDP descending
- `?sort=gdp_asc` - Sort by GDP ascending

---

## 🛠️ Tech Stack

- **Framework:** Django 5.2.7
- **API:** Django REST Framework
- **Database:** MySQL (Aiven Cloud)
- **Hosting:** Railway
- **Image Processing:** Pillow
- **Server:** Gunicorn
- **Static Files:** WhiteNoise

---

## 📦 Installation & Local Setup

### Prerequisites

- Python 3.12+
- MySQL (local or Aiven cloud)
- Git

### 1. Clone Repository

```bash
git clone https://github.com/Olaitan34/country-currency.git
cd country-currency
```

### 2. Create Virtual Environment

```bash
# Windows
python -m venv env
env\Scripts\activate

# Mac/Linux
python3 -m venv env
source env/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the root directory:

```env
# Database Configuration
USE_MYSQL=True

# Option 1: Use DATABASE_URL
DATABASE_URL=mysql://user:password@host:port/database

# Option 2: Use individual credentials
DB_NAME=defaultdb
DB_USER=avnadmin
DB_PASSWORD=your_password
DB_HOST=your-mysql-host.aivencloud.com
DB_PORT=18360

# Django Settings
DEBUG=True
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=localhost,127.0.0.1
```

### 5. Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Create Superuser (Optional)

```bash
python manage.py createsuperuser
```

### 7. Run Development Server

```bash
python manage.py runserver
```

Server will start at `http://127.0.0.1:8000`

---

## 🧪 Testing the API

### Using Postman

1. Import the included `Country_Currency_API.postman_collection.json`
2. Set base URL to `http://localhost:8000` for local testing
3. Run the requests in order (start with refresh)

### Using cURL

```bash
# Refresh countries data
curl -X POST http://localhost:8000/countries/refresh

# Get all countries
curl http://localhost:8000/countries

# Filter by region
curl "http://localhost:8000/countries?region=Africa"

# Get single country
curl http://localhost:8000/countries/Nigeria

# Get status
curl http://localhost:8000/status
```

See `POSTMAN_TESTING_GUIDE.md` for detailed testing instructions.

---

## 🚂 Deployment to Railway

### Quick Deployment Steps

1. **Push to GitHub**
   ```bash
   git add .
   git commit -m "Ready for deployment"
   git push origin main
   ```

2. **Create Railway Project**
   - Go to [railway.app](https://railway.app)
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose your repository

3. **Add MySQL Database**
   - Click "+ New" → "Database" → "Add MySQL"

4. **Set Environment Variables**
   ```env
   DEBUG=False
   SECRET_KEY=your-production-secret-key
   ALLOWED_HOSTS=.railway.app
   USE_MYSQL=True
   DATABASE_URL=${{MySQL.DATABASE_URL}}
   ```

5. **Deploy!**
   - Railway auto-deploys on push
   - Check deployment logs
   - Test your API

See `RAILWAY_DEPLOYMENT_GUIDE.md` for complete deployment instructions.

---

## 📁 Project Structure

```
country-currency/
├── countries/                  # Main app
│   ├── models.py              # Country & RefreshStatus models
│   ├── views.py               # API views
│   ├── serializers.py         # DRF serializers
│   ├── utils.py               # Image generation utilities
│   └── migrations/            # Database migrations
├── countries_project/         # Project settings
│   ├── settings.py            # Django configuration
│   ├── urls.py                # URL routing
│   └── wsgi.py                # WSGI configuration
├── cache/                     # Generated images
├── requirements.txt           # Python dependencies
├── Procfile                   # Railway/Heroku process file
├── railway.json               # Railway configuration
├── runtime.txt                # Python version
├── manage.py                  # Django management
└── README.md                  # This file
```

---

## 🔒 Environment Variables

### Required for Production

| Variable | Description | Example |
|----------|-------------|---------|
| `DEBUG` | Debug mode | `False` |
| `SECRET_KEY` | Django secret key | Generate with Django |
| `ALLOWED_HOSTS` | Allowed domains | `.railway.app` |
| `USE_MYSQL` | Use MySQL database | `True` |
| `DATABASE_URL` | Database connection string | `mysql://user:pass@host:port/db` |

### Optional

| Variable | Description | Default |
|----------|-------------|---------|
| `DB_HOST` | MySQL host | From DATABASE_URL |
| `DB_PORT` | MySQL port | From DATABASE_URL |
| `DB_NAME` | Database name | From DATABASE_URL |
| `DB_USER` | Database user | From DATABASE_URL |
| `DB_PASSWORD` | Database password | From DATABASE_URL |

---

## 📖 API Documentation

### Sample Responses

#### GET /countries?region=Africa

```json
[
  {
    "id": 1,
    "name": "Nigeria",
    "capital": "Abuja",
    "region": "Africa",
    "population": 206139589,
    "currency_code": "NGN",
    "exchange_rate": 1600.23,
    "estimated_gdp": 257674481.25,
    "flag_url": "https://flagcdn.com/ng.svg",
    "last_refreshed_at": "2025-10-29T12:34:56Z"
  }
]
```

#### GET /status

```json
{
  "total_countries": 250,
  "last_refreshed_at": "2025-10-29T12:34:56Z"
}
```

#### Error Response (404)

```json
{
  "error": "Country not found"
}
```

---

## 🧪 Running Tests

```bash
# Run all tests
python manage.py test

# Run specific test
python manage.py test countries.tests
```

---

## 🐛 Troubleshooting

### Database Connection Issues

```bash
# Test MySQL connection
python manage.py check

# If fails, set USE_MYSQL=False to use SQLite
```

### Migration Issues

```bash
# Reset migrations
python manage.py migrate --fake countries zero
python manage.py migrate countries
```

### Static Files Not Loading

```bash
python manage.py collectstatic --noinput
```

---

## 📝 Development Notes

### External APIs Used

- **Countries API:** https://restcountries.com/v2/all
- **Exchange Rates:** https://open.er-api.com/v6/latest/USD

### Key Features Implemented

- ✅ Case-insensitive country name matching
- ✅ Automatic refresh with update/insert logic
- ✅ Random GDP multiplier (1000-2000) on each refresh
- ✅ Handles countries with no currency
- ✅ Handles missing exchange rates
- ✅ Generates summary image with top 5 countries
- ✅ Comprehensive error handling (503, 404, 400)

---

## 🤝 Contributing

This is a submission project for HNG Stage 2. Not accepting contributions at this time.

---

## 📄 License

This project is part of HNG Internship Stage 2 Backend Task.

---

## 👤 Author

**Olaitan34**

- GitHub: [@Olaitan34](https://github.com/Olaitan34)
- Repository: [country-currency](https://github.com/Olaitan34/country-currency)

---

## 🙏 Acknowledgments

- HNG Internship Program
- RestCountries API
- ExchangeRate-API

---

## 📞 Support

For issues or questions:
1. Check `RAILWAY_DEPLOYMENT_GUIDE.md`
2. Check `POSTMAN_TESTING_GUIDE.md`
3. Review Railway deployment logs
4. Test with provided Postman collection

---

**Built with ❤️ for HNG Internship Stage 2**
