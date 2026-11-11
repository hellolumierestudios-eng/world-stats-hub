import requests, os
from datetime import datetime

T = os.getenv("BOT_TOKEN")
C = os.getenv("CHANNEL_ID")
K = os.getenv("API_FOOTBALL_KEY")

H = {"x-apisports-key": K}
today = datetime.now().strftime("%y-%m-%d")

def get(lid):
    try:
        url = "https://v3.football.api-sports.io/fixtures"
        p = {"league": lid, "season": 2026, "next": 5}
        r = requests.get(url, headers=H, params=p, timeout=20)
        print("API", lid, r.status_code)
        return r.json().get("response", [])
    except Exception as e:
        print("API error", e)
        return []

msg = "⚽ WORLD STATS HUB\n- - - - - - - - - - - - - - - - - - - - -"
msg += today + "\nlive\n\n"
names = {39: "EPL", 140: "LaLiga", 78: "Bundesliga", 135: "Serie A", 61: "Ligue 1"}

for lid, name in names.items():
    f = get(lid)
    if f:
        msg += f"--- {name} ---\n"
        for m in f[:6]:
            home = m["teams"]["home"]["name"]
            away = m["teams"]["away"]["name"]
            msg += home + " vs " + away + "\n"
        msg += "\n"

if "---" not in msg:
    print("No games - skipping Telegram")
    exit()

msg += "Follow @WorldStatsHub"
print(msg)

u = "https://api.telegram.org/bot" + T + "/sendMessage"
res = requests.get(u, params={"chat_id": C, "text": msg})
print("TELEGRAM:", res.status_code, res.text[:500])
