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
CASE_EAU: int = 4
CASE_MONTAGNE: int = 5
CASE_PONT: int = 6
CASE_TUNNEL: int = 7
CASE_ROND_POINT: int = 8

# Couleurs de l'environnement (R, G, B) — Thème par défaut "Crème & Sauge"
COULEUR_FOND: tuple[int, int, int] = (239, 232, 220)
COULEUR_GRILLE: tuple[int, int, int] = (224, 216, 204)
COULEUR_ROUTE: tuple[int, int, int] = (58, 63, 72)
COULEUR_BORDURE_ROUTE: tuple[int, int, int] = (46, 50, 58)
COULEUR_EAU: tuple[int, int, int] = (158, 204, 176)
COULEUR_BORDURE_EAU: tuple[int, int, int] = (186, 222, 200)
COULEUR_MONTAGNE: tuple[int, int, int] = (244, 194, 158)
COULEUR_BORDURE_MONTAGNE: tuple[int, int, int] = (252, 218, 192)
COULEUR_SOMMET_MONTAGNE: tuple[int, int, int] = (232, 176, 138)
MARGE_SOMMET_MONTAGNE: int = 6
RAYON_BORDURE_MONTAGNE: int = 4

# Thèmes graphiques complets inspirés de Mini Motorways (Étapes 18 & 19)
THEME_CREME_SAUGE: str = "Crème & Sauge"
THEME_CORAIL_LAGON: str = "Corail & Lagon"
THEME_MODE_NUIT: str = "Mode Nuit"
THEME_BLEU_LAGON: str = "Bleu Lagon"
THEME_VERT_MENTHE: str = "Vert Menthe"

COULEUR_FOND_CREME_SAUGE: tuple[int, int, int] = (239, 232, 220)
COULEUR_EAU_CREME_SAUGE: tuple[int, int, int] = (158, 204, 176)
COULEUR_BORDURE_EAU_CREME_SAUGE: tuple[int, int, int] = (186, 222, 200)
COULEUR_RELIEF_CREME_SAUGE: tuple[int, int, int] = (244, 194, 158)
COULEUR_BORDURE_RELIEF_CREME_SAUGE: tuple[int, int, int] = (252, 218, 192)
COULEUR_SOMMET_CREME_SAUGE: tuple[int, int, int] = (232, 176, 138)
COULEUR_GRILLE_CREME_SAUGE: tuple[int, int, int] = (224, 216, 204)
COULEUR_TEXTE_CREME_SAUGE: tuple[int, int, int] = (45, 48, 56)

COULEUR_FOND_CORAIL_LAGON: tuple[int, int, int] = (226, 114, 114)
COULEUR_EAU_CORAIL_LAGON: tuple[int, int, int] = (173, 212, 219)
COULEUR_BORDURE_EAU_CORAIL_LAGON: tuple[int, int, int] = (202, 230, 235)
COULEUR_RELIEF_CORAIL_LAGON: tuple[int, int, int] = (194, 82, 92)
COULEUR_BORDURE_RELIEF_CORAIL_LAGON: tuple[int, int, int] = (212, 102, 110)
COULEUR_SOMMET_CORAIL_LAGON: tuple[int, int, int] = (172, 68, 78)
COULEUR_GRILLE_CORAIL_LAGON: tuple[int, int, int] = (210, 100, 100)
COULEUR_TEXTE_CORAIL_LAGON: tuple[int, int, int] = (250, 245, 242)

COULEUR_FOND_MODE_NUIT: tuple[int, int, int] = (38, 43, 52)
COULEUR_EAU_MODE_NUIT: tuple[int, int, int] = (56, 82, 108)
COULEUR_BORDURE_EAU_MODE_NUIT: tuple[int, int, int] = (74, 104, 134)
COULEUR_RELIEF_MODE_NUIT: tuple[int, int, int] = (54, 60, 72)
COULEUR_BORDURE_RELIEF_MODE_NUIT: tuple[int, int, int] = (68, 76, 90)
COULEUR_SOMMET_MODE_NUIT: tuple[int, int, int] = (46, 52, 64)
COULEUR_GRILLE_MODE_NUIT: tuple[int, int, int] = (52, 58, 70)
COULEUR_TEXTE_MODE_NUIT: tuple[int, int, int] = (235, 238, 245)

COULEUR_FOND_BLEU_LAGON: tuple[int, int, int] = (242, 236, 224)
COULEUR_EAU_BLEU_LAGON: tuple[int, int, int] = (116, 198, 216)
COULEUR_BORDURE_EAU_BLEU_LAGON: tuple[int, int, int] = (156, 218, 232)
COULEUR_RELIEF_BLEU_LAGON: tuple[int, int, int] = (228, 186, 152)
COULEUR_BORDURE_RELIEF_BLEU_LAGON: tuple[int, int, int] = (242, 206, 176)
COULEUR_SOMMET_BLEU_LAGON: tuple[int, int, int] = (210, 166, 132)
COULEUR_GRILLE_BLEU_LAGON: tuple[int, int, int] = (226, 220, 208)
COULEUR_TEXTE_BLEU_LAGON: tuple[int, int, int] = (45, 48, 56)

COULEUR_FOND_VERT_MENTHE: tuple[int, int, int] = (214, 235, 222)
COULEUR_EAU_VERT_MENTHE: tuple[int, int, int] = (118, 178, 212)
COULEUR_BORDURE_EAU_VERT_MENTHE: tuple[int, int, int] = (154, 202, 228)
COULEUR_RELIEF_VERT_MENTHE: tuple[int, int, int] = (146, 198, 170)
COULEUR_BORDURE_RELIEF_VERT_MENTHE: tuple[int, int, int] = (172, 216, 192)
COULEUR_SOMMET_VERT_MENTHE: tuple[int, int, int] = (124, 178, 150)
COULEUR_GRILLE_VERT_MENTHE: tuple[int, int, int] = (198, 220, 206)
COULEUR_TEXTE_VERT_MENTHE: tuple[int, int, int] = (42, 52, 48)

THEMES_GRAPHIQUES: dict[str, dict[str, tuple[int, int, int]]] = {
    THEME_CREME_SAUGE: {
        "fond": COULEUR_FOND_CREME_SAUGE,
        "eau": COULEUR_EAU_CREME_SAUGE,
        "bordure_eau": COULEUR_BORDURE_EAU_CREME_SAUGE,
        "montagne": COULEUR_RELIEF_CREME_SAUGE,
        "bordure_montagne": COULEUR_BORDURE_RELIEF_CREME_SAUGE,
        "sommet_montagne": COULEUR_SOMMET_CREME_SAUGE,
        "grille": COULEUR_GRILLE_CREME_SAUGE,
        "texte_hud": COULEUR_TEXTE_CREME_SAUGE,
    },
    THEME_CORAIL_LAGON: {
        "fond": COULEUR_FOND_CORAIL_LAGON,
        "eau": COULEUR_EAU_CORAIL_LAGON,
        "bordure_eau": COULEUR_BORDURE_EAU_CORAIL_LAGON,
        "montagne": COULEUR_RELIEF_CORAIL_LAGON,
        "bordure_montagne": COULEUR_BORDURE_RELIEF_CORAIL_LAGON,
        "sommet_montagne": COULEUR_SOMMET_CORAIL_LAGON,
        "grille": COULEUR_GRILLE_CORAIL_LAGON,
        "texte_hud": COULEUR_TEXTE_CORAIL_LAGON,
    },
    THEME_MODE_NUIT: {
        "fond": COULEUR_FOND_MODE_NUIT,
        "eau": COULEUR_EAU_MODE_NUIT,
        "bordure_eau": COULEUR_BORDURE_EAU_MODE_NUIT,
        "montagne": COULEUR_RELIEF_MODE_NUIT,
        "bordure_montagne": COULEUR_BORDURE_RELIEF_MODE_NUIT,
        "sommet_montagne": COULEUR_SOMMET_MODE_NUIT,
        "grille": COULEUR_GRILLE_MODE_NUIT,
        "texte_hud": COULEUR_TEXTE_MODE_NUIT,
    },
    THEME_BLEU_LAGON: {
        "fond": COULEUR_FOND_BLEU_LAGON,
        "eau": COULEUR_EAU_BLEU_LAGON,
        "bordure_eau": COULEUR_BORDURE_EAU_BLEU_LAGON,
        "montagne": COULEUR_RELIEF_BLEU_LAGON,
        "bordure_montagne": COULEUR_BORDURE_RELIEF_BLEU_LAGON,
        "sommet_montagne": COULEUR_SOMMET_BLEU_LAGON,
        "grille": COULEUR_GRILLE_BLEU_LAGON,
        "texte_hud": COULEUR_TEXTE_BLEU_LAGON,
    },
    THEME_VERT_MENTHE: {
        "fond": COULEUR_FOND_VERT_MENTHE,
        "eau": COULEUR_EAU_VERT_MENTHE,
        "bordure_eau": COULEUR_BORDURE_EAU_VERT_MENTHE,
        "montagne": COULEUR_RELIEF_VERT_MENTHE,
        "bordure_montagne": COULEUR_BORDURE_RELIEF_VERT_MENTHE,
        "sommet_montagne": COULEUR_SOMMET_VERT_MENTHE,
        "grille": COULEUR_GRILLE_VERT_MENTHE,
        "texte_hud": COULEUR_TEXTE_VERT_MENTHE,
    },
}

# Palette de couleurs pastel des entités (R, G, B) — Mini Motorways
COULEUR_ROUGE: tuple[int, int, int] = (235, 104, 100)
COULEUR_BLEUE: tuple[int, int, int] = (78, 179, 211)
COULEUR_JAUNE: tuple[int, int, int] = (247, 208, 106)
COULEUR_VERTE: tuple[int, int, int] = (118, 198, 154)
COULEUR_VIOLETTE: tuple[int, int, int] = (168, 138, 212)
COULEUR_ORANGE: tuple[int, int, int] = (242, 148, 92)
COULEUR_CONTOUR_BATIMENT: tuple[int, int, int] = (52, 56, 64)
PALETTE_COULEURS_BATIMENTS: list[tuple[int, int, int]] = [
    COULEUR_ROUGE,
    COULEUR_BLEUE,
    COULEUR_JAUNE,
    COULEUR_VERTE,
    COULEUR_VIOLETTE,
    COULEUR_ORANGE,
]

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
EPAISSEUR_SEGMENT_DIAGONAL: int = 14
LARGEUR_CHAUSSEE: int = 16
BORDURE_CHAUSSEE: int = 2
DECALAGE_VOISIN_NUL: int = 0
DECALAGE_VOISIN_POSITIF: int = 1
DECALAGE_VOISIN_NEGATIF: int = -1
DISTANCE_CHEBYSHEV_ADJACENTE: int = 1
TAILLE_MIN_HISTORIQUE_ELAGAGE: int = 2
INDICE_DERNIERE_CASE_TRACEE: int = -1
INDICE_AVANT_DERNIERE_CASE_TRACEE: int = -2
NB_MAX_ROUTES_ADJACENTES_MAISON: int = 1

# Stock initial et gestion de l'inventaire de routes
STOCK_ROUTES_INITIAL: int = 25
STOCK_ROUTES_EPUISE: int = 0
UNITE_STOCK_ROUTE: int = 1
STOCK_TEST_LIMITE: int = 2

# Paramètres de l'algorithme de pathfinding A* (8 directions)
COUT_INITIAL_CHEMIN: int = 0
COUT_INITIAL_CHEMIN_FLOAT: float = 0.0
COUT_DEPLACEMENT_VOISIN: int = 1
COUT_ORTHOGONAL: float = 1.0
COUT_DIAGONALE: float = 1.414
PAS_INCREMENT_COMPTEUR: int = 1
DIRECTIONS_ORTHOGONALES: list[tuple[int, int]] = [
    (DECALAGE_VOISIN_NUL, DECALAGE_VOISIN_NEGATIF),
    (DECALAGE_VOISIN_NUL, DECALAGE_VOISIN_POSITIF),
    (DECALAGE_VOISIN_NEGATIF, DECALAGE_VOISIN_NUL),
    (DECALAGE_VOISIN_POSITIF, DECALAGE_VOISIN_NUL),
]
DIRECTIONS_DIAGONALES: list[tuple[int, int]] = [
    (DECALAGE_VOISIN_NEGATIF, DECALAGE_VOISIN_NEGATIF),
    (DECALAGE_VOISIN_POSITIF, DECALAGE_VOISIN_NEGATIF),
    (DECALAGE_VOISIN_NEGATIF, DECALAGE_VOISIN_POSITIF),
    (DECALAGE_VOISIN_POSITIF, DECALAGE_VOISIN_POSITIF),
]
DIRECTIONS_HUIT_VOISINS: list[tuple[int, int]] = (
    DIRECTIONS_ORTHOGONALES + DIRECTIONS_DIAGONALES
)

# Paramètres de la flotte de voitures, des états et du trafic à double sens
INTERVALLE_APPARITION_VOITURE: int = 120
NB_MAX_VOITURES_PAR_MAISON: int = 2
NB_VOITURES_PAR_MAISON: int = 2
ETAT_VOITURE_A_LA_MAISON: int = 0
ETAT_VOITURE_ALLER_USINE: int = 1
ETAT_VOITURE_RETOUR_MAISON: int = 2
ETAT_VOITURE_A_L_USINE: int = 3
DUREE_ARRET_USINE: float = 1.5
DUREE_ARRET_USINE_FRAMES: int = int(DUREE_ARRET_USINE * FPS)
COMPTEUR_INITIAL_FRAMES: int = 0
COMPTEUR_INITIAL_LIVRAISONS: int = 0
COMPTEUR_INITIAL_DEMANDES: int = 0
LONGUEUR_MINIMALE_ITINERAIRE: int = 2
INDICE_PREMIERE_ETAPE_ITINERAIRE: int = 1
VITESSE_VOITURE: float = 0.05
DISTANCE_MIN_SECURITE_VOITURE: float = 0.85
SEUIL_ARRIVEE_ETAPE: float = 0.001
DISTANCE_NULLE: float = 0.0
DIRECTION_INITIALE_NULLE: float = 0.0
SEUIL_MEME_DIRECTION: float = 0.5
RAYON_VOITURE: int = 4
RAYON_CONTOUR_VOITURE: int = 1
DECALAGE_CENTRE_CASE: float = 0.5
DECALAGE_VOIE_DROITE_PIXELS: int = 4

# Paramètres de génération des demandes par Usine et seuil de défaite
INTERVALLE_DEMANDE_USINE: int = 240
SEUIL_CRITIQUE_DEMANDES_USINE: int = 6
RAYON_INDICATEUR_DEMANDE: int = 3
RAYON_CONTOUR_DEMANDE: int = 1
NB_COLONNES_GRILLE_DEMANDES: int = 3
ESPACEMENT_INDICATEUR_DEMANDE: int = 9
MARGE_INTERIEURE_DEMANDE: int = 9
COULEUR_INDICATEUR_DEMANDE: tuple[int, int, int] = (255, 255, 255)

# Paramètres d'affichage de l'interface (Score et Partie Perdue)
COULEUR_TEXTE_INTERFACE: tuple[int, int, int] = (45, 45, 50)
COULEUR_FOND_BANDEAU_SCORE: tuple[int, int, int] = (235, 230, 220)
COULEUR_FOND_PANNEAU_DEFAITE: tuple[int, int, int] = (40, 40, 45)
COULEUR_TEXTE_DEFAITE: tuple[int, int, int] = (229, 75, 75)
COULEUR_SOUS_TEXTE_DEFAITE: tuple[int, int, int] = (245, 242, 235)
TAILLE_POLICE_SCORE: int = 26
TAILLE_POLICE_TITRE_DEFAITE: int = 48
TAILLE_POLICE_SOUS_TITRE_DEFAITE: int = 30
POSITION_BANDEAU_SCORE_X: int = 16
POSITION_BANDEAU_SCORE_Y: int = 16
LARGEUR_BANDEAU_SCORE: int = 160
HAUTEUR_BANDEAU_SCORE: int = 42
POSITION_BANDEAU_ROUTES_X: int = 190
POSITION_BANDEAU_ROUTES_Y: int = 16
LARGEUR_BANDEAU_ROUTES: int = 175
HAUTEUR_BANDEAU_ROUTES: int = 42
RAYON_BORDURE_INTERFACE: int = 8
EPAISSEUR_CONTOUR_INTERFACE: int = 2
LARGEUR_PANNEAU_DEFAITE: int = 520
HAUTEUR_PANNEAU_DEFAITE: int = 180
DECALAGE_TITRE_DEFAITE_Y: int = -30
DECALAGE_SOUS_TITRE_DEFAITE_Y: int = 30
DIVISEUR_MOITIE: int = 2

# Constantes de coordonnées et dimensions pour les tests unitaires
TAILLE_GRILLE_TEST: int = 10
INDICE_TEST_ZERO: int = 0
INDICE_TEST_UN: int = 1
INDICE_TEST_DEUX: int = 2
INDICE_TEST_TROIS: int = 3
INDICE_TEST_QUATRE: int = 4
INDICE_TEST_CINQ: int = 5
INDICE_TEST_SIX: int = 6
INDICE_TEST_NEUF: int = 9
INDICE_TEST_NEGATIF: int = -1
LONGUEUR_LISTE_VIDE: int = 0
LONGUEUR_CHEMIN_UN: int = 1

# Paramètres des boutons de la souris
BOUTON_SOURIS_GAUCHE: int = 1
BOUTON_SOURIS_DROIT: int = 3
INDICE_BOUTON_GAUCHE: int = 0
INDICE_BOUTON_DROIT: int = 2

# Paramètres d'apparition procédurale progressive des bâtiments
DELAI_APPARITION_INITIALE_PAIRE: int = 30
INTERVALLE_SPAWN_INITIAL_SECONDES: float = 18.0
INTERVALLE_INITIAL_APPARITION_BATIMENT: int = int(
    INTERVALLE_SPAWN_INITIAL_SECONDES * FPS
)
INTERVALLE_MINIMUM_APPARITION_BATIMENT: int = 300
FACTEUR_ACCELERATION_APPARITION: float = 0.94
PROBABILITE_MAISON_SEULE: float = 0.65
MARGE_BORDURE_APPARITION: int = 1
DISTANCE_MIN_ENTRE_BATIMENTS: int = 2
DISTANCE_MIN_SECOURS_BATIMENT: int = 1
DISTANCE_MAX_INITIALE_BATIMENTS: int = 5
PAS_EXPANSION_DISTANCE_SPAWN: int = 1
MARGE_BORDURE_NULLE: int = 0

# Paramètres de la caméra et du zoom progressif centré sur la grille
ZONE_VISIBLE_INITIALE: float = 12.0
ZONE_VISIBLE_MAXIMALE: float = 30.0
PAS_EXPANSION_ZONE_CAMERA: float = 1.5
MARGE_DECLENCHEMENT_DEZOOM: float = 2.5
MARGE_INTERIEURE_SPAWN_CAMERA: int = 2
VITESSE_INTERPOLATION_CAMERA: float = 0.03
FACTEUR_ECHELLE_UNITE: float = 1.0
DIMENSION_PIXEL_MINIMALE: int = 1
COORDONNEE_CAMERA_ORIGINE_FLOAT: float = 0.0

# Cartes prédéfinies et paramètres de génération du relief naturel
CARTE_PLAINE: str = "Plaine"
CARTE_RIVIERE: str = "Rivière"
CARTE_MONTAGNES: str = "Montagnes"
CARTE_ORLEANS: str = "Orléans"
CARTE_ZURICH: str = "Zurich"
CARTE_MANILA: str = "Manila"
CARTE_RIO: str = "Rio de Janeiro"
CARTES_CARROUSEL: list[str] = [
    CARTE_ORLEANS,
    CARTE_ZURICH,
    CARTE_MANILA,
    CARTE_RIO,
]
CARTES_DISPONIBLES: list[str] = [
    CARTE_ORLEANS,
    CARTE_ZURICH,
    CARTE_MANILA,
    CARTE_RIO,
]
RAYON_ZONE_CENTRALE_DEGAGEE: int = 3
COLONNE_BASE_RIVIERE: int = 19
AMPLITUDE_SINUS_RIVIERE: float = 2.5
FREQUENCE_SINUS_RIVIERE: float = 0.35
LARGEUR_RIVIERE_CASES: int = 2
LIGNE_GUE_RIVIERE_MIN: int = 14
LIGNE_GUE_RIVIERE_MAX: int = 16
MASSIFS_MONTAGNEUX_DEFAUT: list[tuple[int, int, int]] = [
    (7, 8, 3),
    (8, 22, 3),
    (21, 7, 3),
    (22, 21, 3),
    (14, 24, 2),
]

# Paramètres de relief spécifiques aux 4 villes du carrousel (Étape 19)
COLONNE_DEPART_LOIRE_ORLEANS: int = 24
PENTE_DIAGONALE_LOIRE_ORLEANS: float = 0.55
AMPLITUDE_LOIRE_ORLEANS: float = 1.2
FREQUENCE_LOIRE_ORLEANS: float = 0.3
MASSIFS_ZURICH: list[tuple[int, int, int]] = [
    (6, 7, 3),
    (6, 23, 3),
    (23, 8, 3),
    (24, 22, 3),
]
LIGNE_BASE_MANILA: int = 18
AMPLITUDE_SINUS_MANILA: float = 1.8
FREQUENCE_SINUS_MANILA: float = 0.28
LARGEUR_BRAS_MER_MANILA: int = 3
COLONNE_GUE_MANILA_MIN: int = 14
COLONNE_GUE_MANILA_MAX: int = 16
ILOTS_MANILA: list[tuple[int, int, int]] = [
    (7, 22, 2),
    (24, 8, 2),
]
COLONNE_COTE_RIO_BASE: int = 22
AMPLITUDE_BAIE_RIO: float = 2.8
FREQUENCE_BAIE_RIO: float = 0.22
LIGNE_BAIE_SUD_RIO: int = 23
MASSIFS_RIO: list[tuple[int, int, int]] = [
    (7, 7, 3),
    (15, 6, 3),
    (22, 10, 2),
    (8, 17, 2),
]

# Paramètres de l'écran d'accueil de sélection de carte
LARGEUR_BOUTON_CARTE: int = 340
HAUTEUR_BOUTON_CARTE: int = 64
ESPACEMENT_BOUTONS_CARTE_Y: int = 90
POSITION_PREMIER_BOUTON_CARTE_Y: int = 420
POSITION_TITRE_ACCUEIL_Y: int = 240
POSITION_SOUS_TITRE_ACCUEIL_Y: int = 310
COULEUR_BOUTON_CARTE: tuple[int, int, int] = (235, 230, 220)
COULEUR_BOUTON_CARTE_SURVOL: tuple[int, int, int] = (215, 210, 198)

# Stocks initiaux des infrastructures et bonus spéciaux (Étape 16)
STOCK_PONTS_INITIAL: int = 0
STOCK_TUNNELS_INITIAL: int = 0
STOCK_FEUX_INITIAL: int = 0
STOCK_RONDS_POINTS_INITIAL: int = 0
STOCK_AUTOROUTES_INITIAL: int = 0
STOCK_PONTS_DEPART_RIVIERE: int = 1
STOCK_TUNNELS_DEPART_MONTAGNES: int = 1

# Outils de construction sélectionnables (touches 1 à 4 ou HUD cliquable)
OUTIL_ROUTE: int = 1
OUTIL_FEU: int = 2
OUTIL_ROND_POINT: int = 3
OUTIL_AUTOROUTE: int = 4

# Paramètres des feux de circulation, ronds-points et autoroutes
ETAT_FEU_HORIZONTAL_VERT: int = 0
ETAT_FEU_VERTICAL_VERT: int = 1
DUREE_CYCLE_FEU_SECONDES: float = 3.0
INTERVALLE_ALTERNANCE_FEU_FRAMES: int = int(DUREE_CYCLE_FEU_SECONDES * FPS)
MULTIPLICATEUR_VITESSE_AUTOROUTE: float = 2.2
MULTIPLICATEUR_VITESSE_ROND_POINT: float = 1.25
COUT_TRAVERSEE_AUTOROUTE: float = 0.5
COUT_TRAVERSEE_ROND_POINT: float = 0.75
DISTANCE_MIN_AUTOROUTE_CASES: int = 2
FACTEUR_HEURISTIQUE_AVEC_AUTOROUTE: float = 0.05

# Couleurs et dimensions d'affichage des infrastructures spéciales
COULEUR_PONT: tuple[int, int, int] = (74, 80, 92)
COULEUR_BORDURE_PONT: tuple[int, int, int] = (225, 220, 210)
COULEUR_TUNNEL: tuple[int, int, int] = (65, 65, 75)
COULEUR_ENTREE_TUNNEL: tuple[int, int, int] = (35, 35, 42)
COULEUR_ROND_POINT: tuple[int, int, int] = (58, 63, 72)
COULEUR_CENTRE_ROND_POINT: tuple[int, int, int] = (158, 204, 176)
COULEUR_AUTOROUTE: tuple[int, int, int] = (245, 208, 148)
COULEUR_BORDURE_AUTOROUTE: tuple[int, int, int] = (188, 148, 92)
COULEUR_FEU_VERT: tuple[int, int, int] = (118, 198, 154)
COULEUR_FEU_ROUGE: tuple[int, int, int] = (235, 104, 100)
COULEUR_OUTIL_ACTIF: tuple[int, int, int] = (255, 232, 172)
RAYON_EXTERIEUR_ROND_POINT: int = 15
RAYON_INTERIEUR_ROND_POINT: int = 7
RAYON_ENTREE_TUNNEL: int = 10
RAYON_INTERIEUR_TUNNEL: int = 6
RAYON_VOYANT_FEU: int = 3
DECALAGE_VOYANT_FEU: int = 5
LARGEUR_AUTOROUTE: int = 10
BORDURE_AUTOROUTE: int = 2
RAYON_PILIER_AUTOROUTE: int = 8
HAUTEUR_ARCHE_AUTOROUTE: float = 28.0
NB_SEGMENTS_ARCHE_AUTOROUTE: int = 16
COEFFICIENT_PARABOLE_ARCHE: float = 4.0

# Dimensions des boutons de la barre d'outils HUD (en haut)
POSITION_BARRE_OUTILS_X: int = 375
POSITION_BARRE_OUTILS_Y: int = 16
LARGEUR_BOUTON_OUTIL: int = 122
HAUTEUR_BOUTON_OUTIL: int = 42
ESPACEMENT_BOUTONS_OUTIL_X: int = 126
TAILLE_POLICE_OUTIL: int = 20

# Système temporel (horloge visuelle, jours et semaines)
DUREE_JOUR_SECONDES: float = 15.0
DUREE_JOUR_FRAMES: int = int(DUREE_JOUR_SECONDES * FPS)
JOURS_SEMAINE: list[str] = [
    "Lundi",
    "Mardi",
    "Mercredi",
    "Jeudi",
    "Vendredi",
    "Samedi",
    "Dimanche",
]
INDICE_JOUR_LUNDI: int = 0
NUMERO_SEMAINE_INITIALE: int = 1

# Paramètres des récompenses hebdomadaires du Lundi
BONUS_PONT: str = "ponts"
BONUS_TUNNEL: str = "tunnels"
BONUS_FEU: str = "feux"
BONUS_ROND_POINT: str = "ronds_points"
BONUS_AUTOROUTE: str = "autoroutes"
BONUS_STANDARDS_DISPONIBLES: list[str] = [
    BONUS_PONT,
    BONUS_TUNNEL,
    BONUS_FEU,
    BONUS_ROND_POINT,
]
LIBELLES_BONUS_HEBDOMADAIRES: dict[str, str] = {
    BONUS_PONT: "Pont",
    BONUS_TUNNEL: "Tunnel",
    BONUS_FEU: "Feu tricolore",
    BONUS_ROND_POINT: "Rond-point",
    BONUS_AUTOROUTE: "Autoroute",
}
ROUTES_LOT_STANDARD: int = 20
QUANTITE_BONUS_LOT_STANDARD: int = 1
ROUTES_LOT_SPECIAL: int = 10
QUANTITE_AUTOROUTE_LOT_SPECIAL: int = 1
QUANTITE_BONUS_DOUBLE_LOT_SPECIAL: int = 2
PROBABILITE_OFFRE_AUTOROUTE: float = 0.5
INDICE_OPTION_HEBDOMADAIRE_1: int = 0
INDICE_OPTION_HEBDOMADAIRE_2: int = 1
NB_OPTIONS_HEBDOMADAIRES: int = 2

# Paramètres d'affichage de l'horloge HUD et de la modale du Lundi
POSITION_BANDEAU_HORLOGE_X: int = 885
POSITION_BANDEAU_HORLOGE_Y: int = 16
LARGEUR_BANDEAU_HORLOGE: int = 180
HAUTEUR_BANDEAU_HORLOGE: int = 42
DECALAGE_CENTRE_HORLOGE_X: int = 24
RAYON_HORLOGE_HUD: int = 13
EPAISSEUR_AIGUILLE_HORLOGE: int = 2
ANGLE_DEPART_HORLOGE_RAD: float = -1.5707963267948966
ANGLE_TOUR_COMPLET_RAD: float = 6.283185307179586
NB_SEGMENTS_SECTEUR_HORLOGE: int = 24
COULEUR_SECTEUR_HORLOGE: tuple[int, int, int] = (72, 187, 120)
COULEUR_CADRAN_HORLOGE: tuple[int, int, int] = (250, 248, 242)
DECALAGE_TEXTE_HORLOGE_X: int = 14

LARGEUR_PANNEAU_HEBDOMADAIRE: int = 680
HAUTEUR_PANNEAU_HEBDOMADAIRE: int = 340
LARGEUR_CARTE_OFFRE_HEBDO: int = 270
HAUTEUR_CARTE_OFFRE_HEBDO: int = 180
ESPACEMENT_CARTES_OFFRE_X: int = 40
DECALAGE_TITRE_MODALE_HEBDO_Y: int = 42
DECALAGE_SOUS_TITRE_MODALE_HEBDO_Y: int = 82
DECALAGE_CARTES_MODALE_HEBDO_Y: int = 115
DECALAGE_TITRE_CARTE_OFFRE_Y: int = 35
DECALAGE_ROUTES_CARTE_OFFRE_Y: int = 85
DECALAGE_BONUS_CARTE_OFFRE_Y: int = 125
DECALAGE_AIDE_CARTE_OFFRE_Y: int = 158

# Paramètres du Mode Édition (Étape 17)
MODE_EDITION_INITIAL: bool = False
TOUCHE_MODE_EDITION: int = 101
TOUCHE_MODE_EDITION_TAB: int = 9
LIBELLE_MODE_JEU_HUD: str = "Mode Jeu [E] : Editer"
LIBELLE_MODE_EDITION_HUD: str = "Mode Edition [E] : Quitter"
COULEUR_BANDEAU_MODE_JEU: tuple[int, int, int] = (235, 230, 220)
COULEUR_BANDEAU_MODE_EDITION: tuple[int, int, int] = (255, 215, 130)
POSITION_BANDEAU_MODE_X: int = 16
POSITION_BANDEAU_MODE_Y: int = 66
LARGEUR_BANDEAU_MODE: int = 240
HAUTEUR_BANDEAU_MODE: int = 38

# Association des cartes aux thèmes graphiques (Étapes 18 & 19)
THEME_PAR_CARTE: dict[str, str] = {
    CARTE_PLAINE: THEME_CREME_SAUGE,
    CARTE_RIVIERE: THEME_CREME_SAUGE,
    CARTE_MONTAGNES: THEME_CORAIL_LAGON,
    CARTE_ORLEANS: THEME_CREME_SAUGE,
    CARTE_ZURICH: THEME_CORAIL_LAGON,
    CARTE_MANILA: THEME_BLEU_LAGON,
    CARTE_RIO: THEME_VERT_MENTHE,
}

# Configuration détaillée des cartes pour le menu carrousel (Étape 19)
CHEMIN_FICHIER_SCORES: str = "scores.json"
SCORE_INITIAL_DEFAUT: int = 0
CONFIGURATIONS_CARTES: dict[str, dict[str, str | tuple[int, int, int]]] = {
    CARTE_ORLEANS: {
        "nom": CARTE_ORLEANS,
        "description_ligne_1": "La Loire traverse paisiblement",
        "description_ligne_2": "la plaine royale en diagonale.",
        "couleur_bandeau": (158, 204, 176),
        "theme_defaut": THEME_CREME_SAUGE,
        "theme_1": THEME_CREME_SAUGE,
        "theme_2": THEME_MODE_NUIT,
        "theme_3": THEME_CORAIL_LAGON,
    },
    CARTE_ZURICH: {
        "nom": CARTE_ZURICH,
        "description_ligne_1": "La Limmat serpente au coeur",
        "description_ligne_2": "des massifs montagneux alpins.",
        "couleur_bandeau": (232, 118, 118),
        "theme_defaut": THEME_CORAIL_LAGON,
        "theme_1": THEME_CORAIL_LAGON,
        "theme_2": THEME_MODE_NUIT,
        "theme_3": THEME_CREME_SAUGE,
    },
    CARTE_MANILA: {
        "nom": CARTE_MANILA,
        "description_ligne_1": "Un large bras de mer separe",
        "description_ligne_2": "deux rives ponctuees de collines.",
        "couleur_bandeau": (116, 198, 216),
        "theme_defaut": THEME_BLEU_LAGON,
        "theme_1": THEME_BLEU_LAGON,
        "theme_2": THEME_MODE_NUIT,
        "theme_3": THEME_CREME_SAUGE,
    },
    CARTE_RIO: {
        "nom": CARTE_RIO,
        "description_ligne_1": "Construisez entre les plages",
        "description_ligne_2": "et les reliefs escarpes de Rio.",
        "couleur_bandeau": (146, 198, 170),
        "theme_defaut": THEME_VERT_MENTHE,
        "theme_1": THEME_VERT_MENTHE,
        "theme_2": THEME_MODE_NUIT,
        "theme_3": THEME_CREME_SAUGE,
    },
}

# Paramètres de mise en page du menu carrousel Mini Motorways (Étape 19)
COULEUR_FOND_MENU_CARROUSEL: tuple[int, int, int] = (244, 244, 244)
COULEUR_GRILLE_MENU_CARROUSEL: tuple[int, int, int] = (232, 232, 232)
TAILLE_CASE_GRILLE_MENU: int = 24
COULEUR_CORPS_CARTE_MENU: tuple[int, int, int] = (252, 252, 252)
COULEUR_OMBRE_CARTE_MENU: tuple[int, int, int] = (214, 214, 218)
COULEUR_SEPARATEUR_CARTE_MENU: tuple[int, int, int] = (224, 224, 228)
COULEUR_TEXTE_TITRE_CARTE_MENU: tuple[int, int, int] = (48, 52, 60)
COULEUR_TEXTE_DESCRIPTION_MENU: tuple[int, int, int] = (118, 122, 130)
COULEUR_TEXTE_BEST_MENU: tuple[int, int, int] = (88, 92, 100)
COULEUR_ANNEAU_PASTILLE_ACTIVE: tuple[int, int, int] = (48, 52, 60)
COULEUR_ANNEAU_APERCU_CARTE: tuple[int, int, int] = (252, 252, 252)
COULEUR_BOUTON_JOUER_MENU: tuple[int, int, int] = (52, 56, 64)
COULEUR_BOUTON_JOUER_SURVOL: tuple[int, int, int] = (74, 80, 92)
COULEUR_TEXTE_BOUTON_JOUER: tuple[int, int, int] = (250, 248, 242)

LARGEUR_CARTE_CENTRALE_MENU: int = 410
HAUTEUR_CARTE_CENTRALE_MENU: int = 560
HAUTEUR_BANDEAU_CARTE_CENTRALE: int = 275
RAYON_APERCU_CARTE_CENTRALE: int = 104

LARGEUR_CARTE_LATERALE_MENU: int = 360
HAUTEUR_CARTE_LATERALE_MENU: int = 500
HAUTEUR_BANDEAU_CARTE_LATERALE: int = 245
RAYON_APERCU_CARTE_LATERALE: int = 90

CENTRE_CARROUSEL_Y: int = 475
DECALAGE_CARTE_LATERALE_X: int = 445
RAYON_COIN_CARTE_MENU: int = 16
DECALAGE_OMBRE_CARTE_CENTRALE_Y: int = 14
DECALAGE_OMBRE_CARTE_LATERALE_Y: int = 10
EPAISSEUR_ANNEAU_APERCU_MENU: int = 4
FACTEUR_ECHELLE_APERCU_TERRAIN: float = 0.85

NB_PASTILLES_THEME_CARTE: int = 3
INDICE_PASTILLE_GAUCHE: int = -1
INDICE_PASTILLE_CENTRE: int = 0
INDICE_PASTILLE_DROITE: int = 1
RAYON_PASTILLE_THEME_MENU: int = 13
RAYON_ANNEAU_PASTILLE_ACTIVE: int = 17
EPAISSEUR_ANNEAU_PASTILLE: int = 2
ESPACEMENT_PASTILLES_THEME_X: int = 38
DECALAGE_PASTILLES_SOUS_BANDEAU_Y: int = 30
DECALAGE_TITRE_SOUS_BANDEAU_Y: int = 86
DECALAGE_SEPARATEUR_SOUS_BANDEAU_Y: int = 114
DECALAGE_DESC_1_SOUS_BANDEAU_Y: int = 148
DECALAGE_DESC_2_SOUS_BANDEAU_Y: int = 178
MARGE_INTERIEURE_TEXTE_CARTE_X: int = 34
EPAISSEUR_LIGNE_SEPARATEUR_MENU: int = 2

LARGEUR_BOUTON_JOUER_MENU: int = 220
HAUTEUR_BOUTON_JOUER_MENU: int = 54
POSITION_BOUTON_JOUER_Y: int = 865
RAYON_COIN_BOUTON_JOUER: int = 27
TAILLE_POLICE_NOM_VILLE_MENU: int = 38
TAILLE_POLICE_BEST_MENU: int = 26
TAILLE_POLICE_DESCRIPTION_MENU: int = 22
TAILLE_POLICE_BOUTON_JOUER: int = 30
PAS_DEFILEMENT_CARROUSEL: int = 1

# Paramètres esthétiques : ombres portées, reliefs organiques et bâtiments
COULEUR_OMBRE_PORTEE: tuple[int, int, int] = (28, 30, 36)
ALPHA_OMBRE_PORTEE: int = 45
DECALAGE_OMBRE_X: int = 3
DECALAGE_OMBRE_Y: int = 4
DECALAGE_OMBRE_AUTOROUTE_X: int = 6
DECALAGE_OMBRE_AUTOROUTE_Y: int = 18
BORDURE_RELIEF_ORGANIQUE: int = 3
RAYON_SOMMET_RELIEF: int = 11
COULEUR_SOCLE_MAISON: tuple[int, int, int] = (58, 63, 72)
LONGUEUR_ALLEE_MAISON: int = 9
LARGEUR_ALLEE_MAISON: int = 10
MARGE_TOIT_INTERIEUR_MAISON: int = 3
ASSOMBRISSEMENT_FAITE_MAISON: int = 18
COULEUR_CORPS_USINE: tuple[int, int, int] = (58, 63, 72)
COULEUR_LIGNE_PARKING_USINE: tuple[int, int, int] = (230, 232, 236)
MARGE_TOIT_USINE: int = 5
LARGEUR_ZONE_PARKING_USINE: int = 9
NB_PLACES_PARKING_USINE: int = 3
EPAISSEUR_LIGNE_PARKING: int = 1
RAYON_POINT_CENTRE_DEMANDE: int = 1
DIVISEUR_PARITE_USINE: int = 2
RAYON_BADGE_AUTOROUTE: int = 11
BORDURE_BADGE_AUTOROUTE: int = 2
FACTEUR_BEZIER_QUADRATIQUE: float = 2.0
PROGRESSION_MILIEU_COURBE: float = 0.5

# Paramètres du HUD minimaliste Mini Motorways (Étape 18)
JOURS_SEMAINE_ABREGES: dict[str, str] = {
    "Lundi": "LUN",
    "Mardi": "MAR",
    "Mercredi": "MER",
    "Jeudi": "JEU",
    "Vendredi": "VEN",
    "Samedi": "SAM",
    "Dimanche": "DIM",
}
LONGUEUR_ABREVIATION_JOUR: int = 3

# Bouton retour circulaire en haut à gauche
CENTRE_BOUTON_RETOUR_X: int = 38
CENTRE_BOUTON_RETOUR_Y: int = 38
RAYON_BOUTON_RETOUR: int = 20
TAILLE_FLECHE_RETOUR: int = 7
EPAISSEUR_FLECHE_RETOUR: int = 2
COULEUR_FOND_BOUTON_HUD: tuple[int, int, int] = (248, 245, 238)
COULEUR_ICONE_HUD_SOMBRE: tuple[int, int, int] = (48, 52, 60)

# Score avec épingle (pin) et horloge en haut à droite
CENTRE_HORLOGE_HUD_X: int = 1040
CENTRE_HORLOGE_HUD_Y: int = 38
RAYON_HORLOGE_MINIMALISTE: int = 20
POSITION_JOUR_HUD_X: int = 982
POSITION_JOUR_HUD_Y: int = 38
POSITION_SCORE_HUD_X: int = 895
POSITION_SCORE_HUD_Y: int = 38
CENTRE_EPINGLE_SCORE_X: int = 842
CENTRE_EPINGLE_SCORE_Y: int = 34
RAYON_TETE_EPINGLE: int = 7
RAYON_TROU_EPINGLE: int = 3
HAUTEUR_POINTE_EPINGLE: int = 11
DEMI_LARGEUR_POINTE_EPINGLE: int = 5
TAILLE_POLICE_SCORE_HUD: int = 32
TAILLE_POLICE_JOUR_HUD: int = 22

# Dock d'outils minimaliste en bas au centre
CENTRE_DOCK_X: int = LARGEUR_FENETRE // DIVISEUR_MOITIE
CENTRE_DOCK_Y: int = 1030
DEMI_TAILLE_LOSANGE_ROUTES: int = 26
COULEUR_LOSANGE_ROUTES: tuple[int, int, int] = (42, 46, 54)
COULEUR_TEXTE_LOSANGE_ROUTES: tuple[int, int, int] = (248, 246, 240)
RAYON_BOUTON_DOCK: int = 22
ESPACEMENT_BOUTONS_DOCK_X: int = 62
INDICE_DOCK_ROND_POINT: int = -2
INDICE_DOCK_FEU: int = -1
INDICE_DOCK_PONT_TUNNEL: int = 1
INDICE_DOCK_AUTOROUTE: int = 2
INDICE_DOCK_EDITION: int = 3
RAYON_PASTILLE_STOCK_DOCK: int = 9
DECALAGE_PASTILLE_STOCK_X: int = 15
DECALAGE_PASTILLE_STOCK_Y: int = -15
COULEUR_PASTILLE_STOCK: tuple[int, int, int] = (48, 52, 60)
COULEUR_TEXTE_PASTILLE_STOCK: tuple[int, int, int] = (250, 248, 242)
TAILLE_POLICE_PASTILLE_DOCK: int = 16
LARGEUR_ICONE_CORBEILLE: int = 12
HAUTEUR_ICONE_CORBEILLE: int = 14
DECALAGE_COUVERCLE_CORBEILLE_Y: int = 3
