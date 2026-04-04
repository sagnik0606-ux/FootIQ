import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_FOOTBALL_KEY", "")
API_BASE_URL = "https://v3.football.api-sports.io"
API_HOST = "v3.football.api-sports.io"

CACHE_DIR = os.path.join(os.path.dirname(__file__), "data", "cache")
CACHE_TTL_DAYS = 7

MIN_MINUTES = 450  # minimum minutes to include a player in comparisons
