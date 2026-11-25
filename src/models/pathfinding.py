"""Algorithme de pathfinding A* isolé (logique métier pure sans Pygame)."""

import heapq

from src.config import (
    COUT_DEPLACEMENT_VOISIN,
    COUT_INITIAL_CHEMIN,
    PAS_INCREMENT_COMPTEUR,
)
from src.models.grid import Grid


def calculer_distance_manhattan(
    point_a: tuple[int, int],
    point_b: tuple[int, int],
) -> int:
    """Calcule la distance de Manhattan entre deux coordonnées (col, lig).

    Args:
        point_a: Première coordonnée (colonne, ligne).
        point_b: Seconde coordonnée (colonne, ligne).

    Returns:
        La distance de Manhattan entière entre les deux points.
    """
    colonne_a, ligne_a = point_a
    colonne_b, ligne_b = point_b
    ecart_colonne: int = abs(colonne_a - colonne_b)
    ecart_ligne: int = abs(ligne_a - ligne_b)
    return ecart_colonne + ecart_ligne


def reconstruire_chemin(
    parents: dict[tuple[int, int], tuple[int, int]],
    depart: tuple[int, int],
    arrivee: tuple[int, int],
) -> list[tuple[int, int]]:
    """Reconstruit la liste ordonnée des coordonnées du départ à l'arrivée.

    Args:
        parents: Dictionnaire associant chaque case à sa case précédente.
        depart: Coordonnée (colonne, ligne) de départ.
        arrivee: Coordonnée (colonne, ligne) d'arrivée.

    Returns:
        Liste ordonnée des coordonnées (colonne, ligne) du chemin complet.
    """
    chemin_inverse: list[tuple[int, int]] = [arrivee]
    noeud_courant: tuple[int, int] = arrivee

    while noeud_courant != depart:
        noeud_courant = parents[noeud_courant]
        chemin_inverse.append(noeud_courant)

    chemin_inverse.reverse()
    return chemin_inverse


def trouver_chemin_a_etoile(
    grille: Grid,
    depart: tuple[int, int],
    arrivee: tuple[int, int],
) -> list[tuple[int, int]]:
    """Recherche le plus court chemin entre depart et arrivee via A*.

    Args:
        grille: Instance du modèle Grid sur laquelle chercher le chemin.
        depart: Coordonnée (colonne, ligne) de la case de départ.
        arrivee: Coordonnée (colonne, ligne) de la case d'arrivée.

    Returns:
        Liste ordonnée des coordonnées (colonne, ligne) du chemin le plus
        court (incluant depart et arrivee), ou une liste vide si aucun
        chemin n'existe.
    """
    colonne_depart, ligne_depart = depart
    colonne_arrivee, ligne_arrivee = arrivee

    depart_valide: bool = grille.est_coordonnee_valide(
        ligne_depart,
        colonne_depart,
    )
    arrivee_valide: bool = grille.est_coordonnee_valide(
        ligne_arrivee,
        colonne_arrivee,
    )

    if not (depart_valide and arrivee_valide):
        return []
    else:
        pass

    if depart == arrivee:
        return [depart]
    else:
        pass

    file_ouverte: list[tuple[int, int, tuple[int, int]]] = []
    compteur_insertion: int = COUT_INITIAL_CHEMIN
    heuristique_initiale: int = calculer_distance_manhattan(depart, arrivee)

    heapq.heappush(
        file_ouverte,
        (heuristique_initiale, compteur_insertion, depart),
    )

    parents: dict[tuple[int, int], tuple[int, int]] = {}
    couts_g: dict[tuple[int, int], int] = {depart: COUT_INITIAL_CHEMIN}
    ensemble_ferme: set[tuple[int, int]] = set()

    while len(file_ouverte) > COUT_INITIAL_CHEMIN:
        _, _, noeud_courant = heapq.heappop(file_ouverte)

        if noeud_courant == arrivee:
            return reconstruire_chemin(parents, depart, arrivee)
        else:
            pass

        if noeud_courant in ensemble_ferme:
            continue
        else:
            ensemble_ferme.add(noeud_courant)

        voisins: list[tuple[int, int]] = grille.obtenir_voisins_accessibles(
            noeud_courant,
            depart,
            arrivee,
        )

        for voisin in voisins:
            if voisin in ensemble_ferme:
                continue
            else:
                pass

            nouveau_cout_g: int = (
                couts_g[noeud_courant] + COUT_DEPLACEMENT_VOISIN
            )
            voisin_deja_connu: bool = voisin in couts_g

            est_meilleur_chemin: bool = False
            if not voisin_deja_connu:
                est_meilleur_chemin = True
            else:
                if nouveau_cout_g < couts_g[voisin]:
                    est_meilleur_chemin = True
                else:
                    est_meilleur_chemin = False

            if est_meilleur_chemin:
                parents[voisin] = noeud_courant
                couts_g[voisin] = nouveau_cout_g
                score_f: int = nouveau_cout_g + calculer_distance_manhattan(
                    voisin,
                    arrivee,
                )
                compteur_insertion = (
                    compteur_insertion + PAS_INCREMENT_COMPTEUR
                )
                heapq.heappush(
                    file_ouverte,
                    (score_f, compteur_insertion, voisin),
                )
            else:
                pass

    return []
