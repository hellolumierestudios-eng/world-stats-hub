import requests, os
from datatime import datatime
T = os.getenv ("BOT_TOKEN")
C = os. getenv ("CHANNEL_ID")
K = os.getenv ("AP_FOOTBALL_KEY")
H = {"X-rapidapi-key": K, 
H["X-rapidapi-host"] = "v3.football.api-sports.io} 
today = datatime.now()strftime("%y-%m-%d")
def get(lid):
try:
    url = https://v3-football.p.rapidapi.com/fixtures"
    p = {"league": lid, "season": 2026, "next": 10}
    r = request.get(url, headers=H, params=p timeout=20)
    return r.json().get("response", [])
 except:
    return []
msg = WORLD STATS HUB\n
msg += today + "\nlive\n"
names = {39: "EPL", 140: LaLiga", 78: "Bundesliga", 
names[135] = serie A"
names[61] = "laliga 1"
for lid, name in names.items():
    f = get(lid)
    if f:
        msg += "--- " + name + ---\n"
        for m in f[:6]:
            home = m["teams"]["home"]["name"]
            away = m["teams"][away"]["name"]
            msg += home + " vs " + away + "\n"
u = "https://api.telegram.org/bot"  + T + "/sendmessage" 
requests.get(u, params={"chat_id": C, "text": msg{)
print(msg)
