import json, requests
from datetime import date, timedelta

# ESPN leagues - free, no key needed
LEAGUES = {
    "eng.1": "Premier League",
    "esp.1": "La Liga",
    "ita.1": "Serie A",
    "ger.1": "Bundesliga",
    "fra.1": "Ligue 1",
    "ned.1": "Eredivisie",
    "por.1": "Primeira Liga",
    "eng.2": "Championship",
    "uefa.champions": "Champions League",
    "uefa.europa": "Europa League",
    "uefa.europa.conf": "Conference League",
}

matches = []
today = date.today()

for offset in range(-1, 8):  # yesterday to +7 days
    d = today + timedelta(days=offset)
    datestr = d.strftime("%Y%m%d")
    for slug, league_name in LEAGUES.items():
        try:
            url = f"https://site.api.espn.com/apis/site/v2/sports/soccer/{slug}/scoreboard?dates={datestr}"
            r = requests.get(url, timeout=20)
            data = r.json()
            for ev in data.get("events", []):
                comp = ev.get("competitions", [{}])[0]
                teams = comp.get("competitors", [])
                if len(teams) < 2:
                    continue
                home = next((t for t in teams if t.get("homeAway") == "home"), teams[0])
                away = next((t for t in teams if t.get("homeAway") == "away"), teams[1])
                hs = home.get("score")
                as_ = away.get("score")
                try: hs = int(hs) if hs is not None else None
                except: hs = None
                try: as_ = int(as_) if as_ is not None else None
                except: as_ = None
                status = ev.get("status", {})
                st = status.get("type", {})
                m = {
                    "league": league_name,
                    "home": home.get("team", {}).get("displayName", "?"),
                    "away": away.get("team", {}).get("displayName", "?"),
                    "home_team": home.get("team", {}).get("displayName", "?"),
                    "away_team": away.get("team", {}).get("displayName", "?"),
                    "homeScore": hs, "awayScore": as_,
                    "home_score": hs, "away_score": as_,
                    "score_home": hs, "score_away": as_,
                    "status": st.get("description", ""),
                    "state": st.get("state", ""),
                    "minute": status.get("displayClock", ""),
                    "date": d.isoformat(),
                    "time": ev.get("date", "")[11:16] if ev.get("date") else "",
                    "datetime": ev.get("date", ""),
                }
                matches.append(m)
            print("OK", slug, datestr, len(data.get("events", [])))
        except Exception as e:
            print("FAIL", slug, datestr, e)

out = {"updated": today.isoformat(), "matches": matches}
with open("scores.json", "w") as f:
    json.dump(out, f, indent=2)
print(f"Saved: {len(matches)} matches")
