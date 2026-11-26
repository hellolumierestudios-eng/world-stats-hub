import json
import sys
import csv
import io
import requests
from datetime import datetime
from zoneinfo import ZoneInfo

LAGOS = ZoneInfo("Africa/Lagos")

# FixtureDownload - CSV files, no API key, never 403 on GitHub
# Format: league_code -> (Display Name, fixturedownload slug)
LEAGUES = {
    "epl": "Premier League",
    "la-liga": "LaLiga",
    "bundesliga": "Bundesliga",
    "serie-a": "Serie A",
    "ligue-1": "Ligue 1",
    "eredivisie": "Eredivisie",
    "primeira-liga": "Primeira Liga",
    "champions-league": "UEFA Champions League",
    "europa-league": "Europa League",
    "conference-league": "Conference League",
    "championship": "Championship",
    "scottish-premiership": "Scottish Premiership",
}

RATINGS = {
    "Arsenal": 89, "Man City": 88, "Manchester City": 88, "Liverpool": 87, "Chelsea": 85,
    "Tottenham Hotspur": 84, "Tottenham": 84, "Man United": 84, "Manchester United": 84,
    "Newcastle United": 83, "Newcastle": 83, "Aston Villa": 83, "Crystal Palace": 80,
    "Bournemouth": 80, "Brighton": 80, "Sunderland": 78, "Everton": 78,
    "Real Madrid": 90, "Barcelona": 89, "Atletico Madrid": 87, "Atletico": 87,
    "Real Sociedad": 78, "Celta Vigo": 78, "Celta": 78, "Villarreal": 82,
    "Bayern Munich": 90, "Bayern": 90, "Dortmund": 85, "Borussia Dortmund": 85,
    "RB Leipzig": 84, "Leverkusen": 86, "Bayer Leverkusen": 86, "Hoffenheim": 79,
    "Inter": 88, "Inter Milan": 88, "AC Milan": 86, "Milan": 86, "Juventus": 84,
    "Napoli": 86, "Roma": 83, "AS Roma": 83, "Atalanta": 82,
    "PSG": 89, "Paris Saint-Germain": 89, "Marseille": 83, "Olympique Marseille": 83,
    "Monaco": 79, "AS Monaco": 79, "Lyon": 82, "Olympique Lyon": 82, "Lille": 80,
    "Ajax": 82, "PSV": 83, "Feyenoord": 78, "AZ Alkmaar": 78,
    "Porto": 83, "FC Porto": 83, "Benfica": 84, "Sporting CP": 84, "Sporting": 84,
    "Besiktas": 78, "Galatasaray": 84, "Fenerbahce": 83,
    "Omonia Nicosia": 68, "Omonia": 68, "Lillestrom": 68, "Lillestrøm": 68,
    "Levski Sofia": 70, "Levski": 70, "Hapoel Be'er Sheva": 70,
    "Sturm Graz": 74, "Ferencvaros": 76, "Ferencváros": 76, "Celje": 72,
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
        date_str = sys.argv[1]
    else:
        date_str = datetime.now(LAGOS).strftime("%Y%m%d")

    # Convert 20261126 -> 26/11/2026 for CSV matching
    target = f"{date_str[6:8]}/{date_str[4:6]}/{date_str[0:4]}"
    # Also YYYY-MM-DD format
    target2 = f"{date_str[0:4]}-{date_str[4:6]}-{date_str[6:8]}"
    print(f"=== Fetching for {date_str} = {target} / {target2} ===")

    all_matches = []
    by_league = {}

    for slug, league_name in LEAGUES.items():
        # FixtureDownload CSV - no key needed
        url = f"https://fixturedownload.com/download/{slug}-2026-GMTStandardTime.csv"
        # Try 2025 season if 2026 fails
        urls = [url, f"https://fixturedownload.com/download/{slug}-2025-GMTStandardTime.csv"]
        csv_text = None
        for u in urls:
            try:
                r = requests.get(u, timeout=20, headers={"User-Agent": "Mozilla/5.0"})
                print(f"{league_name}: {u} -> {r.status_code}")
                if r.status_code == 200 and len(r.text) > 100:
                    csv_text = r.text
                    break
            except Exception as e:
                print(f"{league_name} error: {e}")
                continue
        if not csv_text:
            continue

        try:
            reader = csv.DictReader(io.StringIO(csv_text))
            # Print first row keys once for debug
            for row in reader:
                # CSV columns: Round, Date, Location, Home Team, Away Team, Result
                d = (row.get("Date") or "").strip()
                # Date can be 26/11/2026 20:00 or 2026-11-26
                date_part = d.split(" ")[0]
                time_part = d.split(" ")[1] if " " in d else "TBD"
                if date_part not in (target, target2, target.replace("/", "-")):
                    continue
                home = (row.get("Home Team") or "").strip()
                away = (row.get("Away Team") or "").strip()
                if not home or not away:
                    continue
                result = (row.get("Result") or "").strip()
                hs = None
                aws = None
                status = "scheduled"
                if result and "-" in result:
                    try:
                        hs, aws = result.split("-")
                        hs = int(hs.strip()); aws = int(aws.strip())
                        status = "finished"
                    except:
                        pass
                pred = calc_prediction(home, away)
                all_matches.append({
                    "home": home, "away": away,
                    "date": date_str, "time": time_part,
                    "status": status,
                    "homeScore": hs, "awayScore": aws,
                    "predH": pred["h"], "predA": pred["a"],
                    "winner": pred["winner"],
                    "league": league_name
                })
                by_league[league_name] = by_league.get(league_name, 0) + 1
        except Exception as e:
            print(f"CSV parse error {league_name}: {e}")

    print("=== DONE ===")
    print(by_league)
    print(f"Total matches: {len(all_matches)}")

    if len(all_matches) == 0:
        print("WARNING: 0 matches - NOT overwriting scores.json")
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
