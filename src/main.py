"""Point d'entrée principal et boucle de jeu de FlowState."""

import pygame

from src.config import (
    BOUTON_SOURIS_GAUCHE,
    FPS,
    HAUTEUR_FENETRE,
    LARGEUR_FENETRE,
    TITRE_FENETRE,
)
from src.controllers.game_engine import GameEngine
from src.controllers.input_handler import InputHandler
from src.models.grid import Grid
from src.views.renderer import Renderer


def choisir_carte_accueil(
    afficheur: Renderer,
    horloge: pygame.time.Clock,
) -> str | None:
    """Affiche l'écran de sélection de carte et retourne le choix du joueur.

    Args:
        afficheur: Instance de Renderer pour dessiner l'écran d'accueil.
        horloge: Horloge Pygame pour cadencer la boucle d'accueil.

    Returns:
        Le nom de la carte choisie ("Plaine", "Rivière", "Montagnes"),
        ou None si le joueur a fermé la fenêtre.
    """
    boutons_cartes: list[tuple[str, pygame.Rect]] = (
        afficheur.obtenir_rectangles_boutons_cartes()
    )
    en_attente_choix: bool = True

    while en_attente_choix:
        position_souris: tuple[int, int] = pygame.mouse.get_pos()
        for evenement in pygame.event.get():
            if evenement.type == pygame.QUIT:
                return None
            else:
                if (
                    evenement.type == pygame.MOUSEBUTTONDOWN
                    and evenement.button == BOUTON_SOURIS_GAUCHE
                ):
                    for nom_carte, rectangle_bouton in boutons_cartes:
                        if rectangle_bouton.collidepoint(evenement.pos):
                            return nom_carte
                        else:
                            pass
                else:
                    pass

        afficheur.dessiner_ecran_selection_carte(position_souris)
        horloge.tick(FPS)

    return None


def executer_jeu() -> None:
    """Initialise Pygame, affiche le choix de carte et lance la simulation."""
    pygame.init()
    dimensions_fenetre: tuple[int, int] = (LARGEUR_FENETRE, HAUTEUR_FENETRE)
    ecran: pygame.Surface = pygame.display.set_mode(dimensions_fenetre)
    pygame.display.set_caption(TITRE_FENETRE)
    horloge: pygame.time.Clock = pygame.time.Clock()

    afficheur: Renderer = Renderer(ecran)
    carte_choisie: str | None = choisir_carte_accueil(afficheur, horloge)
    if carte_choisie is None:
        pygame.quit()
        return
    else:
        pass

    grille: Grid = Grid()
    grille.generer_relief_carte(carte_choisie)
    gestionnaire_entrees: InputHandler = InputHandler()
    moteur_jeu: GameEngine = GameEngine(grille)

    en_cours: bool = True
    while en_cours:
        parametres_camera: tuple[float, float, float, float] = (
            moteur_jeu.obtenir_bornes_grille_camera()
        )
        for evenement in pygame.event.get():
            if evenement.type == pygame.QUIT:
                en_cours = False
            else:
                if not moteur_jeu.partie_perdue:
                    gestionnaire_entrees.gerer_evenement(
                        evenement,
                        grille,
                        parametres_camera,
                        moteur_jeu,
                    )
                else:
                    pass

        moteur_jeu.mettre_a_jour()
        parametres_camera_rendu: tuple[float, float, float, float] = (
            moteur_jeu.obtenir_bornes_grille_camera()
        )
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
