# predict.py - World Stats Hub Match Predictor
# Works with your existing scores.json + main.py
import math, json, os

def poisson(lam, k):
    return (math.exp(-lam) * (lam ** k)) / math.factorial(k)

def predict(home_team, away_team, home_avg, away_avg):
    home_exp = home_avg + 0.25  # home advantage
    away_exp = away_avg
    home_win = draw = away_win = over25 = 0
    best = (0,0)
    best_p = 0

    for h in range(0,7):
        for a in range(0,7):
            p = poisson(home_exp, h) * poisson(away_exp, a)
            if p > best_p:
                best_p = p
                best = (h,a)
            if h > a: home_win += p
            elif h == a: draw += p
            else: away_win += p
            if h + a > 2.5: over25 += p

    result = f"🔥 {home_team} vs {away_team}\n"
    result += f"Most Likely Score: {best[0]}-{best[1]} ({best_p*100:.1f}%)\n"
    result += f"Home Win: {home_win*100:.1f}% | Draw: {draw*100:.1f}% | Away Win: {away_win*100:.1f}%\n"
    result += f"Over 2.5: {over25*100:.1f}%"
    return result

# TEST - Delete this later if you want
if __name__ == "__main__":
    print(predict("Arsenal", "Chelsea", 2.1, 1.4))
    print(predict("Real Madrid", "Barcelona", 2.3, 1.8))
