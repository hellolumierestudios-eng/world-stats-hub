import json
import sys
import time
import requests
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

# Use Lagos time - so date is correct in Nigeria
LAGOS = ZoneInfo("Africa/Lagos")

LEAGUES = {
    "eng.1": "Premier League",
    "esp.1": "LaLiga",
    "ger.1": "Bundesliga",
    "ita.1": "Serie A",
    "fra.1": "Ligue 1",
    "ned.1": "Eredivisie",
    "por.1": "Primeira Liga",
    "tur.1": "Super Lig",
    "uefa.champions": "UEFA Champions League",
    "uefa.europa": "Europa League",
    "uefa.europa.conf": "Conference League",
    "uefa.nations": "Nations League",
    "conmebol.libertadores": "Copa Libertadores",
    "mex.1": "Liga MX",
    "usa.1": "MLS",
    "bra.1": "Brasileirao",
    "arg.1": "Liga Argentina",
    "eng.2": "Championship",
    "esp.2": "LaLiga 2",
    "ger.2": "2. Bundesliga",
    "ita.2": "Serie B",
    "fra.2": "Ligue 2",
    "sco.1": "Scottish Premiership",
    "bel.1": "Belgian Pro League",
    "aut.1": "Austrian Bundesliga",
    "sui.1": "Swiss Super League",
    "gre.1": "Greek Super League",
    "den.1": "Danish Superliga",
    "swe.1": "Allsvenskan",
    "nor.1": "Eliteserien",
}

# Base ratings - used only if ESPN has no data
# If team not here, we use 76 as default, not 75
RATINGS = {
    "Arsenal": 89, "Man City": 88, "Liverpool": 87, "Chelsea": 85,
    "Tottenham": 84, "Man United": 84, "Newcastle": 83, "Aston Villa": 83,
    "Brighton": 80, "West Ham": 79, "Brentford": 79, "Fulham": 78,
    "Crystal Palace": 80, "Bournemouth": 80, "Nottingham Forest": 79,
    "Everton": 78, "Wolves": 77, "Leeds": 77, "Sunderland": 78,
    "Ipswich": 74, "Burnley": 74, "Sheffield Utd": 75,
    "Real Madrid": 90, "Barcelona": 89, "Atletico Madrid": 87, "Sevilla": 80,
    "Real Sociedad": 78, "Villarreal": 82, "Athletic Club": 81, "Real Betis": 80,
    "Celta Vigo": 78, "Valencia": 78, "Getafe": 76,
    "Bayern Munich": 90, "Dortmund": 85, "RB Leipzig": 84, "Leverkusen": 86,
    "Stuttgart": 82, "Hoffenheim": 79, "Frankfurt": 81, "Wolfsburg": 78,
    "Inter": 88, "AC Milan": 86, "Juventus": 84, "Napoli": 86, "Roma": 83,
    "Atalanta": 82, "Lazio": 81, "Fiorentina": 80, "Bologna": 79,
    "PSG": 89, "Marseille": 83, "Monaco": 79, "Lyon": 82, "Lille": 80,
    "Nice": 79, "Rennes": 78, "Lens": 79,
    "Ajax": 82, "PSV": 83, "Feyenoord": 78, "AZ Alkmaar": 78,
    "Porto": 83, "Benfica": 84, "Sporting CP": 84, "Braga": 80,
    "Besiktas": 78, "Galatasaray": 84, "Fenerbahce": 83, "Trabzonspor": 78,
    "Omonia": 68, "Lillestrom": 68, "Levski Sofia": 70, "Hapoel Be'er Sheva": 70,
    "Sturm Graz": 74, "Ferencvaros": 76, "Celje": 72, "Dinamo Zagreb": 76,
    "Celtic": 78, "Rangers": 78, "Anderlecht": 77, "Gent": 76,
    "Club Brugge": 80, "Genk": 78, "Salzburg": 77, "Young Boys": 76,
    "Olympiacos": 78, "PAOK": 77, "Panathinaikos": 77, "AEK Athens": 77,
    "Midtjylland": 75, "FC Copenhagen": 77, "Malmo": 74, "Djurgarden": 74,
    "Bodo/Glimt": 78, "Molde": 74, "Rosenborg": 74,
}

def get_rating(team):
    return RATINGS.get(team, 76)

def calc_prediction(home, away):
    # Simple model: rating diff + home advantage
    hr = get_rating(home) + 3  # home advantage
    ar = get_rating(away)
    diff = hr - ar
    # Base expected goals
    exp_h = 1.45 + diff * 0.06
    exp_a = 1.15 - diff * 0.06
    exp_h = max(0.2, min(4.5, exp_h))
    exp_a = max(0.2, min(4.5, exp_a))
    pred_h = int(round(exp_h))
    pred_a = int(round(exp_a))
    if pred_h > pred_a:
        winner = "home"
    elif pred_a > pred_h:
        winner = "away"
    else:
        winner = "draw"
    return {"h": pred_h, "a": pred_a, "winner": winner}

def get_matches_for_date(date_str):
    all_matches = []
    by_league = {}
    for slug, league_name in LEAGUES.items():
        url = f"https://site.api.espn.com/apis/site/v2/sports/soccer/{slug}/scoreboard?dates={date_str}"
        try:
            r = requests.get(url, timeout=15, headers={"User-Agent": "Mozilla/5.0"})
            if r.status_code != 200:
                continue
            data = r.json()
            events = data.get("events", [])
            count = 0
            for ev in events:
                comps = ev.get("competitions", [{}])[0]
                competitors = comps.get("competitors", [])
                if len(competitors) < 2:
                    continue
                home = next((c for c in competitors if c.get("homeAway") == "home"), competitors[0])
                away = next((c for c in competitors if c.get("homeAway") == "away"), competitors[1])
                home_name = home.get("team", {}).get("displayName", "Unknown")
                away_name = away.get("team", {}).get("displayName", "Unknown")
                status = ev.get("status", {}).get("type", {}).get("state", "pre")
                # Time in Lagos
                dt_str = ev.get("date", "")
                try:
                    dt = datetime.fromisoformat(dt_str.replace("Z", "+00:00")).astimezone(LAGOS)
                    tm = dt.strftime("%I:%M %p").lstrip("0")
                except:
                    tm = "TBD"
                home_score = None
                away_score = None
                if home.get("score") is not None:
                    try: home_score = int(float(home["score"]))
                    except: pass
                if away.get("score") is not None:
                    try: away_score = int(float(away["score"]))
                    except: pass
                pred = calc_prediction(home_name, away_name)
                all_matches.append({
                    "home": home_name, "away": away_name,
                    "date": date_str, "time": tm,
                    "status": status,
                    "homeScore": home_score, "awayScore": away_score,
                    "predH": pred["h"], "predA": pred["a"],
                    "winner": pred["winner"],
                    "league": league_name
                })
                count += 1
            if count > 0:
                by_league[league_name] = count
            time.sleep(0.1)
        except Exception as e:
            print(f"Error {league_name}: {e}")
            continue
    return all_matches, by_league

def main():
    # If no date given, use TODAY in Lagos - no manual date needed
    if len(sys.argv) > 1:
        date_str = sys.argv[1]
    else:
        date_str = datetime.now(LAGOS).strftime("%Y%m%d")

    print(f"Fetching for date: {date_str}")
    all_matches, by_league = get_matches_for_date(date_str)

    # Also fetch tomorrow and yesterday so your site can show all 3 days
    # if your index.html needs it
    print(f"Found {len(all_matches)} matches")
    print(by_league)

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
