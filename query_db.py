import duckdb
import pandas as pd

def main():
    # 1. Connexion à la base de données locale
    con = duckdb.connect('dev.duckdb')

    # 2. Requête pour récupérer les données propres depuis le modèle dbt
    # On sélectionne toutes les colonnes de la table générée par dbt
    query = "SELECT * FROM main.stg_mlb_hitters"
    
    # 3. Chargement des données dans un DataFrame Pandas
    df = con.execute(query).fetchdf()

    # 4. Affichage d'un aperçu dans le terminal
    print("--- Aperçu des données dans la table stg_mlb_hitters ---")
    print(df.head(10))
    print("\n--- Statistiques rapides ---")
    print(df.describe())

    # 5. Export automatique en CSV pour Looker Studio
    output_file = 'data_pour_looker.csv'
    df.to_csv(output_file, index=False)
    print(f"\nSuccès : Le fichier '{output_file}' a été mis à jour pour ton dashboard.")

    # Fermeture de la connexion
    con.close()

if __name__ == "__main__":
    main()