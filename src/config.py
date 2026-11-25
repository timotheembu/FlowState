"""Centralisation de toutes les constantes de configuration du jeu FlowState."""

# Paramètres de la fenêtre et du rafraîchissement
TITRE_FENETRE: str = "FlowState"
LARGEUR_FENETRE: int = 1080
HAUTEUR_FENETRE: int = 1080
FPS: int = 60

# Paramètres de la grille spatiale
NB_LIGNES: int = 30
NB_COLONNES: int = 30
TAILLE_CASE: int = LARGEUR_FENETRE // NB_COLONNES
EPAISSEUR_LIGNE_GRILLE: int = 1
INDICE_MINIMUM_GRILLE: int = 0
COORDONNEE_ORIGINE: int = 0
INCREMENT_BORNE_GRILLE: int = 1

# États possibles d'une case de la grille
CASE_VIDE: int = 0
CASE_MAISON: int = 1
CASE_USINE: int = 2
CASE_ROUTE: int = 3

# Couleurs de l'environnement (R, G, B)
COULEUR_FOND: tuple[int, int, int] = (245, 242, 235)
COULEUR_GRILLE: tuple[int, int, int] = (220, 216, 208)
COULEUR_ROUTE: tuple[int, int, int] = (85, 85, 90)

# Palette de couleurs des entités (R, G, B)
COULEUR_ROUGE: tuple[int, int, int] = (229, 75, 75)
COULEUR_BLEUE: tuple[int, int, int] = (65, 131, 215)
COULEUR_JAUNE: tuple[int, int, int] = (245, 190, 55)
COULEUR_CONTOUR_BATIMENT: tuple[int, int, int] = (60, 60, 60)

# Paramètres d'affichage des bâtiments dans une case
FACTEUR_DOUBLE_MARGE: int = 2
MARGE_MAISON: int = 7
RAYON_BORDURE_MAISON: int = 5
MARGE_USINE: int = 2
RAYON_BORDURE_USINE: int = 4
EPAISSEUR_CONTOUR_USINE: int = 2

# Paramètres d'affichage et de connexion des routes
MARGE_ROUTE: int = 10
RAYON_NOEUD_ROUTE: int = 4
DECALAGE_VOISIN_NUL: int = 0
DECALAGE_VOISIN_POSITIF: int = 1
DECALAGE_VOISIN_NEGATIF: int = -1

# Paramètres des boutons de la souris
BOUTON_SOURIS_GAUCHE: int = 1
BOUTON_SOURIS_DROIT: int = 3
INDICE_BOUTON_GAUCHE: int = 0
INDICE_BOUTON_DROIT: int = 2

# Positions des bâtiments de test (ligne, colonne, couleur)
MAISONS_TEST: list[tuple[int, int, tuple[int, int, int]]] = [
    (4, 4, COULEUR_ROUGE),
    (5, 6, COULEUR_ROUGE),
    (12, 3, COULEUR_BLEUE),
    (14, 5, COULEUR_BLEUE),
    (22, 7, COULEUR_JAUNE),
]

USINES_TEST: list[tuple[int, int, tuple[int, int, int]]] = [
    (6, 22, COULEUR_ROUGE),
    (15, 24, COULEUR_BLEUE),
    (23, 20, COULEUR_JAUNE),
]
