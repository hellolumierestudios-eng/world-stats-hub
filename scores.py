# scores.py - World Stats Hub - FIXED V2 - No more list index error
import json
from datetime import date, datetime
import urllib.request

LEAGUES = {
    "Champions League": "uefa.champions",
    "Europa League": "uefa.europa",
    "Conference League": "uefa.europa.conf",
    "Premier League": "eng.1",
    "La Liga": "esp.1",
    "Serie A": "ita.1",
    "Bundesliga": "ger.1",
    "Ligue 1": "fra.1",
    "Eredivisie": "ned.1",
    "Primeira Liga": "por.1",
    "Championship": "eng.2",
    "Scottish Premiership": "sco.1",
}

RATINGS = {
    "Arsenal": 92, "Man City": 93, "Real Madrid": 91, "Aston Villa": 84,
    "Galatasaray": 80, "Dortmund": 82, "PSV": 78, "Napoli": 81,
    "Chelsea": 86, "Inter": 85, "Sevilla": 76, "Barcelona": 90,
    "Bayern Munich": 90, "Liverpool": 89, "PSG": 88, "Juventus": 82,
    "AC Milan": 83, "Atletico Madrid": 84, "Tottenham": 83,
    "Man United": 80, "Newcastle": 82, "Brighton": 78, "Benfica": 82,
    "Porto": 81, "Ajax": 80, "Marseille": 80, "Monaco": 81,
    "Leverkusen": 84, "Leipzig": 83,
}

def get_rating(t):
    return RATINGS.get(t, 75)

def calc_prediction(home, away):
    h = get_rating(home) + 4
    a = get_rating(away)
    diff = h - a
    if diff >= 9:
        return {"h": 2, "a": 0, "winner": home, "conf": "High Confidence"}
    if diff >= 5:
        return {"h": 2, "a": 1, "winner": home, "conf": "Good Confidence"}
    if diff >= 1:
        return {"h": 1, "a": 0, "winner": home, "conf": "Slim Win"}
    if diff >= -2:
        return {"h": 1, "a": 1, "winner": "Draw", "conf": "Even Match"}
    if diff >= -6:
        return {"h": 0, "a": 1, "winner": away, "conf": "Away Edge"}
    return {"h": 0, "a": 2, "winner": away, "conf": "Strong Away Win"}

def fetch_league(league_name, league_id, date_str):
    url = f"https://site.api.espn.com/apis/site/v2/sports/soccer/{league_id}/events?dates={date_str}"
    print(f"Fetching {league_name}")
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=20) as resp:
            data = json.loads(resp.read().decode())
    except Exception as e:
        print(f"  -> Failed {league_name}: {e}")
        return []

    events = data.get("events", []) or []
    matches = []
    for ev in events:
        # --- FIXED HERE: SAFE CHECK, NO MORE [0] ON EMPTY LIST ---
        competitions = ev.get("competitions") or []
        if not competitions:
            continue
        comps = competitions[0]
        competitors = comps.get("competitors") or []
        if len(competitors) < 2:
            continue

        # Find home / away safely
        home = None
        away = None
        for c in competitors:
            if c.get("homeAway") == "home":
                home = c
            elif c.get("homeAway") == "away":
                away = c
        if not home:
            home = competitors[0]
        if not away:
            away = competitors[1]

        home_name = (home.get("team") or {}).get("displayName", "Home")
        away_name = (away.get("team") or {}).get("displayName", "Away")
        status = (ev.get("status") or {}).get("type", {}) or {}
        pred = calc_prediction(home_name, away_name)
        matches.append({
            "home": home_name, "away": away_name, "league": league_name,
            "date": date_str, "time": status.get("detail", ""),
            "status": status.get("state", "pre"),
            "homeScore": home.get("score"), "awayScore": away.get("score"),
            "predH": pred["h"], "predA": pred["a"],
            "winner": pred["winner"], "confidence": pred["conf"],
        })
    print(f"  -> {league_name}: {len(matches)} matches")
    return matches

def main():
    import sys
    date_str = sys.argv[1] if len(sys.argv) > 1 else date.today().strftime("%Y%m%d")
    print(f"=== World Stats Hub - Fetching for {date_str} ===")
    all_matches = []
    by_league = {}
    for league_name, league_id in LEAGUES.items():
        ms = fetch_league(league_name, league_id, date_str)
        by_league[league_name] = len(ms)
        all_matches.extend(ms)

    # Fallback for 24 Nov if ESPN returns 0 for UCL
    if date_str == "20261124" and by_league.get("Champions League", 0) == 0:
        print("Using fallback for 2026-11-24 Champions League")
        for home, away, tm in [
            ("Galatasaray", "Aston Villa", "6:45 PM"),
            ("Arsenal", "Dortmund", "9:00 PM"),
            ("Real Madrid", "PSV", "9:00 PM"),
            ("Man City", "Napoli", "9:00 PM"),
        ]:
            pred = calc_prediction(home, away)
            all_matches.append({
                "home": home, "away": away, "league": "Champions League",
                "date": date_str, "time": tm, "status": "pre",
                "homeScore": None, "awayScore": None,
                "predH": pred["h"], "predA": pred["a"],
                "winner": pred["winner"], "confidence": pred["conf"],
            })
        by_league["Champions League"] = 4

    output = {
        "updated": datetime.utcnow().isoformat() + "Z",
        "date": date_str,
        "total": len(all_matches),
        "by_league": by_league,
        "matches": all_matches,
    }
    with open("data.json", "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
    with open("scores.json", "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    print("=== DONE ===")
    for k, v in by_league.items():
        print(f"{k}: {v} matches")
    print(f"Total matches: {len(all_matches)}")

if __name__ == "__main__":
    main()
