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
    ESPACEMENT_BOUTONS_OUTIL_X,
    FACTEUR_ECHELLE_UNITE,
    HAUTEUR_BOUTON_OUTIL,
    INDICE_AVANT_DERNIERE_CASE_TRACEE,
    INDICE_BOUTON_DROIT,
    INDICE_BOUTON_GAUCHE,
    INDICE_DERNIERE_CASE_TRACEE,
    LARGEUR_BOUTON_OUTIL,
    OUTIL_AUTOROUTE,
    OUTIL_FEU,
    OUTIL_ROND_POINT,
    OUTIL_ROUTE,
    POSITION_BARRE_OUTILS_X,
    POSITION_BARRE_OUTILS_Y,
    TAILLE_CASE,
    TAILLE_MIN_HISTORIQUE_ELAGAGE,
)
from src.models.entity import Maison, Usine
from src.models.grid import Grid


class InputHandler:
    """Traduit les événements souris et clavier en actions de construction."""

    def __init__(self) -> None:
        """Initialise le gestionnaire d'entrées, la mémoire et l'outil actif."""
        self.derniere_case_tracee: tuple[int, int] | None = None
        self.historique_trace_courant: list[tuple[int, int]] = []
        self.maison_en_reorientation: Maison | None = None
        self.usine_en_reorientation: Usine | None = None
        self.outil_actif: int = OUTIL_ROUTE
        self.depart_autoroute_selectionne: tuple[int, int] | None = None

    def definir_outil_actif(self, nouvel_outil: int) -> None:
        """Change l'outil de construction actif et réinitialise la sélection.

        Args:
            nouvel_outil: Identifiant de l'outil (OUTIL_ROUTE, OUTIL_FEU, etc.).
        """
        self.outil_actif = nouvel_outil
        self.depart_autoroute_selectionne = None
        self.derniere_case_tracee = None
        self.historique_trace_courant = []

    def verifier_clic_barre_outils_hud(
        self,
        position_x: int,
        position_y: int,
    ) -> bool:
        """Vérifie si un clic souris sélectionne un bouton d'outil dans le HUD.

        Args:
            position_x: Coordonnée X du clic en pixels écran.
            position_y: Coordonnée Y du clic en pixels écran.

        Returns:
            True si un bouton d'outil du HUD a été cliqué, False sinon.
        """
        outils_hud: list[int] = [
            OUTIL_ROUTE,
            OUTIL_FEU,
            OUTIL_ROND_POINT,
            OUTIL_AUTOROUTE,
        ]
        for indice_outil, code_outil in enumerate(outils_hud):
            bouton_x: int = (
                POSITION_BARRE_OUTILS_X
                + indice_outil * ESPACEMENT_BOUTONS_OUTIL_X
            )
            rectangle_outil: pygame.Rect = pygame.Rect(
                bouton_x,
                POSITION_BARRE_OUTILS_Y,
                LARGEUR_BOUTON_OUTIL,
                HAUTEUR_BOUTON_OUTIL,
            )
            if rectangle_outil.collidepoint((position_x, position_y)):
                self.definir_outil_actif(code_outil)
                return True
            else:
                pass
        return False

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

    def enregistrer_et_nettoyer_case_tracee(
        self,
        grille: Grid,
        case_nouvelle: tuple[int, int],
        a_ete_posee: bool,
    ) -> None:
        """Enregistre une case posée et annule uniquement un demi-tour A->B->A.

        Conserve intacts tous les virages à 90 degrés (A -> B -> C avec C != A)
        afin que le joueur puisse tracer librement des angles droits sans
        relâcher le clic gauche, tout en supprimant B si le joueur revient
        immédiatement sur A (A -> B -> A) sans connexion externe sur B.

        Args:
            grille: Instance du modèle Grid à mettre à jour.
            case_nouvelle: Coordonnée (colonne, ligne) de la case actuelle.
            a_ete_posee: True si la case vient d'être posée dans ce tracé.
        """
        colonne_c, ligne_c = case_nouvelle
        est_route_active: bool = grille.est_case_route(ligne_c, colonne_c)
        if not a_ete_posee and not est_route_active:
            return
        else:
            pass

        if len(self.historique_trace_courant) >= TAILLE_MIN_HISTORIQUE_ELAGAGE:
            case_b: tuple[int, int] = self.historique_trace_courant[
                INDICE_DERNIERE_CASE_TRACEE
            ]
            case_a: tuple[int, int] = self.historique_trace_courant[
                INDICE_AVANT_DERNIERE_CASE_TRACEE
            ]
            if case_nouvelle == case_a:
                cases_du_demi_tour: list[tuple[int, int]] = [case_a]
                a_lien_externe: bool = (
                    grille.a_connexion_externe_hors_ensemble(
                        case_b,
                        cases_du_demi_tour,
                    )
                )
                if not a_lien_externe:
                    colonne_b, ligne_b = case_b
                    supprimee: bool = grille.supprimer_route(
                        ligne_b,
                        colonne_b,
                    )
                    if supprimee:
                        self.historique_trace_courant.pop()
                    else:
                        pass
                else:
                    pass
                return
            else:
                pass
        else:
            pass

        if a_ete_posee or est_route_active:
            if (
                len(self.historique_trace_courant)
                == DECALAGE_VOISIN_NUL
                or self.historique_trace_courant[INDICE_DERNIERE_CASE_TRACEE]
                != case_nouvelle
            ):
                self.historique_trace_courant.append(case_nouvelle)
            else:
                pass
        else:
            pass

    def interpoler_action_entre_cases(
        self,
        grille: Grid,
        case_depart: tuple[int, int],
        case_arrivee: tuple[int, int],
        est_suppression: bool,
    ) -> None:
        """Applique le tracé, la connexion explicite ou la suppression en continu.

        Lors d'un glissement clic gauche d'une case A vers une case B, pose
        une route sur B si elle est vide ET appelle connecter_cases(A, B).

        Args:
            grille: Instance du modèle Grid à modifier.
            case_depart: Coordonnée (colonne, ligne) précédente.
            case_arrivee: Coordonnée (colonne, ligne) actuelle.
            est_suppression: True pour supprimer, False pour poser et relier.
        """
        colonne_courante, ligne_courante = case_depart
        colonne_cible, ligne_cible = case_arrivee

        while (
            colonne_courante != colonne_cible
            or ligne_courante != ligne_cible
        ):
            case_precedente: tuple[int, int] = (
                colonne_courante,
                ligne_courante,
            )
            pas_colonne: int = self.calculer_pas_unitaire(
                colonne_cible - colonne_courante
            )
            pas_ligne: int = self.calculer_pas_unitaire(
                ligne_cible - ligne_courante
            )
            colonne_courante = colonne_courante + pas_colonne
            ligne_courante = ligne_courante + pas_ligne
            case_etape: tuple[int, int] = (
                colonne_courante,
                ligne_courante,
            )

            if est_suppression:
                grille.supprimer_route(ligne_courante, colonne_courante)
            else:
                a_ete_posee: bool = grille.placer_voie_automatique(
                    ligne_courante,
                    colonne_courante,
                )
                grille.connecter_cases(case_precedente, case_etape)
                self.enregistrer_et_nettoyer_case_tracee(
                    grille,
                    case_etape,
                    a_ete_posee,
                )

    def tenter_reorientation_sortie_maison(
        self,
        grille: Grid,
        ligne: int,
        colonne: int,
    ) -> bool:
        """Tente de réorienter la case_sortie d'une maison lors d'un glissement.

        Args:
            grille: Instance du modèle Grid à modifier.
            ligne: Ligne actuellement survolée par la souris.
            colonne: Colonne actuellement survolée par la souris.

        Returns:
            True si l'action a été traitée comme une sélection ou une
            réorientation de sortie de maison, False si le tracé normal
            doit prendre le relais.
        """
        if self.maison_en_reorientation is None:
            return False
        else:
            pass

        maison: Maison = self.maison_en_reorientation
        if ligne == maison.ligne and colonne == maison.colonne:
            return True
        else:
            pass

        coordonnee_maison: tuple[int, int] = (maison.colonne, maison.ligne)
        coordonnee_cible: tuple[int, int] = (colonne, ligne)
        if grille.sont_cases_adjacentes_chebyshev(
            coordonnee_maison,
            coordonnee_cible,
        ):
            if self.derniere_case_tracee == coordonnee_maison:
                reorientee: bool = grille.reorienter_sortie_maison(
                    maison,
                    ligne,
                    colonne,
                )
                if reorientee and maison.case_sortie is not None:
                    lig_sortie, col_sortie = maison.case_sortie
                    case_sortie_col_lig: tuple[int, int] = (
                        col_sortie,
                        lig_sortie,
                    )
                    self.derniere_case_tracee = case_sortie_col_lig
                    self.historique_trace_courant = [case_sortie_col_lig]
                    self.maison_en_reorientation = None
                    return True
                else:
                    if maison.case_sortie == (ligne, colonne):
                        case_sortie_actuelle: tuple[int, int] = (
                            colonne,
                            ligne,
                        )
                        self.derniere_case_tracee = case_sortie_actuelle
                        self.historique_trace_courant = [case_sortie_actuelle]
                        self.maison_en_reorientation = None
                        return True
                    else:
                        return False
            else:
                self.maison_en_reorientation = None
                return False
        else:
            if maison.case_sortie is not None:
                lig_sortie, col_sortie = maison.case_sortie
                self.derniere_case_tracee = (col_sortie, lig_sortie)
            else:
                pass
            self.maison_en_reorientation = None
            return False

    def tenter_reorientation_sortie_usine(
        self,
        grille: Grid,
        ligne: int,
        colonne: int,
    ) -> bool:
        """Tente de réorienter la case_sortie d'une usine lors d'un glissement.

        Args:
            grille: Instance du modèle Grid à modifier.
            ligne: Ligne actuellement survolée par la souris.
            colonne: Colonne actuellement survolée par la souris.

        Returns:
            True si l'action a été traitée comme une sélection ou une
            réorientation de sortie d'usine, False si le tracé normal
            doit prendre le relais.
        """
        if self.usine_en_reorientation is None:
            return False
        else:
            pass

        usine: Usine = self.usine_en_reorientation
        if ligne == usine.ligne and colonne == usine.colonne:
            return True
        else:
            pass

        coordonnee_usine: tuple[int, int] = (usine.colonne, usine.ligne)
        coordonnee_cible: tuple[int, int] = (colonne, ligne)
        if grille.sont_cases_adjacentes_chebyshev(
            coordonnee_usine,
            coordonnee_cible,
        ):
            if self.derniere_case_tracee == coordonnee_usine:
                reorientee: bool = grille.reorienter_sortie_usine(
                    usine,
                    ligne,
                    colonne,
                )
                if reorientee and usine.case_sortie is not None:
                    lig_sortie, col_sortie = usine.case_sortie
                    case_sortie_col_lig: tuple[int, int] = (
                        col_sortie,
                        lig_sortie,
                    )
                    self.derniere_case_tracee = case_sortie_col_lig
                    self.historique_trace_courant = [case_sortie_col_lig]
                    self.usine_en_reorientation = None
                    return True
                else:
                    if usine.case_sortie == (ligne, colonne):
                        case_sortie_actuelle: tuple[int, int] = (
                            colonne,
                            ligne,
                        )
                        self.derniere_case_tracee = case_sortie_actuelle
                        self.historique_trace_courant = [case_sortie_actuelle]
                        self.usine_en_reorientation = None
                        return True
                    else:
                        return False
            else:
                self.usine_en_reorientation = None
                return False
        else:
            if usine.case_sortie is not None:
                lig_sortie, col_sortie = usine.case_sortie
                self.derniere_case_tracee = (col_sortie, lig_sortie)
            else:
                pass
            self.usine_en_reorientation = None
            return False

    def appliquer_action_clic_gauche(
        self,
        grille: Grid,
        position_x: int,
        position_y: int,
        colonne_debut_camera: float = COORDONNEE_CAMERA_ORIGINE_FLOAT,
        ligne_debut_camera: float = COORDONNEE_CAMERA_ORIGINE_FLOAT,
        taille_case_camera: float = float(TAILLE_CASE),
    ) -> None:
        """Trace une route ou réoriente la case_sortie d'une Maison ou d'une Usine.

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

        if self.outil_actif == OUTIL_FEU:
            if self.derniere_case_tracee is None:
                grille.placer_feu_circulation(ligne, colonne)
                self.derniere_case_tracee = case_actuelle
            else:
                pass
            return
        else:
            pass

        if self.outil_actif == OUTIL_ROND_POINT:
            if self.derniere_case_tracee is None:
                grille.placer_rond_point(ligne, colonne)
                self.derniere_case_tracee = case_actuelle
            else:
                pass
            return
        else:
            pass

        if self.outil_actif == OUTIL_AUTOROUTE:
            if self.derniere_case_tracee is None:
                if self.depart_autoroute_selectionne is None:
                    if grille.est_case_route(ligne, colonne):
                        self.depart_autoroute_selectionne = case_actuelle
                    else:
                        pass
                else:
                    if case_actuelle != self.depart_autoroute_selectionne:
                        grille.placer_autoroute(
                            self.depart_autoroute_selectionne,
                            case_actuelle,
                        )
                        self.depart_autoroute_selectionne = None
                    else:
                        pass
                self.derniere_case_tracee = case_actuelle
            else:
                pass
            return
        else:
            pass

        if self.derniere_case_tracee is None:
            maison_cliquee: Maison | None = (
                grille.obtenir_maison_a_coordonnee(ligne, colonne)
            )
            if maison_cliquee is not None:
                self.maison_en_reorientation = maison_cliquee
                self.derniere_case_tracee = case_actuelle
                return
            else:
                pass

            usine_cliquee: Usine | None = (
                grille.obtenir_usine_a_coordonnee(ligne, colonne)
            )
            if usine_cliquee is not None:
                self.usine_en_reorientation = usine_cliquee
                self.derniere_case_tracee = case_actuelle
                return
            else:
                pass

            maison_sortie: Maison | None = (
                grille.obtenir_maison_proprietaire_sortie(ligne, colonne)
            )
            if maison_sortie is not None:
                self.maison_en_reorientation = maison_sortie
                self.derniere_case_tracee = case_actuelle
                self.historique_trace_courant = [case_actuelle]
                return
            else:
                pass

            usine_sortie: Usine | None = (
                grille.obtenir_usine_proprietaire_sortie(ligne, colonne)
            )
            if usine_sortie is not None:
                self.usine_en_reorientation = usine_sortie
                self.derniere_case_tracee = case_actuelle
                self.historique_trace_courant = [case_actuelle]
                return
            else:
                a_ete_posee: bool = grille.placer_voie_automatique(
                    ligne,
                    colonne,
                )
                self.enregistrer_et_nettoyer_case_tracee(
                    grille,
                    case_actuelle,
                    a_ete_posee,
                )
        else:
            if self.tenter_reorientation_sortie_maison(
                grille,
                ligne,
                colonne,
            ):
                return
            else:
                if self.tenter_reorientation_sortie_usine(
                    grille,
                    ligne,
                    colonne,
                ):
                    return
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

        if evenement.type == pygame.KEYDOWN:
            if (
                evenement.key == pygame.K_1
                or evenement.key == pygame.K_KP1
            ):
                self.definir_outil_actif(OUTIL_ROUTE)
            else:
                if (
                    evenement.key == pygame.K_2
                    or evenement.key == pygame.K_KP2
                ):
                    self.definir_outil_actif(OUTIL_FEU)
                else:
                    if (
                        evenement.key == pygame.K_3
                        or evenement.key == pygame.K_KP3
                    ):
                        self.definir_outil_actif(OUTIL_ROND_POINT)
                    else:
                        if (
                            evenement.key == pygame.K_4
                            or evenement.key == pygame.K_KP4
                        ):
                            self.definir_outil_actif(OUTIL_AUTOROUTE)
                        else:
                            pass
            return
        else:
            pass

        if evenement.type == pygame.MOUSEBUTTONDOWN:
            self.derniere_case_tracee = None
            self.historique_trace_courant = []
            self.maison_en_reorientation = None
            self.usine_en_reorientation = None
            position_x, position_y = evenement.pos
            if evenement.button == BOUTON_SOURIS_GAUCHE:
                if self.verifier_clic_barre_outils_hud(
                    position_x,
                    position_y,
                ):
                    return
                else:
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
                    self.depart_autoroute_selectionne = None
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
                self.historique_trace_courant = []
                self.maison_en_reorientation = None
                self.usine_en_reorientation = None
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
                        self.historique_trace_courant = []
                        self.maison_en_reorientation = None
                        self.usine_en_reorientation = None
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
