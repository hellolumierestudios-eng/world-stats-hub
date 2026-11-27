import json, sys, csv, io, hashlib, requests
from datetime import datetime
from zoneinfo import ZoneInfo
LAGOS = ZoneInfo("Africa/Lagos")

LEAGUES = {
    "epl": "Premier League", "la-liga": "LaLiga", "bundesliga": "Bundesliga",
    "serie-a": "Serie A", "ligue-1": "Ligue 1", "eredivisie": "Eredivisie",
    "primeira-liga": "Primeira Liga", "champions-league": "UEFA Champions League",
    "europa-league": "Europa League", "conference-league": "Conference League",
    "championship": "Championship", "scottish-premiership": "Scottish Premiership",
}

RATINGS = {
    "Arsenal":91,"Man City":90,"Manchester City":90,"Liverpool":89,"Chelsea":86,
    "Tottenham Hotspur":84,"Tottenham":84,"Man United":84,"Manchester United":84,
    "Newcastle United":84,"Newcastle":84,"Aston Villa":84,"Crystal Palace":81,
    "Bournemouth":81,"Brighton":82,"Brighton & Hove Albion":82,"Sunderland":79,
    "Everton":79,"Brentford":79,"Fulham":80,"Leeds United":77,"West Ham":77,
    "Nottingham Forest":80,"Nott'm Forest":80,"Wolves":76,"Burnley":74,
    "Southampton":78,"Middlesbrough":76,"Leicester City":79,"Leicester":79,"Ipswich Town":79,"Ipswich":79,
    "Coventry City":77,"Coventry":77,"West Brom":76,"West Bromwich Albion":76,"Stoke City":75,"Stoke":75,
    "Sheffield United":76,"Sheffield Utd":76,"Sheffield Wednesday":73,"Norwich City":74,"Norwich":74,
    "Watford":74,"Swansea City":73,"Swansea":73,"Millwall":74,"QPR":73,"Queens Park Rangers":73,
    "Hull City":74,"Hull":74,"Blackburn Rovers":74,"Blackburn":74,"Derby County":73,"Derby":73,
    "Preston North End":73,"Preston":73,"Bristol City":74,"Charlton Athletic":72,"Charlton":72,
    "Oxford United":71,"Oxford":71,"Portsmouth":71,"Wrexham":73,"Birmingham City":75,"Birmingham":75,
    "Real Madrid":92,"Barcelona":91,"Atletico Madrid":88,"Atletico":88,"Real Sociedad":80,
    "Celta Vigo":80,"Celta":80,"Villarreal":84,"Real Betis":82,"Sevilla":79,
    "Athletic Bilbao":82,"Athletic Club":82,"Valencia":78,"Getafe":76,"Osasuna":76,
    "Rayo Vallecano":78,"Levante":76,"Alaves":74,"Elche":74,"Espanyol":76,"Mallorca":75,
    "Girona":78,"Oviedo":72,"Real Oviedo":72,
    "Bayern Munich":92,"Bayern":92,"Dortmund":86,"Borussia Dortmund":86,"RB Leipzig":85,
    "Leverkusen":87,"Bayer Leverkusen":87,"Hoffenheim":80,"Stuttgart":83,
    "Eintracht Frankfurt":82,"Frankfurt":82,"Freiburg":81,"Wolfsburg":79,
    "Mönchengladbach":78,"Borussia M'gladbach":78,"Borussia Monchengladbach":78,
    "Werder Bremen":79,"Werder":79,"Augsburg":76,"Union Berlin":77,"FC Union Berlin":77,
    "Heidenheim":73,"Koln":74,"FC Koln":74,"Mainz":76,"Mainz 05":76,"Hamburg":74,"HSV":74,"St Pauli":73,
    "Inter":89,"Inter Milan":89,"AC Milan":87,"Milan":87,"Juventus":85,"Napoli":87,
    "Roma":84,"AS Roma":84,"Atalanta":84,"Lazio":82,"Fiorentina":82,"Bologna":81,
    "Torino":78,"Como":79,"Cagliari":75,"Parma":76,"Udinese":76,"Genoa":75,"Pisa":73,
    "Lecce":73,"Sassuolo":77,"Verona":72,"Hellas Verona":72,"Venezia":74,"Cremonese":74,
    "PSG":91,"Paris Saint-Germain":91,"Marseille":84,"Olympique Marseille":84,
    "Monaco":81,"AS Monaco":81,"Lyon":83,"Olympique Lyon":83,"Lille":82,"Lens":81,
    "Nice":80,"Rennes":78,"Brest":78,"Stade Brestois":78,"Paris FC":76,"Toulouse":76,
    "Strasbourg":78,"Auxerre":74,"Nantes":74,"Le Havre":73,"Metz":72,"Lorient":74,"Angers":73,
    "Ajax":83,"PSV":84,"Feyenoord":80,"AZ Alkmaar":79,"Twente":79,"FC Twente":79,
    "Groningen":75,"FC Groningen":75,"Willem II":72,"Utrecht":76,"FC Utrecht":76,
    "Heerenveen":74,"Sparta Rotterdam":73,"Heracles Almelo":72,"Heracles":72,
    "NEC Nijmegen":74,"NEC":74,"Go Ahead Eagles":74,"PEC Zwolle":72,"Zwolle":72,
    "Fortuna Sittard":72,"Fortuna":72,"Excelsior":71,"Telstar":70,"NAC Breda":71,
    "Porto":84,"FC Porto":84,"Benfica":85,"Sporting CP":85,"Sporting":85,"Braga":81,
    "Maritimo":71,"Nacional":70,"CD Nacional":70,"Estoril":73,"Gil Vicente":73,
    "Rio Ave":72,"Boavista":70,"Moreirense":71,"Guimaraes":73,"Vitoria Guimaraes":73,
    "Santa Clara":72,"AVS":69,"Casa Pia":70,"Tondela":69,
    "Celtic":80,"Rangers":79,"Hearts":76,"Heart of Midlothian":76,"Aberdeen":73,"Hibernian":73,
    "Dundee United":71,"Kilmarnock":70,"Motherwell":71,"St Mirren":70,
    "Kairat Almaty":68,"Kairat":68,"Mjallby":71,"Mjällby":71,"Thun":71,"FC Thun":71,
    "U Craiova":72,"Universitatea Craiova":72,"U. Craiova":72,"Sturm Graz":76,
    "Ferencvaros":77,"Ferencváros":77,"Celje":73,"NK Celje":73,"Omonia Nicosia":70,
    "Lillestrom":70,"Lillestrøm":70,"Levski Sofia":71,"Levski":71,
    "Besiktas":79,"Galatasaray":85,"Fenerbahce":84,"Shakhtar Donetsk":80,
    "Dynamo Kyiv":78,"Sparta Prague":78,"Slavia Prague":79,"PAOK":78,"AEK Athens":78,
    "Olympiacos":82,"Panathinaikos":80,"Basel":77,"Young Boys":77,"Anderlecht":78,
    "Gent":77,"Genk":79,"Legia Warsaw":75,"Lech Poznan":74,"Rijeka":73,
    "Dinamo Zagreb":79,"Samsunspor":74,"Trabzonspor":78,"Drita":66,"Noah":66,
    "Hamrun Spartans":64,"Lincoln Red Imps":63,"Shelbourne":65,"Shamrock Rovers":66,
    "Breidablik":65,"Zrinjski Mostar":68,"KuPS":68,"AEK Larnaca":70,
    "Pafos":72,"Midtjylland":77,"Brann":74,"Aarhus":73,"AGF Aarhus":73,"AGF":73,
    "Racing Club":76,"Racing":76,"Malmo FF":75,"Malmo":75,"Hacken":72,"BK Hacken":72,
}

# V3.1 FIX: Normalize names so SV Werder Bremen, Stade Brestois 29, Marítimo M. are found
def get_rating(t):
    if t in RATINGS:
        return RATINGS[t]
    clean = t.replace("SV ","").replace("FC ","").replace("Stade Brestois 29","Brest").replace("Stade Brestois","Brest").replace("Marítimo M.","Maritimo").replace("Maritimo M.","Maritimo").replace("R. Racing Club","Racing Club").replace("Nott'm Forest","Nottingham Forest").replace("CD Nacional","Nacional").replace("Borussia M'gladbach","Borussia Monchengladbach").replace("Borussia Mönchengladbach","Borussia Monchengladbach")
    if clean in RATINGS:
        return RATINGS[clean]
    # Fuzzy: if a known name is inside this name
    low = t.lower()
    for k,v in RATINGS.items():
        kl = k.lower()
        if kl in low or low in kl:
            return v
    return 72

def calc_prediction(home, away, date_str, form_h=0, form_a=0):
    hr = get_rating(home) + 4 + form_h
    ar = get_rating(away) + form_a
    diff = hr - ar
    exp_h = 1.35 + diff * 0.07
    exp_a = 1.05 - diff * 0.07
    exp_h = max(0.15, min(4.2, exp_h)); exp_a = max(0.15, min(3.8, exp_a))
    seed_str = f"{home}-{away}-{date_str}"
    h = int(hashlib.md5(seed_str.encode()).hexdigest()[:8], 16)
    var_h = ((h % 100) / 100 - 0.5); var_a = (((h // 100) % 100) / 100 - 0.5)
    ph = max(0, min(5, int(round(exp_h + var_h))))
    pa = max(0, min(4, int(round(exp_a + var_a))))
    if ph == 1 and pa == 1 and (h % 3 == 0): ph = 0; pa = 0
    if ph > pa:
        alt1 = f"{ph}-{pa+1}" if pa+1 <= 4 else f"{ph+1}-{pa}"
        alt2 = f"{max(0,ph-1)}-{pa}"
    elif pa > ph:
        alt1 = f"{ph+1}-{pa}"
        alt2 = f"{ph}-{max(0,pa-1)}"
    else:
        alt1 = f"{ph+1}-{pa}"; alt2 = f"{ph}-{pa+1}"
    winner = "home" if ph > pa else "away" if pa > ph else "draw"
    conf = min(92, max(48, 52 + abs(diff) * 1.2))
    if get_rating(home)==72 and get_rating(away)==72: conf = min(conf, 55)
    return {"h": ph, "a": pa, "winner": winner, "conf": int(conf), "alt1": alt1, "alt2": alt2, "diff": round(diff,1)}

def main():
    date_str = sys.argv[1] if len(sys.argv)>1 else datetime.now(LAGOS).strftime("%Y%m%d")
    target = f"{date_str[6:8]}/{date_str[4:6]}/{date_str[0:4]}"
    target2 = f"{date_str[0:4]}-{date_str[4:6]}-{date_str[6:8]}"
    print(f"=== V3.1 Fetching for {date_str} ===")
    all_matches=[]; by_league={}
    form_data = {}
    all_rows = []
    for slug, league_name in LEAGUES.items():
        csv_text=None
        for u in [f"https://fixturedownload.com/download/{slug}-2026-GMTStandardTime.csv", f"https://fixturedownload.com/download/{slug}-2025-GMTStandardTime.csv"]:
            try:
                r=requests.get(u,timeout=20,headers={"User-Agent":"Mozilla/5.0"})
                print(f"{league_name}: {r.status_code}")
                if r.status_code==200 and len(r.text)>100: csv_text=r.text; break
            except Exception as e: print(e); continue
        if not csv_text: continue
        try:
            reader=csv.DictReader(io.StringIO(csv_text))
            rows=list(reader)
            all_rows.extend([(league_name, row) for row in rows])
            for row in rows:
                d=(row.get("Date") or "").strip().split(" ")[0]
                res=(row.get("Result") or "").strip()
                if not res or "-" not in res: continue
                try: hs,aws=map(int,res.split("-"))
                except: continue
                ht=(row.get("Home Team") or "").strip(); at=(row.get("Away Team") or "").strip()
                if ht==at: continue
                if d in (target,target2,target.replace("/","-")): continue
                if ht: form_data.setdefault(ht,[]).append(3 if hs>aws else 1 if hs==aws else 0)
                if at: form_data.setdefault(at,[]).append(3 if aws>hs else 1 if aws==hs else 0)
        except Exception as e: print(f"Parse {league_name}: {e}")
    def form_boost(team):
        lst=form_data.get(team,[])[-5:]
        if not lst: return 0
        avg=sum(lst)/len(lst)
        # V3.1 FIX: was *2.5 (too strong, flipped Chelsea game), now *1.0 = max +/-1.5
        return round((avg-1.5)*1.0,1)
    for league_name, row in all_rows:
        d=(row.get("Date") or "").strip(); date_part=d.split(" ")[0]; time_part=d.split(" ")[1] if " " in d else "TBD"
        if date_part not in (target,target2,target.replace("/","-")): continue
        home=(row.get("Home Team") or "").strip(); away=(row.get("Away Team") or "").strip()
        if not home or not away: continue
        result=(row.get("Result") or "").strip(); hs=None; aws=None; status="scheduled"
        if result and "-" in result:
            try: hs,aws=map(int,result.split("-")); status="finished"
            except: pass
        lagos_time=time_part
        if ":" in time_part:
            try: hh,mm=time_part.split(":"); hh=(int(hh)+1)%24; lagos_time=f"{hh:02d}:{mm} Lagos"
            except: pass
        fh=form_boost(home); fa=form_boost(away)
        pred=calc_prediction(home,away,date_str,fh,fa)
        all_matches.append({"home":home,"away":away,"date":date_str,"time":lagos_time,"status":status,"homeScore":hs,"awayScore":aws,"predH":pred["h"],"predA":pred["a"],"winner":pred["winner"],"conf":pred["conf"],"alt1":pred["alt1"],"alt2":pred["alt2"],"league":league_name,"formH":fh,"formA":fa})
        by_league[league_name]=by_league.get(league_name,0)+1
    print(by_league); print(f"Total: {len(all_matches)}")
    if len(all_matches)==0: print("WARNING 0 - NOT overwriting"); return
    with open("scores.json","w",encoding="utf-8") as f: json.dump({"generated":datetime.now(LAGOS).isoformat(),"date":date_str,"total":len(all_matches),"matches":all_matches},f,ensure_ascii=False,indent=2)
    print("Saved V3.1 scores.json")
if __name__=="__main__": main()
