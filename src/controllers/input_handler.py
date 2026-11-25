"""Contrôleur gérant les entrées utilisateur à la souris pour les routes."""

import pygame

from src.config import (
    BOUTON_SOURIS_DROIT,
    BOUTON_SOURIS_GAUCHE,
    INDICE_BOUTON_DROIT,
    INDICE_BOUTON_GAUCHE,
    TAILLE_CASE,
)
from src.models.grid import Grid


class InputHandler:
    """Traduit les événements souris en actions de tracé ou d'effacement."""

    def convertir_pixels_en_case(
        self,
        position_x: int,
        position_y: int,
    ) -> tuple[int, int]:
        """Convertit des coordonnées pixels (x, y) en indices (colonne, ligne).

        Args:
            position_x: Coordonnée horizontale en pixels.
            position_y: Coordonnée verticale en pixels.

        Returns:
            Un tuple (colonne, ligne) correspondant à la case survolée.
        """
        colonne: int = position_x // TAILLE_CASE
        ligne: int = position_y // TAILLE_CASE
        return (colonne, ligne)

    def appliquer_action_clic_gauche(
        self,
        grille: Grid,
        position_x: int,
        position_y: int,
    ) -> None:
        """Trace une route sur la case correspondant à la position de la souris.

        Args:
            grille: Instance du modèle Grid à modifier.
            position_x: Coordonnée horizontale en pixels.
            position_y: Coordonnée verticale en pixels.
        """
        colonne, ligne = self.convertir_pixels_en_case(position_x, position_y)
        grille.placer_route(ligne, colonne)

    def appliquer_action_clic_droit(
        self,
        grille: Grid,
        position_x: int,
        position_y: int,
    ) -> None:
        """Efface une route sur la case correspondant à la position de la souris.

        Args:
            grille: Instance du modèle Grid à modifier.
            position_x: Coordonnée horizontale en pixels.
            position_y: Coordonnée verticale en pixels.
        """
        colonne, ligne = self.convertir_pixels_en_case(position_x, position_y)
        grille.supprimer_route(ligne, colonne)

    def gerer_evenement(
        self,
        evenement: pygame.event.Event,
        grille: Grid,
    ) -> None:
        """Traite un événement Pygame lié au clic ou au déplacement souris.

        Args:
            evenement: Événement Pygame capturé dans la boucle principale.
            grille: Instance du modèle Grid sur laquelle agir.
        """
        if evenement.type == pygame.MOUSEBUTTONDOWN:
            position_x, position_y = evenement.pos
            if evenement.button == BOUTON_SOURIS_GAUCHE:
                self.appliquer_action_clic_gauche(
                    grille,
                    position_x,
                    position_y,
                )
            else:
                if evenement.button == BOUTON_SOURIS_DROIT:
                    self.appliquer_action_clic_droit(
                        grille,
                        position_x,
                        position_y,
                    )
                else:
                    pass
        else:
            if evenement.type == pygame.MOUSEMOTION:
                position_x, position_y = evenement.pos
                boutons_presses: tuple[bool, bool, bool] = (
                    pygame.mouse.get_pressed()
                )
                if boutons_presses[INDICE_BOUTON_GAUCHE]:
                    self.appliquer_action_clic_gauche(
                        grille,
                        position_x,
                        position_y,
                    )
                else:
                    if boutons_presses[INDICE_BOUTON_DROIT]:
                        self.appliquer_action_clic_droit(
                            grille,
                            position_x,
                            position_y,
                        )
                    else:
                        pass
            else:
                pass
