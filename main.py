import requests, os
from datatime import datatime
T = os.getenv ("BOT_TOKEN")
C = os. getenv ("CHANNEL_ID")
K = os.getenv ("AP_FOOTBALL_KEY")
H = {"X-rapidapi-key": K, "x-rapidapi-host": v3.football.api-sports.io} today = datatime.now()strftime("%y-%m-%d")
def get(1):
try:
    r = requests.get("https://v3-football.p.rapidapi.com/fixtures": headers=H, params={"league": lid, "season": 2026, "next": 10}, timeout=20)
      return r.json().get("response", [])
    except: 
return []
msg = f "WORLD STATS HUB\n{today}\nlive from port harcout to the 🌍 world\n\n"
names = {39: "EPL", 140: laliga", 78: "Bundesliga", 135: serie A", 2: "UCL"}
for lid, name in names. items ():
f = get (lid)
if f:
   msg = f" --- {name} --- \n"
  for m in f [:6]:
       h = m ["teams"] ["away"]
["names"]
        gh = ["goals"] ["home"]; game
            [ga=m ["goals"] ["away"]
        t = m ["fixture"] ["date"] [11:16]
is = m ["fixture"] ["status"] ["short"]
        msg+ = f"{h} {gh} {a} ({s})\n" If s = FT" else" {t} | {h} vs {a} \n"
        msg+ ="\n"
if "---" not in msg: msg+ = NO games today. back tomorrow! \n"
msg+ = "follow @WorldStatsHub"
requests.post (f "https://api.telegram.org/bot {T}/ sendMessage",
json = {"chat_id: C, "test": msg}) print ("Done")
        
