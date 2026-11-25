"""Tests unitaires de l'algorithme de pathfinding A* (sans Pygame)."""

from src.config import (
    COULEUR_BLEUE,
    COULEUR_ROUGE,
    INDICE_TEST_CINQ,
    INDICE_TEST_DEUX,
    INDICE_TEST_NEGATIF,
    INDICE_TEST_NEUF,
    INDICE_TEST_QUATRE,
    INDICE_TEST_SIX,
    INDICE_TEST_TROIS,
    INDICE_TEST_UN,
    INDICE_TEST_ZERO,
    LONGUEUR_CHEMIN_UN,
    LONGUEUR_LISTE_VIDE,
    TAILLE_GRILLE_TEST,
)
from src.models.entity import Maison, Usine
from src.models.grid import Grid
from src.models.pathfinding import (
    calculer_distance_manhattan,
    trouver_chemin_a_etoile,
)


def test_chemin_direct_maison_vers_usine() -> None:
    """Vérifie le calcul d'un chemin direct horizontal entre Maison et Usine."""
    grille: Grid = Grid(TAILLE_GRILLE_TEST, TAILLE_GRILLE_TEST)
    maison: Maison = Maison(INDICE_TEST_DEUX, INDICE_TEST_UN, COULEUR_ROUGE)
    usine: Usine = Usine(INDICE_TEST_DEUX, INDICE_TEST_CINQ, COULEUR_ROUGE)
    grille.placer_maison(maison)
    grille.placer_usine(usine)

    grille.placer_route(INDICE_TEST_DEUX, INDICE_TEST_DEUX)
    grille.placer_route(INDICE_TEST_DEUX, INDICE_TEST_TROIS)
    grille.placer_route(INDICE_TEST_DEUX, INDICE_TEST_QUATRE)

    depart: tuple[int, int] = (INDICE_TEST_UN, INDICE_TEST_DEUX)
    arrivee: tuple[int, int] = (INDICE_TEST_CINQ, INDICE_TEST_DEUX)

    chemin: list[tuple[int, int]] = trouver_chemin_a_etoile(
        grille,
        depart,
        arrivee,
    )
    chemin_attendu: list[tuple[int, int]] = [
        (INDICE_TEST_UN, INDICE_TEST_DEUX),
        (INDICE_TEST_DEUX, INDICE_TEST_DEUX),
        (INDICE_TEST_TROIS, INDICE_TEST_DEUX),
        (INDICE_TEST_QUATRE, INDICE_TEST_DEUX),
        (INDICE_TEST_CINQ, INDICE_TEST_DEUX),
    ]
    assert chemin == chemin_attendu


def test_contournement_obstacle_et_choix_chemin_plus_court() -> None:
    """Vérifie qu'A* contourne un bâtiment et choisit le plus court détour."""
    grille: Grid = Grid(TAILLE_GRILLE_TEST, TAILLE_GRILLE_TEST)
    maison_depart: Maison = Maison(
        INDICE_TEST_DEUX,
        INDICE_TEST_UN,
        COULEUR_ROUGE,
    )
    usine_arrivee: Usine = Usine(
        INDICE_TEST_DEUX,
        INDICE_TEST_TROIS,
        COULEUR_ROUGE,
    )
    batiment_obstacle: Maison = Maison(
        INDICE_TEST_DEUX,
        INDICE_TEST_DEUX,
        COULEUR_BLEUE,
    )
    grille.placer_maison(maison_depart)
    grille.placer_usine(usine_arrivee)
    grille.placer_maison(batiment_obstacle)

    # Détour court par le haut (ligne 1)
    grille.placer_route(INDICE_TEST_UN, INDICE_TEST_UN)
    grille.placer_route(INDICE_TEST_UN, INDICE_TEST_DEUX)
    grille.placer_route(INDICE_TEST_UN, INDICE_TEST_TROIS)

    # Détour plus long par le bas (lignes 3 et 4)
    grille.placer_route(INDICE_TEST_TROIS, INDICE_TEST_UN)
    grille.placer_route(INDICE_TEST_QUATRE, INDICE_TEST_UN)
    grille.placer_route(INDICE_TEST_QUATRE, INDICE_TEST_DEUX)
    grille.placer_route(INDICE_TEST_QUATRE, INDICE_TEST_TROIS)
    grille.placer_route(INDICE_TEST_TROIS, INDICE_TEST_TROIS)

    depart: tuple[int, int] = (INDICE_TEST_UN, INDICE_TEST_DEUX)
    arrivee: tuple[int, int] = (INDICE_TEST_TROIS, INDICE_TEST_DEUX)

    chemin: list[tuple[int, int]] = trouver_chemin_a_etoile(
        grille,
        depart,
        arrivee,
    )
    chemin_court_attendu: list[tuple[int, int]] = [
        (INDICE_TEST_UN, INDICE_TEST_DEUX),
        (INDICE_TEST_UN, INDICE_TEST_UN),
        (INDICE_TEST_DEUX, INDICE_TEST_UN),
        (INDICE_TEST_TROIS, INDICE_TEST_UN),
        (INDICE_TEST_TROIS, INDICE_TEST_DEUX),
    ]
    assert chemin == chemin_court_attendu


def test_reseau_deconnecte_ou_bloque() -> None:
    """Vérifie qu'un réseau coupé retourne une liste vide sans erreur."""
    grille: Grid = Grid(TAILLE_GRILLE_TEST, TAILLE_GRILLE_TEST)
    maison: Maison = Maison(INDICE_TEST_UN, INDICE_TEST_UN, COULEUR_ROUGE)
    usine: Usine = Usine(INDICE_TEST_UN, INDICE_TEST_SIX, COULEUR_ROUGE)
    grille.placer_maison(maison)
    grille.placer_usine(usine)

    # Route incomplète (trou en colonne 4)
    grille.placer_route(INDICE_TEST_UN, INDICE_TEST_DEUX)
    grille.placer_route(INDICE_TEST_UN, INDICE_TEST_TROIS)
    grille.placer_route(INDICE_TEST_UN, INDICE_TEST_CINQ)

    depart: tuple[int, int] = (INDICE_TEST_UN, INDICE_TEST_UN)
    arrivee: tuple[int, int] = (INDICE_TEST_SIX, INDICE_TEST_UN)

    chemin: list[tuple[int, int]] = trouver_chemin_a_etoile(
        grille,
        depart,
        arrivee,
    )
    assert len(chemin) == LONGUEUR_LISTE_VIDE


def test_comportement_aux_limites_de_la_grille() -> None:
    """Vérifie le pathfinding sur les bords et hors des limites de la grille."""
    grille: Grid = Grid(TAILLE_GRILLE_TEST, TAILLE_GRILLE_TEST)

    # Chemin sur le bord supérieur et droit jusqu'au coin (9, 0)
    depart_bord: tuple[int, int] = (INDICE_TEST_ZERO, INDICE_TEST_ZERO)
    arrivee_bord: tuple[int, int] = (INDICE_TEST_DEUX, INDICE_TEST_ZERO)
    grille.placer_route(INDICE_TEST_ZERO, INDICE_TEST_UN)

    chemin_bord: list[tuple[int, int]] = trouver_chemin_a_etoile(
        grille,
        depart_bord,
        arrivee_bord,
    )
    assert chemin_bord == [
        (INDICE_TEST_ZERO, INDICE_TEST_ZERO),
        (INDICE_TEST_UN, INDICE_TEST_ZERO),
        (INDICE_TEST_DEUX, INDICE_TEST_ZERO),
    ]

    # Coordonnées hors limites
    depart_hors_limite: tuple[int, int] = (
        INDICE_TEST_NEGATIF,
        INDICE_TEST_ZERO,
    )
    arrivee_hors_limite: tuple[int, int] = (
        TAILLE_GRILLE_TEST,
        INDICE_TEST_NEUF,
    )
    assert (
        len(
            trouver_chemin_a_etoile(
                grille,
                depart_hors_limite,
                arrivee_bord,
            )
        )
        == LONGUEUR_LISTE_VIDE
    )
    assert (
        len(
            trouver_chemin_a_etoile(
                grille,
                depart_bord,
                arrivee_hors_limite,
            )
        )
        == LONGUEUR_LISTE_VIDE
    )

    # Départ identique à l'arrivée
    chemin_sur_place: list[tuple[int, int]] = trouver_chemin_a_etoile(
        grille,
        depart_bord,
        depart_bord,
    )
    assert len(chemin_sur_place) == LONGUEUR_CHEMIN_UN
    assert calculer_distance_manhattan(depart_bord, depart_bord) == (
        INDICE_TEST_ZERO
    )
