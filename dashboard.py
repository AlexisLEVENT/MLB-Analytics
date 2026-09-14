import streamlit as st
import duckdb

st.set_page_config(page_title="MLB Sorare Analytics", layout="wide")
st.title("⚾ MLB Sorare Scouting Dashboard")

conn = duckdb.connect('dev.duckdb', read_only=True)

# --- SIDEBAR FILTERS ---
st.sidebar.header("Filtres")

# 1. Filtre Équipes (Dynamique)
# On récupère la liste des équipes directement depuis la base
teams_query = "SELECT DISTINCT team FROM stg_mlb_hitters ORDER BY team"
teams = conn.execute(teams_query).df()['team'].tolist()
selected_teams = st.sidebar.multiselect("Équipes", teams, default=teams)

# 2. Filtre Type de joueur
player_types = conn.execute("SELECT DISTINCT player_type FROM stg_mlb_hitters").df()['player_type'].tolist()
selected_type = st.sidebar.multiselect("Type de joueur", player_types, default=player_types)

# --- DATA QUERY ---
# Construction propre de la requête pour éviter les erreurs si un filtre est vide
query = f"""
    SELECT * FROM stg_mlb_hitters 
    WHERE team IN {tuple(selected_teams) if len(selected_teams) > 1 else (f"('{selected_teams[0]}')" if selected_teams else "('')")}
    AND player_type IN {tuple(selected_type) if len(selected_type) > 1 else (f"('{selected_type[0]}')" if selected_type else "('')")}
    ORDER BY sorare_avg_per_game DESC
"""
df = conn.execute(query).df()

# --- MAIN DASHBOARD ---
col1, col2 = st.columns(2)
col1.metric("Joueurs filtrés", len(df))
col2.metric("Moyenne max", f"{df['sorare_avg_per_game'].max():.2f}" if not df.empty else 0)

st.subheader("Classement")
# Remplacement de use_container_width par width='stretch' pour supprimer l'erreur
st.dataframe(df, width=1000)

st.subheader("Performance")
if not df.empty:
    st.bar_chart(df.set_index('player_name')['sorare_avg_per_game'])