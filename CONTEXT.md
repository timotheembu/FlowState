# Cahier des Charges & Architecture — FlowState

## 1. Vision du Projet
Développement d'un clone simplifié de **Mini Motorways** en **Python** avec **Pygame**.
Le projet se construit en **vibecoding itératif strict** : une seule brique fonctionnelle à la fois, testée et validée avant de passer à la suivante. Ne jamais coder une fonctionnalité non demandée.

## 2. Mécaniques de Jeu Cibles
1. **Grille spatiale (30x30 cases) :** Matrice de base. Une case peut être vide, contenir un bâtiment (Maison ou Usine) ou contenir un segment de route.
2. **Maisons (Spawners) :** Apparaissent avec une couleur donnée et génèrent des voitures de cette même couleur.
3. **Usines (Destinations) :** Apparaissent avec une couleur donnée et attirent les voitures correspondantes.
4. **Routes :** Tracées ou effacées à la souris par le joueur, case par case, pour relier Maisons et Usines.
5. **Voitures (Agents) :** Circulent uniquement sur les routes via un algorithme de pathfinding (**A\***) et simulent le trafic (arrêt si la case suivante est occupée).

## 3. Architecture MVC Obligatoire
```text
mini-motorways-clone/
├── src/
│   ├── __init__.py
│   ├── main.py                 # Point d'entrée et boucle principale
│   ├── config.py               # Centralisation de toutes les constantes
│   ├── models/                 # Logique métier pure (AUCUN import de pygame)
│   │   ├── __init__.py
│   │   ├── grid.py             # Matrice spatiale et état des cases
│   │   ├── entity.py           # Classes Maison, Usine, Voiture
│   │   └── pathfinding.py      # Algorithme A* isolé
│   ├── views/                  # Rendu graphique Pygame uniquement
│   │   ├── __init__.py
│   │   └── renderer.py         # Dessin de la grille et des entités
│   └── controllers/            # Gestion du temps et des événements utilisateur
│       ├── __init__.py
│       ├── game_engine.py
│       └── input_handler.py
├── tests/                      # Tests unitaires (pytest / unittest)
│   └── __init__.py
├── .gitignore
├── requirements.txt
└── README.md