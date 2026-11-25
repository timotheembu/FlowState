"""Algorithme de pathfinding A* isolé (logique métier pure sans Pygame)."""

import heapq

from src.config import (
    COUT_DIAGONALE,
    COUT_INITIAL_CHEMIN,
    COUT_INITIAL_CHEMIN_FLOAT,
    COUT_ORTHOGONAL,
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


def calculer_heuristique_octile(
    point_a: tuple[int, int],
    point_b: tuple[int, int],
) -> float:
    """Calcule la distance octile adaptée aux déplacements en 8 directions.

    Args:
        point_a: Première coordonnée (colonne, ligne).
        point_b: Seconde coordonnée (colonne, ligne).

    Returns:
        Estimation flottante admissible du coût entre point_a et point_b.
    """
    colonne_a, ligne_a = point_a
    colonne_b, ligne_b = point_b
    ecart_colonne: int = abs(colonne_a - colonne_b)
    ecart_ligne: int = abs(ligne_a - ligne_b)

    if ecart_colonne < ecart_ligne:
        pas_diagonaux: int = ecart_colonne
        pas_orthogonaux: int = ecart_ligne - ecart_colonne
    else:
        pas_diagonaux = ecart_ligne
        pas_orthogonaux = ecart_colonne - ecart_ligne

    cout_estime: float = (
        float(pas_diagonaux) * COUT_DIAGONALE
        + float(pas_orthogonaux) * COUT_ORTHOGONAL
    )
    return cout_estime


def calculer_cout_deplacement(
    noeud_source: tuple[int, int],
    noeud_cible: tuple[int, int],
) -> float:
    """Détermine le coût d'un pas orthogonal ou diagonal entre deux cases.

    Args:
        noeud_source: Coordonnée (colonne, ligne) de départ du pas.
        noeud_cible: Coordonnée (colonne, ligne) d'arrivée du pas.

    Returns:
        COUT_DIAGONALE si le déplacement est diagonal, COUT_ORTHOGONAL sinon.
    """
    colonne_source, ligne_source = noeud_source
    colonne_cible, ligne_cible = noeud_cible
    ecart_colonne: int = abs(colonne_cible - colonne_source)
    ecart_ligne: int = abs(ligne_cible - ligne_source)

    est_diagonal: bool = (
        ecart_colonne == PAS_INCREMENT_COMPTEUR
        and ecart_ligne == PAS_INCREMENT_COMPTEUR
    )
    if est_diagonal:
        return COUT_DIAGONALE
    else:
        return COUT_ORTHOGONAL


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
    """Recherche le plus court chemin (8 directions) entre depart et arrivee.

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

    file_ouverte: list[tuple[float, int, tuple[int, int]]] = []
    compteur_insertion: int = COUT_INITIAL_CHEMIN
    heuristique_initiale: float = calculer_heuristique_octile(
        depart,
        arrivee,
    )

    heapq.heappush(
        file_ouverte,
        (heuristique_initiale, compteur_insertion, depart),
    )

    parents: dict[tuple[int, int], tuple[int, int]] = {}
    couts_g: dict[tuple[int, int], float] = {
        depart: COUT_INITIAL_CHEMIN_FLOAT,
    }
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

            cout_pas: float = calculer_cout_deplacement(
                noeud_courant,
                voisin,
            )
            nouveau_cout_g: float = couts_g[noeud_courant] + cout_pas
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
                score_f: float = (
                    nouveau_cout_g
                    + calculer_heuristique_octile(voisin, arrivee)
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
