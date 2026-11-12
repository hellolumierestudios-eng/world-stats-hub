import requests
import os
import json
from datetime import datetime, timezone

T = os.environ.get("BOT_TOKEN")
C = os.environ.get("CHANNEL_ID")
K = os.environ.get("API_FOOTBALL_KEY")

print("Has BOT_TOKEN:", bool(T))
print("Has CHANNEL_ID:", bool(C))
print("Has API_KEY:", bool(K))

H = {"x-apisports-key": K}
today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
print("Date used:", today)

# Try 1: all fixtures today, no league, no season
url1 = f"https://v3.football.api-sports.io/fixtures?date={today}"
r = requests.get(url1, headers=H, timeout=30)
print("Try1 status:", r.status_code)
data = r.json()
print("Try1 keys:", list(data.keys()))
print("Try1 errors:", data.get("errors"))
print("Try1 results:", data.get("results"))
all_matches = data.get("response", [])

# Try 2: if 0, try with season 2026 for Premier League only
if len(all_matches) == 0:
    url2 = f"https://v3.football.api-sports.io/fixtures?date={today}&league=39&season=2026"
    r2 = requests.get(url2, headers=H, timeout=30)
    print("Try2 status:", r2.status_code)
    d2 = r2.json()
    print("Try2 errors:", d2.get("errors"))
    print("Try2 results:", d2.get("results"))
    all_matches = d2.get("response", [])

matches = []
for m in all_matches:
    matches.append({
        "league": m["league"]["name"],
        "home": m["teams"]["home"]["name"],
        "away": m["teams"]["away"]["name"],
        "home_goals": m["goals"]["home"],
        "away_goals": m["goals"]["away"],
        "status": m["fixture"]["status"]["short"],
        "minute": m["fixture"]["status"]["elapsed"],
        "time": m["fixture"]["date"]
    })

with open("scores.json", "w") as f:
    json.dump(matches, f, indent=2)

print(f"Saved scores.json with {len(matches)} matches")

if T and C and matches:
    lines = ["⚽ LIVE SCORES UPDATE"]
    for m in matches[:20]:
        score = f"{m['home_goals']}-{m['away_goals']}" if m['home_goals'] is not None else "vs"
        lines.append(f"{m['home']} {score} {m['away']} ({m['status']})")
    text = "\n".join(lines)
    url = f"https://api.telegram.org/bot{T}/sendMessage"
    r = requests.post(url, json={"chat_id": C, "text": text}, timeout=30)
    print("Telegram:", r.status_code, r.text[:300])
else:
    print("Telegram skipped - no token/channel or no matches")
