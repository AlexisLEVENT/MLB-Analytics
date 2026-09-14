#!/bin/bash
echo "--- Lancement du pipeline ---"
dbt run --select stg_mlb_hitters
python query_db.py
echo "--- Pipeline terminé ! data_pour_looker.csv est prêt. ---"