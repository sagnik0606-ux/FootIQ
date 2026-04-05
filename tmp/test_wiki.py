import requests
from urllib.parse import quote

name = "Elliot Anderson"
slug = name.strip().replace(" ", "_")
encoded_slug = quote(slug, safe="")
HEADERS = {"User-Agent": "FootIQ/1.0 (football analytics)"}

r = requests.get(
    f"https://en.wikipedia.org/api/rest_v1/page/summary/{encoded_slug}",
    headers=HEADERS, timeout=5
)
print(f"Status: {r.status_code}")
if r.status_code == 200:
    d = r.json()
    print(f"Title: {d.get('title')}")
    print(f"Type: {d.get('type')}")
    print(f"Description: {d.get('description')}")
    print(f"Extract: {d.get('extract')[:100]}...")
    img = (d.get("originalimage") or d.get("thumbnail") or {}).get("source")
    print(f"Image: {img}")
