import requests, os
from datetime import datetime

T=os.getenv("BOT_TOKEN")
C=os.getenv("CHANNEL_ID")
K=os.getenv("API_FOOTBALL_KEY")
H={"x-rapidapi-key":K,"x-rapidapi-host":"v3.football.api-sports.io"}
today=datetime.now().strftime("%Y-%m-%d")

def get(l):
    try:
        url=f"https://v3.football.api-sports.io"
        url+=f"/fixtures?league={l}&season=2025"
        url+=f"&date={today}"
        r=requests.get(url, headers=H, timeout=20)
        return r.json().get("response",[])
    except: return []

msg=f"WORLD STATS HUB - {today}\n\n"
names={39:"EPL",140:"LaLiga",78:"Bundesliga",135:"Serie A",61:"Ligue 1"}

for lid,name in names.items():
    f=get(lid)
    if f:
        msg+=f"--- {name} ---\n"
        for m in f[:6]:
            h=m["teams"]["home"]["name"]
            a=m["teams"]["away"]["name"]
            gh=m["goals"]["home"]
            ga=m["goals"]["away"]
            t=m["fixture"]["date"][11:16]
            if gh is None:
                msg+=f"{h} vs {a} ({t})\n"
            else:
                msg+=f"{h} {gh}-{ga} {a}\n"
        msg+="\n"

if "---" not in msg: msg+="No games today\n"
msg+="Follow @WorldStatsHub"
requests.post(f"https://api.telegram.org/bot{T}/sendMessage", data={"chat_id":C, "text":msg})
print("Done")
