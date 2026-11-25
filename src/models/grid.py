"""Modèle de la grille spatiale (logique métier pure sans Pygame)."""

from src.config import (
    CASE_MAISON,
    CASE_ROUTE,
    CASE_USINE,
    CASE_VIDE,
    DIRECTIONS_ORTHOGONALES,
    DISTANCE_MIN_ENTRE_BATIMENTS,
    DISTANCE_MIN_SECOURS_BATIMENT,
    INDICE_MINIMUM_GRILLE,
    LONGUEUR_LISTE_VIDE,
    MARGE_BORDURE_APPARITION,
    MARGE_BORDURE_NULLE,
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

    def est_case_route(self, ligne: int, colonne: int) -> bool:
        """Vérifie si une case est valide et contient un segment de route.

        Args:
            ligne: Indice de la ligne.
            colonne: Indice de la colonne.

        Returns:
            True si la case est valide et égale à CASE_ROUTE, False sinon.
        """
        if self.est_coordonnee_valide(ligne, colonne):
            etat_actuel: int = self.matrice[ligne][colonne]
            if etat_actuel == CASE_ROUTE:
                return True
            else:
                return False
        else:
            return False

    def est_case_connectable_route(self, ligne: int, colonne: int) -> bool:
        """Vérifie si une case peut être reliée visuellement à une route.

        Args:
            ligne: Indice de la ligne.
            colonne: Indice de la colonne.

        Returns:
            True si la case contient une route, une maison ou une usine,
            False sinon.
        """
        if self.est_coordonnee_valide(ligne, colonne):
            etat_actuel: int = self.matrice[ligne][colonne]
            est_connectable: bool = (
                etat_actuel == CASE_ROUTE
                or etat_actuel == CASE_MAISON
                or etat_actuel == CASE_USINE
            )
            if est_connectable:
                return True
            else:
                return False
        else:
            return False

    def placer_route(self, ligne: int, colonne: int) -> bool:
        """Place un segment de route uniquement si la case cible est vide.

        Args:
            ligne: Indice de la ligne où poser la route.
            colonne: Indice de la colonne où poser la route.

        Returns:
            True si la route a été posée, False sinon.
        """
        if self.est_case_libre(ligne, colonne):
            self.definir_etat_case(ligne, colonne, CASE_ROUTE)
            return True
        else:
            return False

    def supprimer_route(self, ligne: int, colonne: int) -> bool:
        """Supprime un segment de route sans jamais écraser un bâtiment.

        Args:
            ligne: Indice de la ligne où supprimer la route.
            colonne: Indice de la colonne où supprimer la route.

        Returns:
            True si une route a été supprimée, False sinon.
        """
        if self.est_case_route(ligne, colonne):
            self.definir_etat_case(ligne, colonne, CASE_VIDE)
            return True
        else:
            return False

    def est_case_traversable(
        self,
        coordonnee: tuple[int, int],
        depart: tuple[int, int],
        arrivee: tuple[int, int],
    ) -> bool:
        """Vérifie si une case (col, lig) est traversable pour un trajet donné.

        Une case est traversable si elle est dans la grille et qu'il s'agit
        soit d'une CASE_ROUTE, soit de la case exacte de départ ou d'arrivée.

        Args:
            coordonnee: Coordonnée (colonne, ligne) de la case à tester.
            depart: Coordonnée (colonne, ligne) de départ du trajet.
            arrivee: Coordonnée (colonne, ligne) d'arrivée du trajet.

        Returns:
            True si la case peut être empruntée, False sinon.
        """
        colonne, ligne = coordonnee
        if self.est_coordonnee_valide(ligne, colonne):
            est_borne_trajet: bool = (
                coordonnee == depart or coordonnee == arrivee
            )
            if est_borne_trajet:
                return True
            else:
                if self.est_case_route(ligne, colonne):
                    return True
                else:
                    return False
        else:
            return False

    def obtenir_voisins_accessibles(
        self,
        coordonnee: tuple[int, int],
        depart: tuple[int, int],
        arrivee: tuple[int, int],
    ) -> list[tuple[int, int]]:
        """Retourne les voisins orthogonaux accessibles depuis une case.

        Args:
            coordonnee: Coordonnée (colonne, ligne) de la case courante.
            depart: Coordonnée (colonne, ligne) de départ du trajet.
            arrivee: Coordonnée (colonne, ligne) d'arrivée du trajet.

        Returns:
            Liste des coordonnées (colonne, ligne) des voisins traversables.
        """
        colonne_courante, ligne_courante = coordonnee
        voisins_accessibles: list[tuple[int, int]] = []

        for delta_colonne, delta_ligne in DIRECTIONS_ORTHOGONALES:
            voisin_colonne: int = colonne_courante + delta_colonne
            voisin_ligne: int = ligne_courante + delta_ligne
            coordonnee_voisin: tuple[int, int] = (
                voisin_colonne,
                voisin_ligne,
            )
            if self.est_case_traversable(
                coordonnee_voisin,
                depart,
                arrivee,
            ):
                voisins_accessibles.append(coordonnee_voisin)
            else:
                pass

        return voisins_accessibles

    def est_eloignee_des_batiments(
        self,
        ligne: int,
        colonne: int,
        marge_minimale: int,
    ) -> bool:
        """Vérifie qu'une case respecte une distance minimale des bâtiments.

        Args:
            ligne: Indice de la ligne à tester.
            colonne: Indice de la colonne à tester.
            marge_minimale: Écart minimum requis en lignes ou colonnes.

        Returns:
            True si aucun bâtiment n'est dans le périmètre, False sinon.
        """
        for maison in self.maisons:
            ecart_ligne_maison: int = abs(ligne - maison.ligne)
            ecart_colonne_maison: int = abs(colonne - maison.colonne)
            trop_proche_maison: bool = (
                ecart_ligne_maison < marge_minimale
                and ecart_colonne_maison < marge_minimale
            )
            if trop_proche_maison:
                return False
            else:
                pass

        for usine in self.usines:
            ecart_ligne_usine: int = abs(ligne - usine.ligne)
            ecart_colonne_usine: int = abs(colonne - usine.colonne)
            trop_proche_usine: bool = (
                ecart_ligne_usine < marge_minimale
                and ecart_colonne_usine < marge_minimale
            )
            if trop_proche_usine:
                return False
            else:
                pass

        return True

    def collecter_cases_libres_avec_marges(
        self,
        marge_batiments: int,
        marge_bordure: int,
    ) -> list[tuple[int, int]]:
        """Liste les cases vides respectant les marges de bordure et bâtiments.

        Args:
            marge_batiments: Distance minimale autour des bâtiments existants.
            marge_bordure: Marge minimale par rapport aux bords de la grille.

        Returns:
            Liste des coordonnées (ligne, colonne) éligibles.
        """
        cases_eligibles: list[tuple[int, int]] = []
        ligne_debut: int = INDICE_MINIMUM_GRILLE + marge_bordure
        ligne_fin: int = self.nb_lignes - marge_bordure
        colonne_debut: int = INDICE_MINIMUM_GRILLE + marge_bordure
        colonne_fin: int = self.nb_colonnes - marge_bordure

        for indice_ligne in range(ligne_debut, ligne_fin):
            for indice_colonne in range(colonne_debut, colonne_fin):
                if self.est_case_libre(indice_ligne, indice_colonne):
                    if self.est_eloignee_des_batiments(
                        indice_ligne,
                        indice_colonne,
                        marge_batiments,
                    ):
                        cases_eligibles.append(
                            (indice_ligne, indice_colonne)
                        )
                    else:
                        pass
                else:
                    pass

        return cases_eligibles

    def obtenir_cases_libres_pour_apparition(
        self,
        marge_batiments: int = DISTANCE_MIN_ENTRE_BATIMENTS,
        marge_bordure: int = MARGE_BORDURE_APPARITION,
    ) -> list[tuple[int, int]]:
        """Retourne les cases libres valides pour faire apparaître un bâtiment.

        Si aucune case ne respecte la marge idéale, replie sur toutes les
        cases vides restantes de la grille.

        Args:
            marge_batiments: Distance minimale souhaitée avec les bâtiments.
            marge_bordure: Marge souhaitée avec les bords de la grille.

        Returns:
            Liste des coordonnées (ligne, colonne) disponibles.
        """
        cases_ideales: list[tuple[int, int]] = (
            self.collecter_cases_libres_avec_marges(
                marge_batiments,
                marge_bordure,
            )
        )
        if len(cases_ideales) > LONGUEUR_LISTE_VIDE:
            return cases_ideales
        else:
            cases_secours: list[tuple[int, int]] = (
                self.collecter_cases_libres_avec_marges(
                    DISTANCE_MIN_SECOURS_BATIMENT,
                    MARGE_BORDURE_NULLE,
                )
            )
            return cases_secours
