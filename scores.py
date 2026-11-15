import requests, json, datetime

# ESPN - No API key needed, never suspends
LEAGUES = [
    # CLUB LEAGUES
    ("eng.1", "Premier League"),
    ("esp.1", "La Liga"),
    ("ita.1", "Serie A"),
    ("ger.1", "Bundesliga"),
    ("fra.1", "Ligue 1"),
    ("ned.1", "Eredivisie"),
    ("por.1", "Primeira Liga"),
    ("eng.2", "Championship"),
    ("uefa.champions", "Champions League"),
    ("uefa.europa", "Europa League"),
    # INTERNATIONAL - NATIONAL TEAMS
    ("fifa.worldq.uefa", "World Cup Qualifiers - Europe"),
    ("uefa.nations", "UEFA Nations League"),
    ("fifa.friendly", "International Friendlies"),
]

today = datetime.date.today()
date_str = today.strftime("%Y%m%d")
print(f"Date used: {today}")

# NEW: Create updated time for the site
now_str = datetime.datetime.now().strftime("%d %b %Y, %I:%M %p")
print(f"Updated: {now_str}")

all_matches = []

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
            state = status.get("type", {}).get("state", "")
            display = status.get("type", {}).get("shortDetail", "")

            home_score = home.get("score")
            away_score = away.get("score")
            try: home_score = int(home_score) if home_score is not None else None
            except: pass
            try: away_score = int(away_score) if away_score is not None else None
            except: pass

            all_matches.append({
                "league": league_name,
                "home": home.get("team", {}).get("displayName", "Home"),
                "away": away.get("team", {}).get("displayName", "Away"),
                "home_score": home_score,
                "away_score": away_score,
                "status": display,
                "state": state,
                "date": today.isoformat(),
                "time": display
            })
    except Exception as e:
        print(f"{league_name} error: {e}")

print(f"Total matches: {len(all_matches)}")

# FIXED: Now saves updated time too
with open("scores.json", "w") as f:
    json.dump({"matches": all_matches, "updated": now_str}, f, indent=2)

print(f"Saved scores.json with {len(all_matches)} matches")
