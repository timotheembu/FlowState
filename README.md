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
│   │   └── entity.py           # Classes Maison et Usine
│   ├── views/                  # Rendu graphique Pygame uniquement
│   │   ├── __init__.py
│   │   └── renderer.py         # Dessin de la grille et des entités
│   └── controllers/            # Gestion du temps et des événements utilisateur
│       └── __init__.py
├── tests/                      # Tests unitaires
│   └── __init__.py
├── .gitignore
├── requirements.txt
└── README.md
```

## Prérequis & Installation

1. Créer et activer un environnement virtuel Python :
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

2. Installer les dépendances :
   ```bash
   pip install -r requirements.txt
   ```

## Lancement

Depuis la racine du projet :

```bash
python3 -m src.main
```
