"""Tests unitaires du modèle Grid (sans dépendance à Pygame)."""

import pytest

from src.config import (
    CASE_MAISON,
    CASE_ROUTE,
    CASE_USINE,
    CASE_VIDE,
    COULEUR_BLEUE,
    COULEUR_ROUGE,
    INDICE_TEST_CINQ,
    INDICE_TEST_DEUX,
    INDICE_TEST_NEGATIF,
    INDICE_TEST_QUATRE,
    INDICE_TEST_TROIS,
    INDICE_TEST_UN,
    INDICE_TEST_ZERO,
    LONGUEUR_LISTE_VIDE,
    STOCK_ROUTES_EPUISE,
    STOCK_TEST_LIMITE,
    TAILLE_GRILLE_TEST,
    UNITE_STOCK_ROUTE,
)
from src.models.entity import Maison, Usine
from src.models.grid import Grid


def test_initialisation_et_reinitialisation_grille() -> None:
    """Vérifie que la grille s'initialise avec des cases vides."""
    grille: Grid = Grid(TAILLE_GRILLE_TEST, TAILLE_GRILLE_TEST)
    assert grille.nb_lignes == TAILLE_GRILLE_TEST
    assert grille.nb_colonnes == TAILLE_GRILLE_TEST
    assert len(grille.maisons) == LONGUEUR_LISTE_VIDE
    assert len(grille.usines) == LONGUEUR_LISTE_VIDE
    assert (
        grille.obtenir_etat_case(INDICE_TEST_ZERO, INDICE_TEST_ZERO)
        == CASE_VIDE
    )


def test_validation_coordonnees_et_exceptions_limites() -> None:
    """Vérifie la détection des coordonnées hors limites de la grille."""
    grille: Grid = Grid(TAILLE_GRILLE_TEST, TAILLE_GRILLE_TEST)

    assert grille.est_coordonnee_valide(INDICE_TEST_ZERO, INDICE_TEST_ZERO)
    assert not grille.est_coordonnee_valide(
        INDICE_TEST_NEGATIF,
        INDICE_TEST_ZERO,
    )
    assert not grille.est_coordonnee_valide(
        TAILLE_GRILLE_TEST,
        INDICE_TEST_ZERO,
    )
    assert not grille.est_coordonnee_valide(
        INDICE_TEST_ZERO,
        TAILLE_GRILLE_TEST,
    )

    with pytest.raises(ValueError):
        grille.obtenir_etat_case(INDICE_TEST_NEGATIF, INDICE_TEST_ZERO)

    with pytest.raises(ValueError):
        grille.definir_etat_case(
            TAILLE_GRILLE_TEST,
            INDICE_TEST_ZERO,
            CASE_ROUTE,
        )


def test_protection_batiments_contre_routes() -> None:
    """Vérifie qu'une route ne peut ni écraser ni supprimer un bâtiment."""
    grille: Grid = Grid(TAILLE_GRILLE_TEST, TAILLE_GRILLE_TEST)
    maison: Maison = Maison(INDICE_TEST_DEUX, INDICE_TEST_TROIS, COULEUR_ROUGE)
    usine: Usine = Usine(INDICE_TEST_QUATRE, INDICE_TEST_CINQ, COULEUR_BLEUE)

    assert grille.placer_maison(maison)
    assert grille.placer_usine(usine)

    assert not grille.placer_route(INDICE_TEST_DEUX, INDICE_TEST_TROIS)
    assert not grille.placer_route(INDICE_TEST_QUATRE, INDICE_TEST_CINQ)
    assert not grille.supprimer_route(INDICE_TEST_DEUX, INDICE_TEST_TROIS)
    assert not grille.supprimer_route(INDICE_TEST_QUATRE, INDICE_TEST_CINQ)

    assert (
        grille.obtenir_etat_case(INDICE_TEST_DEUX, INDICE_TEST_TROIS)
        == CASE_MAISON
    )
    assert (
        grille.obtenir_etat_case(INDICE_TEST_QUATRE, INDICE_TEST_CINQ)
        == CASE_USINE
    )


def test_pose_et_suppression_route() -> None:
    """Vérifie la pose et la suppression d'une route sur une case vide."""
    grille: Grid = Grid(TAILLE_GRILLE_TEST, TAILLE_GRILLE_TEST)

    assert grille.placer_route(INDICE_TEST_UN, INDICE_TEST_UN)
    assert grille.est_case_route(INDICE_TEST_UN, INDICE_TEST_UN)
    assert not grille.placer_route(INDICE_TEST_UN, INDICE_TEST_UN)

    assert grille.supprimer_route(INDICE_TEST_UN, INDICE_TEST_UN)
    assert grille.est_case_libre(INDICE_TEST_UN, INDICE_TEST_UN)
    assert not grille.supprimer_route(INDICE_TEST_UN, INDICE_TEST_UN)


def test_voisins_accessibles_et_traversabilite() -> None:
    """Vérifie que seules les routes et bornes du trajet sont traversables."""
    grille: Grid = Grid(TAILLE_GRILLE_TEST, TAILLE_GRILLE_TEST)
    depart: tuple[int, int] = (INDICE_TEST_UN, INDICE_TEST_UN)
    arrivee: tuple[int, int] = (INDICE_TEST_TROIS, INDICE_TEST_UN)

    maison_depart: Maison = Maison(
        INDICE_TEST_UN,
        INDICE_TEST_UN,
        COULEUR_ROUGE,
    )
    usine_arrivee: Usine = Usine(
        INDICE_TEST_UN,
        INDICE_TEST_TROIS,
        COULEUR_ROUGE,
    )
    maison_obstacle: Maison = Maison(
        INDICE_TEST_DEUX,
        INDICE_TEST_DEUX,
        COULEUR_BLEUE,
    )

    grille.placer_maison(maison_depart)
    grille.placer_usine(usine_arrivee)
    grille.placer_maison(maison_obstacle)
    grille.placer_route(INDICE_TEST_UN, INDICE_TEST_DEUX)

    case_route: tuple[int, int] = (INDICE_TEST_DEUX, INDICE_TEST_UN)
    voisins: list[tuple[int, int]] = grille.obtenir_voisins_accessibles(
        case_route,
        depart,
        arrivee,
    )

    assert depart in voisins
    assert arrivee in voisins
    assert (INDICE_TEST_DEUX, INDICE_TEST_DEUX) not in voisins
    assert (INDICE_TEST_DEUX, INDICE_TEST_ZERO) not in voisins


def test_voisins_diagonaux_et_gestion_stock_routes() -> None:
    """Vérifie l'accès aux voisins diagonaux et la limite du stock de routes."""
    grille: Grid = Grid(
        TAILLE_GRILLE_TEST,
        TAILLE_GRILLE_TEST,
        stock_routes_initial=STOCK_TEST_LIMITE,
    )
    assert grille.stock_routes == STOCK_TEST_LIMITE

    assert grille.placer_route(INDICE_TEST_UN, INDICE_TEST_UN)
    assert grille.stock_routes == STOCK_TEST_LIMITE - UNITE_STOCK_ROUTE

    assert grille.placer_route(INDICE_TEST_DEUX, INDICE_TEST_DEUX)
    assert grille.stock_routes == STOCK_ROUTES_EPUISE

    # Stock épuisé : impossible de poser une troisième route
    assert not grille.placer_route(INDICE_TEST_TROIS, INDICE_TEST_TROIS)
    assert not grille.est_case_route(INDICE_TEST_TROIS, INDICE_TEST_TROIS)

    # Les deux routes posées en (1,1) et (2,2) sont voisines en diagonale
    depart: tuple[int, int] = (INDICE_TEST_ZERO, INDICE_TEST_ZERO)
    arrivee: tuple[int, int] = (INDICE_TEST_TROIS, INDICE_TEST_TROIS)
    voisins_un_un: list[tuple[int, int]] = grille.obtenir_voisins_accessibles(
        (INDICE_TEST_UN, INDICE_TEST_UN),
        depart,
        arrivee,
    )
    assert (INDICE_TEST_DEUX, INDICE_TEST_DEUX) in voisins_un_un
    assert depart in voisins_un_un

    # Remboursement du stock à la suppression
    assert grille.supprimer_route(INDICE_TEST_DEUX, INDICE_TEST_DEUX)
    assert grille.stock_routes == UNITE_STOCK_ROUTE
