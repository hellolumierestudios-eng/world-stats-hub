import json
import sys
import requests
from datetime import datetime
from zoneinfo import ZoneInfo

LAGOS = ZoneInfo("Africa/Lagos")

# TheSportsDB League IDs - these work on GitHub
LEAGUES = {
    "4328": "Premier League",
    "4335": "LaLiga",
    "4331": "Bundesliga",
    "4332": "Serie A",
    "4334": "Ligue 1",
    "4337": "Eredivisie",
    "4344": "Primeira Liga",
    "4480": "UEFA Champions League",
    "4481": "Europa League",
    "4482": "Conference League",
    "4329": "Championship",
    "4330": "Scottish Premiership",
    "4339": "Super Lig",
    "4346": "Belgian Pro League",
    "4347": "Austrian Bundesliga",
}

RATINGS = {
    "Arsenal": 89, "Man City": 88, "Liverpool": 87, "Chelsea": 85,
    "Tottenham Hotspur": 84, "Tottenham": 84, "Man United": 84,
    "Newcastle": 83, "Aston Villa": 83, "Crystal Palace": 80,
    "Bournemouth": 80, "Brighton": 80, "Sunderland": 78,
    "Ipswich Town": 74, "Ipswich": 74,
    "Real Madrid": 90, "Barcelona": 89, "Atletico Madrid": 87,
    "Real Sociedad": 78, "Celta Vigo": 78, "Villarreal": 82,
    "Bayern Munich": 90, "Dortmund": 85, "RB Leipzig": 84,
    "Leverkusen": 86, "Hoffenheim": 79, "Stuttgart": 82,
    "Inter": 88, "AC Milan": 86, "Juventus": 84, "Napoli": 86,
    "PSG": 89, "Marseille": 83, "Monaco": 79, "Lyon": 82, "Lille": 80,
    "Ajax": 82, "PSV": 83, "Feyenoord": 78,
    "Porto": 83, "Benfica": 84, "Sporting CP": 84,
    "Besiktas": 78, "Galatasaray": 84, "Fenerbahce": 83,
    "Omonia Nicosia": 68, "Omonia": 68, "Lillestrom": 68,
    "Levski Sofia": 70, "Hapoel Be'er Sheva": 70,
    "Sturm Graz": 74, "Ferencvaros": 76, "Celje": 72,
    "Celtic": 78, "Rangers": 78,
}

def get_rating(t):
    return RATINGS.get(t, 76)

def calc_prediction(home, away):
    hr = get_rating(home) + 3
    ar = get_rating(away)
    diff = hr - ar
    exp_h = max(0.2, min(4.5, 1.45 + diff * 0.06))
    exp_a = max(0.2, min(4.5, 1.15 - diff * 0.06))
    ph = int(round(exp_h))
    pa = int(round(exp_a))
    winner = "home" if ph > pa else "away" if pa > ph else "draw"
    return {"h": ph, "a": pa, "winner": winner}

def main():
    if len(sys.argv) > 1:
        date_str = sys.argv[1]  # 20261126
    else:
        date_str = datetime.now(LAGOS).strftime("%Y%m%d")

    # TheSportsDB needs YYYY-MM-DD
    api_date = f"{date_str[0:4]}-{date_str[4:6]}-{date_str[6:8]}"
    print(f"=== Fetching for {date_str} / {api_date} ===")

    all_matches = []
    by_league = {}

    # 1. Try TheSportsDB - works on GitHub
    url = f"https://www.thesportsdb.com/api/v1/json/3/eventsday.php?d={api_date}&s=Soccer"
    try:
        r = requests.get(url, timeout=20, headers={"User-Agent": "Mozilla/5.0"})
        print(f"TheSportsDB status: {r.status_code}")
        data = r.json()
        events = data.get("events") or []
        print(f"TheSportsDB returned: {len(events)} events")
        for ev in events:
            league = ev.get("strLeague", "Unknown")
            # Only keep leagues we want
            if league not in LEAGUES.values() and league not in ["English Premier League", "Spanish La Liga", "German Bundesliga", "Italian Serie A", "French Ligue 1", "UEFA Europa League", "UEFA Champions League", "UEFA Conference League"]:
                # Map TheSportsDB names to our names
                mapping = {
                    "English Premier League": "Premier League",
                    "Spanish La Liga": "LaLiga",
                    "German Bundesliga": "Bundesliga",
                    "Italian Serie A": "Serie A",
                    "French Ligue 1": "Ligue 1",
                    "UEFA Europa League": "Europa League",
                    "UEFA Champions League": "UEFA Champions League",
                    "UEFA Conference League": "Conference League",
                    "Dutch Eredivisie": "Eredivisie",
                    "Portuguese Primeira Liga": "Primeira Liga",
                }
                if league in mapping:
                    league = mapping[league]
                else:
                    continue

            home = ev.get("strHomeTeam", "")
            away = ev.get("strAwayTeam", "")
            tm = ev.get("strTime", "TBD") or "TBD"
            # Convert to Lagos time display - TheSportsDB gives UTC time
            status = "scheduled"
            hs = ev.get("intHomeScore")
            aws = ev.get("intAwayScore")
            if hs is not None and hs != "":
                status = "finished"
            pred = calc_prediction(home, away)
            all_matches.append({
                "home": home, "away": away,
                "date": date_str, "time": tm,
                "status": status,
                "homeScore": int(hs) if hs not in (None, "") else None,
                "awayScore": int(aws) if aws not in (None, "") else None,
                "predH": pred["h"], "predA": pred["a"],
                "winner": pred["winner"],
                "league": league
            })
            by_league[league] = by_league.get(league, 0) + 1
    except Exception as e:
        print(f"TheSportsDB error: {e}")

    print("=== DONE ===")
    print(by_league)
    print(f"Total matches: {len(all_matches)}")

    # CRITICAL FIX: Don't overwrite with 0 matches!
    # If API returns 0, keep old scores.json so site doesn't go blank
    if len(all_matches) == 0:
        print("WARNING: 0 matches found - NOT overwriting scores.json, keeping old file")
        return

    with open("scores.json", "w", encoding="utf-8") as f:
        json.dump({
            "generated": datetime.now(LAGOS).isoformat(),
            "date": date_str,
            "total": len(all_matches),
            "matches": all_matches
        }, f, ensure_ascii=False, indent=2)
    print("Saved scores.json")

if __name__ == "__main__":
    main()
