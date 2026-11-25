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

# Couleurs (R, G, B)
COULEUR_FOND: tuple[int, int, int] = (245, 242, 235)
COULEUR_GRILLE: tuple[int, int, int] = (220, 216, 208)
