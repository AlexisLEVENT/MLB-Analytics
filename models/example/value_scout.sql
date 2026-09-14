with source_data as (
    -- La fonction ref() permet à dbt de lier dynamiquement ce modèle à ton fichier CSV seedé
    select * from {{ ref('roster_sample') }}
)

select
    player_name,
    position,
    floor_price_euros,
    points_l5,
    points_l30,
    
    -- 1. Le Ratio de Forme : un score > 1 signifie que le joueur surperforme son historique (il est chaud)
    round(points_l5 / nullif(points_l30, 0), 2) as form_ratio,
    
    -- 2. Le Rendement : Combien de points récents le joueur rapporte pour chaque euro investi
    round(points_l5 / nullif(floor_price_euros, 0), 2) as points_per_euro

from source_data
order by points_per_euro desc