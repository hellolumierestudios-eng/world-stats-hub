import os, json, requests
from datetime import date

API_KEY = os.environ.get("API_FOOTBALL_KEY")
today = date.today().isoformat()

headers = {"x-rapidapi-key": API_KEY, "x-rapidapi-host": "v3.football.api-sports.io"}
url = f"https://v3.football.api-sports.io/fixtures?date={today}"

matches = []
try:
    r = requests.get(url, headers=headers, timeout=20)
    data = r.json().get("response", [])
    for m in data[:15]:
        matches.append({
            "home": m["teams"]["home"]["name"],
            "away": m["teams"]["away"]["name"],
            "score": f"{m['goals']['home']} - {m['goals']['away']}" if m['goals']['home'] is not None else "vs",
            "league": m["league"]["name"],
            "status": m["fixture"]["status"]["long"]
        })
except Exception as e:
    print("Error:", e)

players = [
    "Victor Osimhen - Born in Lagos, sold pure water on the street as a boy, now one of the best strikers in the world. From grass to grace.",
    "Sadio Mane - From a small village in Senegal, he walked 400km to try out for football. Now a legend.",
    "Cristiano Ronaldo - Grew up poor in Madeira, shared one room with his family. Now 5x Ballon d'Or winner.",
    "N'Golo Kante - Used to pick up trash to survive in Paris. Now World Cup winner.",
    "Mohamed Salah - From a small village in Egypt, travelled 4 hours daily to training. Now King of Liverpool."
]
player_life = players[date.today().day % len(players)]

output = {
    "updated": today,
    "matches": matches,
    "transfers": "Check Telegram @WorldStatsHub for latest transfer news!",
    "player_life": player_life
}

# Save to BOTH places - root for bot, and folder for website
for path in ["scores.json", "world-stats-hub/scores.json"]:
    try:
        with open(path, "w") as f:
            json.dump(output, f, indent=2)
        print("Saved", path)
    except Exception as e:
        print("Skip", path, e)
