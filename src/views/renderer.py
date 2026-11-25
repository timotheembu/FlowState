"""Vue chargée du rendu graphique Pygame de la grille, des entités et de l'ATH."""

import pygame

from src.config import (
    COMPTEUR_INITIAL_LIVRAISONS,
    COORDONNEE_ORIGINE,
    COULEUR_CONTOUR_BATIMENT,
    COULEUR_FOND,
    COULEUR_FOND_BANDEAU_SCORE,
    COULEUR_FOND_PANNEAU_DEFAITE,
    COULEUR_GRILLE,
    COULEUR_INDICATEUR_DEMANDE,
    COULEUR_ROUTE,
    COULEUR_SOUS_TEXTE_DEFAITE,
    COULEUR_TEXTE_DEFAITE,
    COULEUR_TEXTE_INTERFACE,
    DECALAGE_CENTRE_CASE,
    DECALAGE_SOUS_TITRE_DEFAITE_Y,
    DECALAGE_TITRE_DEFAITE_Y,
    DECALAGE_VOIE_DROITE_PIXELS,
    DECALAGE_VOISIN_NEGATIF,
    DECALAGE_VOISIN_POSITIF,
    DIVISEUR_MOITIE,
    EPAISSEUR_CONTOUR_INTERFACE,
    EPAISSEUR_CONTOUR_USINE,
    EPAISSEUR_LIGNE_GRILLE,
    ESPACEMENT_INDICATEUR_DEMANDE,
    FACTEUR_DOUBLE_MARGE,
    HAUTEUR_BANDEAU_SCORE,
    HAUTEUR_FENETRE,
    HAUTEUR_PANNEAU_DEFAITE,
    INCREMENT_BORNE_GRILLE,
    LARGEUR_BANDEAU_SCORE,
    LARGEUR_FENETRE,
    LARGEUR_PANNEAU_DEFAITE,
    MARGE_INTERIEURE_DEMANDE,
    MARGE_MAISON,
    MARGE_ROUTE,
    MARGE_USINE,
    NB_COLONNES_GRILLE_DEMANDES,
    POSITION_BANDEAU_SCORE_X,
    POSITION_BANDEAU_SCORE_Y,
    RAYON_BORDURE_INTERFACE,
    RAYON_BORDURE_MAISON,
    RAYON_BORDURE_USINE,
    RAYON_CONTOUR_DEMANDE,
    RAYON_CONTOUR_VOITURE,
    RAYON_INDICATEUR_DEMANDE,
    RAYON_NOEUD_ROUTE,
    RAYON_VOITURE,
    SEUIL_CRITIQUE_DEMANDES_USINE,
    TAILLE_CASE,
    TAILLE_POLICE_SCORE,
    TAILLE_POLICE_SOUS_TITRE_DEFAITE,
    TAILLE_POLICE_TITRE_DEFAITE,
)
from src.models.entity import Maison, Usine, Voiture
from src.models.grid import Grid


class Renderer:
    """Gère l'affichage graphique du jeu sur la fenêtre Pygame."""

    def __init__(self, ecran: pygame.Surface) -> None:
        """Initialise le moteur de rendu avec la surface principale.

        Args:
            ecran: Surface Pygame sur laquelle dessiner.
        """
        self.ecran: pygame.Surface = ecran
        self.police_score: pygame.font.Font = pygame.font.SysFont(
            None,
            TAILLE_POLICE_SCORE,
        )
        self.police_titre_defaite: pygame.font.Font = pygame.font.SysFont(
            None,
            TAILLE_POLICE_TITRE_DEFAITE,
        )
        self.police_sous_titre_defaite: pygame.font.Font = (
            pygame.font.SysFont(
                None,
                TAILLE_POLICE_SOUS_TITRE_DEFAITE,
            )
        )

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

    def dessiner_demandes_usine(self, usine: Usine) -> None:
        """Dessine les indicateurs de demandes en attente sur une usine.

        Args:
            usine: Instance de Usine dont il faut afficher les demandes.
        """
        case_x: int = usine.colonne * TAILLE_CASE
        case_y: int = usine.ligne * TAILLE_CASE

        nb_indicateurs: int = usine.demandes_actives
        if nb_indicateurs > SEUIL_CRITIQUE_DEMANDES_USINE:
            nb_indicateurs = SEUIL_CRITIQUE_DEMANDES_USINE
        else:
            pass

        for indice_demande in range(nb_indicateurs):
            colonne_point: int = (
                indice_demande % NB_COLONNES_GRILLE_DEMANDES
            )
            ligne_point: int = (
                indice_demande // NB_COLONNES_GRILLE_DEMANDES
            )
            centre_point_x: int = (
                case_x
                + MARGE_INTERIEURE_DEMANDE
                + colonne_point * ESPACEMENT_INDICATEUR_DEMANDE
            )
            centre_point_y: int = (
                case_y
                + MARGE_INTERIEURE_DEMANDE
                + ligne_point * ESPACEMENT_INDICATEUR_DEMANDE
            )
            centre_point: tuple[int, int] = (centre_point_x, centre_point_y)
            pygame.draw.circle(
                self.ecran,
                COULEUR_INDICATEUR_DEMANDE,
                centre_point,
                RAYON_INDICATEUR_DEMANDE,
            )
            pygame.draw.circle(
                self.ecran,
                COULEUR_CONTOUR_BATIMENT,
                centre_point,
                RAYON_INDICATEUR_DEMANDE,
                width=RAYON_CONTOUR_DEMANDE,
            )

    def dessiner_usines(self, usines: list[Usine]) -> None:
        """Dessine chaque usine et ses indicateurs de demandes en attente.

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
            self.dessiner_demandes_usine(usine)

    def dessiner_connexions_case_route(
        self,
        grille: Grid,
        ligne: int,
        colonne: int,
    ) -> None:
        """Dessine les extensions reliant une route à ses voisins connectables.

        Args:
            grille: Instance du modèle Grid contenant l'état des cases.
            ligne: Indice de la ligne de la case de route.
            colonne: Indice de la colonne de la case de route.
        """
        taille_route: int = (
            TAILLE_CASE - FACTEUR_DOUBLE_MARGE * MARGE_ROUTE
        )
        case_x: int = colonne * TAILLE_CASE
        case_y: int = ligne * TAILLE_CASE
        centre_x: int = case_x + MARGE_ROUTE
        centre_y: int = case_y + MARGE_ROUTE

        ligne_haut: int = ligne + DECALAGE_VOISIN_NEGATIF
        if grille.est_case_connectable_route(ligne_haut, colonne):
            hauteur_extension_haut: int = MARGE_ROUTE + MARGE_MAISON
            debut_y_haut: int = case_y - MARGE_MAISON
            segment_haut: pygame.Rect = pygame.Rect(
                centre_x,
                debut_y_haut,
                taille_route,
                hauteur_extension_haut,
            )
            pygame.draw.rect(self.ecran, COULEUR_ROUTE, segment_haut)
        else:
            pass

        ligne_bas: int = ligne + DECALAGE_VOISIN_POSITIF
        if grille.est_case_connectable_route(ligne_bas, colonne):
            debut_y_bas: int = centre_y + taille_route
            hauteur_extension_bas: int = MARGE_ROUTE + MARGE_MAISON
            segment_bas: pygame.Rect = pygame.Rect(
                centre_x,
                debut_y_bas,
                taille_route,
                hauteur_extension_bas,
            )
            pygame.draw.rect(self.ecran, COULEUR_ROUTE, segment_bas)
        else:
            pass

        colonne_gauche: int = colonne + DECALAGE_VOISIN_NEGATIF
        if grille.est_case_connectable_route(ligne, colonne_gauche):
            largeur_extension_gauche: int = MARGE_ROUTE + MARGE_MAISON
            debut_x_gauche: int = case_x - MARGE_MAISON
            segment_gauche: pygame.Rect = pygame.Rect(
                debut_x_gauche,
                centre_y,
                largeur_extension_gauche,
                taille_route,
            )
            pygame.draw.rect(self.ecran, COULEUR_ROUTE, segment_gauche)
        else:
            pass

        colonne_droite: int = colonne + DECALAGE_VOISIN_POSITIF
        if grille.est_case_connectable_route(ligne, colonne_droite):
            debut_x_droite: int = centre_x + taille_route
            largeur_extension_droite: int = MARGE_ROUTE + MARGE_MAISON
            segment_droite: pygame.Rect = pygame.Rect(
                debut_x_droite,
                centre_y,
                largeur_extension_droite,
                taille_route,
            )
            pygame.draw.rect(self.ecran, COULEUR_ROUTE, segment_droite)
        else:
            pass

    def dessiner_routes(self, grille: Grid) -> None:
        """Dessine tous les segments de route présents sur la grille.

        Args:
            grille: Instance du modèle Grid à parcourir.
        """
        taille_route: int = (
            TAILLE_CASE - FACTEUR_DOUBLE_MARGE * MARGE_ROUTE
        )
        for indice_ligne in range(grille.nb_lignes):
            for indice_colonne in range(grille.nb_colonnes):
                if grille.est_case_route(indice_ligne, indice_colonne):
                    position_x: int = (
                        indice_colonne * TAILLE_CASE + MARGE_ROUTE
                    )
                    position_y: int = (
                        indice_ligne * TAILLE_CASE + MARGE_ROUTE
                    )
                    noeud_route: pygame.Rect = pygame.Rect(
                        position_x,
                        position_y,
                        taille_route,
                        taille_route,
                    )
                    pygame.draw.rect(
                        self.ecran,
                        COULEUR_ROUTE,
                        noeud_route,
                        border_radius=RAYON_NOEUD_ROUTE,
                    )
                    self.dessiner_connexions_case_route(
                        grille,
                        indice_ligne,
                        indice_colonne,
                    )
                else:
                    pass

    def dessiner_voitures(self, voitures: list[Voiture]) -> None:
        """Dessine chaque voiture décalée sur sa voie de droite.

        Args:
            voitures: Liste des instances de Voiture en circulation.
        """
        for voiture in voitures:
            if voiture.est_en_circulation():
                decalage_droite_x, decalage_droite_y = (
                    voiture.obtenir_vecteur_decalage_droite()
                )
                centre_x: int = int(
                    (voiture.position_colonne + DECALAGE_CENTRE_CASE)
                    * TAILLE_CASE
                    + decalage_droite_x * DECALAGE_VOIE_DROITE_PIXELS
                )
                centre_y: int = int(
                    (voiture.position_ligne + DECALAGE_CENTRE_CASE)
                    * TAILLE_CASE
                    + decalage_droite_y * DECALAGE_VOIE_DROITE_PIXELS
                )
                centre_voiture: tuple[int, int] = (centre_x, centre_y)
                pygame.draw.circle(
                    self.ecran,
                    voiture.couleur,
                    centre_voiture,
                    RAYON_VOITURE,
                )
                pygame.draw.circle(
                    self.ecran,
                    COULEUR_CONTOUR_BATIMENT,
                    centre_voiture,
                    RAYON_VOITURE,
                    width=RAYON_CONTOUR_VOITURE,
                )
            else:
                pass

    def dessiner_bandeau_score(self, score: int) -> None:
        """Affiche le compteur de score en haut à gauche de la fenêtre.

        Args:
            score: Nombre total de livraisons effectuées.
        """
        rectangle_bandeau: pygame.Rect = pygame.Rect(
            POSITION_BANDEAU_SCORE_X,
            POSITION_BANDEAU_SCORE_Y,
            LARGEUR_BANDEAU_SCORE,
            HAUTEUR_BANDEAU_SCORE,
        )
        pygame.draw.rect(
            self.ecran,
            COULEUR_FOND_BANDEAU_SCORE,
            rectangle_bandeau,
            border_radius=RAYON_BORDURE_INTERFACE,
        )
        pygame.draw.rect(
            self.ecran,
            COULEUR_CONTOUR_BATIMENT,
            rectangle_bandeau,
            width=EPAISSEUR_CONTOUR_INTERFACE,
            border_radius=RAYON_BORDURE_INTERFACE,
        )
        surface_texte: pygame.Surface = self.police_score.render(
            f"Score : {score}",
            True,
            COULEUR_TEXTE_INTERFACE,
        )
        rectangle_texte: pygame.Rect = surface_texte.get_rect(
            center=rectangle_bandeau.center
        )
        self.ecran.blit(surface_texte, rectangle_texte)

    def dessiner_ecran_defaite(self, score: int) -> None:
        """Affiche le panneau central de Partie Perdue avec le score final.

        Args:
            score: Score final atteint avant la saturation d'une usine.
        """
        centre_ecran_x: int = LARGEUR_FENETRE // DIVISEUR_MOITIE
        centre_ecran_y: int = HAUTEUR_FENETRE // DIVISEUR_MOITIE
        panneau_x: int = (
            centre_ecran_x - LARGEUR_PANNEAU_DEFAITE // DIVISEUR_MOITIE
        )
        panneau_y: int = (
            centre_ecran_y - HAUTEUR_PANNEAU_DEFAITE // DIVISEUR_MOITIE
        )
        rectangle_panneau: pygame.Rect = pygame.Rect(
            panneau_x,
            panneau_y,
            LARGEUR_PANNEAU_DEFAITE,
            HAUTEUR_PANNEAU_DEFAITE,
        )
        pygame.draw.rect(
            self.ecran,
            COULEUR_FOND_PANNEAU_DEFAITE,
            rectangle_panneau,
            border_radius=RAYON_BORDURE_INTERFACE,
        )
        pygame.draw.rect(
            self.ecran,
            COULEUR_TEXTE_DEFAITE,
            rectangle_panneau,
            width=EPAISSEUR_CONTOUR_INTERFACE,
            border_radius=RAYON_BORDURE_INTERFACE,
        )

        surface_titre: pygame.Surface = self.police_titre_defaite.render(
            "PARTIE PERDUE - Usine saturee !",
            True,
            COULEUR_TEXTE_DEFAITE,
        )
        rectangle_titre: pygame.Rect = surface_titre.get_rect(
            center=(
                centre_ecran_x,
                centre_ecran_y + DECALAGE_TITRE_DEFAITE_Y,
            )
        )
        self.ecran.blit(surface_titre, rectangle_titre)

        surface_score_final: pygame.Surface = (
            self.police_sous_titre_defaite.render(
                f"Score final : {score}",
                True,
                COULEUR_SOUS_TEXTE_DEFAITE,
            )
        )
        rectangle_score_final: pygame.Rect = surface_score_final.get_rect(
            center=(
                centre_ecran_x,
                centre_ecran_y + DECALAGE_SOUS_TITRE_DEFAITE_Y,
            )
        )
        self.ecran.blit(surface_score_final, rectangle_score_final)

    def afficher(
        self,
        grille: Grid,
        voitures: list[Voiture] | None = None,
        score: int = COMPTEUR_INITIAL_LIVRAISONS,
        partie_perdue: bool = False,
    ) -> None:
        """Effectue le rendu complet d'une frame et met à jour l'écran.

        Args:
            grille: Instance du modèle Grid à afficher.
            voitures: Liste optionnelle des voitures actives à dessiner.
            score: Score actuel du joueur.
            partie_perdue: Indique si l'écran de défaite doit être affiché.
        """
        self.dessiner_fond()
        self.dessiner_grille(grille)
        self.dessiner_routes(grille)
        self.dessiner_maisons(grille.maisons)
        self.dessiner_usines(grille.usines)
        if voitures is not None:
            self.dessiner_voitures(voitures)
        else:
            pass
        self.dessiner_bandeau_score(score)
        if partie_perdue:
            self.dessiner_ecran_defaite(score)
        else:
            pass
        pygame.display.flip()
