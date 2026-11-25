"""Vue chargée du rendu graphique Pygame avec caméra à zoom progressif."""

import pygame

from src.config import (
    COMPTEUR_INITIAL_LIVRAISONS,
    COORDONNEE_CAMERA_ORIGINE_FLOAT,
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
    DIMENSION_PIXEL_MINIMALE,
    DIRECTIONS_DIAGONALES,
    DIVISEUR_MOITIE,
    EPAISSEUR_CONTOUR_INTERFACE,
    EPAISSEUR_CONTOUR_USINE,
    EPAISSEUR_LIGNE_GRILLE,
    EPAISSEUR_SEGMENT_DIAGONAL,
    ESPACEMENT_INDICATEUR_DEMANDE,
    FACTEUR_DOUBLE_MARGE,
    FACTEUR_ECHELLE_UNITE,
    HAUTEUR_BANDEAU_ROUTES,
    HAUTEUR_BANDEAU_SCORE,
    HAUTEUR_FENETRE,
    HAUTEUR_PANNEAU_DEFAITE,
    INCREMENT_BORNE_GRILLE,
    LARGEUR_BANDEAU_ROUTES,
    LARGEUR_BANDEAU_SCORE,
    LARGEUR_FENETRE,
    LARGEUR_PANNEAU_DEFAITE,
    MARGE_INTERIEURE_DEMANDE,
    MARGE_MAISON,
    MARGE_ROUTE,
    MARGE_USINE,
    NB_COLONNES_GRILLE_DEMANDES,
    POSITION_BANDEAU_ROUTES_X,
    POSITION_BANDEAU_ROUTES_Y,
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

    def mettre_a_echelle(
        self,
        valeur_base: int,
        facteur_zoom: float,
    ) -> int:
        """Met à l'échelle une dimension en pixels selon le facteur de zoom.

        Args:
            valeur_base: Dimension de référence à zoom 1.0.
            facteur_zoom: Multiplicateur de zoom actuel.

        Returns:
            Entier mis à l'échelle (au moins DIMENSION_PIXEL_MINIMALE).
        """
        valeur_zoomee: int = int(round(float(valeur_base) * facteur_zoom))
        if valeur_zoomee < DIMENSION_PIXEL_MINIMALE:
            return DIMENSION_PIXEL_MINIMALE
        else:
            return valeur_zoomee

    def convertir_monde_en_ecran(
        self,
        colonne_monde: float,
        ligne_monde: float,
        colonne_debut_camera: float,
        ligne_debut_camera: float,
        taille_case_camera: float,
    ) -> tuple[int, int]:
        """Projette une coordonnée flottante de grille en pixels écran.

        Args:
            colonne_monde: Coordonnée colonne dans le monde.
            ligne_monde: Coordonnée ligne dans le monde.
            colonne_debut_camera: Colonne du bord gauche de la caméra.
            ligne_debut_camera: Ligne du bord supérieur de la caméra.
            taille_case_camera: Taille d'une case en pixels écran.

        Returns:
            Un tuple (position_x, position_y) en pixels sur l'écran.
        """
        position_x: int = int(
            round((colonne_monde - colonne_debut_camera) * taille_case_camera)
        )
        position_y: int = int(
            round((ligne_monde - ligne_debut_camera) * taille_case_camera)
        )
        return (position_x, position_y)

    def dessiner_fond(self) -> None:
        """Remplit l'écran avec la couleur de fond."""
        self.ecran.fill(COULEUR_FOND)

    def dessiner_grille(
        self,
        grille: Grid,
        colonne_debut_camera: float,
        ligne_debut_camera: float,
        taille_case_camera: float,
    ) -> None:
        """Trace les lignes horizontales et verticales de la grille zoomée.

        Args:
            grille: Instance du modèle Grid à représenter.
            colonne_debut_camera: Colonne du bord gauche de la caméra.
            ligne_debut_camera: Ligne du bord supérieur de la caméra.
            taille_case_camera: Taille d'une case en pixels écran.
        """
        nb_traits_horizontaux: int = (
            grille.nb_lignes + INCREMENT_BORNE_GRILLE
        )
        for indice_ligne in range(nb_traits_horizontaux):
            _, position_y = self.convertir_monde_en_ecran(
                COORDONNEE_CAMERA_ORIGINE_FLOAT,
                float(indice_ligne),
                colonne_debut_camera,
                ligne_debut_camera,
                taille_case_camera,
            )
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
            position_x, _ = self.convertir_monde_en_ecran(
                float(indice_colonne),
                COORDONNEE_CAMERA_ORIGINE_FLOAT,
                colonne_debut_camera,
                ligne_debut_camera,
                taille_case_camera,
            )
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

    def dessiner_maisons(
        self,
        maisons: list[Maison],
        colonne_debut_camera: float,
        ligne_debut_camera: float,
        taille_case_camera: float,
        facteur_zoom: float,
    ) -> None:
        """Dessine chaque maison mise à l'échelle de la caméra.

        Args:
            maisons: Liste des instances de Maison à dessiner.
            colonne_debut_camera: Colonne du bord gauche de la caméra.
            ligne_debut_camera: Ligne du bord supérieur de la caméra.
            taille_case_camera: Taille d'une case en pixels écran.
            facteur_zoom: Facteur d'échelle actuel.
        """
        marge_maison_zoom: int = self.mettre_a_echelle(
            MARGE_MAISON,
            facteur_zoom,
        )
        taille_case_int: int = int(round(taille_case_camera))
        taille_maison: int = (
            taille_case_int - FACTEUR_DOUBLE_MARGE * marge_maison_zoom
        )
        rayon_bordure: int = self.mettre_a_echelle(
            RAYON_BORDURE_MAISON,
            facteur_zoom,
        )

        for maison in maisons:
            case_x, case_y = self.convertir_monde_en_ecran(
                float(maison.colonne),
                float(maison.ligne),
                colonne_debut_camera,
                ligne_debut_camera,
                taille_case_camera,
            )
            rectangle_maison: pygame.Rect = pygame.Rect(
                case_x + marge_maison_zoom,
                case_y + marge_maison_zoom,
                taille_maison,
                taille_maison,
            )
            pygame.draw.rect(
                self.ecran,
                maison.couleur,
                rectangle_maison,
                border_radius=rayon_bordure,
            )

    def dessiner_demandes_usine(
        self,
        usine: Usine,
        case_x: int,
        case_y: int,
        facteur_zoom: float,
    ) -> None:
        """Dessine les indicateurs de demandes en attente sur une usine.

        Args:
            usine: Instance de Usine dont il faut afficher les demandes.
            case_x: Coordonnée X en pixels écran du coin de la case.
            case_y: Coordonnée Y en pixels écran du coin de la case.
            facteur_zoom: Facteur d'échelle actuel.
        """
        nb_indicateurs: int = usine.demandes_actives
        if nb_indicateurs > SEUIL_CRITIQUE_DEMANDES_USINE:
            nb_indicateurs = SEUIL_CRITIQUE_DEMANDES_USINE
        else:
            pass

        marge_interieure_zoom: int = self.mettre_a_echelle(
            MARGE_INTERIEURE_DEMANDE,
            facteur_zoom,
        )
        espacement_zoom: int = self.mettre_a_echelle(
            ESPACEMENT_INDICATEUR_DEMANDE,
            facteur_zoom,
        )
        rayon_point_zoom: int = self.mettre_a_echelle(
            RAYON_INDICATEUR_DEMANDE,
            facteur_zoom,
        )
        epaisseur_contour_zoom: int = self.mettre_a_echelle(
            RAYON_CONTOUR_DEMANDE,
            facteur_zoom,
        )

        for indice_demande in range(nb_indicateurs):
            colonne_point: int = (
                indice_demande % NB_COLONNES_GRILLE_DEMANDES
            )
            ligne_point: int = (
                indice_demande // NB_COLONNES_GRILLE_DEMANDES
            )
            centre_point_x: int = (
                case_x
                + marge_interieure_zoom
                + colonne_point * espacement_zoom
            )
            centre_point_y: int = (
                case_y
                + marge_interieure_zoom
                + ligne_point * espacement_zoom
            )
            centre_point: tuple[int, int] = (centre_point_x, centre_point_y)
            pygame.draw.circle(
                self.ecran,
                COULEUR_INDICATEUR_DEMANDE,
                centre_point,
                rayon_point_zoom,
            )
            pygame.draw.circle(
                self.ecran,
                COULEUR_CONTOUR_BATIMENT,
                centre_point,
                rayon_point_zoom,
                width=epaisseur_contour_zoom,
            )

    def dessiner_usines(
        self,
        usines: list[Usine],
        colonne_debut_camera: float,
        ligne_debut_camera: float,
        taille_case_camera: float,
        facteur_zoom: float,
    ) -> None:
        """Dessine chaque usine et ses indicateurs de demandes avec zoom.

        Args:
            usines: Liste des instances de Usine à dessiner.
            colonne_debut_camera: Colonne du bord gauche de la caméra.
            ligne_debut_camera: Ligne du bord supérieur de la caméra.
            taille_case_camera: Taille d'une case en pixels écran.
            facteur_zoom: Facteur d'échelle actuel.
        """
        marge_usine_zoom: int = self.mettre_a_echelle(
            MARGE_USINE,
            facteur_zoom,
        )
        taille_case_int: int = int(round(taille_case_camera))
        taille_usine: int = (
            taille_case_int - FACTEUR_DOUBLE_MARGE * marge_usine_zoom
        )
        rayon_bordure: int = self.mettre_a_echelle(
            RAYON_BORDURE_USINE,
            facteur_zoom,
        )
        epaisseur_contour: int = self.mettre_a_echelle(
            EPAISSEUR_CONTOUR_USINE,
            facteur_zoom,
        )

        for usine in usines:
            case_x, case_y = self.convertir_monde_en_ecran(
                float(usine.colonne),
                float(usine.ligne),
                colonne_debut_camera,
                ligne_debut_camera,
                taille_case_camera,
            )
            rectangle_usine: pygame.Rect = pygame.Rect(
                case_x + marge_usine_zoom,
                case_y + marge_usine_zoom,
                taille_usine,
                taille_usine,
            )
            pygame.draw.rect(
                self.ecran,
                usine.couleur,
                rectangle_usine,
                border_radius=rayon_bordure,
            )
            pygame.draw.rect(
                self.ecran,
                COULEUR_CONTOUR_BATIMENT,
                rectangle_usine,
                width=epaisseur_contour,
                border_radius=rayon_bordure,
            )
            self.dessiner_demandes_usine(
                usine,
                case_x,
                case_y,
                facteur_zoom,
            )

    def dessiner_connexions_case_route(
        self,
        grille: Grid,
        ligne: int,
        colonne: int,
        colonne_debut_camera: float,
        ligne_debut_camera: float,
        taille_case_camera: float,
        facteur_zoom: float,
    ) -> None:
        """Dessine les extensions reliant une route à ses voisins connectables.

        Args:
            grille: Instance du modèle Grid contenant l'état des cases.
            ligne: Indice de la ligne de la case de route.
            colonne: Indice de la colonne de la case de route.
            colonne_debut_camera: Colonne du bord gauche de la caméra.
            ligne_debut_camera: Ligne du bord supérieur de la caméra.
            taille_case_camera: Taille d'une case en pixels écran.
            facteur_zoom: Facteur d'échelle actuel.
        """
        marge_route_zoom: int = self.mettre_a_echelle(
            MARGE_ROUTE,
            facteur_zoom,
        )
        marge_maison_zoom: int = self.mettre_a_echelle(
            MARGE_MAISON,
            facteur_zoom,
        )
        taille_case_int: int = int(round(taille_case_camera))
        taille_route: int = (
            taille_case_int - FACTEUR_DOUBLE_MARGE * marge_route_zoom
        )
        case_x, case_y = self.convertir_monde_en_ecran(
            float(colonne),
            float(ligne),
            colonne_debut_camera,
            ligne_debut_camera,
            taille_case_camera,
        )
        centre_x: int = case_x + marge_route_zoom
        centre_y: int = case_y + marge_route_zoom

        ligne_haut: int = ligne + DECALAGE_VOISIN_NEGATIF
        if grille.est_case_connectable_route(ligne_haut, colonne):
            hauteur_extension_haut: int = (
                marge_route_zoom + marge_maison_zoom
            )
            debut_y_haut: int = case_y - marge_maison_zoom
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
            hauteur_extension_bas: int = (
                marge_route_zoom + marge_maison_zoom
            )
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
            largeur_extension_gauche: int = (
                marge_route_zoom + marge_maison_zoom
            )
            debut_x_gauche: int = case_x - marge_maison_zoom
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
            largeur_extension_droite: int = (
                marge_route_zoom + marge_maison_zoom
            )
            segment_droite: pygame.Rect = pygame.Rect(
                debut_x_droite,
                centre_y,
                largeur_extension_droite,
                taille_route,
            )
            pygame.draw.rect(self.ecran, COULEUR_ROUTE, segment_droite)
        else:
            pass

        point_centre_case: tuple[int, int] = self.convertir_monde_en_ecran(
            float(colonne) + DECALAGE_CENTRE_CASE,
            float(ligne) + DECALAGE_CENTRE_CASE,
            colonne_debut_camera,
            ligne_debut_camera,
            taille_case_camera,
        )
        epaisseur_diagonale_zoom: int = self.mettre_a_echelle(
            EPAISSEUR_SEGMENT_DIAGONAL,
            facteur_zoom,
        )

        for delta_colonne, delta_ligne in DIRECTIONS_DIAGONALES:
            voisin_ligne: int = ligne + delta_ligne
            voisin_colonne: int = colonne + delta_colonne
            if grille.est_case_connectable_route(
                voisin_ligne,
                voisin_colonne,
            ):
                point_centre_voisin: tuple[int, int] = (
                    self.convertir_monde_en_ecran(
                        float(voisin_colonne) + DECALAGE_CENTRE_CASE,
                        float(voisin_ligne) + DECALAGE_CENTRE_CASE,
                        colonne_debut_camera,
                        ligne_debut_camera,
                        taille_case_camera,
                    )
                )
                pygame.draw.line(
                    self.ecran,
                    COULEUR_ROUTE,
                    point_centre_case,
                    point_centre_voisin,
                    epaisseur_diagonale_zoom,
                )
            else:
                pass

    def dessiner_routes(
        self,
        grille: Grid,
        colonne_debut_camera: float,
        ligne_debut_camera: float,
        taille_case_camera: float,
        facteur_zoom: float,
    ) -> None:
        """Dessine tous les segments de route avec la transformation caméra.

        Args:
            grille: Instance du modèle Grid à parcourir.
            colonne_debut_camera: Colonne du bord gauche de la caméra.
            ligne_debut_camera: Ligne du bord supérieur de la caméra.
            taille_case_camera: Taille d'une case en pixels écran.
            facteur_zoom: Facteur d'échelle actuel.
        """
        marge_route_zoom: int = self.mettre_a_echelle(
            MARGE_ROUTE,
            facteur_zoom,
        )
        taille_case_int: int = int(round(taille_case_camera))
        taille_route: int = (
            taille_case_int - FACTEUR_DOUBLE_MARGE * marge_route_zoom
        )
        rayon_noeud_zoom: int = self.mettre_a_echelle(
            RAYON_NOEUD_ROUTE,
            facteur_zoom,
        )

        for indice_ligne in range(grille.nb_lignes):
            for indice_colonne in range(grille.nb_colonnes):
                if grille.est_case_route(indice_ligne, indice_colonne):
                    case_x, case_y = self.convertir_monde_en_ecran(
                        float(indice_colonne),
                        float(indice_ligne),
                        colonne_debut_camera,
                        ligne_debut_camera,
                        taille_case_camera,
                    )
                    noeud_route: pygame.Rect = pygame.Rect(
                        case_x + marge_route_zoom,
                        case_y + marge_route_zoom,
                        taille_route,
                        taille_route,
                    )
                    pygame.draw.rect(
                        self.ecran,
                        COULEUR_ROUTE,
                        noeud_route,
                        border_radius=rayon_noeud_zoom,
                    )
                    self.dessiner_connexions_case_route(
                        grille,
                        indice_ligne,
                        indice_colonne,
                        colonne_debut_camera,
                        ligne_debut_camera,
                        taille_case_camera,
                        facteur_zoom,
                    )
                else:
                    pass

    def dessiner_voitures(
        self,
        voitures: list[Voiture],
        colonne_debut_camera: float,
        ligne_debut_camera: float,
        taille_case_camera: float,
        facteur_zoom: float,
    ) -> None:
        """Dessine chaque voiture décalée sur sa voie de droite avec zoom.

        Args:
            voitures: Liste des instances de Voiture en circulation.
            colonne_debut_camera: Colonne du bord gauche de la caméra.
            ligne_debut_camera: Ligne du bord supérieur de la caméra.
            taille_case_camera: Taille d'une case en pixels écran.
            facteur_zoom: Facteur d'échelle actuel.
        """
        rayon_voiture_zoom: int = self.mettre_a_echelle(
            RAYON_VOITURE,
            facteur_zoom,
        )
        epaisseur_contour_zoom: int = self.mettre_a_echelle(
            RAYON_CONTOUR_VOITURE,
            facteur_zoom,
        )
        decalage_voie_zoom: float = (
            float(DECALAGE_VOIE_DROITE_PIXELS) * facteur_zoom
        )

        for voiture in voitures:
            if voiture.est_en_circulation():
                decalage_droite_x, decalage_droite_y = (
                    voiture.obtenir_vecteur_decalage_droite()
                )
                base_x, base_y = self.convertir_monde_en_ecran(
                    voiture.position_colonne + DECALAGE_CENTRE_CASE,
                    voiture.position_ligne + DECALAGE_CENTRE_CASE,
                    colonne_debut_camera,
                    ligne_debut_camera,
                    taille_case_camera,
                )
                centre_x: int = int(
                    round(float(base_x) + decalage_droite_x * decalage_voie_zoom)
                )
                centre_y: int = int(
                    round(float(base_y) + decalage_droite_y * decalage_voie_zoom)
                )
                centre_voiture: tuple[int, int] = (centre_x, centre_y)
                pygame.draw.circle(
                    self.ecran,
                    voiture.couleur,
                    centre_voiture,
                    rayon_voiture_zoom,
                )
                pygame.draw.circle(
                    self.ecran,
                    COULEUR_CONTOUR_BATIMENT,
                    centre_voiture,
                    rayon_voiture_zoom,
                    width=epaisseur_contour_zoom,
                )
            else:
                pass

    def dessiner_bandeau_score(self, score: int) -> None:
        """Affiche le compteur de score fixe en haut à gauche de la fenêtre.

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

    def dessiner_bandeau_routes(self, stock_routes: int) -> None:
        """Affiche le stock de cases de route fixe en haut de l'écran.

        Args:
            stock_routes: Nombre de cases de route restantes dans l'inventaire.
        """
        rectangle_bandeau: pygame.Rect = pygame.Rect(
            POSITION_BANDEAU_ROUTES_X,
            POSITION_BANDEAU_ROUTES_Y,
            LARGEUR_BANDEAU_ROUTES,
            HAUTEUR_BANDEAU_ROUTES,
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
            f"Routes : {stock_routes}",
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
        parametres_camera: tuple[float, float, float, float] | None = None,
    ) -> None:
        """Effectue le rendu complet d'une frame avec caméra et HUD fixe.

        Args:
            grille: Instance du modèle Grid à afficher.
            voitures: Liste optionnelle des voitures actives à dessiner.
            score: Score actuel du joueur.
            partie_perdue: Indique si l'écran de défaite doit être affiché.
            parametres_camera: Tuple optionnel (colonne_debut, ligne_debut,
                taille_case_camera, facteur_zoom).
        """
        if parametres_camera is not None:
            (
                colonne_debut_cam,
                ligne_debut_cam,
                taille_case_cam,
                facteur_zoom,
            ) = parametres_camera
        else:
            colonne_debut_cam = COORDONNEE_CAMERA_ORIGINE_FLOAT
            ligne_debut_cam = COORDONNEE_CAMERA_ORIGINE_FLOAT
            taille_case_cam = float(TAILLE_CASE)
            facteur_zoom = FACTEUR_ECHELLE_UNITE

        self.dessiner_fond()
        self.dessiner_grille(
            grille,
            colonne_debut_cam,
            ligne_debut_cam,
            taille_case_cam,
        )
        self.dessiner_routes(
            grille,
            colonne_debut_cam,
            ligne_debut_cam,
            taille_case_cam,
            facteur_zoom,
        )
        self.dessiner_maisons(
            grille.maisons,
            colonne_debut_cam,
            ligne_debut_cam,
            taille_case_cam,
            facteur_zoom,
        )
        self.dessiner_usines(
            grille.usines,
            colonne_debut_cam,
            ligne_debut_cam,
            taille_case_cam,
            facteur_zoom,
        )
        if voitures is not None:
            self.dessiner_voitures(
                voitures,
                colonne_debut_cam,
                ligne_debut_cam,
                taille_case_cam,
                facteur_zoom,
            )
        else:
            pass
        self.dessiner_bandeau_score(score)
        self.dessiner_bandeau_routes(grille.stock_routes)
        if partie_perdue:
            self.dessiner_ecran_defaite(score)
        else:
            pass
        pygame.display.flip()
