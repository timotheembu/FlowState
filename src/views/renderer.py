"""Vue chargée du rendu graphique Pygame de la grille et des bâtiments."""

import pygame

from src.config import (
    COORDONNEE_ORIGINE,
    COULEUR_CONTOUR_BATIMENT,
    COULEUR_FOND,
    COULEUR_GRILLE,
    EPAISSEUR_CONTOUR_USINE,
    EPAISSEUR_LIGNE_GRILLE,
    FACTEUR_DOUBLE_MARGE,
    HAUTEUR_FENETRE,
    INCREMENT_BORNE_GRILLE,
    LARGEUR_FENETRE,
    MARGE_MAISON,
    MARGE_USINE,
    RAYON_BORDURE_MAISON,
    RAYON_BORDURE_USINE,
    TAILLE_CASE,
)
from src.models.entity import Maison, Usine
from src.models.grid import Grid


class Renderer:
    """Gère l'affichage graphique du jeu sur la fenêtre Pygame."""

    def __init__(self, ecran: pygame.Surface) -> None:
        """Initialise le moteur de rendu avec la surface principale.

        Args:
            ecran: Surface Pygame sur laquelle dessiner.
        """
        self.ecran: pygame.Surface = ecran

    def dessiner_fond(self) -> None:
        """Remplit l'écran avec la couleur de fond."""
        self.ecran.fill(COULEUR_FOND)

    def dessiner_grille(self, grille: Grid) -> None:
        """Trace les lignes horizontales et verticales de la grille.

        Args:
            grille: Instance du modèle Grid à représenter.
        """
        nb_traits_horizontaux: int = (
            grille.nb_lignes + INCREMENT_BORNE_GRILLE
        )
        for indice_ligne in range(nb_traits_horizontaux):
            position_y: int = indice_ligne * TAILLE_CASE
            point_depart_horizontal: tuple[int, int] = (
                COORDONNEE_ORIGINE,
                position_y,
            )
            point_fin_horizontal: tuple[int, int] = (
                LARGEUR_FENETRE,
                position_y,
            )
            pygame.draw.line(
                self.ecran,
                COULEUR_GRILLE,
                point_depart_horizontal,
                point_fin_horizontal,
                EPAISSEUR_LIGNE_GRILLE,
            )

        nb_traits_verticaux: int = (
            grille.nb_colonnes + INCREMENT_BORNE_GRILLE
        )
        for indice_colonne in range(nb_traits_verticaux):
            position_x: int = indice_colonne * TAILLE_CASE
            point_depart_vertical: tuple[int, int] = (
                position_x,
                COORDONNEE_ORIGINE,
            )
            point_fin_vertical: tuple[int, int] = (
                position_x,
                HAUTEUR_FENETRE,
            )
            pygame.draw.line(
                self.ecran,
                COULEUR_GRILLE,
                point_depart_vertical,
                point_fin_vertical,
                EPAISSEUR_LIGNE_GRILLE,
            )

    def dessiner_maisons(self, maisons: list[Maison]) -> None:
        """Dessine chaque maison sous forme de petit carré plein arrondi.

        Args:
            maisons: Liste des instances de Maison à dessiner.
        """
        taille_maison: int = (
            TAILLE_CASE - FACTEUR_DOUBLE_MARGE * MARGE_MAISON
        )
        for maison in maisons:
            position_x: int = maison.colonne * TAILLE_CASE + MARGE_MAISON
            position_y: int = maison.ligne * TAILLE_CASE + MARGE_MAISON
            rectangle_maison: pygame.Rect = pygame.Rect(
                position_x,
                position_y,
                taille_maison,
                taille_maison,
            )
            pygame.draw.rect(
                self.ecran,
                maison.couleur,
                rectangle_maison,
                border_radius=RAYON_BORDURE_MAISON,
            )

    def dessiner_usines(self, usines: list[Usine]) -> None:
        """Dessine chaque usine sous forme de grand carré bordé.

        Args:
            usines: Liste des instances de Usine à dessiner.
        """
        taille_usine: int = (
            TAILLE_CASE - FACTEUR_DOUBLE_MARGE * MARGE_USINE
        )
        for usine in usines:
            position_x: int = usine.colonne * TAILLE_CASE + MARGE_USINE
            position_y: int = usine.ligne * TAILLE_CASE + MARGE_USINE
            rectangle_usine: pygame.Rect = pygame.Rect(
                position_x,
                position_y,
                taille_usine,
                taille_usine,
            )
            pygame.draw.rect(
                self.ecran,
                usine.couleur,
                rectangle_usine,
                border_radius=RAYON_BORDURE_USINE,
            )
            pygame.draw.rect(
                self.ecran,
                COULEUR_CONTOUR_BATIMENT,
                rectangle_usine,
                width=EPAISSEUR_CONTOUR_USINE,
                border_radius=RAYON_BORDURE_USINE,
            )

    def afficher(self, grille: Grid) -> None:
        """Effectue le rendu complet d'une frame et met à jour l'écran.

        Args:
            grille: Instance du modèle Grid à afficher.
        """
        self.dessiner_fond()
        self.dessiner_grille(grille)
        self.dessiner_maisons(grille.maisons)
        self.dessiner_usines(grille.usines)
        pygame.display.flip()
