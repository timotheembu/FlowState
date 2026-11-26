"""Point d'entrée principal et boucle de jeu de FlowState."""

import pygame

from src.config import (
    BOUTON_SOURIS_GAUCHE,
    CARTES_CARROUSEL,
    CENTRE_BOUTON_RETOUR_X,
    CENTRE_BOUTON_RETOUR_Y,
    CONFIGURATIONS_CARTES,
    DECALAGE_VOISIN_NEGATIF,
    DECALAGE_VOISIN_NUL,
    DECALAGE_VOISIN_POSITIF,
    FPS,
    HAUTEUR_BANDEAU_CARTE_CENTRALE,
    HAUTEUR_FENETRE,
    INDICE_MINIMUM_GRILLE,
    LARGEUR_FENETRE,
    RAYON_BOUTON_RETOUR,
    THEME_CREME_SAUGE,
    TITRE_FENETRE,
)
from src.controllers.game_engine import (
    GameEngine,
    charger_meilleurs_scores,
)
from src.controllers.input_handler import InputHandler
from src.models.grid import Grid
from src.views.renderer import Renderer


def initialiser_themes_par_carte() -> dict[str, str]:
    """Construit le dictionnaire des thèmes sélectionnés par défaut par carte.

    Returns:
        Dictionnaire associant chaque ville à son thème graphique par défaut.
    """
    themes_initiaux: dict[str, str] = {}
    for nom_carte in CARTES_CARROUSEL:
        if nom_carte in CONFIGURATIONS_CARTES:
            config_carte: dict[str, str | tuple[int, int, int]] = (
                CONFIGURATIONS_CARTES[nom_carte]
            )
            themes_initiaux[nom_carte] = str(config_carte["theme_defaut"])
        else:
            themes_initiaux[nom_carte] = THEME_CREME_SAUGE
    return themes_initiaux


def choisir_carte_accueil(
    afficheur: Renderer,
    horloge: pygame.time.Clock,
    indice_initial: int = INDICE_MINIMUM_GRILLE,
    themes_par_carte: dict[str, str] | None = None,
) -> tuple[str, str, int] | None:
    """Affiche le carrousel de sélection de carte et retourne le choix.

    Args:
        afficheur: Instance de Renderer pour dessiner le menu carrousel.
        horloge: Horloge Pygame pour cadencer la boucle d'accueil.
        indice_initial: Indice de la carte sélectionnée au départ.
        themes_par_carte: Dictionnaire optionnel des variantes de thème.

    Returns:
        Un tuple (nom_carte, nom_theme, indice_carte), ou None si le joueur
        quitte l'application.
    """
    if themes_par_carte is not None:
        themes_actifs: dict[str, str] = themes_par_carte
    else:
        themes_actifs = initialiser_themes_par_carte()

    meilleurs_scores: dict[str, int] = charger_meilleurs_scores()
    nb_cartes: int = len(CARTES_CARROUSEL)
    indice_courant: int = indice_initial % nb_cartes
    gestionnaire_menu: InputHandler = InputHandler()
    en_attente_choix: bool = True

    while en_attente_choix:
        position_souris: tuple[int, int] = pygame.mouse.get_pos()
        nom_carte_centrale: str = CARTES_CARROUSEL[indice_courant]
        theme_carte_centrale: str = themes_actifs.get(
            nom_carte_centrale,
            THEME_CREME_SAUGE,
        )
        rectangle_centrale: pygame.Rect = (
            afficheur.obtenir_rectangle_carte_centrale_menu()
        )
        rectangle_gauche: pygame.Rect = (
            afficheur.obtenir_rectangle_carte_gauche_menu()
        )
        rectangle_droite: pygame.Rect = (
            afficheur.obtenir_rectangle_carte_droite_menu()
        )
        rectangle_jouer: pygame.Rect = (
            afficheur.obtenir_rectangle_bouton_jouer_menu()
        )
        pastilles_centrale: list[tuple[str, tuple[int, int], int]] = (
            afficheur.obtenir_cercles_pastilles_theme_menu(
                nom_carte_centrale,
                rectangle_centrale,
                HAUTEUR_BANDEAU_CARTE_CENTRALE,
            )
        )

        for evenement in pygame.event.get():
            if evenement.type == pygame.QUIT:
                return None
            else:
                pass

            if evenement.type == pygame.KEYDOWN:
                if (
                    evenement.key == pygame.K_LEFT
                    or evenement.key == pygame.K_q
                ):
                    indice_courant = (
                        indice_courant + DECALAGE_VOISIN_NEGATIF
                    ) % nb_cartes
                else:
                    if (
                        evenement.key == pygame.K_RIGHT
                        or evenement.key == pygame.K_d
                    ):
                        indice_courant = (
                            indice_courant + DECALAGE_VOISIN_POSITIF
                        ) % nb_cartes
                    else:
                        if (
                            evenement.key == pygame.K_RETURN
                            or evenement.key == pygame.K_KP_ENTER
                            or evenement.key == pygame.K_SPACE
                        ):
                            return (
                                nom_carte_centrale,
                                theme_carte_centrale,
                                indice_courant,
                            )
                        else:
                            if evenement.key == pygame.K_ESCAPE:
                                return None
                            else:
                                pass
            else:
                pass

            if evenement.type == pygame.MOUSEWHEEL:
                if evenement.y > DECALAGE_VOISIN_NUL or (
                    evenement.x < DECALAGE_VOISIN_NUL
                ):
                    indice_courant = (
                        indice_courant + DECALAGE_VOISIN_NEGATIF
                    ) % nb_cartes
                else:
                    if evenement.y < DECALAGE_VOISIN_NUL or (
                        evenement.x > DECALAGE_VOISIN_NUL
                    ):
                        indice_courant = (
                            indice_courant + DECALAGE_VOISIN_POSITIF
                        ) % nb_cartes
                    else:
                        pass
            else:
                pass

            if (
                evenement.type == pygame.MOUSEBUTTONDOWN
                and evenement.button == BOUTON_SOURIS_GAUCHE
            ):
                clic_x, clic_y = evenement.pos
                if gestionnaire_menu.est_clic_dans_cercle(
                    clic_x,
                    clic_y,
                    CENTRE_BOUTON_RETOUR_X,
                    CENTRE_BOUTON_RETOUR_Y,
                    RAYON_BOUTON_RETOUR,
                ):
                    return None
                else:
                    pass

                pastille_cliquee: bool = False
                for (
                    nom_theme_pastille,
                    centre_pastille,
                    rayon_pastille,
                ) in pastilles_centrale:
                    if gestionnaire_menu.est_clic_dans_cercle(
                        clic_x,
                        clic_y,
                        centre_pastille[INDICE_MINIMUM_GRILLE],
                        centre_pastille[DECALAGE_VOISIN_POSITIF],
                        rayon_pastille,
                    ):
                        themes_actifs[nom_carte_centrale] = (
                            nom_theme_pastille
                        )
                        pastille_cliquee = True
                    else:
                        pass

                if not pastille_cliquee:
                    if rectangle_jouer.collidepoint((clic_x, clic_y)):
                        theme_retenu: str = themes_actifs.get(
                            nom_carte_centrale,
                            THEME_CREME_SAUGE,
                        )
                        return (
                            nom_carte_centrale,
                            theme_retenu,
                            indice_courant,
                        )
                    else:
                        if rectangle_gauche.collidepoint(
                            (clic_x, clic_y)
                        ) and not rectangle_centrale.collidepoint(
                            (clic_x, clic_y)
                        ):
                            indice_courant = (
                                indice_courant + DECALAGE_VOISIN_NEGATIF
                            ) % nb_cartes
                        else:
                            if rectangle_droite.collidepoint(
                                (clic_x, clic_y)
                            ) and not rectangle_centrale.collidepoint(
                                (clic_x, clic_y)
                            ):
                                indice_courant = (
                                    indice_courant + DECALAGE_VOISIN_POSITIF
                                ) % nb_cartes
                            else:
                                pass
                else:
                    pass
            else:
                pass

        afficheur.dessiner_menu_carrousel(
            indice_courant,
            themes_actifs,
            meilleurs_scores,
            position_souris,
        )
        horloge.tick(FPS)

    return None


def executer_jeu() -> None:
    """Initialise Pygame, affiche le carrousel de cartes et lance le jeu."""
    pygame.init()
    dimensions_fenetre: tuple[int, int] = (LARGEUR_FENETRE, HAUTEUR_FENETRE)
    ecran: pygame.Surface = pygame.display.set_mode(dimensions_fenetre)
    pygame.display.set_caption(TITRE_FENETRE)
    horloge: pygame.time.Clock = pygame.time.Clock()

    afficheur: Renderer = Renderer(ecran)
    themes_par_carte: dict[str, str] = initialiser_themes_par_carte()
    indice_carte_active: int = INDICE_MINIMUM_GRILLE
    application_active: bool = True

    while application_active:
        choix_menu: tuple[str, str, int] | None = choisir_carte_accueil(
            afficheur,
            horloge,
            indice_carte_active,
            themes_par_carte,
        )
        if choix_menu is None:
            application_active = False
        else:
            carte_choisie, theme_choisi, indice_carte_active = choix_menu
            afficheur.definir_theme_graphique(theme_choisi)
            grille: Grid = Grid()
            grille.generer_relief_carte(carte_choisie)
            gestionnaire_entrees: InputHandler = InputHandler()
            moteur_jeu: GameEngine = GameEngine(grille, carte_choisie)

            en_cours: bool = True
            while en_cours:
                parametres_camera: tuple[float, float, float, float] = (
                    moteur_jeu.obtenir_bornes_grille_camera()
                )
                for evenement in pygame.event.get():
                    if evenement.type == pygame.QUIT:
                        en_cours = False
                        application_active = False
                    else:
                        gestionnaire_entrees.gerer_evenement(
                            evenement,
                            grille,
                            parametres_camera,
                            moteur_jeu,
                        )

                if gestionnaire_entrees.demande_retour_menu:
                    moteur_jeu.verifier_et_sauvegarder_meilleur_score()
                    en_cours = False
                else:
                    moteur_jeu.mettre_a_jour()
                    parametres_camera_rendu: tuple[
                        float,
                        float,
                        float,
                        float,
                    ] = moteur_jeu.obtenir_bornes_grille_camera()
                    afficheur.afficher(
                        grille,
                        moteur_jeu.voitures,
                        moteur_jeu.score,
                        moteur_jeu.partie_perdue,
                        parametres_camera_rendu,
                        gestionnaire_entrees.outil_actif,
                        moteur_jeu.obtenir_nom_jour_courant(),
                        moteur_jeu.numero_semaine,
                        moteur_jeu.obtenir_progression_jour(),
                        moteur_jeu.choix_hebdomadaire_actif,
                        moteur_jeu.offres_hebdomadaires,
                        gestionnaire_entrees.mode_edition,
                    )
                    horloge.tick(FPS)

    pygame.quit()


if __name__ == "__main__":
    executer_jeu()
