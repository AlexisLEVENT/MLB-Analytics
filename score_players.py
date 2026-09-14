import json

def calculate_score(stats):
    score = 0
    # On ajoute des poids pour le pitching (ex: strikeouts = +2 points)
    # Les stats de pitching sont souvent sous "strikeOuts" aussi dans l'API, 
    # mais il faut distinguer le contexte.
    
    # Frappeur
    score += stats.get("homeRuns", 0) * 10
    score += stats.get("hits", 0) * 2
    
    # Lanceur (Si le joueur a des "strikeOuts" en tant que lanceur, 
    # on les ajoute ici - c'est une simplification)
    score += stats.get("strikeOuts", 0) * 0.5 
    
    # Pénalités
    score -= stats.get("errors", 0) * 5
    
    return score

with open("team_stats_2026.json", "r") as f:
    players = json.load(f)

# Tri des joueurs par score (les meilleurs en haut)
players.sort(key=lambda x: calculate_score(x), reverse=True)

print(f"{'JOUEUR':<20} | {'SCORE':<10} | {'STATUS'}")
print("-" * 45)

for p in players:
    score = calculate_score(p)
    status = "🟢 VERT" if score > 50 else "🔴 ROUGE"
    print(f"{p['name']:<20} | {score:<10} | {status}")