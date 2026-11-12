import requests
import os
import json
from datetime import datetime, timezone

T = os.environ.get("BOT_TOKEN")
C = os.environ.get("CHANNEL_ID")
K = os.environ.get("API_FOOTBALL_KEY")

H = {"x-apisports-key": K}
today = datetime.now(timezone.utc).strftime("%Y-%m-%d")

LEAGUES = [39, 140, 135, 78, 61, 2, 3, 88, 94, 71]

def get(lid):
    url = f"https://v3.football.api-sports.io/fixtures?date={today}&league={lid}&season=2025"
    r = requests.get(url, headers=H, timeout=30)
    return r.json().get("response", [])

all_matches = []
for lid in LEAGUES:
    try:
        all_matches.extend(get(lid))
    except Exception as e:
        print(f"League {lid} failed: {e}")

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

# Telegram
if T and C and matches:
    lines = ["⚽ LIVE SCORES UPDATE"]
    for m in matches[:20]:
        score = f"{m['home_goals']}-{m['away_goals']}" if m['home_goals'] is not None else "vs"
        lines.append(f"{m['home']} {score} {m['away']} ({m['status']})")
    text = "\n".join(lines)
    url = f"https://api.telegram.org/bot{T}/sendMessage"
    r = requests.post(url, json={"chat_id": C, "text": text}, timeout=30)
    print("Telegram:", r.status_code, r.text[:200])
else:
    print("Telegram skipped - no token/channel or no matches")
