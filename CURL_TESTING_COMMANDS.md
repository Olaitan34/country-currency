# 🚀 cURL Testing Commands - Country Currency API

## Quick Test Commands (Copy & Paste)

### 1. Refresh Countries (POST)
```bash
curl -X POST http://localhost:8000/countries/refresh
```

### 2. Get Status
```bash
curl http://localhost:8000/status
```

### 3. Get All Countries
```bash
curl http://localhost:8000/countries
```

### 4. Filter by Region
```bash
curl "http://localhost:8000/countries?region=Africa"
```

### 5. Filter by Currency
```bash
curl "http://localhost:8000/countries?currency=NGN"
```

### 6. Sort by GDP (Descending)
```bash
curl "http://localhost:8000/countries?sort=gdp_desc"
```

### 7. Combined Filters
```bash
curl "http://localhost:8000/countries?region=Africa&sort=gdp_desc"
```

### 8. Get Single Country
```bash
curl http://localhost:8000/countries/Nigeria
```

### 9. Delete Country
```bash
curl -X DELETE http://localhost:8000/countries/Nigeria
```

### 10. Get Summary Image
```bash
curl http://localhost:8000/countries/image --output summary.png
```

---

## PowerShell Commands (For Windows)

### 1. Refresh Countries
```powershell
Invoke-RestMethod -Uri "http://localhost:8000/countries/refresh" -Method POST
```

### 2. Get Status
```powershell
Invoke-RestMethod -Uri "http://localhost:8000/status"
```

### 3. Get All Countries
```powershell
Invoke-RestMethod -Uri "http://localhost:8000/countries"
```

### 4. Filter by Region
```powershell
Invoke-RestMethod -Uri "http://localhost:8000/countries?region=Africa"
```

### 5. Get Single Country
```powershell
Invoke-RestMethod -Uri "http://localhost:8000/countries/Nigeria"
```

### 6. Delete Country
```powershell
Invoke-RestMethod -Uri "http://localhost:8000/countries/TestCountry" -Method DELETE
```

### 7. Download Image
```powershell
Invoke-WebRequest -Uri "http://localhost:8000/countries/image" -OutFile "summary.png"
```

---

## Pretty JSON Output (with jq)

If you have `jq` installed:

```bash
curl http://localhost:8000/countries | jq
curl http://localhost:8000/status | jq
curl "http://localhost:8000/countries?region=Africa" | jq
```

---

## Test 404 Error
```bash
curl http://localhost:8000/countries/InvalidCountry
```

Expected:
```json
{"error": "Country not found"}
```

---

## Full Test Sequence

Run these commands in order:

```bash
# 1. Refresh data
curl -X POST http://localhost:8000/countries/refresh

# 2. Check status
curl http://localhost:8000/status

# 3. Get all countries
curl http://localhost:8000/countries

# 4. Filter by Africa
curl "http://localhost:8000/countries?region=Africa"

# 5. Get Nigeria
curl http://localhost:8000/countries/Nigeria

# 6. Get image
curl http://localhost:8000/countries/image --output summary.png

# 7. View the image
start summary.png  # Windows
open summary.png   # Mac
xdg-open summary.png  # Linux
```
