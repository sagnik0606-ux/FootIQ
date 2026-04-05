# ⚽ FootIQ — Football Analytics Web Application

A Python/Flask web application for comprehensive football analytics powered by FBref data across 4 seasons. Search players, analyze performance metrics, compare statistics, and visualize trends with interactive Matplotlib charts.

## 🎯 Features

### Core Features
- **Player Search** — Search and discover football players by name across 5 major leagues with intelligent filtering
- **Detailed Statistics** — View comprehensive player stats (goals, assists, passes, tackles, xG, xA, and 50+ metrics)
- **Performance Visualization** — Server-side Matplotlib charts rendered as interactive images
- **Player Profiles** — Wikipedia integration for player photos and bios (cached locally)
- **Season Comparison** — Compare player performance across multiple seasons (4 seasons of data)
- **Interactive Dashboards** — Multi-league support (Premier League, La Liga, Serie A, Bundesliga, Ligue 1)

### Scout Matching Engine **[CORE FEATURE]**
- **15 Closest Players Similarity Matching** — Advanced player recommendation system that finds the 15 most similar players based on:
  - **Similarity Index Calculation** — Multi-dimensional performance comparison using normalized metrics
  - **Position-Based Matching** — Matches only players in the same position group (Attacker, Midfielder, Defender, Goalkeeper)
  - **Age-Based Filtering** — Configurable age cap with automatic pool widening if insufficient matches found
  - **Minimum Activity Filter** — Only considers players with 400+ minutes played in the season
  - **Smart Candidate Ranking** — Returns top 15 matches ranked by similarity score
  - **League Pool Options** — Search across all leagues or filter by specific league
  - **Real-Time Metrics** — Calculates 25+ normalized metrics for comparison

### Advanced Analytics Engine
- **Player Archetypes** — Intelligent player classification and archetype detection system
- **Similarity Index Scoring** — Proprietary algorithm for computing player similarity (0-100 scale)
- **Performance Scoring** — Normalized performance scoring system with league adjustments
- **Statistical Insights** — Advanced data analysis with actionable insights
- **Data Normalization** — Smart normalization for cross-season and cross-league comparisons
- **Performance Adjustments** — Dynamic adjustments based on league, position, and era

### Visualization Suite
- **Radar Charts** — 360° performance comparison across multiple dimensions
- **Pizza Charts** — Advanced segmented performance breakdown with visual segmentation
- **Percentile Charts** — Player ranking against peer groups (0-100 scale)
- **Lollipop Charts** — Horizontal statistical comparisons with visual clarity
- **Bar Charts** — Traditional metric comparisons across seasons/players
- **Solo Charts** — Individual player deep-dive visualizations with archetype context

### Data & Architecture
- **Intelligent Caching System** — Smart cache management with JSON-based persistence
- **Advanced Data Fetcher** — Real-time data retrieval and aggregation with fallback mechanisms
- **Offline-First Architecture** — All core functionality works completely offline after initial load
- **Responsive Design** — Mobile-friendly interface
- **No Database Required** — Pure CSV-based data (no SQL setup needed)
- **Zero Build Tools** — No npm, no Node.js, no Docker, no complex setup
- **Multi-League Processing** — Supports 5 major football leagues simultaneously

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
├── app.py                      # Main Flask application & routes
├── config.py                   # Configuration settings
├── requirements.txt            # Python dependencies
├── football_master.csv         # FBref data (4 seasons)
├── .env.example                # Environment template
├── .env                        # Your local config (not committed)
├── .gitignore                  # Git ignore rules
├── README.md                   # This file
│
├── core/                       # Advanced analytics engine
│   ├── __init__.py
│   ├── archetype.py            # Player archetype classification system
│   ├── scorer.py               # Performance scoring algorithms
│   ├── normalizer.py           # Data normalization for comparisons
│   ├── adjuster.py             # Performance adjustment system
│   ├── insights.py             # Statistical insights & analysis
│   ├── cache.py                # Intelligent caching system
│   └── fetcher.py              # Advanced data fetcher
│
├── static/                     # Frontend assets
│   ├── css/
│   │   └── style.css           # Application styles
│   ├── js/
│   │   ├── app.js              # Main application logic
│   │   └── scout.js            # Scout/search functionality
│   └── images/                 # Static images
│
├── templates/                  # HTML templates
│   ├── base.html               # Base template
│   ├── hub.html                # Main hub/dashboard
│   ├── player.html             # Player detail page
│   └── scout.html              # Scout/search interface
│
├── data/
│   └── cache/                  # Intelligent cache storage
│       ├── players_*.json      # Cached player data
│       └── wiki_img_*.json     # Cached Wikipedia images
│
├── visuals/                    # Visualization modules
│   ├── __init__.py
│   ├── radar.py                # Radar chart visualization
│   ├── pizza.py                # Pizza chart visualization
│   ├── percentile.py           # Percentile chart visualization
│   ├── lollipop.py             # Lollipop chart visualization
│   ├── bar.py                  # Bar chart visualization
│   └── solo.py                 # Solo player visualization
│
├── tests/                      # Unit tests
│   └── (test suite)
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

### Hub Page (`hub.html`)
- Central analytics dashboard
- Recent searches and quick access
- Featured player recommendations
- Performance statistics overview
- League-wide statistics

### Player Detail Page (`player.html`)
- Comprehensive player profile
- Season-by-season statistics table
- Multiple performance visualizations (radar, pizza, percentile)
- Wikipedia bio and cached photo
- Career highlights and archetype classification
- Performance comparison with peers
- Historical performance trends

### Scout Page (`scout.html`)
- Advanced player search with autocomplete
- Multi-filter options (position, league, season)
- Real-time search results
- Quick player comparison view
- Player statistics table with sorting
- Archive of recent searches

---

## 🖼️ Advanced Chart Generation

FootIQ features a sophisticated **multi-chart visualization system** powered by **Matplotlib**:

### Chart Types
1. **Radar Charts** (`radar.py`) — 360° performance comparison across multiple dimensions
2. **Pizza Charts** (`pizza.py`) — Advanced segmented performance breakdown with visual appeal
3. **Percentile Charts** (`percentile.py`) — Player ranking against peer groups (0-100 scale)
4. **Lollipop Charts** (`lollipop.py`) — Horizontal statistical comparisons with visual clarity
5. **Bar Charts** (`bar.py`) — Traditional metric comparisons across seasons/players
6. **Solo Charts** (`solo.py`) — Individual player deep-dive visualizations

### Generation Pipeline
1. Request triggers data retrieval from cache
2. Data normalization applied based on league/position/season
3. Matplotlib creates visualization based on selected chart type
4. Chart converted to base64 PNG encoding
5. Embedded directly in frontend as image
6. No external charting library dependencies needed

**Supported metrics:**
- Goals, Assists, Shots on Target, Expected Goals (xG)
- Pass completion, Pass success rate, Progressive passes
- Tackles, Interceptions, Blocks, Clearances
- Expected Assists (xA), Pressure success rate
- Dribbles, Fouls committed, And more...

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

## ⭐ Scout Matching System - The Game Changer

FootIQ's **Scout Matcher** is an advanced recommendation engine that helps identify the 15 most similar players to any given target player. This is perfect for recruitment, analysis, and fantasy football.

### How It Works

1. **User selects a target player** from any of the 5 supported leagues and season
2. **System extracts 25+ normalized performance metrics** (goals, assists, passes, defensive stats, expected metrics, etc.)
3. **Position-based matching** ensures only players in the same position group are compared
4. **Similarity Index Calculation** using advanced scoring algorithm compares:
   - Offensive metrics (goals, assists, xG, xA, shooting accuracy)
   - Passing metrics (completion rate, key passes, progressive passes)
   - Defensive metrics (tackles, interceptions, blocks, clearances)
   - Physical metrics (dribbles, aerial win %, fouls drawn)
   - Advanced metrics (SCA/90, GCA/90, npxG, touches in penalty area)

5. **Ranking Algorithm** scores similarity on 0-100 scale
6. **Returns top 15 matches** with similarity scores
7. **Automatic pool widening** if insufficient matches (expands age filters)

### Key Parameters

| Parameter | Description | Default |
|-----------|-------------|---------|
| **Max Age** | Upper age limit for candidate matches | 40 years |
| **League Pool** | Search within specific league or all leagues | All Leagues |
| **Position Group** | Automatically detected from target player | Same position |
| **Minimum Minutes** | Only players with 400+ minutes in season | 400 mins |
| **Season** | Historical data available from 4 seasons | 2024-25 |

### Supported Leagues
- 🏴󠁧󠁢󠁥󠁮󠁧󠁿 **Premier League** (England)
- 🇪🇸 **La Liga** (Spain)
- 🇮🇹 **Serie A** (Italy)
- 🇩🇪 **Bundesliga** (Germany)
- 🇫🇷 **Ligue 1** (France)

### Example Use Cases
- **Recruitment** — Find similar players when your top target is unavailable
- **Replacement Analysis** — Identify cost-effective alternatives with similar profiles
- **Fantasy Football** — Find undervalued players with similar output to expensive stars
- **Tactical Analysis** — Understand player archetypes and find comparable profiles
- **Market Research** — Benchmark player performance against similar profiles

---

FootIQ includes a sophisticated analytics system for intelligent player evaluation:

### Archetype Classification (`core/archetype.py`)
- Automatically classifies players into archetypes (Striker, Midfielder, Defender, etc.)
- Uses multi-dimensional performance metrics
- Enables peer-group comparison
- Updates dynamically based on performance data

### Performance Scoring (`core/scorer.py`)
- Normalizes player performance across different eras and leagues
- Weights metrics based on player position and role
- Generates comparable scores across seasons
- Identifies emerging and declining trends

### Data Normalization (`core/normalizer.py`)
- Standardizes metrics across leagues and seasons
- Handles missing data intelligently
- Scales performance on consistent scale (0-100)
- Enables cross-league comparisons

### Performance Adjustments (`core/adjuster.py`)
- League-specific performance adjustments
- Position-based metric weights
- Era-based calibration
- Environmental context awareness

### Statistical Insights (`core/insights.py`)
- Automatic insight generation from data patterns
- Trend identification and prediction
- Comparative analysis with peer groups
- Performance change analysis

---

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