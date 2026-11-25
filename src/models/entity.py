"""Modèles des entités bâtiments (Maison et Usine) sans dépendance à Pygame."""


class Maison:
    """Représente une maison (générateur de voitures d'une couleur donnée)."""

    def __init__(
        self,
        ligne: int,
        colonne: int,
        couleur: tuple[int, int, int],
    ) -> None:
        """Initialise une maison avec ses coordonnées et sa couleur.

        Args:
            ligne: Indice de la ligne sur la grille.
            colonne: Indice de la colonne sur la grille.
            couleur: Tuple RGB représentant la couleur de la maison.
        """
        self.ligne: int = ligne
        self.colonne: int = colonne
        self.couleur: tuple[int, int, int] = couleur


class Usine:
    """Représente une usine (destination des voitures d'une couleur donnée)."""

    def __init__(
        self,
        ligne: int,
        colonne: int,
        couleur: tuple[int, int, int],
    ) -> None:
        """Initialise une usine avec ses coordonnées et sa couleur.

        Args:
            ligne: Indice de la ligne sur la grille.
            colonne: Indice de la colonne sur la grille.
            couleur: Tuple RGB représentant la couleur de l'usine.
        """
        self.ligne: int = ligne
        self.colonne: int = colonne
        self.couleur: tuple[int, int, int] = couleur
