# FlowState

Clone simplifié de **Mini Motorways** développé en **Python** avec **Pygame**, conçu selon une architecture **MVC (Modèle-Vue-Contrôleur)** stricte.

## Architecture du Projet

```text
FlowState/
├── src/
│   ├── __init__.py
│   ├── main.py                 # Point d'entrée et boucle principale
│   ├── config.py               # Centralisation de toutes les constantes
│   ├── models/                 # Logique métier pure (aucun import de pygame)
│   │   ├── __init__.py
│   │   ├── grid.py             # Matrice spatiale et état des cases
│   │   ├── entity.py           # Classes Maison et Usine
│   │   └── pathfinding.py      # Algorithme A* isolé
│   ├── views/                  # Rendu graphique Pygame uniquement
│   │   ├── __init__.py
│   │   └── renderer.py         # Dessin de la grille et des entités
│   └── controllers/            # Gestion du temps et des événements utilisateur
│       ├── __init__.py
│       └── input_handler.py    # Tracé et effacement des routes à la souris
├── tests/                      # Tests unitaires
│   ├── __init__.py
│   ├── test_grid.py            # Tests unitaires de la grille
│   └── test_pathfinding.py     # Tests unitaires de l'algorithme A*
├── .gitignore
├── requirements.txt
└── README.md
```

## Prérequis & Installation

1. Créer et activer un environnement virtuel Python :

   **Sous Linux / macOS :**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

   **Sous Windows (PowerShell) :**
   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

2. Installer les dépendances :
   ```bash
   pip install -r requirements.txt
   ```

## Lancement

Depuis la racine du projet :

- **Linux / macOS :**
  ```bash
  python3 -m src.main
  ```
- **Windows :**
  ```powershell
  python -m src.main
  ```

