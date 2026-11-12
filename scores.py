import requests, os, json
from datetime import datetime, timedelta

K = os.getenv("API_FOOTBALL_KEY")
H = {"x-apisports-key": K}
now = datetime.now()
today = now.strftime("%Y-%m-%d")
dates = [(now + timedelta(days=i)).strftime("%Y-%m-%d") for i in range(0, 11)]

def get(lid, date):
    try:
        url = "https://v3.football.api-sports.io/fixtures"
        p = {"league": lid, "season": 2026, "date": date}
        r = requests.get(url, headers=H, params=p, timeout=20)
        print("API", lid, date, r.status_code)
        x = r.json().get("response", [])
        err = r.json().get("errors")
        print("COUNT", lid, date, len(x))
        print("ERR", err)
        return r.json().get("response", [])
    except Exception as e:
        print("API error", e)
        return []

names = {39: "Premier League", 140: "Laliga", 78: "Bundesliga", 135: "Serie A", 61: "Ligue 1", 40: "Championship", 88: "Eredivisie", 94: "Primeira Liga"}

matches = []
for date in dates:
    for lid, name in names.items():
        f = get(lid, date)
        for m in f[:4]:
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
            matches.append({"home": home, "away": away, "score": score, "time": time, "league": name, "status": status, "date": date})

output = {"updated": today, "matches": matches}
with open("scores.json", "w") as f:
    json.dump(output, f, indent=2)
print("Saved:", output)
