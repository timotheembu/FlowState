"""Vue chargée du rendu graphique Pygame avec caméra à zoom progressif."""

import math
import pygame

from src.config import (
    ALPHA_OMBRE_PORTEE,
    ANGLE_DEPART_HORLOGE_RAD,
    ANGLE_TOUR_COMPLET_RAD,
    ASSOMBRISSEMENT_FAITE_MAISON,
    BORDURE_AUTOROUTE,
    BORDURE_BADGE_AUTOROUTE,
    BORDURE_CHAUSSEE,
    BORDURE_RELIEF_ORGANIQUE,
    CARTES_DISPONIBLES,
    CENTRE_BOUTON_RETOUR_X,
    CENTRE_BOUTON_RETOUR_Y,
    CENTRE_DOCK_X,
    CENTRE_DOCK_Y,
    CENTRE_EPINGLE_SCORE_X,
    CENTRE_EPINGLE_SCORE_Y,
    CENTRE_HORLOGE_HUD_X,
    CENTRE_HORLOGE_HUD_Y,
    COEFFICIENT_PARABOLE_ARCHE,
    COMPTEUR_INITIAL_LIVRAISONS,
    COORDONNEE_CAMERA_ORIGINE_FLOAT,
    COORDONNEE_ORIGINE,
    COULEUR_AUTOROUTE,
    COULEUR_BANDEAU_MODE_EDITION,
    COULEUR_BANDEAU_MODE_JEU,
    COULEUR_BORDURE_AUTOROUTE,
    COULEUR_BORDURE_EAU,
    COULEUR_BORDURE_MONTAGNE,
    COULEUR_BORDURE_PONT,
    COULEUR_BORDURE_ROUTE,
    COULEUR_BOUTON_CARTE,
    COULEUR_BOUTON_CARTE_SURVOL,
    COULEUR_CADRAN_HORLOGE,
    COULEUR_CENTRE_ROND_POINT,
    COULEUR_CONTOUR_BATIMENT,
    COULEUR_CORPS_USINE,
    COULEUR_EAU,
    COULEUR_ENTREE_TUNNEL,
    COULEUR_FEU_ROUGE,
    COULEUR_FEU_VERT,
    COULEUR_FOND,
    COULEUR_FOND_BANDEAU_SCORE,
    COULEUR_FOND_BOUTON_HUD,
    COULEUR_FOND_PANNEAU_DEFAITE,
    COULEUR_GRILLE,
    COULEUR_ICONE_HUD_SOMBRE,
    COULEUR_INDICATEUR_DEMANDE,
    COULEUR_LIGNE_PARKING_USINE,
    COULEUR_LOSANGE_ROUTES,
    COULEUR_MONTAGNE,
    COULEUR_OMBRE_PORTEE,
    COULEUR_OUTIL_ACTIF,
    COULEUR_PASTILLE_STOCK,
    COULEUR_PONT,
    COULEUR_ROND_POINT,
    COULEUR_ROUTE,
    COULEUR_SECTEUR_HORLOGE,
    COULEUR_SOCLE_MAISON,
    COULEUR_SOMMET_MONTAGNE,
    COULEUR_SOUS_TEXTE_DEFAITE,
    COULEUR_TEXTE_DEFAITE,
    COULEUR_TEXTE_INTERFACE,
    COULEUR_TEXTE_LOSANGE_ROUTES,
    COULEUR_TEXTE_PASTILLE_STOCK,
    COULEUR_TUNNEL,
    DECALAGE_AIDE_CARTE_OFFRE_Y,
    DECALAGE_BONUS_CARTE_OFFRE_Y,
    DECALAGE_CARTES_MODALE_HEBDO_Y,
    DECALAGE_CENTRE_CASE,
    DECALAGE_CENTRE_HORLOGE_X,
    DECALAGE_COUVERCLE_CORBEILLE_Y,
    DECALAGE_OMBRE_AUTOROUTE_X,
    DECALAGE_OMBRE_AUTOROUTE_Y,
    DECALAGE_OMBRE_X,
    DECALAGE_OMBRE_Y,
    DECALAGE_PASTILLE_STOCK_X,
    DECALAGE_PASTILLE_STOCK_Y,
    DECALAGE_ROUTES_CARTE_OFFRE_Y,
    DECALAGE_SOUS_TITRE_DEFAITE_Y,
    DECALAGE_SOUS_TITRE_MODALE_HEBDO_Y,
    DECALAGE_TEXTE_HORLOGE_X,
    DECALAGE_TITRE_CARTE_OFFRE_Y,
    DECALAGE_TITRE_DEFAITE_Y,
    DECALAGE_TITRE_MODALE_HEBDO_Y,
    DECALAGE_VOIE_DROITE_PIXELS,
    DECALAGE_VOISIN_NUL,
    DECALAGE_VOYANT_FEU,
    DEMI_LARGEUR_POINTE_EPINGLE,
    DEMI_TAILLE_LOSANGE_ROUTES,
    DIMENSION_PIXEL_MINIMALE,
    DIRECTIONS_HUIT_VOISINS,
    DIVISEUR_MOITIE,
    DIVISEUR_PARITE_USINE,
    EPAISSEUR_AIGUILLE_HORLOGE,
    EPAISSEUR_CONTOUR_INTERFACE,
    EPAISSEUR_CONTOUR_USINE,
    EPAISSEUR_FLECHE_RETOUR,
    EPAISSEUR_LIGNE_GRILLE,
    EPAISSEUR_LIGNE_PARKING,
    ESPACEMENT_BOUTONS_CARTE_Y,
    ESPACEMENT_BOUTONS_DOCK_X,
    ESPACEMENT_BOUTONS_OUTIL_X,
    ESPACEMENT_CARTES_OFFRE_X,
    ESPACEMENT_INDICATEUR_DEMANDE,
    ETAT_FEU_HORIZONTAL_VERT,
    FACTEUR_BEZIER_QUADRATIQUE,
    FACTEUR_DOUBLE_MARGE,
    FACTEUR_ECHELLE_UNITE,
    HAUTEUR_ARCHE_AUTOROUTE,
    HAUTEUR_BANDEAU_HORLOGE,
    HAUTEUR_BANDEAU_MODE,
    HAUTEUR_BANDEAU_ROUTES,
    HAUTEUR_BANDEAU_SCORE,
    HAUTEUR_BOUTON_CARTE,
    HAUTEUR_BOUTON_OUTIL,
    HAUTEUR_CARTE_OFFRE_HEBDO,
    HAUTEUR_FENETRE,
    HAUTEUR_ICONE_CORBEILLE,
    HAUTEUR_PANNEAU_DEFAITE,
    HAUTEUR_PANNEAU_HEBDOMADAIRE,
    HAUTEUR_POINTE_EPINGLE,
    INCREMENT_BORNE_GRILLE,
    INDICE_DOCK_AUTOROUTE,
    INDICE_DOCK_EDITION,
    INDICE_DOCK_FEU,
    INDICE_DOCK_PONT_TUNNEL,
    INDICE_DOCK_ROND_POINT,
    INDICE_JOUR_LUNDI,
    JOURS_SEMAINE,
    JOURS_SEMAINE_ABREGES,
    LARGEUR_ALLEE_MAISON,
    LARGEUR_AUTOROUTE,
    LARGEUR_BANDEAU_HORLOGE,
    LARGEUR_BANDEAU_MODE,
    LARGEUR_BANDEAU_ROUTES,
    LARGEUR_BANDEAU_SCORE,
    LARGEUR_BOUTON_CARTE,
    LARGEUR_BOUTON_OUTIL,
    LARGEUR_CARTE_OFFRE_HEBDO,
    LARGEUR_CHAUSSEE,
    LARGEUR_FENETRE,
    LARGEUR_ICONE_CORBEILLE,
    LARGEUR_PANNEAU_DEFAITE,
    LARGEUR_PANNEAU_HEBDOMADAIRE,
    LARGEUR_ZONE_PARKING_USINE,
    LIBELLE_MODE_EDITION_HUD,
    LIBELLE_MODE_JEU_HUD,
    LONGUEUR_ABREVIATION_JOUR,
    LONGUEUR_ALLEE_MAISON,
    LONGUEUR_MINIMALE_ITINERAIRE,
    MARGE_INTERIEURE_DEMANDE,
    MARGE_MAISON,
    MARGE_SOMMET_MONTAGNE,
    MARGE_TOIT_INTERIEUR_MAISON,
    MARGE_TOIT_USINE,
    MARGE_USINE,
    MODE_EDITION_INITIAL,
    NB_COLONNES_GRILLE_DEMANDES,
    NB_OPTIONS_HEBDOMADAIRES,
    NB_PLACES_PARKING_USINE,
    NB_SEGMENTS_ARCHE_AUTOROUTE,
    NB_SEGMENTS_SECTEUR_HORLOGE,
    NUMERO_SEMAINE_INITIALE,
    OUTIL_AUTOROUTE,
    OUTIL_FEU,
    OUTIL_ROND_POINT,
    OUTIL_ROUTE,
    PAS_INCREMENT_COMPTEUR,
    POSITION_BANDEAU_HORLOGE_X,
    POSITION_BANDEAU_HORLOGE_Y,
    POSITION_BANDEAU_MODE_X,
    POSITION_BANDEAU_MODE_Y,
    POSITION_BANDEAU_ROUTES_X,
    POSITION_BANDEAU_ROUTES_Y,
    POSITION_BANDEAU_SCORE_X,
    POSITION_BANDEAU_SCORE_Y,
    POSITION_BARRE_OUTILS_X,
    POSITION_BARRE_OUTILS_Y,
    POSITION_JOUR_HUD_X,
    POSITION_JOUR_HUD_Y,
    POSITION_PREMIER_BOUTON_CARTE_Y,
    POSITION_SCORE_HUD_X,
    POSITION_SCORE_HUD_Y,
    POSITION_SOUS_TITRE_ACCUEIL_Y,
    POSITION_TITRE_ACCUEIL_Y,
    PROGRESSION_MILIEU_COURBE,
    RAYON_BADGE_AUTOROUTE,
    RAYON_BORDURE_INTERFACE,
    RAYON_BORDURE_MAISON,
    RAYON_BORDURE_MONTAGNE,
    RAYON_BORDURE_USINE,
    RAYON_BOUTON_DOCK,
    RAYON_BOUTON_RETOUR,
    RAYON_CONTOUR_DEMANDE,
    RAYON_CONTOUR_VOITURE,
    RAYON_ENTREE_TUNNEL,
    RAYON_EXTERIEUR_ROND_POINT,
    RAYON_HORLOGE_HUD,
    RAYON_HORLOGE_MINIMALISTE,
    RAYON_INDICATEUR_DEMANDE,
    RAYON_INTERIEUR_ROND_POINT,
    RAYON_INTERIEUR_TUNNEL,
    RAYON_PASTILLE_STOCK_DOCK,
    RAYON_PILIER_AUTOROUTE,
    RAYON_POINT_CENTRE_DEMANDE,
    RAYON_SOMMET_RELIEF,
    RAYON_TETE_EPINGLE,
    RAYON_TROU_EPINGLE,
    RAYON_VOITURE,
    RAYON_VOYANT_FEU,
    SEUIL_CRITIQUE_DEMANDES_USINE,
    TAILLE_CASE,
    TAILLE_FLECHE_RETOUR,
    TAILLE_POLICE_JOUR_HUD,
    TAILLE_POLICE_OUTIL,
    TAILLE_POLICE_PASTILLE_DOCK,
    TAILLE_POLICE_SCORE,
    TAILLE_POLICE_SCORE_HUD,
    TAILLE_POLICE_SOUS_TITRE_DEFAITE,
    TAILLE_POLICE_TITRE_DEFAITE,
    THEME_CREME_SAUGE,
    THEME_PAR_CARTE,
    THEMES_GRAPHIQUES,
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
        self.police_score_hud: pygame.font.Font = pygame.font.SysFont(
            None,
            TAILLE_POLICE_SCORE_HUD,
        )
        self.police_jour_hud: pygame.font.Font = pygame.font.SysFont(
            None,
            TAILLE_POLICE_JOUR_HUD,
        )
        self.police_pastille_dock: pygame.font.Font = pygame.font.SysFont(
            None,
            TAILLE_POLICE_PASTILLE_DOCK,
        )
        self.nom_theme_actif: str = THEME_CREME_SAUGE
        self.couleur_fond_active: tuple[int, int, int] = COULEUR_FOND
        self.couleur_eau_active: tuple[int, int, int] = COULEUR_EAU
        self.couleur_bordure_eau_active: tuple[int, int, int] = (
            COULEUR_BORDURE_EAU
        )
        self.couleur_montagne_active: tuple[int, int, int] = COULEUR_MONTAGNE
        self.couleur_bordure_montagne_active: tuple[int, int, int] = (
            COULEUR_BORDURE_MONTAGNE
        )
        self.couleur_sommet_active: tuple[int, int, int] = (
            COULEUR_SOMMET_MONTAGNE
        )
        self.couleur_grille_active: tuple[int, int, int] = COULEUR_GRILLE
        self.couleur_texte_hud_active: tuple[int, int, int] = (
            COULEUR_TEXTE_INTERFACE
        )

    def definir_theme_graphique(self, nom_theme: str) -> None:
        """Applique un thème graphique complet ("Crème & Sauge", etc.).

        Args:
            nom_theme: Nom du thème présent dans THEMES_GRAPHIQUES.
        """
        if nom_theme in THEMES_GRAPHIQUES:
            palette_theme: dict[str, tuple[int, int, int]] = (
                THEMES_GRAPHIQUES[nom_theme]
            )
            self.nom_theme_actif = nom_theme
            self.couleur_fond_active = palette_theme["fond"]
            self.couleur_eau_active = palette_theme["eau"]
            self.couleur_bordure_eau_active = palette_theme["bordure_eau"]
            self.couleur_montagne_active = palette_theme["montagne"]
            self.couleur_bordure_montagne_active = palette_theme[
                "bordure_montagne"
            ]
            self.couleur_sommet_active = palette_theme["sommet_montagne"]
            self.couleur_grille_active = palette_theme["grille"]
            self.couleur_texte_hud_active = palette_theme["texte_hud"]
        else:
            pass

    def definir_theme_carte(self, nom_carte: str) -> None:
        """Sélectionne automatiquement le thème pastel associé à une carte.

        Args:
            nom_carte: Nom de la carte choisie ("Plaine", "Rivière", etc.).
        """
        if nom_carte in THEME_PAR_CARTE:
            self.definir_theme_graphique(THEME_PAR_CARTE[nom_carte])
        else:
            self.definir_theme_graphique(THEME_CREME_SAUGE)

    def calculer_couleur_ombre_fond(self) -> tuple[int, int, int]:
        """Calcule une teinte d'ombre douce harmonisée avec le fond actif.

        Returns:
            Un tuple RGB légèrement plus sombre que le fond de carte actuel.
        """
        facteur_ombre: float = float(ALPHA_OMBRE_PORTEE) / float(
             ALPHA_OMBRE_PORTEE + COULEUR_FOND[COORDONNEE_ORIGINE]
        )
        rouge_fond, vert_fond, bleu_fond = self.couleur_fond_active
        rouge_ombre, vert_ombre, bleu_ombre = COULEUR_OMBRE_PORTEE
        rouge_final: int = int(
            round(
                float(rouge_fond) * (FACTEUR_ECHELLE_UNITE - facteur_ombre)
                + float(rouge_ombre) * facteur_ombre
            )
        )
        vert_final: int = int(
            round(
                float(vert_fond) * (FACTEUR_ECHELLE_UNITE - facteur_ombre)
                + float(vert_ombre) * facteur_ombre
            )
        )
        bleu_final: int = int(
            round(
                float(bleu_fond) * (FACTEUR_ECHELLE_UNITE - facteur_ombre)
                + float(bleu_ombre) * facteur_ombre
            )
        )
        return (rouge_final, vert_final, bleu_final)

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
        """Remplit l'écran avec la couleur de fond du thème actif."""
        self.ecran.fill(self.couleur_fond_active)

    def est_case_relief_eau(
        self,
        grille: Grid,
        ligne: int,
        colonne: int,
    ) -> bool:
        """Vérifie si une case appartient au lit d'une rivière (eau ou pont).

        Args:
            grille: Instance du modèle Grid.
            ligne: Indice de ligne.
            colonne: Indice de colonne.

        Returns:
            True si la case est de l'eau ou un pont, False sinon.
        """
        if not grille.est_coordonnee_valide(ligne, colonne):
            return False
        else:
            return (
                grille.est_case_eau(ligne, colonne)
                or grille.est_case_pont(ligne, colonne)
            )

    def est_case_relief_montagne(
        self,
        grille: Grid,
        ligne: int,
        colonne: int,
    ) -> bool:
        """Vérifie si une case appartient à un massif (montagne ou tunnel).

        Args:
            grille: Instance du modèle Grid.
            ligne: Indice de ligne.
            colonne: Indice de colonne.

        Returns:
            True si la case est une montagne ou un tunnel, False sinon.
        """
        if not grille.est_coordonnee_valide(ligne, colonne):
            return False
        else:
            return (
                grille.est_case_montagne(ligne, colonne)
                or grille.est_case_tunnel(ligne, colonne)
            )

    def dessiner_passe_relief_organique(
        self,
        grille: Grid,
        colonne_debut_camera: float,
        ligne_debut_camera: float,
        taille_case_camera: float,
        est_passe_eau: bool,
        couleur_passe: tuple[int, int, int],
        diametre_pixels: int,
    ) -> None:
        """Trace une couche organique continue (disques et raccords épais).

        Args:
            grille: Instance du modèle Grid à parcourir.
            colonne_debut_camera: Colonne du bord gauche de la caméra.
            ligne_debut_camera: Ligne du bord supérieur de la caméra.
            taille_case_camera: Taille d'une case en pixels écran.
            est_passe_eau: True pour l'eau, False pour les montagnes.
            couleur_passe: Couleur RGB de la couche à dessiner.
            diametre_pixels: Épaisseur des raccords entre cases voisines.
        """
        rayon_disque: int = diametre_pixels // DIVISEUR_MOITIE
        if rayon_disque < DIMENSION_PIXEL_MINIMALE:
            rayon_disque = DIMENSION_PIXEL_MINIMALE
        else:
            pass

        for indice_ligne in range(grille.nb_lignes):
            for indice_colonne in range(grille.nb_colonnes):
                if est_passe_eau:
                    case_active: bool = self.est_case_relief_eau(
                        grille,
                        indice_ligne,
                        indice_colonne,
                    )
                else:
                    case_active = self.est_case_relief_montagne(
                        grille,
                        indice_ligne,
                        indice_colonne,
                    )

                if case_active:
                    centre_case: tuple[int, int] = (
                        self.convertir_monde_en_ecran(
                            float(indice_colonne) + DECALAGE_CENTRE_CASE,
                            float(indice_ligne) + DECALAGE_CENTRE_CASE,
                            colonne_debut_camera,
                            ligne_debut_camera,
                            taille_case_camera,
                        )
                    )
                    pygame.draw.circle(
                        self.ecran,
                        couleur_passe,
                        centre_case,
                        rayon_disque,
                    )
                    for dec_lig, dec_col in DIRECTIONS_HUIT_VOISINS:
                        lig_voisin: int = indice_ligne + dec_lig
                        col_voisin: int = indice_colonne + dec_col
                        if est_passe_eau:
                            voisin_actif: bool = self.est_case_relief_eau(
                                grille,
                                lig_voisin,
                                col_voisin,
                            )
                        else:
                            voisin_actif = self.est_case_relief_montagne(
                                grille,
                                lig_voisin,
                                col_voisin,
                            )
                        if voisin_actif:
                            centre_voisin: tuple[int, int] = (
                                self.convertir_monde_en_ecran(
                                    float(col_voisin) + DECALAGE_CENTRE_CASE,
                                    float(lig_voisin) + DECALAGE_CENTRE_CASE,
                                    colonne_debut_camera,
                                    ligne_debut_camera,
                                    taille_case_camera,
                                )
                            )
                            pygame.draw.line(
                                self.ecran,
                                couleur_passe,
                                centre_case,
                                centre_voisin,
                                diametre_pixels,
                            )
                        else:
                            pass
                else:
                    pass

    def dessiner_obstacles_naturels(
        self,
        grille: Grid,
        colonne_debut_camera: float,
        ligne_debut_camera: float,
        taille_case_camera: float,
        facteur_zoom: float,
    ) -> None:
        """Dessine les rivières et montagnes avec des contours organiques doux.

        Args:
            grille: Instance du modèle Grid à parcourir.
            colonne_debut_camera: Colonne du bord gauche de la caméra.
            ligne_debut_camera: Ligne du bord supérieur de la caméra.
            taille_case_camera: Taille d'une case en pixels écran.
            facteur_zoom: Facteur d'échelle actuel.
        """
        diametre_coeur: int = int(round(taille_case_camera))
        if diametre_coeur < DIMENSION_PIXEL_MINIMALE:
            diametre_coeur = DIMENSION_PIXEL_MINIMALE
        else:
            pass
        bordure_zoom: int = self.mettre_a_echelle(
            BORDURE_RELIEF_ORGANIQUE,
            facteur_zoom,
        )
        diametre_bordure: int = (
            diametre_coeur + FACTEUR_DOUBLE_MARGE * bordure_zoom
        )
        diametre_sommet: int = self.mettre_a_echelle(
            FACTEUR_DOUBLE_MARGE * RAYON_SOMMET_RELIEF,
            facteur_zoom,
        )

        self.dessiner_passe_relief_organique(
            grille,
            colonne_debut_camera,
            ligne_debut_camera,
            taille_case_camera,
            True,
            self.couleur_bordure_eau_active,
            diametre_bordure,
        )
        self.dessiner_passe_relief_organique(
            grille,
            colonne_debut_camera,
            ligne_debut_camera,
            taille_case_camera,
            True,
            self.couleur_eau_active,
            diametre_coeur,
        )

        self.dessiner_passe_relief_organique(
            grille,
            colonne_debut_camera,
            ligne_debut_camera,
            taille_case_camera,
            False,
            self.couleur_bordure_montagne_active,
            diametre_bordure,
        )
        self.dessiner_passe_relief_organique(
            grille,
            colonne_debut_camera,
            ligne_debut_camera,
            taille_case_camera,
            False,
            self.couleur_montagne_active,
            diametre_coeur,
        )
        self.dessiner_passe_relief_organique(
            grille,
            colonne_debut_camera,
            ligne_debut_camera,
            taille_case_camera,
            False,
            self.couleur_sommet_active,
            diametre_sommet,
        )

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
                self.couleur_grille_active,
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
                self.couleur_grille_active,
                point_depart_vertical,
                point_fin_vertical,
                EPAISSEUR_LIGNE_GRILLE,
            )

    def assombrir_couleur(
        self,
        couleur: tuple[int, int, int],
        delta: int,
    ) -> tuple[int, int, int]:
        """Assombrit légèrement une couleur RGB sans descendre sous zéro.

        Args:
            couleur: Tuple (R, G, B) de départ.
            delta: Valeur entière à soustraire à chaque canal.

        Returns:
            Nouveau tuple (R, G, B) assombri.
        """
        canal_r, canal_g, canal_b = couleur
        nouveau_r: int = canal_r - delta
        if nouveau_r < COORDONNEE_ORIGINE:
            nouveau_r = COORDONNEE_ORIGINE
        else:
            pass
        nouveau_g: int = canal_g - delta
        if nouveau_g < COORDONNEE_ORIGINE:
            nouveau_g = COORDONNEE_ORIGINE
        else:
            pass
        nouveau_b: int = canal_b - delta
        if nouveau_b < COORDONNEE_ORIGINE:
            nouveau_b = COORDONNEE_ORIGINE
        else:
            pass
        return (nouveau_r, nouveau_g, nouveau_b)

    def dessiner_maisons(
        self,
        maisons: list[Maison],
        colonne_debut_camera: float,
        ligne_debut_camera: float,
        taille_case_camera: float,
        facteur_zoom: float,
    ) -> None:
        """Dessine chaque maison avec ombre portée, socle orienté et toit.

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
        decalage_ombre_x: int = self.mettre_a_echelle(
            DECALAGE_OMBRE_X,
            facteur_zoom,
        )
        decalage_ombre_y: int = self.mettre_a_echelle(
            DECALAGE_OMBRE_Y,
            facteur_zoom,
        )
        largeur_allee_zoom: int = self.mettre_a_echelle(
            LARGEUR_ALLEE_MAISON,
            facteur_zoom,
        )
        marge_toit_zoom: int = self.mettre_a_echelle(
            MARGE_TOIT_INTERIEUR_MAISON,
            facteur_zoom,
        )
        couleur_ombre: tuple[int, int, int] = (
            self.calculer_couleur_ombre_fond()
        )

        for maison in maisons:
            case_x, case_y = self.convertir_monde_en_ecran(
                float(maison.colonne),
                float(maison.ligne),
                colonne_debut_camera,
                ligne_debut_camera,
                taille_case_camera,
            )
            centre_maison: tuple[int, int] = self.convertir_monde_en_ecran(
                float(maison.colonne) + DECALAGE_CENTRE_CASE,
                float(maison.ligne) + DECALAGE_CENTRE_CASE,
                colonne_debut_camera,
                ligne_debut_camera,
                taille_case_camera,
            )
            rectangle_ombre: pygame.Rect = pygame.Rect(
                case_x + marge_maison_zoom + decalage_ombre_x,
                case_y + marge_maison_zoom + decalage_ombre_y,
                taille_maison,
                taille_maison,
            )
            pygame.draw.rect(
                self.ecran,
                couleur_ombre,
                rectangle_ombre,
                border_radius=rayon_bordure,
            )

            if maison.case_sortie is not None:
                lig_sortie, col_sortie = maison.case_sortie
                centre_sortie: tuple[int, int] = self.convertir_monde_en_ecran(
                    float(col_sortie) + DECALAGE_CENTRE_CASE,
                    float(lig_sortie) + DECALAGE_CENTRE_CASE,
                    colonne_debut_camera,
                    ligne_debut_camera,
                    taille_case_camera,
                )
                milieu_allee_x: int = (
                    centre_maison[COORDONNEE_ORIGINE]
                    + centre_sortie[COORDONNEE_ORIGINE]
                ) // DIVISEUR_MOITIE
                milieu_allee_y: int = (
                    centre_maison[PAS_INCREMENT_COMPTEUR]
                    + centre_sortie[PAS_INCREMENT_COMPTEUR]
                ) // DIVISEUR_MOITIE
                pygame.draw.line(
                    self.ecran,
                    COULEUR_SOCLE_MAISON,
                    centre_maison,
                    (milieu_allee_x, milieu_allee_y),
                    largeur_allee_zoom,
                )
            else:
                pass

            rectangle_socle: pygame.Rect = pygame.Rect(
                case_x + marge_maison_zoom - DIMENSION_PIXEL_MINIMALE,
                case_y + marge_maison_zoom - DIMENSION_PIXEL_MINIMALE,
                taille_maison + FACTEUR_DOUBLE_MARGE,
                taille_maison + FACTEUR_DOUBLE_MARGE,
            )
            pygame.draw.rect(
                self.ecran,
                COULEUR_SOCLE_MAISON,
                rectangle_socle,
                border_radius=rayon_bordure,
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

            taille_faite: int = (
                taille_maison - FACTEUR_DOUBLE_MARGE * marge_toit_zoom
            )
            if taille_faite > DIMENSION_PIXEL_MINIMALE:
                couleur_faite: tuple[int, int, int] = self.assombrir_couleur(
                    maison.couleur,
                    ASSOMBRISSEMENT_FAITE_MAISON,
                )
                rectangle_faite: pygame.Rect = pygame.Rect(
                    case_x + marge_maison_zoom + marge_toit_zoom,
                    case_y + marge_maison_zoom + marge_toit_zoom,
                    taille_faite,
                    taille_faite,
                )
                pygame.draw.rect(
                    self.ecran,
                    couleur_faite,
                    rectangle_faite,
                    border_radius=rayon_bordure,
                )
            else:
                pass

    def dessiner_demandes_usine(
        self,
        usine: Usine,
        case_x: int,
        case_y: int,
        facteur_zoom: float,
    ) -> None:
        """Dessine les pastilles blanches de demandes avec point central coloré.

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
        rayon_centre_zoom: int = self.mettre_a_echelle(
            RAYON_POINT_CENTRE_DEMANDE,
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
                usine.couleur,
                centre_point,
                rayon_centre_zoom,
            )

    def dessiner_usines(
        self,
        usines: list[Usine],
        colonne_debut_camera: float,
        ligne_debut_camera: float,
        taille_case_camera: float,
        facteur_zoom: float,
    ) -> None:
        """Dessine chaque usine avec ombre, corps ardoise, parking et toit.

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
        decalage_ombre_x: int = self.mettre_a_echelle(
            DECALAGE_OMBRE_X,
            facteur_zoom,
        )
        decalage_ombre_y: int = self.mettre_a_echelle(
            DECALAGE_OMBRE_Y,
            facteur_zoom,
        )
        marge_toit_zoom: int = self.mettre_a_echelle(
            MARGE_TOIT_USINE,
            facteur_zoom,
        )
        largeur_parking_zoom: int = self.mettre_a_echelle(
            LARGEUR_ZONE_PARKING_USINE,
            facteur_zoom,
        )
        epaisseur_parking_zoom: int = self.mettre_a_echelle(
            EPAISSEUR_LIGNE_PARKING,
            facteur_zoom,
        )
        couleur_ombre: tuple[int, int, int] = (
            self.calculer_couleur_ombre_fond()
        )

        for usine in usines:
            case_x, case_y = self.convertir_monde_en_ecran(
                float(usine.colonne),
                float(usine.ligne),
                colonne_debut_camera,
                ligne_debut_camera,
                taille_case_camera,
            )
            rectangle_ombre: pygame.Rect = pygame.Rect(
                case_x + marge_usine_zoom + decalage_ombre_x,
                case_y + marge_usine_zoom + decalage_ombre_y,
                taille_usine,
                taille_usine,
            )
            pygame.draw.rect(
                self.ecran,
                couleur_ombre,
                rectangle_ombre,
                border_radius=rayon_bordure,
            )

            rectangle_usine: pygame.Rect = pygame.Rect(
                case_x + marge_usine_zoom,
                case_y + marge_usine_zoom,
                taille_usine,
                taille_usine,
            )
            pygame.draw.rect(
                self.ecran,
                COULEUR_CORPS_USINE,
                rectangle_usine,
                border_radius=rayon_bordure,
            )

            pas_place_y: int = taille_usine // (
                NB_PLACES_PARKING_USINE + INCREMENT_BORNE_GRILLE
            )
            depart_ligne_x: int = (
                rectangle_usine.right - largeur_parking_zoom
            )
            fin_ligne_x: int = (
                rectangle_usine.right - marge_usine_zoom
            )
            for indice_ligne_pk in range(
                PAS_INCREMENT_COMPTEUR,
                NB_PLACES_PARKING_USINE + INCREMENT_BORNE_GRILLE,
            ):
                pos_ligne_y: int = (
                    rectangle_usine.top + indice_ligne_pk * pas_place_y
                )
                pygame.draw.line(
                    self.ecran,
                    COULEUR_LIGNE_PARKING_USINE,
                    (depart_ligne_x, pos_ligne_y),
                    (fin_ligne_x, pos_ligne_y),
                    epaisseur_parking_zoom,
                )

            largeur_toit: int = (
                taille_usine - largeur_parking_zoom - marge_toit_zoom
            )
            hauteur_toit: int = (
                taille_usine - FACTEUR_DOUBLE_MARGE * marge_toit_zoom
            )
            if (
                largeur_toit > DIMENSION_PIXEL_MINIMALE
                and hauteur_toit > DIMENSION_PIXEL_MINIMALE
            ):
                rectangle_toit: pygame.Rect = pygame.Rect(
                    rectangle_usine.left + marge_toit_zoom,
                    rectangle_usine.top + marge_toit_zoom,
                    largeur_toit,
                    hauteur_toit,
                )
                parite_usine: int = (
                    usine.ligne + usine.colonne
                ) % DIVISEUR_PARITE_USINE
                if parite_usine == COORDONNEE_ORIGINE:
                    pygame.draw.rect(
                        self.ecran,
                        usine.couleur,
                        rectangle_toit,
                        border_radius=rayon_bordure,
                    )
                else:
                    rayon_toit_circulaire: int = (
                        min(largeur_toit, hauteur_toit) // DIVISEUR_MOITIE
                    )
                    pygame.draw.circle(
                        self.ecran,
                        usine.couleur,
                        rectangle_toit.center,
                        rayon_toit_circulaire,
                    )
            else:
                pass

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
        decalage_x: int = COORDONNEE_ORIGINE,
        decalage_y: int = COORDONNEE_ORIGINE,
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
            decalage_x: Décalage horizontal en pixels (pour l'ombre portée).
            decalage_y: Décalage vertical en pixels (pour l'ombre portée).
        """
        centre_base_x, centre_base_y = self.convertir_monde_en_ecran(
            float(colonne) + DECALAGE_CENTRE_CASE,
            float(ligne) + DECALAGE_CENTRE_CASE,
            colonne_debut_camera,
            ligne_debut_camera,
            taille_case_camera,
        )
        point_centre_case: tuple[int, int] = (
            centre_base_x + decalage_x,
            centre_base_y + decalage_y,
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
                voisin_base_x, voisin_base_y = self.convertir_monde_en_ecran(
                    float(voisin_colonne) + DECALAGE_CENTRE_CASE,
                    float(voisin_ligne) + DECALAGE_CENTRE_CASE,
                    colonne_debut_camera,
                    ligne_debut_camera,
                    taille_case_camera,
                )
                point_centre_voisin: tuple[int, int] = (
                    voisin_base_x + decalage_x,
                    voisin_base_y + decalage_y,
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
        decalage_x: int = COORDONNEE_ORIGINE,
        decalage_y: int = COORDONNEE_ORIGINE,
    ) -> None:
        """Exécute une passe complète (ombre, bordure ou chaussée) sur routes.

        Args:
            grille: Instance du modèle Grid à parcourir.
            colonne_debut_camera: Colonne du bord gauche de la caméra.
            ligne_debut_camera: Ligne du bord supérieur de la caméra.
            taille_case_camera: Taille d'une case en pixels écran.
            couleur_ruban: Couleur RGB de la couche à tracer.
            largeur_ruban_pixels: Largeur en pixels du ruban à tracer.
            decalage_x: Décalage horizontal en pixels (pour l'ombre portée).
            decalage_y: Décalage vertical en pixels (pour l'ombre portée).
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
                        decalage_x,
                        decalage_y,
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
        """Dessine les routes avec ombre portée, bordure et asphalte ardoise.

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
        decalage_ombre_x: int = self.mettre_a_echelle(
            DECALAGE_OMBRE_X,
            facteur_zoom,
        )
        decalage_ombre_y: int = self.mettre_a_echelle(
            DECALAGE_OMBRE_Y,
            facteur_zoom,
        )
        couleur_ombre: tuple[int, int, int] = (
            self.calculer_couleur_ombre_fond()
        )

        self.dessiner_passe_ruban_routes(
            grille,
            colonne_debut_camera,
            ligne_debut_camera,
            taille_case_camera,
            couleur_ombre,
            largeur_bordure_zoom,
            decalage_ombre_x,
            decalage_ombre_y,
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
        """Dessine les autoroutes en courbe de Bézier avec ombre et badge.

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
        rayon_badge_zoom: int = self.mettre_a_echelle(
            RAYON_BADGE_AUTOROUTE,
            facteur_zoom,
        )
        decalage_ombre_x: int = self.mettre_a_echelle(
            DECALAGE_OMBRE_AUTOROUTE_X,
            facteur_zoom,
        )
        decalage_ombre_y: int = self.mettre_a_echelle(
            DECALAGE_OMBRE_AUTOROUTE_Y,
            facteur_zoom,
        )
        fleche_arche_pixels: float = HAUTEUR_ARCHE_AUTOROUTE * facteur_zoom
        couleur_ombre: tuple[int, int, int] = (
            self.calculer_couleur_ombre_fond()
        )

        for indice_auto, (case_a, case_b) in enumerate(grille.autoroutes):
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

            controle_x: float = (
                float(depart_x + arrivee_x) * PROGRESSION_MILIEU_COURBE
            )
            controle_y: float = (
                float(depart_y + arrivee_y) * PROGRESSION_MILIEU_COURBE
                - FACTEUR_BEZIER_QUADRATIQUE * fleche_arche_pixels
            )

            points_arche: list[tuple[int, int]] = []
            points_ombre: list[tuple[int, int]] = []
            for indice_seg in range(
                NB_SEGMENTS_ARCHE_AUTOROUTE + INCREMENT_BORNE_GRILLE
            ):
                t_courbe: float = float(indice_seg) / float(
                    NB_SEGMENTS_ARCHE_AUTOROUTE
                )
                un_moins_t: float = FACTEUR_ECHELLE_UNITE - t_courbe
                bezier_x: float = (
                    un_moins_t * un_moins_t * float(depart_x)
                    + FACTEUR_BEZIER_QUADRATIQUE
                    * un_moins_t
                    * t_courbe
                    * controle_x
                    + t_courbe * t_courbe * float(arrivee_x)
                )
                bezier_y: float = (
                    un_moins_t * un_moins_t * float(depart_y)
                    + FACTEUR_BEZIER_QUADRATIQUE
                    * un_moins_t
                    * t_courbe
                    * controle_y
                    + t_courbe * t_courbe * float(arrivee_y)
                )
                pt_x: int = int(round(bezier_x))
                pt_y: int = int(round(bezier_y))
                points_arche.append((pt_x, pt_y))
                points_ombre.append(
                    (pt_x + decalage_ombre_x, pt_y + decalage_ombre_y)
                )

            for indice_pt in range(NB_SEGMENTS_ARCHE_AUTOROUTE):
                ombre_debut: tuple[int, int] = points_ombre[indice_pt]
                ombre_fin: tuple[int, int] = points_ombre[
                    indice_pt + INCREMENT_BORNE_GRILLE
                ]
                pygame.draw.line(
                    self.ecran,
                    couleur_ombre,
                    ombre_debut,
                    ombre_fin,
                    largeur_autoroute_zoom,
                )

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

            indice_milieu: int = (
                NB_SEGMENTS_ARCHE_AUTOROUTE // DIVISEUR_MOITIE
            )
            centre_badge: tuple[int, int] = points_arche[indice_milieu]
            pygame.draw.circle(
                self.ecran,
                COULEUR_BORDURE_AUTOROUTE,
                centre_badge,
                rayon_badge_zoom + BORDURE_BADGE_AUTOROUTE,
            )
            pygame.draw.circle(
                self.ecran,
                COULEUR_AUTOROUTE,
                centre_badge,
                rayon_badge_zoom,
            )
            numero_autoroute: int = indice_auto + PAS_INCREMENT_COMPTEUR
            surface_numero: pygame.Surface = self.police_pastille_dock.render(
                str(numero_autoroute),
                True,
                COULEUR_ICONE_HUD_SOMBRE,
            )
            rect_numero: pygame.Rect = surface_numero.get_rect(
                center=centre_badge
            )
            self.ecran.blit(surface_numero, rect_numero)

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

    def dessiner_bouton_retour_hud(self) -> None:
        """Dessine le bouton circulaire de retour vers le menu en haut à gauche."""
        centre_bouton: tuple[int, int] = (
            CENTRE_BOUTON_RETOUR_X,
            CENTRE_BOUTON_RETOUR_Y,
        )
        pygame.draw.circle(
            self.ecran,
            COULEUR_FOND_BOUTON_HUD,
            centre_bouton,
            RAYON_BOUTON_RETOUR,
        )
        pygame.draw.circle(
            self.ecran,
            COULEUR_CONTOUR_BATIMENT,
            centre_bouton,
            RAYON_BOUTON_RETOUR,
            width=EPAISSEUR_CONTOUR_INTERFACE,
        )
        pointe_gauche: tuple[int, int] = (
            CENTRE_BOUTON_RETOUR_X - TAILLE_FLECHE_RETOUR,
            CENTRE_BOUTON_RETOUR_Y,
        )
        branche_haut: tuple[int, int] = (
            CENTRE_BOUTON_RETOUR_X,
            CENTRE_BOUTON_RETOUR_Y - TAILLE_FLECHE_RETOUR,
        )
        branche_bas: tuple[int, int] = (
            CENTRE_BOUTON_RETOUR_X,
            CENTRE_BOUTON_RETOUR_Y + TAILLE_FLECHE_RETOUR,
        )
        queue_droite: tuple[int, int] = (
            CENTRE_BOUTON_RETOUR_X + TAILLE_FLECHE_RETOUR,
            CENTRE_BOUTON_RETOUR_Y,
        )
        pygame.draw.line(
            self.ecran,
            COULEUR_ICONE_HUD_SOMBRE,
            pointe_gauche,
            branche_haut,
            EPAISSEUR_FLECHE_RETOUR,
        )
        pygame.draw.line(
            self.ecran,
            COULEUR_ICONE_HUD_SOMBRE,
            pointe_gauche,
            branche_bas,
            EPAISSEUR_FLECHE_RETOUR,
        )
        pygame.draw.line(
            self.ecran,
            COULEUR_ICONE_HUD_SOMBRE,
            pointe_gauche,
            queue_droite,
            EPAISSEUR_FLECHE_RETOUR,
        )

    def dessiner_epingle_score(
        self,
        centre_x: int,
        centre_y: int,
    ) -> None:
        """Dessine une icône d'épingle de localisation (pin) à côté du score.

        Args:
            centre_x: Coordonnée X de la tête circulaire de l'épingle.
            centre_y: Coordonnée Y de la tête circulaire de l'épingle.
        """
        couleur_epingle: tuple[int, int, int] = self.couleur_texte_hud_active
        pointe_bas: tuple[int, int] = (
            centre_x,
            centre_y + HAUTEUR_POINTE_EPINGLE,
        )
        cote_gauche: tuple[int, int] = (
            centre_x - DEMI_LARGEUR_POINTE_EPINGLE,
            centre_y + RAYON_TROU_EPINGLE,
        )
        cote_droit: tuple[int, int] = (
            centre_x + DEMI_LARGEUR_POINTE_EPINGLE,
            centre_y + RAYON_TROU_EPINGLE,
        )
        pygame.draw.polygon(
            self.ecran,
            couleur_epingle,
            [cote_gauche, cote_droit, pointe_bas],
        )
        pygame.draw.circle(
            self.ecran,
            couleur_epingle,
            (centre_x, centre_y),
            RAYON_TETE_EPINGLE,
        )
        pygame.draw.circle(
            self.ecran,
            self.couleur_fond_active,
            (centre_x, centre_y),
            RAYON_TROU_EPINGLE,
        )

    def dessiner_bandeau_score(self, score: int) -> None:
        """Affiche l'épingle de localisation et le score en haut à droite.

        Args:
            score: Nombre total de livraisons effectuées.
        """
        self.dessiner_epingle_score(
            CENTRE_EPINGLE_SCORE_X,
            CENTRE_EPINGLE_SCORE_Y,
        )
        surface_texte: pygame.Surface = self.police_score_hud.render(
            str(score),
            True,
            self.couleur_texte_hud_active,
        )
        rectangle_texte: pygame.Rect = surface_texte.get_rect(
            midleft=(
                POSITION_SCORE_HUD_X - DEMI_TAILLE_LOSANGE_ROUTES,
                POSITION_SCORE_HUD_Y,
            )
        )
        self.ecran.blit(surface_texte, rectangle_texte)

    def dessiner_bandeau_routes(self, stock_routes: int) -> None:
        """Dessine le losange central noir affichant le stock de routes en bas.

        Args:
            stock_routes: Nombre de cases de route restantes dans l'inventaire.
        """
        sommet_haut: tuple[int, int] = (
            CENTRE_DOCK_X,
            CENTRE_DOCK_Y - DEMI_TAILLE_LOSANGE_ROUTES,
        )
        sommet_droite: tuple[int, int] = (
            CENTRE_DOCK_X + DEMI_TAILLE_LOSANGE_ROUTES,
            CENTRE_DOCK_Y,
        )
        sommet_bas: tuple[int, int] = (
            CENTRE_DOCK_X,
            CENTRE_DOCK_Y + DEMI_TAILLE_LOSANGE_ROUTES,
        )
        sommet_gauche: tuple[int, int] = (
            CENTRE_DOCK_X - DEMI_TAILLE_LOSANGE_ROUTES,
            CENTRE_DOCK_Y,
        )
        points_losange: list[tuple[int, int]] = [
            sommet_haut,
            sommet_droite,
            sommet_bas,
            sommet_gauche,
        ]
        pygame.draw.polygon(
            self.ecran,
            COULEUR_LOSANGE_ROUTES,
            points_losange,
        )
        pygame.draw.polygon(
            self.ecran,
            COULEUR_FOND_BOUTON_HUD,
            points_losange,
            width=EPAISSEUR_CONTOUR_INTERFACE,
        )
        surface_stock: pygame.Surface = self.police_score.render(
            str(stock_routes),
            True,
            COULEUR_TEXTE_LOSANGE_ROUTES,
        )
        rectangle_stock: pygame.Rect = surface_stock.get_rect(
            center=(CENTRE_DOCK_X, CENTRE_DOCK_Y)
        )
        self.ecran.blit(surface_stock, rectangle_stock)

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

    def dessiner_pastille_stock_dock(
        self,
        centre_bouton_x: int,
        centre_bouton_y: int,
        quantite: int,
    ) -> None:
        """Dessine la petite pastille circulaire de quantité sur un bouton dock.

        Args:
            centre_bouton_x: Coordonnée X du bouton circulaire parent.
            centre_bouton_y: Coordonnée Y du bouton circulaire parent.
            quantite: Stock disponible à afficher dans la pastille.
        """
        centre_pastille: tuple[int, int] = (
            centre_bouton_x + DECALAGE_PASTILLE_STOCK_X,
            centre_bouton_y + DECALAGE_PASTILLE_STOCK_Y,
        )
        pygame.draw.circle(
            self.ecran,
            COULEUR_PASTILLE_STOCK,
            centre_pastille,
            RAYON_PASTILLE_STOCK_DOCK,
        )
        surface_qte: pygame.Surface = self.police_pastille_dock.render(
            str(quantite),
            True,
            COULEUR_TEXTE_PASTILLE_STOCK,
        )
        rect_qte: pygame.Rect = surface_qte.get_rect(center=centre_pastille)
        self.ecran.blit(surface_qte, rect_qte)

    def dessiner_barre_outils_bonus(
        self,
        grille: Grid,
        outil_actif: int = OUTIL_ROUTE,
    ) -> None:
        """Affiche les boutons circulaires de bonus autour du losange central.

        Args:
            grille: Instance du modèle Grid contenant les stocks de bonus.
            outil_actif: Identifiant de l'outil actuellement sélectionné.
        """
        boutons_dock: list[tuple[int, int, str, int]] = [
            (
                INDICE_DOCK_ROND_POINT,
                OUTIL_ROND_POINT,
                "O",
                grille.stock_ronds_points,
            ),
            (
                INDICE_DOCK_FEU,
                OUTIL_FEU,
                "F",
                grille.stock_feux,
            ),
            (
                INDICE_DOCK_PONT_TUNNEL,
                OUTIL_ROUTE,
                "P/T",
                grille.stock_ponts + grille.stock_tunnels,
            ),
            (
                INDICE_DOCK_AUTOROUTE,
                OUTIL_AUTOROUTE,
                "A",
                grille.stock_autoroutes,
            ),
        ]

        for position_rel, code_outil, icone_texte, stock_bonus in boutons_dock:
            centre_x: int = (
                CENTRE_DOCK_X + position_rel * ESPACEMENT_BOUTONS_DOCK_X
            )
            centre_y: int = CENTRE_DOCK_Y
            if code_outil == outil_actif:
                couleur_fond: tuple[int, int, int] = COULEUR_OUTIL_ACTIF
            else:
                couleur_fond = COULEUR_FOND_BOUTON_HUD

            pygame.draw.circle(
                self.ecran,
                couleur_fond,
                (centre_x, centre_y),
                RAYON_BOUTON_DOCK,
            )
            pygame.draw.circle(
                self.ecran,
                COULEUR_CONTOUR_BATIMENT,
                (centre_x, centre_y),
                RAYON_BOUTON_DOCK,
                width=EPAISSEUR_CONTOUR_INTERFACE,
            )

            if code_outil == OUTIL_ROND_POINT:
                pygame.draw.circle(
                    self.ecran,
                    COULEUR_ICONE_HUD_SOMBRE,
                    (centre_x, centre_y),
                    RAYON_INTERIEUR_ROND_POINT,
                    width=EPAISSEUR_CONTOUR_INTERFACE,
                )
            else:
                if code_outil == OUTIL_FEU:
                    pygame.draw.circle(
                        self.ecran,
                        COULEUR_FEU_ROUGE,
                        (centre_x, centre_y - DECALAGE_VOYANT_FEU),
                        RAYON_VOYANT_FEU,
                    )
                    pygame.draw.circle(
                        self.ecran,
                        COULEUR_FEU_VERT,
                        (centre_x, centre_y + DECALAGE_VOYANT_FEU),
                        RAYON_VOYANT_FEU,
                    )
                else:
                    surface_icone: pygame.Surface = self.police_outil.render(
                        icone_texte,
                        True,
                        COULEUR_ICONE_HUD_SOMBRE,
                    )
                    rect_icone: pygame.Rect = surface_icone.get_rect(
                        center=(centre_x, centre_y)
                    )
                    self.ecran.blit(surface_icone, rect_icone)

            self.dessiner_pastille_stock_dock(
                centre_x,
                centre_y,
                stock_bonus,
            )

    def dessiner_bandeau_mode_edition(self, mode_edition: bool) -> None:
        """Dessine le bouton circulaire Édition/Corbeille à droite du dock.

        Args:
            mode_edition: True si le Mode Édition est actif, False sinon.
        """
        centre_x: int = (
            CENTRE_DOCK_X + INDICE_DOCK_EDITION * ESPACEMENT_BOUTONS_DOCK_X
        )
        centre_y: int = CENTRE_DOCK_Y
        if mode_edition:
            couleur_fond: tuple[int, int, int] = COULEUR_BANDEAU_MODE_EDITION
        else:
            couleur_fond = COULEUR_FOND_BOUTON_HUD

        pygame.draw.circle(
            self.ecran,
            couleur_fond,
            (centre_x, centre_y),
            RAYON_BOUTON_DOCK,
        )
        pygame.draw.circle(
            self.ecran,
            COULEUR_CONTOUR_BATIMENT,
            (centre_x, centre_y),
            RAYON_BOUTON_DOCK,
            width=EPAISSEUR_CONTOUR_INTERFACE,
        )

        rect_corps_corbeille: pygame.Rect = pygame.Rect(
            centre_x - LARGEUR_ICONE_CORBEILLE // DIVISEUR_MOITIE,
            centre_y
            - HAUTEUR_ICONE_CORBEILLE // DIVISEUR_MOITIE
            + DECALAGE_COUVERCLE_CORBEILLE_Y,
            LARGEUR_ICONE_CORBEILLE,
            HAUTEUR_ICONE_CORBEILLE - DECALAGE_COUVERCLE_CORBEILLE_Y,
        )
        pygame.draw.rect(
            self.ecran,
            COULEUR_ICONE_HUD_SOMBRE,
            rect_corps_corbeille,
            width=EPAISSEUR_CONTOUR_INTERFACE,
        )
        pygame.draw.line(
            self.ecran,
            COULEUR_ICONE_HUD_SOMBRE,
            (
                rect_corps_corbeille.left - DIMENSION_PIXEL_MINIMALE,
                rect_corps_corbeille.top,
            ),
            (
                rect_corps_corbeille.right + DIMENSION_PIXEL_MINIMALE,
                rect_corps_corbeille.top,
            ),
            EPAISSEUR_CONTOUR_INTERFACE,
        )

    def dessiner_horloge_hud(
        self,
        nom_jour: str,
        numero_semaine: int,
        progression_jour: float,
    ) -> None:
        """Dessine le jour abrégé (LUN, MAR...) et l'horloge en haut à droite.

        Args:
            nom_jour: Nom du jour actuel (ex: "Lundi").
            numero_semaine: Numéro de la semaine en cours.
            progression_jour: Fraction écoulée de la journée (0.0 à 1.0).
        """
        if nom_jour in JOURS_SEMAINE_ABREGES:
            jour_abrege: str = JOURS_SEMAINE_ABREGES[nom_jour]
        else:
            jour_abrege = nom_jour[:LONGUEUR_ABREVIATION_JOUR].upper()

        surface_jour: pygame.Surface = self.police_jour_hud.render(
            f"{jour_abrege} S{numero_semaine}",
            True,
            self.couleur_texte_hud_active,
        )
        rectangle_jour: pygame.Rect = surface_jour.get_rect(
            center=(POSITION_JOUR_HUD_X, POSITION_JOUR_HUD_Y)
        )
        self.ecran.blit(surface_jour, rectangle_jour)

        centre_horloge: tuple[int, int] = (
            CENTRE_HORLOGE_HUD_X,
            CENTRE_HORLOGE_HUD_Y,
        )
        pygame.draw.circle(
            self.ecran,
            COULEUR_CADRAN_HORLOGE,
            centre_horloge,
            RAYON_HORLOGE_MINIMALISTE,
        )

        points_secteur: list[tuple[int, int]] = [centre_horloge]
        nb_etapes_arc: int = int(
            round(float(NB_SEGMENTS_SECTEUR_HORLOGE) * progression_jour)
        )
        if nb_etapes_arc >= PAS_INCREMENT_COMPTEUR:
            for indice_arc in range(nb_etapes_arc + PAS_INCREMENT_COMPTEUR):
                fraction_arc: float = float(indice_arc) / float(
                    NB_SEGMENTS_SECTEUR_HORLOGE
                )
                angle_courant: float = (
                    ANGLE_DEPART_HORLOGE_RAD
                    + fraction_arc * ANGLE_TOUR_COMPLET_RAD
                )
                point_x: int = int(
                    round(
                        float(CENTRE_HORLOGE_HUD_X)
                        + math.cos(angle_courant)
                        * float(RAYON_HORLOGE_MINIMALISTE)
                    )
                )
                point_y: int = int(
                    round(
                        float(CENTRE_HORLOGE_HUD_Y)
                        + math.sin(angle_courant)
                        * float(RAYON_HORLOGE_MINIMALISTE)
                    )
                )
                points_secteur.append((point_x, point_y))

            if len(points_secteur) > LONGUEUR_MINIMALE_ITINERAIRE:
                pygame.draw.polygon(
                    self.ecran,
                    COULEUR_SECTEUR_HORLOGE,
                    points_secteur,
                )
            else:
                pass
        else:
            pass

        angle_aiguille: float = (
            ANGLE_DEPART_HORLOGE_RAD
            + progression_jour * ANGLE_TOUR_COMPLET_RAD
        )
        extremite_x: int = int(
            round(
                float(CENTRE_HORLOGE_HUD_X)
                + math.cos(angle_aiguille)
                * float(
                    RAYON_HORLOGE_MINIMALISTE - EPAISSEUR_AIGUILLE_HORLOGE
                )
            )
        )
        extremite_y: int = int(
            round(
                float(CENTRE_HORLOGE_HUD_Y)
                + math.sin(angle_aiguille)
                * float(
                    RAYON_HORLOGE_MINIMALISTE - EPAISSEUR_AIGUILLE_HORLOGE
                )
            )
        )
        pygame.draw.line(
            self.ecran,
            COULEUR_ICONE_HUD_SOMBRE,
            centre_horloge,
            (extremite_x, extremite_y),
            EPAISSEUR_AIGUILLE_HORLOGE,
        )
        pygame.draw.circle(
            self.ecran,
            COULEUR_ICONE_HUD_SOMBRE,
            centre_horloge,
            RAYON_HORLOGE_MINIMALISTE,
            width=EPAISSEUR_AIGUILLE_HORLOGE,
        )

    def obtenir_rectangles_cartes_hebdomadaires(
        self,
    ) -> list[pygame.Rect]:
        """Retourne les rectangles cliquables des 2 offres hebdomadaires.

        Returns:
            Liste des 2 pygame.Rect (Option 1 à gauche, Option 2 à droite).
        """
        centre_ecran_x: int = LARGEUR_FENETRE // DIVISEUR_MOITIE
        centre_ecran_y: int = HAUTEUR_FENETRE // DIVISEUR_MOITIE
        panneau_y: int = (
            centre_ecran_y - HAUTEUR_PANNEAU_HEBDOMADAIRE // DIVISEUR_MOITIE
        )
        largeur_totale_cartes: int = (
            FACTEUR_DOUBLE_MARGE * LARGEUR_CARTE_OFFRE_HEBDO
            + ESPACEMENT_CARTES_OFFRE_X
        )
        depart_cartes_x: int = (
            centre_ecran_x - largeur_totale_cartes // DIVISEUR_MOITIE
        )
        cartes_y: int = panneau_y + DECALAGE_CARTES_MODALE_HEBDO_Y

        rectangles: list[pygame.Rect] = []
        for indice_carte in range(NB_OPTIONS_HEBDOMADAIRES):
            carte_x: int = depart_cartes_x + indice_carte * (
                LARGEUR_CARTE_OFFRE_HEBDO + ESPACEMENT_CARTES_OFFRE_X
            )
            rectangle_carte: pygame.Rect = pygame.Rect(
                carte_x,
                cartes_y,
                LARGEUR_CARTE_OFFRE_HEBDO,
                HAUTEUR_CARTE_OFFRE_HEBDO,
            )
            rectangles.append(rectangle_carte)
        return rectangles

    def dessiner_modale_choix_hebdomadaire(
        self,
        numero_semaine: int,
        offres: list[dict[str, int | str]],
    ) -> None:
        """Affiche la fenêtre modale de pause et de récompenses du lundi.

        Args:
            numero_semaine: Numéro de la nouvelle semaine.
            offres: Liste des 2 dictionnaires d'offres hebdomadaires.
        """
        centre_ecran_x: int = LARGEUR_FENETRE // DIVISEUR_MOITIE
        centre_ecran_y: int = HAUTEUR_FENETRE // DIVISEUR_MOITIE
        panneau_x: int = (
            centre_ecran_x - LARGEUR_PANNEAU_HEBDOMADAIRE // DIVISEUR_MOITIE
        )
        panneau_y: int = (
            centre_ecran_y - HAUTEUR_PANNEAU_HEBDOMADAIRE // DIVISEUR_MOITIE
        )
        rectangle_panneau: pygame.Rect = pygame.Rect(
            panneau_x,
            panneau_y,
            LARGEUR_PANNEAU_HEBDOMADAIRE,
            HAUTEUR_PANNEAU_HEBDOMADAIRE,
        )
        pygame.draw.rect(
            self.ecran,
            COULEUR_FOND_PANNEAU_DEFAITE,
            rectangle_panneau,
            border_radius=RAYON_BORDURE_INTERFACE,
        )
        pygame.draw.rect(
            self.ecran,
            COULEUR_SOUS_TEXTE_DEFAITE,
            rectangle_panneau,
            width=EPAISSEUR_CONTOUR_INTERFACE,
            border_radius=RAYON_BORDURE_INTERFACE,
        )

        surface_titre: pygame.Surface = (
            self.police_sous_titre_defaite.render(
                f"Lundi - Semaine {numero_semaine} : Dotation Hebdomadaire",
                True,
                COULEUR_SOUS_TEXTE_DEFAITE,
            )
        )
        rectangle_titre: pygame.Rect = surface_titre.get_rect(
            center=(
                centre_ecran_x,
                panneau_y + DECALAGE_TITRE_MODALE_HEBDO_Y,
            )
        )
        self.ecran.blit(surface_titre, rectangle_titre)

        surface_instruction: pygame.Surface = self.police_score.render(
            "Cliquez sur l'une des deux offres pour continuer la partie :",
            True,
            COULEUR_SOUS_TEXTE_DEFAITE,
        )
        rectangle_instruction: pygame.Rect = surface_instruction.get_rect(
            center=(
                centre_ecran_x,
                panneau_y + DECALAGE_SOUS_TITRE_MODALE_HEBDO_Y,
            )
        )
        self.ecran.blit(surface_instruction, rectangle_instruction)

        position_souris: tuple[int, int] = pygame.mouse.get_pos()
        rectangles_cartes: list[pygame.Rect] = (
            self.obtenir_rectangles_cartes_hebdomadaires()
        )

        for indice_offre, rectangle_carte in enumerate(rectangles_cartes):
            if indice_offre < len(offres):
                offre: dict[str, int | str] = offres[indice_offre]
                if rectangle_carte.collidepoint(position_souris):
                    couleur_carte: tuple[int, int, int] = COULEUR_OUTIL_ACTIF
                else:
                    couleur_carte = COULEUR_BOUTON_CARTE

                pygame.draw.rect(
                    self.ecran,
                    couleur_carte,
                    rectangle_carte,
                    border_radius=RAYON_BORDURE_INTERFACE,
                )
                pygame.draw.rect(
                    self.ecran,
                    COULEUR_CONTOUR_BATIMENT,
                    rectangle_carte,
                    width=EPAISSEUR_CONTOUR_INTERFACE,
                    border_radius=RAYON_BORDURE_INTERFACE,
                )

                surface_titre_offre: pygame.Surface = (
                    self.police_score.render(
                        str(offre["titre"]),
                        True,
                        COULEUR_TEXTE_INTERFACE,
                    )
                )
                rect_titre_offre: pygame.Rect = (
                    surface_titre_offre.get_rect(
                        center=(
                            rectangle_carte.centerx,
                            rectangle_carte.top
                            + DECALAGE_TITRE_CARTE_OFFRE_Y,
                        )
                    )
                )
                self.ecran.blit(surface_titre_offre, rect_titre_offre)

                surface_routes: pygame.Surface = (
                    self.police_sous_titre_defaite.render(
                        str(offre["texte_routes"]),
                        True,
                        COULEUR_TEXTE_INTERFACE,
                    )
                )
                rect_routes: pygame.Rect = surface_routes.get_rect(
                    center=(
                        rectangle_carte.centerx,
                        rectangle_carte.top + DECALAGE_ROUTES_CARTE_OFFRE_Y,
                    )
                )
                self.ecran.blit(surface_routes, rect_routes)

                surface_bonus: pygame.Surface = (
                    self.police_sous_titre_defaite.render(
                        str(offre["texte_bonus"]),
                        True,
                        COULEUR_SECTEUR_HORLOGE,
                    )
                )
                rect_bonus: pygame.Rect = surface_bonus.get_rect(
                    center=(
                        rectangle_carte.centerx,
                        rectangle_carte.top + DECALAGE_BONUS_CARTE_OFFRE_Y,
                    )
                )
                self.ecran.blit(surface_bonus, rect_bonus)

                numero_touche: int = (
                    indice_offre + PAS_INCREMENT_COMPTEUR
                )
                surface_aide: pygame.Surface = self.police_outil.render(
                    f"Clic gauche ou Touche [{numero_touche}]",
                    True,
                    COULEUR_TEXTE_INTERFACE,
                )
                rect_aide: pygame.Rect = surface_aide.get_rect(
                    center=(
                        rectangle_carte.centerx,
                        rectangle_carte.top + DECALAGE_AIDE_CARTE_OFFRE_Y,
                    )
                )
                self.ecran.blit(surface_aide, rect_aide)
            else:
                pass

    def afficher(
        self,
        grille: Grid,
        voitures: list[Voiture] | None = None,
        score: int = COMPTEUR_INITIAL_LIVRAISONS,
        partie_perdue: bool = False,
        parametres_camera: tuple[float, float, float, float] | None = None,
        outil_actif: int = OUTIL_ROUTE,
        nom_jour: str = JOURS_SEMAINE[INDICE_JOUR_LUNDI],
        numero_semaine: int = NUMERO_SEMAINE_INITIALE,
        progression_jour: float = COORDONNEE_CAMERA_ORIGINE_FLOAT,
        choix_hebdomadaire_actif: bool = False,
        offres_hebdomadaires: list[dict[str, int | str]] | None = None,
        mode_edition: bool = MODE_EDITION_INITIAL,
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
            nom_jour: Nom du jour actuel à afficher sur l'horloge HUD.
            numero_semaine: Numéro de la semaine en cours.
            progression_jour: Fraction de la journée écoulée (0.0 à 1.0).
            choix_hebdomadaire_actif: True si la modale du lundi est active.
            offres_hebdomadaires: Liste optionnelle des 2 offres du lundi.
            mode_edition: True pour afficher la grille et la barre d'outils.
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
        if mode_edition:
            self.dessiner_grille(
                grille,
                colonne_debut_cam,
                ligne_debut_cam,
                taille_case_cam,
            )
        else:
            pass
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
        self.dessiner_bouton_retour_hud()
        self.dessiner_bandeau_score(score)
        self.dessiner_bandeau_routes(grille.stock_routes)
        self.dessiner_bandeau_mode_edition(mode_edition)
        if mode_edition:
            self.dessiner_barre_outils_bonus(grille, outil_actif)
        else:
            pass
        self.dessiner_horloge_hud(
            nom_jour,
            numero_semaine,
            progression_jour,
        )
        if choix_hebdomadaire_actif and offres_hebdomadaires is not None:
            self.dessiner_modale_choix_hebdomadaire(
                numero_semaine,
                offres_hebdomadaires,
            )
        else:
            pass
        if partie_perdue:
            self.dessiner_ecran_defaite(score)
        else:
            pass
        pygame.display.flip()
