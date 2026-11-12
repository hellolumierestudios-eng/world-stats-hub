import requests, os, json
from datetime import datetime

K = os.getenv("API_FOOTBALL_KEY")
H = {"x-apisports-key": K}
today = datetime.now().strftime("%Y-%m-%d")

def get(lid):
    try:
        url = "https://v3.football.api-sports.io/fixtures"
        p = {"league": lid, "season": 2026, "date": today}
        r = requests.get(url, headers=H, params=p, timeout=20)
        print("API", lid, r.status_code)
        return r.json().get("response", [])
    except Exception as e:
        print("API error", e)
        return []

names = {39: "Premier League", 140: "La Liga", 78: "Bundesliga", 135: "Serie A", 61: "Ligue 1"}

matches = []
for lid, name in names.items():
    f = get(lid)
    for m in f[:6]:
        home = m["teams"]["home"]["name"]
        away = m["teams"]["away"]["name"]
        gh = m["goals"]["home"]
        ga = m["goals"]["away"]
        status = m["fixture"]["status"]["short"]
        if gh is None or ga is None:
            score = "vs"
            time = m["fixture"]["date"][11:16]
        else:
            score = f"{gh} - {ga}"
            time = status
        matches.append({"home": home, "away": away, "score": score, "time": time, "league": name, "status": status})

output = {"updated": today, "matches": matches}
with open("scores.json", "w") as f:
    json.dump(output, f, indent=2)
print("Saved:", output)
