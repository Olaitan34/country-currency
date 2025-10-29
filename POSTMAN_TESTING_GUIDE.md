# 🧪 Postman Testing Guide - Country Currency API

## Base URL
```
http://localhost:8000
```

---

## 📋 Test Endpoints in This Order:

### 1️⃣ **POST /countries/refresh** - Fetch & Cache Countries

**Purpose:** Fetch all countries from external APIs and populate your database

**Method:** `POST`  
**URL:** `http://localhost:8000/countries/refresh`  
**Headers:** 
```
Content-Type: application/json
```
**Body:** None (leave empty)

**Expected Response (200 OK):**
```json
{
  "message": "Refresh successful",
  "total_countries": 250,
  "last_refreshed_at": "2025-10-29T12:34:56.789Z"
}
```

**Test Cases:**
- ✅ Should return 200 with total countries
- ✅ Should update database with all countries
- ✅ Should generate summary image
- ⚠️ If external API fails, should return 503

---

### 2️⃣ **GET /status** - Check Refresh Status

**Method:** `GET`  
**URL:** `http://localhost:8000/status`  
**Headers:** None needed

**Expected Response (200 OK):**
```json
{
  "total_countries": 250,
  "last_refreshed_at": "2025-10-29T12:34:56.789Z"
}
```

**Test Cases:**
- ✅ Should show total countries
- ✅ Should show last refresh timestamp
- ✅ If never refreshed, should return 0 and null

---

### 3️⃣ **GET /countries** - List All Countries

**Method:** `GET`  
**URL:** `http://localhost:8000/countries`  
**Headers:** None needed

**Expected Response (200 OK):**
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
    "last_refreshed_at": "2025-10-29T12:34:56.789Z"
  },
  {
    "id": 2,
    "name": "Ghana",
    "capital": "Accra",
    "region": "Africa",
    "population": 31072940,
    "currency_code": "GHS",
    "exchange_rate": 15.34,
    "estimated_gdp": 3029834520.6,
    "flag_url": "https://flagcdn.com/gh.svg",
    "last_refreshed_at": "2025-10-29T12:34:56.789Z"
  }
]
```

---

### 4️⃣ **GET /countries?region=Africa** - Filter by Region

**Method:** `GET`  
**URL:** `http://localhost:8000/countries?region=Africa`  
**Headers:** None needed

**Expected Response:** List of African countries only

**Other Region Examples:**
```
http://localhost:8000/countries?region=Europe
http://localhost:8000/countries?region=Asia
http://localhost:8000/countries?region=Americas
```

---

### 5️⃣ **GET /countries?currency=NGN** - Filter by Currency

**Method:** `GET`  
**URL:** `http://localhost:8000/countries?currency=NGN`  
**Headers:** None needed

**Expected Response:** Countries using NGN currency

**Other Currency Examples:**
```
http://localhost:8000/countries?currency=USD
http://localhost:8000/countries?currency=EUR
http://localhost:8000/countries?currency=GBP
```

---

### 6️⃣ **GET /countries?sort=gdp_desc** - Sort by GDP (Descending)

**Method:** `GET`  
**URL:** `http://localhost:8000/countries?sort=gdp_desc`  
**Headers:** None needed

**Expected Response:** Countries sorted by highest GDP first

**Other Sort Options:**
```
http://localhost:8000/countries?sort=gdp_asc  (lowest to highest)
```

---

### 7️⃣ **GET /countries?region=Africa&sort=gdp_desc** - Combine Filters

**Method:** `GET`  
**URL:** `http://localhost:8000/countries?region=Africa&sort=gdp_desc`  
**Headers:** None needed

**Expected Response:** African countries sorted by GDP

**More Combinations:**
```
http://localhost:8000/countries?region=Europe&currency=EUR
http://localhost:8000/countries?currency=USD&sort=gdp_desc
```

---

### 8️⃣ **GET /countries/Nigeria** - Get Single Country

**Method:** `GET`  
**URL:** `http://localhost:8000/countries/Nigeria`  
**Headers:** None needed

**Expected Response (200 OK):**
```json
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
  "last_refreshed_at": "2025-10-29T12:34:56.789Z"
}
```

**Test Cases:**
- ✅ Should work with exact name: `Nigeria`
- ✅ Should work case-insensitive: `nigeria` or `NIGERIA`
- ✅ Test with spaces: `United States`
- ❌ Non-existent country should return 404

**Other Examples:**
```
http://localhost:8000/countries/Ghana
http://localhost:8000/countries/United%20States
http://localhost:8000/countries/United%20Kingdom
```

---

### 9️⃣ **GET /countries/InvalidCountry** - Test 404 Error

**Method:** `GET`  
**URL:** `http://localhost:8000/countries/InvalidCountry`  
**Headers:** None needed

**Expected Response (404 NOT FOUND):**
```json
{
  "error": "Country not found"
}
```

---

### 🔟 **DELETE /countries/Nigeria** - Delete a Country

**Method:** `DELETE`  
**URL:** `http://localhost:8000/countries/Nigeria`  
**Headers:** None needed  
**Body:** None

**Expected Response (204 NO CONTENT):**
- Empty response body
- Status code: 204

**Test Cases:**
- ✅ Should delete successfully
- ✅ Subsequent GET should return 404
- ❌ Deleting non-existent country should return 404

**Test Flow:**
1. DELETE `/countries/Nigeria` → 204
2. GET `/countries/Nigeria` → 404 (country not found)
3. Run POST `/countries/refresh` to restore it

---

### 1️⃣1️⃣ **GET /countries/image** - Get Summary Image

**Method:** `GET`  
**URL:** `http://localhost:8000/countries/image`  
**Headers:** None needed

**Expected Response (200 OK):**
- Content-Type: `image/png`
- Binary image data (PNG file)
- Should display image in Postman preview

**Test Cases:**
- ✅ After refresh, image should exist
- ❌ Before any refresh, should return 404:
```json
{
  "error": "Summary image not found"
}
```

**Note:** You can also open this URL directly in your browser to see the image.

---

## 🧪 **Validation Testing**

### Test Case: Create Country with Missing Fields (if you have a create endpoint)

**Method:** `POST`  
**URL:** `http://localhost:8000/countries` (if implemented)  
**Headers:**
```
Content-Type: application/json
```
**Body:**
```json
{
  "name": "Test Country"
}
```

**Expected Response (400 BAD REQUEST):**
```json
{
  "error": "Validation failed",
  "details": {
    "population": "is required",
    "currency_code": "is required"
  }
}
```

---

## 🔥 **Error Testing**

### Test External API Failure

**Scenario:** Stop your internet or use invalid API URLs

**Method:** `POST`  
**URL:** `http://localhost:8000/countries/refresh`

**Expected Response (503 SERVICE UNAVAILABLE):**
```json
{
  "error": "External data source unavailable",
  "details": "Could not fetch data from Countries or Exchange API"
}
```

---

## 📊 **Postman Collection Structure**

Create folders in Postman:

```
📁 Country Currency API
  📁 1. Setup
    - POST Refresh Countries
    - GET Status
  
  📁 2. List & Filters
    - GET All Countries
    - GET Filter by Region (Africa)
    - GET Filter by Currency (NGN)
    - GET Sort by GDP Desc
    - GET Combined Filters
  
  📁 3. Single Country
    - GET Country (Nigeria)
    - GET Country (Ghana)
    - GET Country Not Found (404)
  
  📁 4. Delete
    - DELETE Country
  
  📁 5. Image
    - GET Summary Image
  
  📁 6. Error Cases
    - GET 404 Error
    - External API Failure Test
```

---

## 🚀 **Quick Test Sequence**

**Run these in order for complete testing:**

1. ✅ POST `/countries/refresh` → Populate database
2. ✅ GET `/status` → Verify data loaded
3. ✅ GET `/countries` → See all countries
4. ✅ GET `/countries?region=Africa` → Test filtering
5. ✅ GET `/countries?sort=gdp_desc` → Test sorting
6. ✅ GET `/countries/Nigeria` → Get single country
7. ✅ GET `/countries/image` → View summary image
8. ✅ DELETE `/countries/Nigeria` → Delete a country
9. ✅ GET `/countries/Nigeria` → Verify 404
10. ✅ POST `/countries/refresh` → Restore deleted country

---

## 💡 **Tips for Postman:**

1. **Save Base URL as Environment Variable:**
   - Variable: `base_url`
   - Value: `http://localhost:8000`
   - Use: `{{base_url}}/countries`

2. **Create Tests Tab Scripts:**
```javascript
// Test for 200 status
pm.test("Status code is 200", function () {
    pm.response.to.have.status(200);
});

// Test response has data
pm.test("Response has countries", function () {
    var jsonData = pm.response.json();
    pm.expect(jsonData).to.be.an('array');
});
```

3. **Save Responses as Examples** - Right-click → Save Response → Save as Example

4. **Use Collection Runner** - Run all tests automatically

---

## 🌐 **Testing on Deployed Server**

Once deployed, replace `http://localhost:8000` with your deployed URL:

```
https://your-app.railway.app/countries/refresh
https://your-app.herokuapp.com/countries
etc.
```

---

## ✅ **Success Criteria:**

- [ ] All endpoints return correct status codes
- [ ] Refresh populates database with 250+ countries
- [ ] Filters work correctly (region, currency)
- [ ] Sorting works (GDP asc/desc)
- [ ] Single country retrieval works
- [ ] Delete removes country from database
- [ ] Image is generated and accessible
- [ ] Error cases return proper error messages
- [ ] Response format matches specifications

---

**Happy Testing! 🎉**
