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
```

## 4. Suivi des Étapes (Vibecoding Itératif)
- [x] **Étape 1 :** Arborescence MVC, configuration, modèle `Grid` et affichage de la grille 30x30.
- [x] **Étape 2 :** Modèles `Maison` et `Usine`, placement sur la grille et rendu graphique différencié par couleur.
- [x] **Étape 3 :** Tracé et effacement des routes à la souris.
- [x] **Étape 4 :** Algorithme de pathfinding A\*.
- [x] **Étape 5 :** Génération, déplacement des voitures et simulation du trafic.
- [x] **Étape 6 :** Apparition procédurale progressive (carte vide au départ, apparition d'une première paire Maison/Usine de même couleur, puis accélération des apparitions avec maisons isolées pouvant se rattacher à une usine existante de même couleur).
- [x] **Étape 7 :** Gameplay complet : demandes générées par les Usines (plusieurs usines possibles par couleur), flotte limitée de voitures par Maison effectuant l'aller-retour, routes à double sens, score et défaite (Game Over) si une Usine est saturée.
- [x] **Étape 8 :** Routes en diagonale (8 directions dans `Grid`, `InputHandler`, `Pathfinding` A* et `Renderer`) et stock limité de cases de route (remboursé à la suppression).
- [x] **Étape 9 :** Caméra avec zoom progressif (départ zoomé au centre, dézoom au fur et à mesure de l'expansion) et courbe de difficulté progressive (spawns plus lents au début, bâtiments proches puis éloignés).
- [x] **Étape 10 :** Raffinement gameplay & visuel : maison isolée obligatoirement rattachée à une couleur d'usine existante, rendu continu et fluide de l'asphalte, et suppression automatique des cases parasites dans les virages.
- [ ] **Étape 11 :** Système temporel (horloge visuelle + défilement des jours) et choix hebdomadaire chaque lundi (pause et sélection entre deux lots de routes/bonus : pont, tunnel, feu, rond-point, autoroute).
- [ ] **Étape 12 :** Mode Édition (touche dédiée pour activer/désactiver le mode construction ; tracé actif uniquement en mode édition et grille masquée en mode jeu normal).
- [ ] **Étape 13 :** Génération et sélection de cartes avec obstacles naturels (`CASE_EAU`, `CASE_MONTAGNE`).
- [ ] **Étape 14 :** Logique fonctionnelle complète des bonus spéciaux (Ponts sur eau, Tunnels sous montagne, Feux de circulation, Ronds-points, Autoroutes).