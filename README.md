# Astro Engine 🌟

Professional-grade Vedic Astrology calculation engine built with Python, FastAPI, and Swiss Ephemeris.

## Features

✅ Complete birth chart calculations with all planetary positions  
✅ All 12 house systems (Placidus, Koch, Equal, Whole Sign, etc.)  
✅ Divisional charts (D1 through D60)  
✅ Panchang (Tithi, Nakshatra, Yoga, Karana, Rahu Kaal)  
✅ Vimshottari Dasha system (Mahadasha, Antardasha, Pratyantardasha)  
✅ KP (Krishnamurti Paddhati) system with sub-lords  
✅ Ashtakoot compatibility matching (8 Kutas)  
✅ Ashtakavarga (8-point benefic system)  
✅ Yoga and Dosha detection (30+ types)  
✅ Comprehensive remedies system (Gemstones, Mantras, Charity)  
✅ Complete Horoscope generation engine  
✅ REST API with FastAPI  

## Quick Start

### Prerequisites

- **Python 3.10 or higher**
- **UV package manager** (faster than pip)

### Installation Steps

#### 1. Install UV Package Manager

```cmd
pip install uv
```

#### 2. Navigate to Project Directory

```cmd
cd astro-engine
```

#### 3. Create Virtual Environment

```cmd
uv venv
```

#### 4. Activate Virtual Environment

**Windows (CMD):**
```cmd
.venv\Scripts\activate
```

**Windows (PowerShell):**
```powershell
.venv\Scripts\Activate.ps1
```

**Linux/Mac:**
```bash
source .venv/bin/activate
```

#### 5. Install Dependencies

```cmd
uv pip install -e .
```

This will install:
- FastAPI
- Uvicorn
- Pyswisseph (Swiss Ephemeris)
- Pydantic
- Python-dateutil
- Pytz
- All other required dependencies

#### 6. Download Swiss Ephemeris Data Files

**CRITICAL:** The engine won't work without these files!

**Step-by-step:**

1. **Visit GitHub Repository** (Recommended - Faster):
   https://github.com/aloistr/swisseph/tree/master/ephe

   **OR** use **Dropbox** (Alternative):
   https://www.dropbox.com/scl/fo/y3naz62gy6f6qfrhquu7u/h?rlkey=ejltdhb262zglm7eo6yfj2940&dl=0

2. **Download these specific files** (from GitHub `ephe` folder or Dropbox):
   - `seas_18.se1` - Asteroid ephemeris file
   - `semo_18.se1` - Moon ephemeris file
   - `sepl_18.se1` - Planet ephemeris file

   **From GitHub:** Click on each file → Click "Download" button on the right
   
   **From Dropbox:** Navigate to `ephe` folder → Select and download the 3 files

3. **Create the ephemeris_data folder** in your project root:
   ```cmd
   mkdir ephemeris_data
   ```

4. **Move/Copy the downloaded files** into the `ephemeris_data` folder:
   ```
   astro-engine/
   └── ephemeris_data/
       ├── seas_18.se1
       ├── semo_18.se1
       └── sepl_18.se1
   ```

**Full path should be:**
```
C:\Users\hp\OneDrive\Desktop\open_source\astrobaba\astro-engine\ephemeris_data\seas_18.se1
C:\Users\hp\OneDrive\Desktop\open_source\astrobaba\astro-engine\ephemeris_data\semo_18.se1
C:\Users\hp\OneDrive\Desktop\open_source\astrobaba\astro-engine\ephemeris_data\sepl_18.se1
```

**Quick Download Links:**
- GitHub: https://github.com/aloistr/swisseph/tree/master/ephe (Click individual files → Download)
- Dropbox: https://www.dropbox.com/scl/fo/y3naz62gy6f6qfrhquu7u/h?rlkey=ejltdhb262zglm7eo6yfj2940&dl=0 (Go to `ephe` folder)

**Note:** These are binary files (`.se1` extension). You only need these 3 files for basic planetary calculations. Total size ~7-8 MB.

#### 7. Configure Environment

```cmd
copy .env.example .env
```

Edit `.env` file and update if needed:
- `CORS_ORIGINS` - Add your Node.js URL (already includes http://localhost:6001)
- `EPHEMERIS_PATH` - Path to ephemeris data (default: ./ephemeris_data)
- `SECRET_KEY` - Change for production

#### 8. Run the Server

**Option A: Using the startup script (Windows)**

```cmd
start.bat
```

**Option B: Using uvicorn directly**

```cmd
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

#### 9. Verify Installation

Open browser and visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/

## API Documentation

### Base URL
```
http://localhost:8000/api/v1
```

### Available Endpoints

#### 1. Birth Chart
```http
POST /api/v1/chart
Content-Type: application/json

{
  "name": "John Doe",
  "date": "1990-05-15",
  "time": "14:30:00",
  "latitude": 28.6139,
  "longitude": 77.2090,
  "timezone": "Asia/Kolkata"
}
```

#### 2. Vimshottari Dasha
```http
POST /api/v1/dasha
```

#### 3. Panchang
```http
POST /api/v1/panchang
```

#### 4. Divisional Charts
```http
POST /api/v1/divisional/all
```

#### 5. KP System
```http
POST /api/v1/kp
```

#### 6. Compatibility Matching
```http
POST /api/v1/matching/ashtakoot
```

#### 7. Yogas & Doshas
```http
POST /api/v1/yogas
```

#### 8. Ashtakavarga
```http
POST /api/v1/horoscope/ashtakavarga
```

#### 9. Complete Horoscope
```http
POST /api/v1/horoscope/complete
```

## Calling from Node.js

### Example: Fetch Birth Chart

```javascript
const axios = require('axios');

async function getBirthChart() {
  try {
    const response = await axios.post('http://localhost:8000/api/v1/chart', {
      name: "John Doe",
      date: "1990-05-15",
      time: "14:30:00",
      latitude: 28.6139,
      longitude: 77.2090,
      timezone: "Asia/Kolkata"
    });
    
    console.log(response.data);
    return response.data;
  } catch (error) {
    console.error('Error:', error.response?.data || error.message);
  }
}

getBirthChart();
```

### Example: Complete Horoscope

```javascript
async function getCompleteHoroscope() {
  try {
    const response = await axios.post('http://localhost:8000/api/v1/horoscope/complete', {
      birth_data: {
        name: "John Doe",
        date: "1990-05-15",
        time: "14:30:00",
        latitude: 28.6139,
        longitude: 77.2090,
        timezone: "Asia/Kolkata"
      }
    });
    
    console.log(response.data);
    return response.data;
  } catch (error) {
    console.error('Error:', error.response?.data || error.message);
  }
}
```

### Example: Using Fetch API

```javascript
async function getBirthChart() {
  const response = await fetch('http://localhost:8000/api/v1/chart', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      name: "John Doe",
      date: "1990-05-15",
      time: "14:30:00",
      latitude: 28.6139,
      longitude: 77.2090,
      timezone: "Asia/Kolkata"
    })
  });
  
  const data = await response.json();
  console.log(data);
}
```

📖 **For complete Node.js integration guide, see [NODE_JS_INTEGRATION.md](NODE_JS_INTEGRATION.md)**

## Project Structure

```
astro-engine/
├── app/
│   ├── core/
│   │   ├── ephemeris.py          # Swiss Ephemeris wrapper
│   │   ├── chart_engine.py       # Birth chart calculator
│   │   ├── horoscope_engine.py   # Horoscope generator
│   │   ├── remedies.py           # Remedies system
│   │   ├── vedic/
│   │   │   ├── divisional_charts.py
│   │   │   ├── dasha.py
│   │   │   ├── panchang.py
│   │   │   ├── yogas_doshas.py
│   │   │   └── ashtakavarga.py
│   │   ├── kp/
│   │   │   └── kp_system.py
│   │   └── matching/
│   │       └── ashtakoot.py
│   ├── api/
│   │   └── v1/
│   │       ├── endpoints/
│   │       │   ├── chart.py
│   │       │   ├── dasha.py
│   │       │   ├── panchang.py
│   │       │   ├── divisional.py
│   │       │   ├── kp.py
│   │       │   ├── matching.py
│   │       │   ├── yogas.py
│   │       │   └── horoscope.py
│   │       ├── models.py
│   │       └── router.py
│   ├── config.py
│   └── main.py
├── tests/
├── ephemeris_data/              # Place .se1 files here
├── .env.example
├── pyproject.toml
├── README.md
└── start.bat
```

## Troubleshooting

### Issue: Import errors during installation
**Solution**: Make sure you're using Python 3.10 or higher
```cmd
python --version
```

### Issue: "Ephemeris file not found"
**Solution**: Download the Swiss Ephemeris .se1 files and place them in `ephemeris_data/` folder

### Issue: CORS errors from Node.js
**Solution**: Make sure your Node.js URL is added to `.env`:
```
CORS_ORIGINS=["http://localhost:6001", "http://localhost:3000"]
```

### Issue: Port already in use
**Solution**: Change the port in `.env`:
```
API_PORT=8001
```

## Testing

Run tests:
```cmd
pytest tests/
```

Run with coverage:
```cmd
pytest --cov=app tests/
```

## Development

For development with auto-reload:
```cmd
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## Production Deployment

1. Change `DEBUG=false` in `.env`
2. Set strong `SECRET_KEY`
3. Use production ASGI server:
```cmd
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

## License

MIT License

## Support

For issues and questions, please check the API documentation at `/docs` endpoint.
