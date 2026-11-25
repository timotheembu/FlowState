"""Modèle de la grille spatiale (logique métier pure sans Pygame)."""

from src.config import (
    CASE_MAISON,
    CASE_USINE,
    CASE_VIDE,
    INDICE_MINIMUM_GRILLE,
    NB_COLONNES,
    NB_LIGNES,
)
from src.models.entity import Maison, Usine


class Grid:
    """Représente la matrice spatiale 2D du jeu et les bâtiments placés."""

    def __init__(
        self,
        nb_lignes: int = NB_LIGNES,
        nb_colonnes: int = NB_COLONNES,
    ) -> None:
        """Initialise la grille avec des cases vides et sans bâtiment.

        Args:
            nb_lignes: Nombre de lignes de la grille.
            nb_colonnes: Nombre de colonnes de la grille.
        """
        self.nb_lignes: int = nb_lignes
        self.nb_colonnes: int = nb_colonnes
        self.matrice: list[list[int]] = []
        self.maisons: list[Maison] = []
        self.usines: list[Usine] = []
        self.reinitialiser()

    def reinitialiser(self) -> None:
        """Remplit intégralement la matrice avec CASE_VIDE et vide les listes."""
        nouvelle_matrice: list[list[int]] = []
        for _ in range(self.nb_lignes):
            ligne_courante: list[int] = []
            for _ in range(self.nb_colonnes):
                ligne_courante.append(CASE_VIDE)
            nouvelle_matrice.append(ligne_courante)
        self.matrice = nouvelle_matrice
        self.maisons = []
        self.usines = []

    def est_coordonnee_valide(self, ligne: int, colonne: int) -> bool:
        """Vérifie si une coordonnée (ligne, colonne) est dans la grille.

        Args:
            ligne: Indice de la ligne à vérifier.
            colonne: Indice de la colonne à vérifier.

        Returns:
            True si la coordonnée est dans les limites, False sinon.
        """
        ligne_valide: bool = (
            INDICE_MINIMUM_GRILLE <= ligne < self.nb_lignes
        )
        colonne_valide: bool = (
            INDICE_MINIMUM_GRILLE <= colonne < self.nb_colonnes
        )

        if ligne_valide and colonne_valide:
            return True
        else:
            return False

    def obtenir_etat_case(self, ligne: int, colonne: int) -> int:
        """Retourne l'état de la case située aux coordonnées données.

        Args:
            ligne: Indice de la ligne.
            colonne: Indice de la colonne.

        Returns:
            L'entier représentant l'état de la case.

        Raises:
            ValueError: Si les coordonnées sont hors des limites de la grille.
        """
        if self.est_coordonnee_valide(ligne, colonne):
            return self.matrice[ligne][colonne]
        else:
            raise ValueError(
                f"Coordonnées hors limites : ({ligne}, {colonne})"
            )

    def definir_etat_case(self, ligne: int, colonne: int, etat: int) -> None:
        """Modifie l'état de la case située aux coordonnées données.

        Args:
            ligne: Indice de la ligne.
            colonne: Indice de la colonne.
            etat: Nouvel état à affecter à la case.

        Raises:
            ValueError: Si les coordonnées sont hors des limites de la grille.
        """
        if self.est_coordonnee_valide(ligne, colonne):
            self.matrice[ligne][colonne] = etat
        else:
            raise ValueError(
                f"Coordonnées hors limites : ({ligne}, {colonne})"
            )

    def est_case_libre(self, ligne: int, colonne: int) -> bool:
        """Vérifie si une case est dans les limites et actuellement vide.

        Args:
            ligne: Indice de la ligne.
            colonne: Indice de la colonne.

        Returns:
            True si la case est valide et égale à CASE_VIDE, False sinon.
        """
        if self.est_coordonnee_valide(ligne, colonne):
            etat_actuel: int = self.matrice[ligne][colonne]
            if etat_actuel == CASE_VIDE:
                return True
            else:
                return False
        else:
            return False

    def placer_maison(self, maison: Maison) -> bool:
        """Place une maison sur la grille si la case cible est libre.

        Args:
            maison: Instance de Maison à placer.

        Returns:
            True si la maison a pu être placée, False sinon.
        """
        if self.est_case_libre(maison.ligne, maison.colonne):
            self.definir_etat_case(maison.ligne, maison.colonne, CASE_MAISON)
            self.maisons.append(maison)
            return True
        else:
            return False

    def placer_usine(self, usine: Usine) -> bool:
        """Place une usine sur la grille si la case cible est libre.

        Args:
            usine: Instance de Usine à placer.

        Returns:
            True si l'usine a pu être placée, False sinon.
        """
        if self.est_case_libre(usine.ligne, usine.colonne):
            self.definir_etat_case(usine.ligne, usine.colonne, CASE_USINE)
            self.usines.append(usine)
            return True
        else:
            return False
