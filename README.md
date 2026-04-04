# ⚽ FootIQ — Football Analytics Web Application

A Python/Flask web application for comprehensive football analytics powered by FBref data across 4 seasons. Search players, analyze performance metrics, compare statistics, and visualize trends with interactive Matplotlib charts.

## 🎯 Features

- **Player Search** — Search and discover football players by name
- **Detailed Statistics** — View comprehensive player stats (goals, assists, passes, tackles, etc.)
- **Performance Visualization** — Server-side Matplotlib charts rendered as interactive images
- **Player Profiles** — Wikipedia integration for player photos and bios (cached locally)
- **Season Comparison** — Compare player performance across multiple seasons
- **Offline-First Architecture** — All core functionality works completely offline
- **Responsive Design** — Mobile-friendly interface
- **No Database Required** — Pure CSV-based data (no SQL setup needed)
- **Zero Build Tools** — No npm, no Node.js, no Docker, no complex setup

## 🛠️ Tech Stack

| Component | Technology | Details |
|-----------|-----------|---------|
| **Backend** | Python 3.x + Flask | Lightweight REST API |
| **Frontend** | HTML5, CSS3, Vanilla JavaScript | No frameworks, no build tools |
| **Data Source** | CSV (`football_master.csv`) | FBref stats across 4 seasons |
| **Charts** | Matplotlib | Server-side rendering, base64 PNG output |
| **Images** | Wikipedia REST API | Runtime fetch with local caching |
| **Environment** | python-dotenv | Secure configuration management |
| **Data Processing** | pandas | CSV parsing and filtering |

## 📋 Prerequisites

- **Python 3.7+** — [Download here](https://www.python.org/downloads/)
- **pip** — Comes automatically with Python
- **Modern browser** — Chrome, Firefox, Safari, or Edge
- **football_master.csv** — Already in project root

## 🚀 Quick Start (3 Steps)

### Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 2: Run the App

```bash
python app.py
```

You should see:
```
 * Running on http://127.0.0.1:5000
 * Press CTRL+C to quit
```

### Step 3: Open in Browser

Navigate to: **http://127.0.0.1:5000**

---

## 📖 Detailed Setup Instructions

### Windows

```bash
# 1. Navigate to project folder
cd D:\College\Football Project

# 2. Create virtual environment (optional but recommended)
python -m venv venv

# 3. Activate virtual environment
venv\Scripts\activate

# 4. Install dependencies
pip install -r requirements.txt

# 5. Run the app
python app.py
```

### macOS / Linux

```bash
# 1. Navigate to project folder
cd /path/to/FootIQ

# 2. Create virtual environment
python3 -m venv venv

# 3. Activate virtual environment
source venv/bin/activate

# 4. Install dependencies
pip install -r requirements.txt

# 5. Run the app
python3 app.py
```

### Configuration (Optional)

1. Copy `.env.example` to `.env`:
   ```bash
   cp .env.example .env
   ```

2. Edit `.env` if you want to customize:
   - `FLASK_ENV` — Set to `development` or `production`
   - `FLASK_DEBUG` — Set to `True` for auto-reload during development
   - API keys for Wikipedia (usually not needed)

3. Never commit `.env` — It's in `.gitignore` ✅

---

## 📁 Project Structure

```
FootIQ/
├── app.py                      # Main Flask application
├── config.py                   # Configuration settings
├── requirements.txt            # Python dependencies
├── football_master.csv         # FBref data (4 seasons)
├── .env.example                # Environment template
├── .env                        # Your local config (not committed)
├── .gitignore                  # Git ignore rules
├── README.md                   # This file
│
├── core/                       # Application logic
│   ├── __init__.py
│   ├── player_service.py       # Player search & stats logic
│   ├── chart_service.py        # Matplotlib chart generation
│   └── cache_service.py        # Wikipedia image caching
│
├── static/                     # Frontend assets
│   ├── css/
│   │   └── style.css           # Application styles
│   ├── js/
│   │   └── script.js           # Client-side logic
│   └── images/                 # Static images
│
├── templates/                  # HTML templates
│   ├── index.html              # Home page with search
│   ├── player.html             # Player detail page
│   ├── compare.html            # Player comparison
│   └── base.html               # Base template
│
├── data/
│   └── cache/
│       └── player_images/      # Cached Wikipedia photos
│
├── tests/                      # Unit tests
│   ├── test_player_service.py
│   └── test_chart_service.py
│
├── visuals/                    # Generated charts (temp)
│   └── *.png                   # Matplotlib output
│
├── __pycache__/                # Python cache (auto-generated)
└── .vscode/                    # VS Code settings (optional)
```

---

## 🔌 API Endpoints

### Pages (HTML)

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/` | GET | Home page with player search |
| `/player/<player_name>` | GET | Player detail page with stats & charts |
| `/compare` | GET | Compare multiple players |

### API Routes

| Endpoint | Method | Purpose | Example |
|----------|--------|---------|---------|
| `/api/search` | GET | Search players | `/api/search?q=Messi` |
| `/api/player/<name>` | GET | Get player stats | `/api/player/Lionel%20Messi` |
| `/api/stats/<name>` | GET | Get detailed stats | `/api/stats/Cristiano%20Ronaldo` |
| `/api/chart/<name>` | GET | Get player chart (PNG) | `/api/chart/Messi?metric=goals` |

---

## 📊 Data Format

### football_master.csv Structure

The CSV contains FBref data with these key columns:

```
Player, Nation, Squad, Season, Age, Pos, MP, Min, Gls, Ast, 
G-PK, PK, PKatt, CrdY, CrdR, xG, xA, xG+xA, ...
```

**Seasons Covered:** 4 seasons of international/club data  
**Players:** 1000+ unique players  
**Statistics:** 50+ performance metrics

---

## 🎨 Frontend Features

### Home Page (`index.html`)
- Search bar with autocomplete
- Recent players or featured players
- Quick stats overview

### Player Detail Page (`player.html`)
- Player name, number, position, squad
- Season-by-season statistics table
- Performance charts (goals, assists, etc.)
- Wikipedia bio and photo
- Career highlights

### Comparison Page (`compare.html`)
- Side-by-side player comparison
- Stats tables
- Visual charts comparing metrics
- Export as image

---

## 🖼️ Chart Generation

Charts are generated server-side using **Matplotlib**:

1. Request triggers chart generation
2. Matplotlib creates visualization
3. Chart converted to base64 PNG
4. Returned to frontend as image
5. No external charting library needed

**Supported metrics:**
- Goals, Assists, Shots on Target
- Pass completion, Pass success rate
- Tackles, Interceptions, Clearances
- xG (Expected Goals), xA (Expected Assists)
- And more...

---

## 🖼️ Image Caching

Player photos are fetched from Wikipedia at runtime:

1. User requests player page
2. App checks local cache: `data/cache/player_images/`
3. If cached: return immediately
4. If not cached: fetch from Wikipedia API
5. Save to cache for future requests
6. Serve from cache (no repeat API calls)

**Why?** Faster loading + offline capability after first load

---

## 🧪 Running Tests

```bash
# Run all tests
python -m pytest

# Run specific test file
python -m pytest tests/test_player_service.py

# Run with coverage
python -m pytest --cov=core tests/
```

---

## 🔐 Security Notes

1. **Credentials in .env** — Never hardcode API keys or secrets
2. **CSV Data** — Player data is public, no sensitive info
3. **Wikipedia API** — Free, no authentication required (optional key if rate-limited)
4. **CORS** — Enable if frontend separated from backend
5. **Input Validation** — All search queries are sanitized

---

## 🚨 Troubleshooting

### Issue: "ModuleNotFoundError: No module named 'flask'"
**Solution:** Run `pip install -r requirements.txt`

### Issue: "Port 5000 already in use"
**Solution:** Kill existing process or change port in `app.py`:
```python
if __name__ == '__main__':
    app.run(debug=True, port=5001)  # Change 5000 to 5001
```

### Issue: "football_master.csv not found"
**Solution:** Make sure the CSV is in project root:
```bash
ls football_master.csv  # macOS/Linux
dir football_master.csv  # Windows
```

### Issue: "Wikipedia images not loading"
**Solution:** App works offline for stats. Photos require internet.  
Check `.env` has correct Wikipedia API settings.

### Issue: Charts not displaying
**Solution:** Ensure Matplotlib is installed:
```bash
pip install matplotlib
```

---

## 📈 Future Enhancements

- [ ] Database integration (SQLite/PostgreSQL) for faster queries
- [ ] User authentication and saved comparisons
- [ ] Advanced filtering (by position, age, season)
- [ ] Statistical analysis (correlation, regression)
- [ ] Real-time data updates from FBref
- [ ] Mobile app (React Native)
- [ ] Dark mode UI
- [ ] Export to PDF/Excel
- [ ] Player prediction models (ML)
- [ ] Team analytics

---

## 📄 License

No specific license. Contact the author for usage rights.

---

## 👨‍💻 Author

**Sagnik**  
GitHub: [@sagnik0606-ux](https://github.com/sagnik0606-ux)  
Email: basu.sagnik0606@gmail.com

---

## 🤝 Contributing

Want to improve FootIQ? 

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Commit changes: `git commit -m "Add amazing feature"`
4. Push branch: `git push origin feature/amazing-feature`
5. Open a Pull Request

---

## 🙋 Support

Found a bug or have questions?  
[Open an issue](https://github.com/sagnik0606-ux/FootIQ/issues) on GitHub.

---

**Made with ⚽ for football analytics enthusiasts**
