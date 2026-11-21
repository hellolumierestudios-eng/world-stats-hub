import requests, json, datetime, hashlib
from predict import predict

# ESPN - No API key needed
LEAGUES = [
    ("eng.1", "Premier League"),
    ("esp.1", "La Liga"),
    ("ita.1", "Serie A"),
    ("ger.1", "Bundesliga"),
    ("fra.1", "Ligue 1"),
    ("ned.1", "Eredivisie"),
    ("por.1", "Primeira Liga"),
    ("eng.2", "Championship"),
]

today = datetime.date.today()
date_str = today.strftime("%Y%m%d")
now_str = datetime.datetime.now().strftime("%d %b %Y, %I:%M %p")

all_matches = []

def team_strength(team_name):
    # Gives each team a different strength 1.0 to 2.0
    # Same team always gets same strength, different teams get different
    h = int(hashlib.md5(team_name.encode()).hexdigest()[:4], 16)
    return 1.0 + (h % 100) / 100.0

for league_id, league_name in LEAGUES:
    url = f"https://site.api.espn.com/apis/site/v2/sports/soccer/{league_id}/scoreboard?dates={date_str}"
    try:
        r = requests.get(url, timeout=15)
        data = r.json()
        events = data.get("events", [])
        print(f"{league_name}: {len(events)} matches")
        for ev in events:
            comp = ev.get("competitions", [{}])[0]
            competitors = comp.get("competitors", [])
            if len(competitors) < 2:
                continue
            home = next((c for c in competitors if c.get("homeAway") == "home"), competitors[0])
            away = next((c for c in competitors if c.get("homeAway") == "away"), competitors[1])
            status = ev.get("status", {})
            display = status.get("type", {}).get("shortDetail", "")
            state = status.get("type", {}).get("state", "")

            home_name = home.get("team", {}).get("displayName", "Home")
            away_name = away.get("team", {}).get("displayName", "Away")

            # NEW: Different prediction for each match
            home_strength = team_strength(home_name) + 0.3  # Home advantage
            away_strength = team_strength(away_name)
            try:
                prediction_text = predict(home_name, away_name, home_strength, away_strength)
            except Exception as e:
                prediction_text = "Prediction coming soon"
                print(f"Predict error: {e}")

            all_matches.append({
                "league": league_name,
                "home": home_name,
                "away": away_name,
                "status": display,
                "state": state,
                "date": today.isoformat(),
                "time": display,
                "prediction": prediction_text,
                "home_strength": round(home_strength, 2),
                "away_strength": round(away_strength, 2)
            })
    except Exception as e:
        print(f"{league_name} error: {e}")

print(f"Total matches: {len(all_matches)}")

# Save for WEBSITE
with open("scores.json", "w") as f:
    json.dump({"matches": all_matches, "updated": now_str}, f, indent=2)

print(f"Saved scores.json with {len(all_matches)} matches")
