"""Point d'entrée principal et boucle de jeu de FlowState."""

import pygame

from src.config import (
    FPS,
    HAUTEUR_FENETRE,
    LARGEUR_FENETRE,
    TITRE_FENETRE,
)
from src.models.grid import Grid
from src.views.renderer import Renderer


def executer_jeu() -> None:
    """Initialise Pygame et exécute la boucle principale du jeu."""
    pygame.init()
    dimensions_fenetre: tuple[int, int] = (LARGEUR_FENETRE, HAUTEUR_FENETRE)
    ecran: pygame.Surface = pygame.display.set_mode(dimensions_fenetre)
    pygame.display.set_caption(TITRE_FENETRE)
    horloge: pygame.time.Clock = pygame.time.Clock()

    grille: Grid = Grid()
    afficheur: Renderer = Renderer(ecran)

    en_cours: bool = True
    while en_cours:
        for evenement in pygame.event.get():
            if evenement.type == pygame.QUIT:
                en_cours = False
            else:
                en_cours = en_cours

        afficheur.afficher(grille)
        horloge.tick(FPS)

    pygame.quit()


if __name__ == "__main__":
    executer_jeu()
