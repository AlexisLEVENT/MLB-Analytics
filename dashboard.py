import os
import subprocess
import streamlit as st
import duckdb


# --------------------------------------------------
# CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="MLB Sorare Analytics",
    layout="wide"
)

st.title("⚾ MLB Sorare Scouting Dashboard")


# --------------------------------------------------
# INITIALISATION DE LA BASE DUCKDB
# --------------------------------------------------

DB_PATH = "dev.duckdb"


if not os.path.exists(DB_PATH):

    with st.spinner("Initialisation de la base de données..."):

        result = subprocess.run(
            [
                "dbt",
                "run",
                "--profiles-dir",
                ".",
                "--select",
                "stg_mlb_hitters"
            ],
            capture_output=True,
            text=True
        )

    if result.returncode != 0:
        st.error("Erreur lors de l'initialisation de la base de données.")
        st.code(result.stdout + "\n" + result.stderr)
        st.stop()


# --------------------------------------------------
# CONNEXION DUCKDB
# --------------------------------------------------

conn = duckdb.connect(DB_PATH, read_only=True)


# --------------------------------------------------
# SIDEBAR FILTERS
# --------------------------------------------------

st.sidebar.header("Filtres")


# Filtre Équipes
teams_query = """
    SELECT DISTINCT team
    FROM stg_mlb_hitters
    ORDER BY team
"""

teams = conn.execute(teams_query).df()["team"].tolist()

selected_teams = st.sidebar.multiselect(
    "Équipes",
    teams,
    default=teams
)


# Filtre Type de joueur
player_types = conn.execute(
    """
    SELECT DISTINCT player_type
    FROM stg_mlb_hitters
    ORDER BY player_type
    """
).df()["player_type"].tolist()

selected_type = st.sidebar.multiselect(
    "Type de joueur",
    player_types,
    default=player_types
)


# --------------------------------------------------
# DATA QUERY
# --------------------------------------------------

query = f"""
    SELECT *
    FROM stg_mlb_hitters
    WHERE team IN {
        tuple(selected_teams)
        if len(selected_teams) > 1
        else (
            f"('{selected_teams[0]}')"
            if selected_teams
            else "('')"
        )
    }
    AND player_type IN {
        tuple(selected_type)
        if len(selected_type) > 1
        else (
            f"('{selected_type[0]}')"
            if selected_type
            else "('')"
        )
    }
    ORDER BY sorare_avg_per_game DESC
"""

df = conn.execute(query).df()


# --------------------------------------------------
# MAIN DASHBOARD
# --------------------------------------------------

col1, col2 = st.columns(2)

col1.metric(
    "Joueurs filtrés",
    len(df)
)

col2.metric(
    "Moyenne max",
    f"{df['sorare_avg_per_game'].max():.2f}"
    if not df.empty
    else 0
)


st.subheader("Classement")

st.dataframe(
    df,
    width="stretch"
)


st.subheader("Performance")

if not df.empty:

    st.bar_chart(
        df.set_index("player_name")["sorare_avg_per_game"]
    )