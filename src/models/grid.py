"""Modèle de la grille spatiale (logique métier pure sans Pygame)."""

from src.config import (
    CASE_VIDE,
    INDICE_MINIMUM_GRILLE,
    NB_COLONNES,
    NB_LIGNES,
)


class Grid:
    """Représente la matrice spatiale 2D du jeu."""

    def __init__(
        self,
        nb_lignes: int = NB_LIGNES,
        nb_colonnes: int = NB_COLONNES,
    ) -> None:
        """Initialise la grille avec des cases vides.

        Args:
            nb_lignes: Nombre de lignes de la grille.
            nb_colonnes: Nombre de colonnes de la grille.
        """
        self.nb_lignes: int = nb_lignes
        self.nb_colonnes: int = nb_colonnes
        self.matrice: list[list[int]] = []
        self.reinitialiser()

    def reinitialiser(self) -> None:
        """Remplit intégralement la matrice avec la valeur CASE_VIDE."""
        nouvelle_matrice: list[list[int]] = []
        for _ in range(self.nb_lignes):
            ligne_courante: list[int] = []
            for _ in range(self.nb_colonnes):
                ligne_courante.append(CASE_VIDE)
            nouvelle_matrice.append(ligne_courante)
        self.matrice = nouvelle_matrice

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
