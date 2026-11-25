"""Vue chargée du rendu graphique Pygame de la grille."""

import pygame

from src.config import (
    COORDONNEE_ORIGINE,
    COULEUR_FOND,
    COULEUR_GRILLE,
    EPAISSEUR_LIGNE_GRILLE,
    HAUTEUR_FENETRE,
    INCREMENT_BORNE_GRILLE,
    LARGEUR_FENETRE,
    TAILLE_CASE,
)
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

    def afficher(self, grille: Grid) -> None:
        """Effectue le rendu complet d'une frame et met à jour l'écran.

        Args:
            grille: Instance du modèle Grid à afficher.
        """
        self.dessiner_fond()
        self.dessiner_grille(grille)
        pygame.display.flip()
