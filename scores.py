import json
import sys
import csv
import io
import hashlib
import requests
from datetime import datetime
from zoneinfo import ZoneInfo

LAGOS = ZoneInfo("Africa/Lagos")

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

# EXPANDED RATINGS - 0-100, based on UEFA coefficient + squad value
RATINGS = {
    # Premier League
    "Arsenal": 91, "Man City": 90, "Manchester City": 90, "Liverpool": 89, "Chelsea": 86,
    "Tottenham Hotspur": 84, "Tottenham": 84, "Man United": 84, "Manchester United": 84,
    "Newcastle United": 84, "Newcastle": 84, "Aston Villa": 84, "Crystal Palace": 81,
    "Bournemouth": 81, "Brighton": 82, "Brighton & Hove Albion": 82, "Sunderland": 79,
    "Everton": 79, "Brentford": 79, "Fulham": 80, "Leeds United": 77, "West Ham": 77,
    "Nottingham Forest": 80, "Wolves": 76, "Burnley": 74,
    # LaLiga
    "Real Madrid": 92, "Barcelona": 91, "Atletico Madrid": 88, "Atletico": 88,
    "Real Sociedad": 80, "Celta Vigo": 80, "Celta": 80, "Villarreal": 84,
    "Real Betis": 82, "Sevilla": 79, "Athletic Bilbao": 82, "Athletic Club": 82,
    "Valencia": 78, "Getafe": 76, "Osasuna": 76, "Rayo Vallecano": 78,
    # Bundesliga
    "Bayern Munich": 92, "Bayern": 92, "Dortmund": 86, "Borussia Dortmund": 86,
    "RB Leipzig": 85, "Leverkusen": 87, "Bayer Leverkusen": 87, "Hoffenheim": 80,
    "Stuttgart": 83, "Eintracht Frankfurt": 82, "Frankfurt": 82, "Freiburg": 81,
    "Wolfsburg": 79, "Mönchengladbach": 78, "Borussia M'gladbach": 78,
    # Serie A
    "Inter": 89, "Inter Milan": 89, "AC Milan": 87, "Milan": 87, "Juventus": 85,
    "Napoli": 87, "Roma": 84, "AS Roma": 84, "Atalanta": 84, "Lazio": 82,
    "Fiorentina": 82, "Bologna": 81, "Torino": 78, "Como": 79,
    # Ligue 1
    "PSG": 91, "Paris Saint-Germain": 91, "Marseille": 84, "Olympique Marseille": 84,
    "Monaco": 81, "AS Monaco": 81, "Lyon": 83, "Olympique Lyon": 83, "Lille": 82,
    "Lens": 81, "Nice": 80, "Rennes": 78,
    # Eredivisie / Primeira
    "Ajax": 83, "PSV": 84, "Feyenoord": 80, "AZ Alkmaar": 79, "Twente": 79, "FC Twente": 79,
    "Porto": 84, "FC Porto": 84, "Benfica": 85, "Sporting CP": 85, "Sporting": 85, "Braga": 81,
    # Europa / Conference - THIS WAS MISSING BEFORE
    "Kairat Almaty": 68, "Kairat": 68, "Mjallby": 71, "Mjällby": 71,
    "Thun": 71, "FC Thun": 71, "U Craiova": 72, "Universitatea Craiova": 72,
    "U. Craiova": 72, "Sturm Graz": 76, "Ferencvaros": 77, "Ferencváros": 77,
    "Celje": 73, "NK Celje": 73, "Omonia Nicosia": 70, "Omonia": 70,
    "Lillestrom": 70, "Lillestrøm": 70, "Levski Sofia": 71, "Levski": 71,
    "Hapoel Be'er Sheva": 71, "Besiktas": 79, "Galatasaray": 85, "Fenerbahce": 84,
    "Celtic": 80, "Rangers": 79, "Shakhtar Donetsk": 80, "Shakhtar": 80,
    "Dynamo Kyiv": 78, "Sparta Prague": 78, "Slavia Prague": 79,
    "PAOK": 78, "AEK Athens": 78, "Olympiacos": 82, "Panathinaikos": 80,
    "Basel": 77, "Young Boys": 77, "Anderlecht": 78, "Gent": 77, "Genk": 79,
    "Legia Warsaw": 75, "Lech Poznan": 74, "Rijeka": 73, "Dinamo Zagreb": 79,
    "Samsunspor": 74, "Trabzonspor": 78, "Go Ahead Eagles": 74, "Utrecht": 76,
    "Drita": 66, "Noah": 66, "Hamrun Spartans": 64, "Hamrun": 64,
    "Lincoln Red Imps": 63, "Shelbourne": 65, "Shamrock Rovers": 66,
    "Breidablik": 65, "Zrinjski Mostar": 68, "Zrinjski": 68, "KuPS": 68,
    "AEK Larnaca": 70, "Omonia 29M": 66, "Crystal Palace": 81,
}

def get_rating(t):
    return RATINGS.get(t, 72)

def calc_prediction(home, away, date_str=""):
    hr = get_rating(home) + 4  # Home advantage
    ar = get_rating(away)
    diff = hr - ar

    # Expected goals - more realistic range
    exp_h = 1.35 + diff * 0.07
    exp_a = 1.05 - diff * 0.07
    exp_h = max(0.15, min(4.2, exp_h))
    exp_a = max(0.15, min(3.8, exp_a))

    # Deterministic variance from team names + date
    # Same fixture always gives same prediction, but different fixtures vary
    seed_str = f"{home}-{away}-{date_str}"
    h = int(hashlib.md5(seed_str.encode()).hexdigest()[:8], 16)
    # Add -0.5 to +0.5 variance
    var_h = ((h % 100) / 100 - 0.5)
    var_a = (((h // 100) % 100) / 100 - 0.5)

    ph = int(round(exp_h + var_h))
    pa = int(round(exp_a + var_a))
    ph = max(0, min(5, ph))
    pa = max(0, min(4, pa))

    # Avoid too many 2-1: if both 1, sometimes make 0-0 or 1-1
    if ph == 1 and pa == 1 and (h % 3 == 0):
        ph = 0; pa = 0

    winner = "home" if ph > pa else "away" if pa > ph else "draw"
    # Confidence based on diff
    conf = min(92, max(48, 52 + abs(diff) * 1.2))
    return {"h": ph, "a": pa, "winner": winner, "conf": int(conf)}

def main():
    if len(sys.argv) > 1:
        date_str = sys.argv[1]
    else:
        date_str = datetime.now(LAGOS).strftime("%Y%m%d")

    target = f"{date_str[6:8]}/{date_str[4:6]}/{date_str[0:4]}"
    target2 = f"{date_str[0:4]}-{date_str[4:6]}-{date_str[6:8]}"
    print(f"=== Fetching for {date_str} = {target} ===")
    all_matches = []
    by_league = {}

    for slug, league_name in LEAGUES.items():
        urls = [f"https://fixturedownload.com/download/{slug}-2026-GMTStandardTime.csv",
                f"https://fixturedownload.com/download/{slug}-2025-GMTStandardTime.csv"]
        csv_text = None
        for u in urls:
            try:
                r = requests.get(u, timeout=20, headers={"User-Agent": "Mozilla/5.0"})
                print(f"{league_name}: {r.status_code}")
                if r.status_code == 200 and len(r.text) > 100:
                    csv_text = r.text; break
            except Exception as e:
                print(f"{league_name} error: {e}"); continue
        if not csv_text: continue
        try:
            reader = csv.DictReader(io.StringIO(csv_text))
            for row in reader:
                d = (row.get("Date") or "").strip()
                date_part = d.split(" ")[0]
                time_part = d.split(" ")[1] if " " in d else "TBD"
                if date_part not in (target, target2, target.replace("/", "-")): continue
                home = (row.get("Home Team") or "").strip()
                away = (row.get("Away Team") or "").strip()
                if not home or not away: continue
                result = (row.get("Result") or "").strip()
                hs = None; aws = None; status = "scheduled"
                if result and "-" in result:
                    try:
                        hs, aws = result.split("-"); hs = int(hs.strip()); aws = int(aws.strip()); status = "finished"
                    except: pass
                # Convert GMT time to Lagos +1h
                lagos_time = time_part
                if ":" in time_part:
                    try:
                        hh, mm = time_part.split(":"); hh = (int(hh) + 1) % 24
                        lagos_time = f"{hh:02d}:{mm} Lagos"
                    except: pass
                pred = calc_prediction(home, away, date_str)
                all_matches.append({
                    "home": home, "away": away, "date": date_str, "time": lagos_time,
                    "status": status, "homeScore": hs, "awayScore": aws,
                    "predH": pred["h"], "predA": pred["a"], "winner": pred["winner"], "conf": pred["conf"],
                    "league": league_name
                })
                by_league[league_name] = by_league.get(league_name, 0) + 1
        except Exception as e:
            print(f"CSV parse error {league_name}: {e}")

    print(by_league); print(f"Total matches: {len(all_matches)}")
    if len(all_matches) == 0:
        print("WARNING: 0 matches - NOT overwriting"); return
    with open("scores.json", "w", encoding="utf-8") as f:
        json.dump({"generated": datetime.now(LAGOS).isoformat(), "date": date_str, "total": len(all_matches), "matches": all_matches}, f, ensure_ascii=False, indent=2)
    print("Saved scores.json")

if __name__ == "__main__":
    main()
