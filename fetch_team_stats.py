import requests
import json
import pandas as pd  # Import indispensable pour le CSV

def fetch_all_mlb():
    all_players = []
    
    # 1. Récupérer la liste de toutes les équipes
    teams_url = "https://statsapi.mlb.com/api/v1/teams?sportId=1"
    teams = requests.get(teams_url).json()['teams']
    
    for team in teams:
        team_id = team['id']
        team_name = team['name']
        print(f"--- Récupération de l'équipe : {team_name} ---")
        
        # 2. Récupérer le roster de l'équipe
        roster_url = f"https://statsapi.mlb.com/api/v1/teams/{team_id}/roster"
        roster = requests.get(roster_url).json().get('roster', [])
        
        for player in roster:
            pid = player['person']['id']
            
            # 3. Récupérer les stats (hitting) pour chaque joueur
            stats_url = f"https://statsapi.mlb.com/api/v1/people/{pid}/stats?stats=season&group=hitting&season=2026"
            res = requests.get(stats_url).json()
            
            try:
                if 'stats' in res and len(res['stats'][0]['splits']) > 0:
                    stats = res['stats'][0]['splits'][0]['stat']
                    stats['name'] = player['person']['fullName']
                    stats['team'] = team_name
                    all_players.append(stats)
                    print(f"  + {stats['name']} ajouté")
            except:
                continue

    # Sauvegarde finale en JSON (pour dbt)
    with open('all_mlb_stats_2026.json', 'w') as f:
        json.dump(all_players, f)
    
    # ADAPTATION : Export en CSV (pour Looker Studio)
    df = pd.DataFrame(all_players)
    df.to_csv('all_mlb_stats_2026.csv', index=False)
    
    print(f"\n✅ Terminé ! {len(all_players)} joueurs récupérés.")
    print(f"✅ Fichiers générés : all_mlb_stats_2026.json ET all_mlb_stats_2026.csv")

if __name__ == "__main__":
    fetch_all_mlb()