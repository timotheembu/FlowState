"""Vue chargée du rendu graphique Pygame avec caméra à zoom progressif."""

import pygame

from src.config import (
    BORDURE_AUTOROUTE,
    BORDURE_CHAUSSEE,
    CARTES_DISPONIBLES,
    COEFFICIENT_PARABOLE_ARCHE,
    COMPTEUR_INITIAL_LIVRAISONS,
    COORDONNEE_CAMERA_ORIGINE_FLOAT,
    COORDONNEE_ORIGINE,
    COULEUR_AUTOROUTE,
    COULEUR_BORDURE_AUTOROUTE,
    COULEUR_BORDURE_PONT,
    COULEUR_BORDURE_ROUTE,
    COULEUR_BOUTON_CARTE,
    COULEUR_BOUTON_CARTE_SURVOL,
    COULEUR_CENTRE_ROND_POINT,
    COULEUR_CONTOUR_BATIMENT,
    COULEUR_EAU,
    COULEUR_ENTREE_TUNNEL,
    COULEUR_FEU_ROUGE,
    COULEUR_FEU_VERT,
    COULEUR_FOND,
    COULEUR_FOND_BANDEAU_SCORE,
    COULEUR_FOND_PANNEAU_DEFAITE,
    COULEUR_GRILLE,
    COULEUR_INDICATEUR_DEMANDE,
    COULEUR_MONTAGNE,
    COULEUR_OUTIL_ACTIF,
    COULEUR_PONT,
    COULEUR_ROND_POINT,
    COULEUR_ROUTE,
    COULEUR_SOMMET_MONTAGNE,
    COULEUR_SOUS_TEXTE_DEFAITE,
    COULEUR_TEXTE_DEFAITE,
    COULEUR_TEXTE_INTERFACE,
    COULEUR_TUNNEL,
    DECALAGE_CENTRE_CASE,
    DECALAGE_SOUS_TITRE_DEFAITE_Y,
    DECALAGE_TITRE_DEFAITE_Y,
    DECALAGE_VOIE_DROITE_PIXELS,
    DECALAGE_VOYANT_FEU,
    DIMENSION_PIXEL_MINIMALE,
    DIVISEUR_MOITIE,
    EPAISSEUR_CONTOUR_INTERFACE,
    EPAISSEUR_CONTOUR_USINE,
    EPAISSEUR_LIGNE_GRILLE,
    ESPACEMENT_BOUTONS_CARTE_Y,
    ESPACEMENT_BOUTONS_OUTIL_X,
    ESPACEMENT_INDICATEUR_DEMANDE,
    ETAT_FEU_HORIZONTAL_VERT,
    FACTEUR_DOUBLE_MARGE,
    FACTEUR_ECHELLE_UNITE,
    HAUTEUR_ARCHE_AUTOROUTE,
    HAUTEUR_BANDEAU_ROUTES,
    HAUTEUR_BANDEAU_SCORE,
    HAUTEUR_BOUTON_CARTE,
    HAUTEUR_BOUTON_OUTIL,
    HAUTEUR_FENETRE,
    HAUTEUR_PANNEAU_DEFAITE,
    INCREMENT_BORNE_GRILLE,
    LARGEUR_AUTOROUTE,
    LARGEUR_BANDEAU_ROUTES,
    LARGEUR_BANDEAU_SCORE,
    LARGEUR_BOUTON_CARTE,
    LARGEUR_BOUTON_OUTIL,
    LARGEUR_CHAUSSEE,
    LARGEUR_FENETRE,
    LARGEUR_PANNEAU_DEFAITE,
    MARGE_INTERIEURE_DEMANDE,
    MARGE_MAISON,
    MARGE_SOMMET_MONTAGNE,
    MARGE_USINE,
    NB_COLONNES_GRILLE_DEMANDES,
    NB_SEGMENTS_ARCHE_AUTOROUTE,
    OUTIL_AUTOROUTE,
    OUTIL_FEU,
    OUTIL_ROND_POINT,
    OUTIL_ROUTE,
    POSITION_BANDEAU_ROUTES_X,
    POSITION_BANDEAU_ROUTES_Y,
    POSITION_BANDEAU_SCORE_X,
    POSITION_BANDEAU_SCORE_Y,
    POSITION_BARRE_OUTILS_X,
    POSITION_BARRE_OUTILS_Y,
    POSITION_PREMIER_BOUTON_CARTE_Y,
    POSITION_SOUS_TITRE_ACCUEIL_Y,
    POSITION_TITRE_ACCUEIL_Y,
    RAYON_BORDURE_INTERFACE,
    RAYON_BORDURE_MAISON,
    RAYON_BORDURE_MONTAGNE,
    RAYON_BORDURE_USINE,
    RAYON_CONTOUR_DEMANDE,
    RAYON_CONTOUR_VOITURE,
    RAYON_ENTREE_TUNNEL,
    RAYON_EXTERIEUR_ROND_POINT,
    RAYON_INDICATEUR_DEMANDE,
    RAYON_INTERIEUR_ROND_POINT,
    RAYON_INTERIEUR_TUNNEL,
    RAYON_PILIER_AUTOROUTE,
    RAYON_VOITURE,
    RAYON_VOYANT_FEU,
    SEUIL_CRITIQUE_DEMANDES_USINE,
    TAILLE_CASE,
    TAILLE_POLICE_OUTIL,
    TAILLE_POLICE_SCORE,
    TAILLE_POLICE_SOUS_TITRE_DEFAITE,
    TAILLE_POLICE_TITRE_DEFAITE,
    TITRE_FENETRE,
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
        self.police_outil: pygame.font.Font = pygame.font.SysFont(
            None,
            TAILLE_POLICE_OUTIL,
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

    def dessiner_obstacles_naturels(
        self,
        grille: Grid,
        colonne_debut_camera: float,
        ligne_debut_camera: float,
        taille_case_camera: float,
        facteur_zoom: float,
    ) -> None:
        """Dessine les cases d'eau (CASE_EAU) et de montagne (CASE_MONTAGNE).

        Args:
            grille: Instance du modèle Grid à parcourir.
            colonne_debut_camera: Colonne du bord gauche de la caméra.
            ligne_debut_camera: Ligne du bord supérieur de la caméra.
            taille_case_camera: Taille d'une case en pixels écran.
            facteur_zoom: Facteur d'échelle actuel.
        """
        marge_sommet_zoom: int = self.mettre_a_echelle(
            MARGE_SOMMET_MONTAGNE,
            facteur_zoom,
        )
        rayon_montagne_zoom: int = self.mettre_a_echelle(
            RAYON_BORDURE_MONTAGNE,
            facteur_zoom,
        )

        for indice_ligne in range(grille.nb_lignes):
            for indice_colonne in range(grille.nb_colonnes):
                est_eau: bool = (
                    grille.est_case_eau(indice_ligne, indice_colonne)
                    or grille.est_case_pont(indice_ligne, indice_colonne)
                )
                est_montagne: bool = (
                    grille.est_case_montagne(indice_ligne, indice_colonne)
                    or grille.est_case_tunnel(indice_ligne, indice_colonne)
                )
                if est_eau or est_montagne:
                    case_x, case_y = self.convertir_monde_en_ecran(
                        float(indice_colonne),
                        float(indice_ligne),
                        colonne_debut_camera,
                        ligne_debut_camera,
                        taille_case_camera,
                    )
                    suiv_x, suiv_y = self.convertir_monde_en_ecran(
                        float(indice_colonne + INCREMENT_BORNE_GRILLE),
                        float(indice_ligne + INCREMENT_BORNE_GRILLE),
                        colonne_debut_camera,
                        ligne_debut_camera,
                        taille_case_camera,
                    )
                    largeur_case_px: int = suiv_x - case_x
                    hauteur_case_px: int = suiv_y - case_y
                    rectangle_case: pygame.Rect = pygame.Rect(
                        case_x,
                        case_y,
                        largeur_case_px,
                        hauteur_case_px,
                    )

                    if est_eau:
                        pygame.draw.rect(
                            self.ecran,
                            COULEUR_EAU,
                            rectangle_case,
                        )
                    else:
                        pygame.draw.rect(
                            self.ecran,
                            COULEUR_MONTAGNE,
                            rectangle_case,
                            border_radius=rayon_montagne_zoom,
                        )
                        largeur_sommet: int = (
                            largeur_case_px
                            - FACTEUR_DOUBLE_MARGE * marge_sommet_zoom
                        )
                        hauteur_sommet: int = (
                            hauteur_case_px
                            - FACTEUR_DOUBLE_MARGE * marge_sommet_zoom
                        )
                        if (
                            largeur_sommet > DIMENSION_PIXEL_MINIMALE
                            and hauteur_sommet > DIMENSION_PIXEL_MINIMALE
                        ):
                            rectangle_sommet: pygame.Rect = pygame.Rect(
                                case_x + marge_sommet_zoom,
                                case_y + marge_sommet_zoom,
                                largeur_sommet,
                                hauteur_sommet,
                            )
                            pygame.draw.rect(
                                self.ecran,
                                COULEUR_SOMMET_MONTAGNE,
                                rectangle_sommet,
                                border_radius=rayon_montagne_zoom,
                            )
                        else:
                            pass
                else:
                    pass

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
        couleur_ruban: tuple[int, int, int],
        largeur_ruban_pixels: int,
        rayon_joint_pixels: int,
    ) -> None:
        """Trace un joint circulaire et les rubans vers les voisins connectés.

        Args:
            grille: Instance du modèle Grid contenant l'état des cases.
            ligne: Indice de la ligne de la case de route.
            colonne: Indice de la colonne de la case de route.
            colonne_debut_camera: Colonne du bord gauche de la caméra.
            ligne_debut_camera: Ligne du bord supérieur de la caméra.
            taille_case_camera: Taille d'une case en pixels écran.
            couleur_ruban: Couleur RGB de la passe actuelle (bordure/asphalte).
            largeur_ruban_pixels: Épaisseur en pixels des segments de ligne.
            rayon_joint_pixels: Rayon en pixels des joints circulaires.
        """
        point_centre_case: tuple[int, int] = self.convertir_monde_en_ecran(
            float(colonne) + DECALAGE_CENTRE_CASE,
            float(ligne) + DECALAGE_CENTRE_CASE,
            colonne_debut_camera,
            ligne_debut_camera,
            taille_case_camera,
        )
        pygame.draw.circle(
            self.ecran,
            couleur_ruban,
            point_centre_case,
            rayon_joint_pixels,
        )

        coordonnee_case: tuple[int, int] = (colonne, ligne)
        voisins_connectes: set[tuple[int, int]] = (
            grille.obtenir_voisins_connectes(coordonnee_case)
        )
        for voisin_colonne, voisin_ligne in voisins_connectes:
            if grille.sont_cases_connectees_visuellement(
                ligne,
                colonne,
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
                    couleur_ruban,
                    point_centre_case,
                    point_centre_voisin,
                    largeur_ruban_pixels,
                )
                pygame.draw.circle(
                    self.ecran,
                    couleur_ruban,
                    point_centre_voisin,
                    rayon_joint_pixels,
                )
            else:
                pass

    def dessiner_passe_ruban_routes(
        self,
        grille: Grid,
        colonne_debut_camera: float,
        ligne_debut_camera: float,
        taille_case_camera: float,
        couleur_ruban: tuple[int, int, int],
        largeur_ruban_pixels: int,
    ) -> None:
        """Exécute une passe complète (bordure ou chaussée) sur le réseau.

        Args:
            grille: Instance du modèle Grid à parcourir.
            colonne_debut_camera: Colonne du bord gauche de la caméra.
            ligne_debut_camera: Ligne du bord supérieur de la caméra.
            taille_case_camera: Taille d'une case en pixels écran.
            couleur_ruban: Couleur RGB de la couche à tracer.
            largeur_ruban_pixels: Largeur en pixels du ruban à tracer.
        """
        rayon_joint_pixels: int = largeur_ruban_pixels // DIVISEUR_MOITIE
        if rayon_joint_pixels < DIMENSION_PIXEL_MINIMALE:
            rayon_joint_pixels = DIMENSION_PIXEL_MINIMALE
        else:
            pass

        for indice_ligne in range(grille.nb_lignes):
            for indice_colonne in range(grille.nb_colonnes):
                if grille.est_case_route(indice_ligne, indice_colonne):
                    self.dessiner_connexions_case_route(
                        grille,
                        indice_ligne,
                        indice_colonne,
                        colonne_debut_camera,
                        ligne_debut_camera,
                        taille_case_camera,
                        couleur_ruban,
                        largeur_ruban_pixels,
                        rayon_joint_pixels,
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
        """Dessine les routes sous forme d'un ruban continu en deux passes.

        La première passe trace une bordure extérieure plus large, et la
        seconde passe superpose le ruban d'asphalte avec joints circulaires.

        Args:
            grille: Instance du modèle Grid à parcourir.
            colonne_debut_camera: Colonne du bord gauche de la caméra.
            ligne_debut_camera: Ligne du bord supérieur de la caméra.
            taille_case_camera: Taille d'une case en pixels écran.
            facteur_zoom: Facteur d'échelle actuel.
        """
        largeur_totale_bordure_base: int = (
            LARGEUR_CHAUSSEE + FACTEUR_DOUBLE_MARGE * BORDURE_CHAUSSEE
        )
        largeur_bordure_zoom: int = self.mettre_a_echelle(
            largeur_totale_bordure_base,
            facteur_zoom,
        )
        largeur_chaussee_zoom: int = self.mettre_a_echelle(
            LARGEUR_CHAUSSEE,
            facteur_zoom,
        )

        self.dessiner_passe_ruban_routes(
            grille,
            colonne_debut_camera,
            ligne_debut_camera,
            taille_case_camera,
            COULEUR_BORDURE_ROUTE,
            largeur_bordure_zoom,
        )
        self.dessiner_passe_ruban_routes(
            grille,
            colonne_debut_camera,
            ligne_debut_camera,
            taille_case_camera,
            COULEUR_ROUTE,
            largeur_chaussee_zoom,
        )
        self.dessiner_infrastructures_speciales(
            grille,
            colonne_debut_camera,
            ligne_debut_camera,
            taille_case_camera,
            facteur_zoom,
        )

    def dessiner_infrastructures_speciales(
        self,
        grille: Grid,
        colonne_debut_camera: float,
        ligne_debut_camera: float,
        taille_case_camera: float,
        facteur_zoom: float,
    ) -> None:
        """Dessine les ponts, tunnels, ronds-points et feux de circulation.

        Args:
            grille: Instance du modèle Grid à parcourir.
            colonne_debut_camera: Colonne du bord gauche de la caméra.
            ligne_debut_camera: Ligne du bord supérieur de la caméra.
            taille_case_camera: Taille d'une case en pixels écran.
            facteur_zoom: Facteur d'échelle actuel.
        """
        rayon_pont_zoom: int = self.mettre_a_echelle(
            LARGEUR_CHAUSSEE // DIVISEUR_MOITIE + BORDURE_CHAUSSEE,
            facteur_zoom,
        )
        rayon_interieur_pont_zoom: int = self.mettre_a_echelle(
            LARGEUR_CHAUSSEE // DIVISEUR_MOITIE,
            facteur_zoom,
        )
        rayon_entree_tunnel_zoom: int = self.mettre_a_echelle(
            RAYON_ENTREE_TUNNEL,
            facteur_zoom,
        )
        rayon_interieur_tunnel_zoom: int = self.mettre_a_echelle(
            RAYON_INTERIEUR_TUNNEL,
            facteur_zoom,
        )
        rayon_ext_rond_point_zoom: int = self.mettre_a_echelle(
            RAYON_EXTERIEUR_ROND_POINT,
            facteur_zoom,
        )
        rayon_int_rond_point_zoom: int = self.mettre_a_echelle(
            RAYON_INTERIEUR_ROND_POINT,
            facteur_zoom,
        )
        rayon_voyant_feu_zoom: int = self.mettre_a_echelle(
            RAYON_VOYANT_FEU,
            facteur_zoom,
        )
        decalage_voyant_zoom: int = self.mettre_a_echelle(
            DECALAGE_VOYANT_FEU,
            facteur_zoom,
        )

        for indice_ligne in range(grille.nb_lignes):
            for indice_colonne in range(grille.nb_colonnes):
                centre_case: tuple[int, int] = self.convertir_monde_en_ecran(
                    float(indice_colonne) + DECALAGE_CENTRE_CASE,
                    float(indice_ligne) + DECALAGE_CENTRE_CASE,
                    colonne_debut_camera,
                    ligne_debut_camera,
                    taille_case_camera,
                )
                if grille.est_case_pont(indice_ligne, indice_colonne):
                    pygame.draw.circle(
                        self.ecran,
                        COULEUR_BORDURE_PONT,
                        centre_case,
                        rayon_pont_zoom,
                    )
                    pygame.draw.circle(
                        self.ecran,
                        COULEUR_PONT,
                        centre_case,
                        rayon_interieur_pont_zoom,
                    )
                else:
                    if grille.est_case_tunnel(indice_ligne, indice_colonne):
                        pygame.draw.circle(
                            self.ecran,
                            COULEUR_TUNNEL,
                            centre_case,
                            rayon_entree_tunnel_zoom,
                        )
                        pygame.draw.circle(
                            self.ecran,
                            COULEUR_ENTREE_TUNNEL,
                            centre_case,
                            rayon_interieur_tunnel_zoom,
                        )
                    else:
                        if grille.est_case_rond_point(
                            indice_ligne,
                            indice_colonne,
                        ):
                            pygame.draw.circle(
                                self.ecran,
                                COULEUR_BORDURE_ROUTE,
                                centre_case,
                                rayon_ext_rond_point_zoom
                                + BORDURE_CHAUSSEE,
                            )
                            pygame.draw.circle(
                                self.ecran,
                                COULEUR_ROND_POINT,
                                centre_case,
                                rayon_ext_rond_point_zoom,
                            )
                            pygame.draw.circle(
                                self.ecran,
                                COULEUR_CENTRE_ROND_POINT,
                                centre_case,
                                rayon_int_rond_point_zoom,
                            )
                        else:
                            pass

        for (lig_feu, col_feu), feu in grille.feux_circulation.items():
            centre_x, centre_y = self.convertir_monde_en_ecran(
                float(col_feu) + DECALAGE_CENTRE_CASE,
                float(lig_feu) + DECALAGE_CENTRE_CASE,
                colonne_debut_camera,
                ligne_debut_camera,
                taille_case_camera,
            )
            if feu.etat_axe_vert == ETAT_FEU_HORIZONTAL_VERT:
                couleur_horizontale: tuple[int, int, int] = COULEUR_FEU_VERT
                couleur_verticale: tuple[int, int, int] = COULEUR_FEU_ROUGE
            else:
                couleur_horizontale = COULEUR_FEU_ROUGE
                couleur_verticale = COULEUR_FEU_VERT

            pygame.draw.circle(
                self.ecran,
                couleur_horizontale,
                (centre_x - decalage_voyant_zoom, centre_y),
                rayon_voyant_feu_zoom,
            )
            pygame.draw.circle(
                self.ecran,
                couleur_horizontale,
                (centre_x + decalage_voyant_zoom, centre_y),
                rayon_voyant_feu_zoom,
            )
            pygame.draw.circle(
                self.ecran,
                couleur_verticale,
                (centre_x, centre_y - decalage_voyant_zoom),
                rayon_voyant_feu_zoom,
            )
            pygame.draw.circle(
                self.ecran,
                couleur_verticale,
                (centre_x, centre_y + decalage_voyant_zoom),
                rayon_voyant_feu_zoom,
            )

    def dessiner_autoroutes(
        self,
        grille: Grid,
        colonne_debut_camera: float,
        ligne_debut_camera: float,
        taille_case_camera: float,
        facteur_zoom: float,
    ) -> None:
        """Dessine les arches aériennes des autoroutes par-dessus la carte.

        Args:
            grille: Instance du modèle Grid contenant les autoroutes.
            colonne_debut_camera: Colonne du bord gauche de la caméra.
            ligne_debut_camera: Ligne du bord supérieur de la caméra.
            taille_case_camera: Taille d'une case en pixels écran.
            facteur_zoom: Facteur d'échelle actuel.
        """
        largeur_autoroute_zoom: int = self.mettre_a_echelle(
            LARGEUR_AUTOROUTE,
            facteur_zoom,
        )
        largeur_bordure_zoom: int = self.mettre_a_echelle(
            LARGEUR_AUTOROUTE + FACTEUR_DOUBLE_MARGE * BORDURE_AUTOROUTE,
            facteur_zoom,
        )
        rayon_pilier_zoom: int = self.mettre_a_echelle(
            RAYON_PILIER_AUTOROUTE,
            facteur_zoom,
        )
        fleche_arche_pixels: float = HAUTEUR_ARCHE_AUTOROUTE * facteur_zoom

        for case_a, case_b in grille.autoroutes:
            col_a, lig_a = case_a
            col_b, lig_b = case_b
            depart_x, depart_y = self.convertir_monde_en_ecran(
                float(col_a) + DECALAGE_CENTRE_CASE,
                float(lig_a) + DECALAGE_CENTRE_CASE,
                colonne_debut_camera,
                ligne_debut_camera,
                taille_case_camera,
            )
            arrivee_x, arrivee_y = self.convertir_monde_en_ecran(
                float(col_b) + DECALAGE_CENTRE_CASE,
                float(lig_b) + DECALAGE_CENTRE_CASE,
                colonne_debut_camera,
                ligne_debut_camera,
                taille_case_camera,
            )

            points_arche: list[tuple[int, int]] = []
            for indice_seg in range(
                NB_SEGMENTS_ARCHE_AUTOROUTE + INCREMENT_BORNE_GRILLE
            ):
                progression: float = float(indice_seg) / float(
                    NB_SEGMENTS_ARCHE_AUTOROUTE
                )
                interp_x: float = (
                    float(depart_x)
                    + (float(arrivee_x) - float(depart_x)) * progression
                )
                interp_y_base: float = (
                    float(depart_y)
                    + (float(arrivee_y) - float(depart_y)) * progression
                )
                elevation_arche: float = (
                    COEFFICIENT_PARABOLE_ARCHE
                    * progression
                    * (FACTEUR_ECHELLE_UNITE - progression)
                    * fleche_arche_pixels
                )
                point_courbe: tuple[int, int] = (
                    int(round(interp_x)),
                    int(round(interp_y_base - elevation_arche)),
                )
                points_arche.append(point_courbe)

            pygame.draw.circle(
                self.ecran,
                COULEUR_BORDURE_AUTOROUTE,
                (depart_x, depart_y),
                rayon_pilier_zoom,
            )
            pygame.draw.circle(
                self.ecran,
                COULEUR_BORDURE_AUTOROUTE,
                (arrivee_x, arrivee_y),
                rayon_pilier_zoom,
            )

            for indice_pt in range(NB_SEGMENTS_ARCHE_AUTOROUTE):
                pt_debut: tuple[int, int] = points_arche[indice_pt]
                pt_fin: tuple[int, int] = points_arche[
                    indice_pt + INCREMENT_BORNE_GRILLE
                ]
                pygame.draw.line(
                    self.ecran,
                    COULEUR_BORDURE_AUTOROUTE,
                    pt_debut,
                    pt_fin,
                    largeur_bordure_zoom,
                )

            for indice_pt in range(NB_SEGMENTS_ARCHE_AUTOROUTE):
                pt_debut = points_arche[indice_pt]
                pt_fin = points_arche[indice_pt + INCREMENT_BORNE_GRILLE]
                pygame.draw.line(
                    self.ecran,
                    COULEUR_AUTOROUTE,
                    pt_debut,
                    pt_fin,
                    largeur_autoroute_zoom,
                )

            pygame.draw.circle(
                self.ecran,
                COULEUR_AUTOROUTE,
                (depart_x, depart_y),
                rayon_pilier_zoom - BORDURE_AUTOROUTE,
            )
            pygame.draw.circle(
                self.ecran,
                COULEUR_AUTOROUTE,
                (arrivee_x, arrivee_y),
                rayon_pilier_zoom - BORDURE_AUTOROUTE,
            )

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

    def obtenir_rectangles_boutons_cartes(
        self,
    ) -> list[tuple[str, pygame.Rect]]:
        """Retourne les rectangles cliquables de sélection de carte à l'accueil.

        Returns:
            Liste de tuples (nom_carte, rectangle_bouton).
        """
        centre_ecran_x: int = LARGEUR_FENETRE // DIVISEUR_MOITIE
        bouton_x: int = (
            centre_ecran_x - LARGEUR_BOUTON_CARTE // DIVISEUR_MOITIE
        )
        boutons: list[tuple[str, pygame.Rect]] = []

        for indice_carte, nom_carte in enumerate(CARTES_DISPONIBLES):
            bouton_y: int = (
                POSITION_PREMIER_BOUTON_CARTE_Y
                + indice_carte * ESPACEMENT_BOUTONS_CARTE_Y
            )
            rectangle_bouton: pygame.Rect = pygame.Rect(
                bouton_x,
                bouton_y,
                LARGEUR_BOUTON_CARTE,
                HAUTEUR_BOUTON_CARTE,
            )
            boutons.append((nom_carte, rectangle_bouton))

        return boutons

    def dessiner_ecran_selection_carte(
        self,
        position_souris: tuple[int, int],
    ) -> None:
        """Affiche l'écran d'accueil permettant de choisir la carte de départ.

        Args:
            position_souris: Coordonnée actuelle (x, y) du curseur souris.
        """
        self.dessiner_fond()
        centre_ecran_x: int = LARGEUR_FENETRE // DIVISEUR_MOITIE

        surface_titre: pygame.Surface = self.police_titre_defaite.render(
            TITRE_FENETRE,
            True,
            COULEUR_TEXTE_INTERFACE,
        )
        rectangle_titre: pygame.Rect = surface_titre.get_rect(
            center=(centre_ecran_x, POSITION_TITRE_ACCUEIL_Y)
        )
        self.ecran.blit(surface_titre, rectangle_titre)

        surface_sous_titre: pygame.Surface = (
            self.police_sous_titre_defaite.render(
                "Choisissez une carte pour commencer",
                True,
                COULEUR_TEXTE_INTERFACE,
            )
        )
        rectangle_sous_titre: pygame.Rect = surface_sous_titre.get_rect(
            center=(centre_ecran_x, POSITION_SOUS_TITRE_ACCUEIL_Y)
        )
        self.ecran.blit(surface_sous_titre, rectangle_sous_titre)

        boutons_cartes: list[tuple[str, pygame.Rect]] = (
            self.obtenir_rectangles_boutons_cartes()
        )
        for nom_carte, rectangle_bouton in boutons_cartes:
            if rectangle_bouton.collidepoint(position_souris):
                couleur_fond_bouton: tuple[int, int, int] = (
                    COULEUR_BOUTON_CARTE_SURVOL
                )
            else:
                couleur_fond_bouton = COULEUR_BOUTON_CARTE

            pygame.draw.rect(
                self.ecran,
                couleur_fond_bouton,
                rectangle_bouton,
                border_radius=RAYON_BORDURE_INTERFACE,
            )
            pygame.draw.rect(
                self.ecran,
                COULEUR_CONTOUR_BATIMENT,
                rectangle_bouton,
                width=EPAISSEUR_CONTOUR_INTERFACE,
                border_radius=RAYON_BORDURE_INTERFACE,
            )
            surface_nom_carte: pygame.Surface = (
                self.police_sous_titre_defaite.render(
                    f"Carte : {nom_carte}",
                    True,
                    COULEUR_TEXTE_INTERFACE,
                )
            )
            rectangle_texte: pygame.Rect = surface_nom_carte.get_rect(
                center=rectangle_bouton.center
            )
            self.ecran.blit(surface_nom_carte, rectangle_texte)

        pygame.display.flip()

    def dessiner_barre_outils_bonus(
        self,
        grille: Grid,
        outil_actif: int = OUTIL_ROUTE,
    ) -> None:
        """Affiche les boutons d'outils et les stocks de bonus dans le HUD.

        Args:
            grille: Instance du modèle Grid contenant les stocks de bonus.
            outil_actif: Identifiant de l'outil actuellement sélectionné.
        """
        libelles_outils: list[tuple[int, str]] = [
            (
                OUTIL_ROUTE,
                f"[1] Voie P:{grille.stock_ponts} T:{grille.stock_tunnels}",
            ),
            (OUTIL_FEU, f"[2] Feux : {grille.stock_feux}"),
            (
                OUTIL_ROND_POINT,
                f"[3] Ronds-pts : {grille.stock_ronds_points}",
            ),
            (
                OUTIL_AUTOROUTE,
                f"[4] Autoroutes : {grille.stock_autoroutes}",
            ),
        ]

        for indice_outil, (code_outil, texte_outil) in enumerate(
            libelles_outils
        ):
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
            if code_outil == outil_actif:
                couleur_fond: tuple[int, int, int] = COULEUR_OUTIL_ACTIF
            else:
                couleur_fond = COULEUR_FOND_BANDEAU_SCORE

            pygame.draw.rect(
                self.ecran,
                couleur_fond,
                rectangle_outil,
                border_radius=RAYON_BORDURE_INTERFACE,
            )
            pygame.draw.rect(
                self.ecran,
                COULEUR_CONTOUR_BATIMENT,
                rectangle_outil,
                width=EPAISSEUR_CONTOUR_INTERFACE,
                border_radius=RAYON_BORDURE_INTERFACE,
            )
            surface_texte: pygame.Surface = self.police_outil.render(
                texte_outil,
                True,
                COULEUR_TEXTE_INTERFACE,
            )
            rectangle_texte: pygame.Rect = surface_texte.get_rect(
                center=rectangle_outil.center
            )
            self.ecran.blit(surface_texte, rectangle_texte)

    def afficher(
        self,
        grille: Grid,
        voitures: list[Voiture] | None = None,
        score: int = COMPTEUR_INITIAL_LIVRAISONS,
        partie_perdue: bool = False,
        parametres_camera: tuple[float, float, float, float] | None = None,
        outil_actif: int = OUTIL_ROUTE,
    ) -> None:
        """Effectue le rendu complet d'une frame avec caméra et HUD fixe.

        Args:
            grille: Instance du modèle Grid à afficher.
            voitures: Liste optionnelle des voitures actives à dessiner.
            score: Score actuel du joueur.
            partie_perdue: Indique si l'écran de défaite doit être affiché.
            parametres_camera: Tuple optionnel (colonne_debut, ligne_debut,
                taille_case_camera, facteur_zoom).
            outil_actif: Outil de construction sélectionné dans le HUD.
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
        self.dessiner_obstacles_naturels(
            grille,
            colonne_debut_cam,
            ligne_debut_cam,
            taille_case_cam,
            facteur_zoom,
        )
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
        self.dessiner_autoroutes(
            grille,
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
        self.dessiner_barre_outils_bonus(grille, outil_actif)
        if partie_perdue:
            self.dessiner_ecran_defaite(score)
        else:
            pass
        pygame.display.flip()
