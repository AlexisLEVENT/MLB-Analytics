# ⚾ MLB Analytics

## End-to-End Data Engineering & Analytics Pipeline

Projet personnel de **Data Engineering et Analytics** consacré à l'analyse des performances des joueurs MLB.

L'objectif est de construire une chaîne complète allant de la récupération des données jusqu'à leur transformation, leur scoring et leur visualisation dans un dashboard interactif.

---

## 🏗️ Architecture

```text
MLB Data
   │
   ▼
Python Extraction
   │
   ▼
DuckDB
   │
   ▼
dbt / SQL Transformation
   │
   ▼
Player Scoring
   │
   ▼
Streamlit Dashboard
```

---

## 🛠️ Stack technique

- **Python** — extraction, traitement et scoring des données
- **SQL** — requêtes et transformations analytiques
- **DuckDB** — stockage et interrogation des données
- **dbt** — modélisation et transformation des données
- **Streamlit** — dashboard analytique interactif
- **Shell** — automatisation de l'exécution du pipeline

---

## 📊 Fonctionnalités

### Data Pipeline

Le projet permet de récupérer et traiter des données de performance de joueurs MLB à travers plusieurs scripts Python.

### Data Transformation

Les données sont structurées et transformées avec dbt et SQL afin de produire des modèles exploitables pour l'analyse.

### Player Scoring

Un système de scoring permet de calculer et comparer les performances des joueurs à partir des données disponibles.

### Analytics Dashboard

Une application Streamlit permet d'explorer les données et les scores des joueurs à travers différents filtres et indicateurs.

---

## 📂 Structure du projet

```text
MLB-Analytics/
│
├── dashboard.py
├── fetch_team_stats.py
├── score_players.py
├── query_db.py
├── run_all.sh
├── requirements.txt
├── dbt_project.yml
├── profiles.yml
│
├── all_mlb_stats_2026.csv
├── all_mlb_stats_2026.json
├── data_pour_looker.csv
├── staging_ohtani_stats.json
├── team_stats_2026.json
│
├── models/
│   ├── example/
│   ├── models/
│   └── stg_mlb_players.sql
│
├── analyses/
├── macros/
├── seeds/
├── snapshots/
└── tests/
```

---

## 🔄 Pipeline

### 1. Extraction

Les données MLB sont récupérées et préparées à l'aide de scripts Python.

### 2. Stockage

Les données sont exploitées avec DuckDB pour permettre leur interrogation et leur analyse.

### 3. Transformation

Les transformations sont organisées dans dbt et SQL, avec une structure comprenant notamment les modèles, seeds, snapshots et tests.

### 4. Scoring

Les performances des joueurs sont analysées afin de produire un système de scoring exploitable pour la comparaison des joueurs.

### 5. Visualisation

Les résultats sont exposés à travers un dashboard interactif développé avec Streamlit.

---

## 🎯 Objectifs Data Engineering

Ce projet me permet de travailler sur plusieurs problématiques rencontrées dans des environnements Data :

- ingestion et préparation de données
- manipulation de données avec Python
- SQL et modélisation analytique
- utilisation de DuckDB
- transformation avec dbt
- automatisation d'un pipeline
- conception d'indicateurs
- restitution analytique avec Streamlit

---

## 🚀 Dashboard

👉 [Open the MLB Sorare Scouting Dashboard](https://mlb-analytics-9cmzwdidgjrpb9uvdwttk3.streamlit.app)

---

## 👤 Auteur

**Alexis Levent**

Data Engineer / Analytics Engineer

[GitHub](https://github.com/AlexisLEVENT)  
[LinkedIn](https://fr.linkedin.com/in/alexis-levent-795ba411b)
