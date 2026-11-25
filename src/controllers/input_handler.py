"""Contrôleur gérant les entrées utilisateur à la souris avec zoom caméra."""

import math
import pygame

from src.config import (
    BOUTON_SOURIS_DROIT,
    BOUTON_SOURIS_GAUCHE,
    COORDONNEE_CAMERA_ORIGINE_FLOAT,
    DECALAGE_VOISIN_NEGATIF,
    DECALAGE_VOISIN_NUL,
    DECALAGE_VOISIN_POSITIF,
    FACTEUR_ECHELLE_UNITE,
    INDICE_BOUTON_DROIT,
    INDICE_BOUTON_GAUCHE,
    TAILLE_CASE,
)
from src.models.grid import Grid


class InputHandler:
    """Traduit les événements souris en actions de tracé ou d'effacement."""

    def __init__(self) -> None:
        """Initialise le gestionnaire d'entrées et la mémoire de tracé."""
        self.derniere_case_tracee: tuple[int, int] | None = None

    def convertir_pixels_en_case(
        self,
        position_x: int,
        position_y: int,
        colonne_debut_camera: float = COORDONNEE_CAMERA_ORIGINE_FLOAT,
        ligne_debut_camera: float = COORDONNEE_CAMERA_ORIGINE_FLOAT,
        taille_case_camera: float = float(TAILLE_CASE),
    ) -> tuple[int, int]:
        """Convertit des coordonnées pixels (x, y) en indices (colonne, ligne).

        Prend en compte le décalage et l'échelle de la caméra zoomée.

        Args:
            position_x: Coordonnée horizontale en pixels écran.
            position_y: Coordonnée verticale en pixels écran.
            colonne_debut_camera: Colonne flottante du bord gauche visible.
            ligne_debut_camera: Ligne flottante du bord supérieur visible.
            taille_case_camera: Taille actuelle d'une case en pixels écran.

        Returns:
            Un tuple (colonne, ligne) correspondant à la case survolée.
        """
        colonne_flottante: float = (
            colonne_debut_camera + float(position_x) / taille_case_camera
        )
        ligne_flottante: float = (
            ligne_debut_camera + float(position_y) / taille_case_camera
        )
        colonne: int = int(math.floor(colonne_flottante))
        ligne: int = int(math.floor(ligne_flottante))
        return (colonne, ligne)

    def calculer_pas_unitaire(self, ecart: int) -> int:
        """Retourne le signe unitaire (-1, 0 ou 1) d'un écart de coordonnées.

        Args:
            ecart: Différence entière entre deux indices.

        Returns:
            -1 si négatif, 1 si positif, 0 si nul.
        """
        if ecart > DECALAGE_VOISIN_NUL:
            return DECALAGE_VOISIN_POSITIF
        else:
            if ecart < DECALAGE_VOISIN_NUL:
                return DECALAGE_VOISIN_NEGATIF
            else:
                return DECALAGE_VOISIN_NUL

    def interpoler_action_entre_cases(
        self,
        grille: Grid,
        case_depart: tuple[int, int],
        case_arrivee: tuple[int, int],
        est_suppression: bool,
    ) -> None:
        """Applique le tracé ou la suppression en continu (incluant diagonales).

        Args:
            grille: Instance du modèle Grid à modifier.
            case_depart: Coordonnée (colonne, ligne) précédente.
            case_arrivee: Coordonnée (colonne, ligne) actuelle.
            est_suppression: True pour supprimer, False pour poser une route.
        """
        colonne_courante, ligne_courante = case_depart
        colonne_cible, ligne_cible = case_arrivee

        while (
            colonne_courante != colonne_cible
            or ligne_courante != ligne_cible
        ):
            pas_colonne: int = self.calculer_pas_unitaire(
                colonne_cible - colonne_courante
            )
            pas_ligne: int = self.calculer_pas_unitaire(
                ligne_cible - ligne_courante
            )
            colonne_courante = colonne_courante + pas_colonne
            ligne_courante = ligne_courante + pas_ligne

            if est_suppression:
                grille.supprimer_route(ligne_courante, colonne_courante)
            else:
                grille.placer_route(ligne_courante, colonne_courante)

    def appliquer_action_clic_gauche(
        self,
        grille: Grid,
        position_x: int,
        position_y: int,
        colonne_debut_camera: float = COORDONNEE_CAMERA_ORIGINE_FLOAT,
        ligne_debut_camera: float = COORDONNEE_CAMERA_ORIGINE_FLOAT,
        taille_case_camera: float = float(TAILLE_CASE),
    ) -> None:
        """Trace une route (avec interpolation diagonale) sous la souris.

        Args:
            grille: Instance du modèle Grid à modifier.
            position_x: Coordonnée horizontale en pixels.
            position_y: Coordonnée verticale en pixels.
            colonne_debut_camera: Colonne flottante du bord gauche visible.
            ligne_debut_camera: Ligne flottante du bord supérieur visible.
            taille_case_camera: Taille actuelle d'une case en pixels écran.
        """
        colonne, ligne = self.convertir_pixels_en_case(
            position_x,
            position_y,
            colonne_debut_camera,
            ligne_debut_camera,
            taille_case_camera,
        )
        case_actuelle: tuple[int, int] = (colonne, ligne)

        if self.derniere_case_tracee is None:
            grille.placer_route(ligne, colonne)
        else:
            self.interpoler_action_entre_cases(
                grille,
                self.derniere_case_tracee,
                case_actuelle,
                est_suppression=False,
            )
        self.derniere_case_tracee = case_actuelle

    def appliquer_action_clic_droit(
        self,
        grille: Grid,
        position_x: int,
        position_y: int,
        colonne_debut_camera: float = COORDONNEE_CAMERA_ORIGINE_FLOAT,
        ligne_debut_camera: float = COORDONNEE_CAMERA_ORIGINE_FLOAT,
        taille_case_camera: float = float(TAILLE_CASE),
    ) -> None:
        """Efface une route (avec interpolation diagonale) sous la souris.

        Args:
            grille: Instance du modèle Grid à modifier.
            position_x: Coordonnée horizontale en pixels.
            position_y: Coordonnée verticale en pixels.
            colonne_debut_camera: Colonne flottante du bord gauche visible.
            ligne_debut_camera: Ligne flottante du bord supérieur visible.
            taille_case_camera: Taille actuelle d'une case en pixels écran.
        """
        colonne, ligne = self.convertir_pixels_en_case(
            position_x,
            position_y,
            colonne_debut_camera,
            ligne_debut_camera,
            taille_case_camera,
        )
        case_actuelle: tuple[int, int] = (colonne, ligne)

        if self.derniere_case_tracee is None:
            grille.supprimer_route(ligne, colonne)
        else:
            self.interpoler_action_entre_cases(
                grille,
                self.derniere_case_tracee,
                case_actuelle,
                est_suppression=True,
            )
        self.derniere_case_tracee = case_actuelle

    def gerer_evenement(
        self,
        evenement: pygame.event.Event,
        grille: Grid,
        parametres_camera: tuple[float, float, float, float] | None = None,
    ) -> None:
        """Traite un événement Pygame lié au clic ou au déplacement souris.

        Args:
            evenement: Événement Pygame capturé dans la boucle principale.
            grille: Instance du modèle Grid sur laquelle agir.
            parametres_camera: Tuple optionnel (colonne_debut, ligne_debut,
                taille_case_camera, facteur_zoom).
        """
        if parametres_camera is not None:
            colonne_debut, ligne_debut, taille_case_cam, _ = parametres_camera
        else:
            colonne_debut = COORDONNEE_CAMERA_ORIGINE_FLOAT
            ligne_debut = COORDONNEE_CAMERA_ORIGINE_FLOAT
            taille_case_cam = float(TAILLE_CASE) * FACTEUR_ECHELLE_UNITE

        if evenement.type == pygame.MOUSEBUTTONDOWN:
            self.derniere_case_tracee = None
            position_x, position_y = evenement.pos
            if evenement.button == BOUTON_SOURIS_GAUCHE:
                self.appliquer_action_clic_gauche(
                    grille,
                    position_x,
                    position_y,
                    colonne_debut,
                    ligne_debut,
                    taille_case_cam,
                )
            else:
                if evenement.button == BOUTON_SOURIS_DROIT:
                    self.appliquer_action_clic_droit(
                        grille,
                        position_x,
                        position_y,
                        colonne_debut,
                        ligne_debut,
                        taille_case_cam,
                    )
                else:
                    pass
        else:
            if evenement.type == pygame.MOUSEBUTTONUP:
                self.derniere_case_tracee = None
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
                            colonne_debut,
                            ligne_debut,
                            taille_case_cam,
                        )
                    else:
                        if boutons_presses[INDICE_BOUTON_DROIT]:
                            self.appliquer_action_clic_droit(
                                grille,
                                position_x,
                                position_y,
                                colonne_debut,
                                ligne_debut,
                                taille_case_cam,
                            )
                        else:
                            self.derniere_case_tracee = None
                else:
                    pass
