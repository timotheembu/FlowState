"""Modèle de la grille spatiale (logique métier pure sans Pygame)."""

from math import hypot, sin

from src.config import (
    AMPLITUDE_SINUS_RIVIERE,
    CARTE_MONTAGNES,
    CARTE_PLAINE,
    CARTE_RIVIERE,
    CASE_EAU,
    CASE_MAISON,
    CASE_MONTAGNE,
    CASE_ROUTE,
    CASE_USINE,
    CASE_VIDE,
    COLONNE_BASE_RIVIERE,
    COMPTEUR_INITIAL_FRAMES,
    DIRECTIONS_HUIT_VOISINS,
    DISTANCE_CHEBYSHEV_ADJACENTE,
    DISTANCE_MIN_ENTRE_BATIMENTS,
    DISTANCE_MIN_SECOURS_BATIMENT,
    DIVISEUR_MOITIE,
    FREQUENCE_SINUS_RIVIERE,
    INDICE_MINIMUM_GRILLE,
    LARGEUR_RIVIERE_CASES,
    LIGNE_GUE_RIVIERE_MAX,
    LIGNE_GUE_RIVIERE_MIN,
    LONGUEUR_LISTE_VIDE,
    MARGE_BORDURE_APPARITION,
    MARGE_BORDURE_NULLE,
    MASSIFS_MONTAGNEUX_DEFAUT,
    NB_COLONNES,
    NB_LIGNES,
    NB_MAX_ROUTES_ADJACENTES_MAISON,
    PAS_INCREMENT_COMPTEUR,
    RAYON_ZONE_CENTRALE_DEGAGEE,
    STOCK_ROUTES_EPUISE,
    STOCK_ROUTES_INITIAL,
    UNITE_STOCK_ROUTE,
)
from src.models.entity import Maison, Usine


class Grid:
    """Représente la matrice spatiale 2D du jeu et les bâtiments placés."""

    def __init__(
        self,
        nb_lignes: int = NB_LIGNES,
        nb_colonnes: int = NB_COLONNES,
        stock_routes_initial: int = STOCK_ROUTES_INITIAL,
    ) -> None:
        """Initialise la grille avec des cases vides et un stock de routes.

        Args:
            nb_lignes: Nombre de lignes de la grille.
            nb_colonnes: Nombre de colonnes de la grille.
            stock_routes_initial: Stock initial de cases de route disponibles.
        """
        self.nb_lignes: int = nb_lignes
        self.nb_colonnes: int = nb_colonnes
        self.stock_routes_initial: int = stock_routes_initial
        self.stock_routes: int = stock_routes_initial
        self.matrice: list[list[int]] = []
        self.maisons: list[Maison] = []
        self.usines: list[Usine] = []
        self.connexions: dict[tuple[int, int], set[tuple[int, int]]] = {}
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
        self.connexions = {}
        self.stock_routes = self.stock_routes_initial

    def obtenir_voisins_connectes(
        self,
        coordonnee: tuple[int, int],
    ) -> set[tuple[int, int]]:
        """Retourne l'ensemble des coordonnées (col, lig) connectées à une case.

        Args:
            coordonnee: Coordonnée (colonne, ligne) de la case interrogée.

        Returns:
            Un ensemble de tuples (colonne, ligne) explicitement connectés.
        """
        if coordonnee in self.connexions:
            return set(self.connexions[coordonnee])
        else:
            return set()

    def sont_cases_connectees(
        self,
        case_a: tuple[int, int],
        case_b: tuple[int, int],
    ) -> bool:
        """Vérifie si deux coordonnées (col, lig) sont reliées dans le graphe.

        Args:
            case_a: Coordonnée (colonne, ligne) de la première case.
            case_b: Coordonnée (colonne, ligne) de la seconde case.

        Returns:
            True si une arête existe entre case_a et case_b, False sinon.
        """
        if case_a in self.connexions:
            if case_b in self.connexions[case_a]:
                return True
            else:
                return False
        else:
            return False

    def ajouter_arete_connexion(
        self,
        case_a: tuple[int, int],
        case_b: tuple[int, int],
    ) -> None:
        """Enregistre une arête bidirectionnelle entre case_a et case_b.

        Args:
            case_a: Coordonnée (colonne, ligne) de la première case.
            case_b: Coordonnée (colonne, ligne) de la seconde case.
        """
        if case_a not in self.connexions:
            self.connexions[case_a] = set()
        else:
            pass
        if case_b not in self.connexions:
            self.connexions[case_b] = set()
        else:
            pass
        self.connexions[case_a].add(case_b)
        self.connexions[case_b].add(case_a)

    def retirer_toutes_connexions_case(
        self,
        coordonnee: tuple[int, int],
    ) -> None:
        """Supprime toutes les arêtes incidentes à coordonnee dans le graphe.

        Args:
            coordonnee: Coordonnée (colonne, ligne) de la case à déconnecter.
        """
        if coordonnee in self.connexions:
            voisins_lies: list[tuple[int, int]] = list(
                self.connexions[coordonnee]
            )
            for voisin in voisins_lies:
                if voisin in self.connexions:
                    self.connexions[voisin].discard(coordonnee)
                    if len(self.connexions[voisin]) == LONGUEUR_LISTE_VIDE:
                        del self.connexions[voisin]
                    else:
                        pass
                else:
                    pass
            del self.connexions[coordonnee]
        else:
            pass

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

        Une case contenant un obstacle naturel (CASE_EAU ou CASE_MONTAGNE),
        un bâtiment ou une route n'est pas libre.

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

    def est_case_eau(self, ligne: int, colonne: int) -> bool:
        """Vérifie si une case est valide et contient de l'eau (CASE_EAU).

        Args:
            ligne: Indice de la ligne.
            colonne: Indice de la colonne.

        Returns:
            True si la case est valide et égale à CASE_EAU, False sinon.
        """
        if self.est_coordonnee_valide(ligne, colonne):
            etat_actuel: int = self.matrice[ligne][colonne]
            if etat_actuel == CASE_EAU:
                return True
            else:
                return False
        else:
            return False

    def est_case_montagne(self, ligne: int, colonne: int) -> bool:
        """Vérifie si une case est valide et contient une montagne.

        Args:
            ligne: Indice de la ligne.
            colonne: Indice de la colonne.

        Returns:
            True si la case est valide et égale à CASE_MONTAGNE, False sinon.
        """
        if self.est_coordonnee_valide(ligne, colonne):
            etat_actuel: int = self.matrice[ligne][colonne]
            if etat_actuel == CASE_MONTAGNE:
                return True
            else:
                return False
        else:
            return False

    def est_obstacle_naturel(self, ligne: int, colonne: int) -> bool:
        """Indique si la case contient un obstacle naturel (eau ou montagne).

        Args:
            ligne: Indice de la ligne.
            colonne: Indice de la colonne.

        Returns:
            True si la case est CASE_EAU ou CASE_MONTAGNE, False sinon.
        """
        if self.est_case_eau(ligne, colonne):
            return True
        else:
            if self.est_case_montagne(ligne, colonne):
                return True
            else:
                return False

    def a_voisin_libre_pour_sortie(self, ligne: int, colonne: int) -> bool:
        """Vérifie qu'une case possède au moins un voisin vide (CASE_VIDE).

        Empêche un bâtiment d'apparaître encerclé d'obstacles naturels sans
        pouvoir poser son bout de route (case_sortie).

        Args:
            ligne: Indice de la ligne candidate.
            colonne: Indice de la colonne candidate.

        Returns:
            True si au moins l'un des 8 voisins est CASE_VIDE, False sinon.
        """
        for delta_colonne, delta_ligne in DIRECTIONS_HUIT_VOISINS:
            voisin_ligne: int = ligne + delta_ligne
            voisin_colonne: int = colonne + delta_colonne
            if self.est_case_libre(voisin_ligne, voisin_colonne):
                return True
            else:
                pass
        return False

    def est_dans_zone_centrale_degagee(
        self,
        ligne: int,
        colonne: int,
    ) -> bool:
        """Vérifie si une case appartient au cœur central réservé au départ.

        Args:
            ligne: Indice de la ligne.
            colonne: Indice de la colonne.

        Returns:
            True si la case est dans le rayon central dégagé, False sinon.
        """
        centre_ligne: int = self.nb_lignes // DIVISEUR_MOITIE
        centre_colonne: int = self.nb_colonnes // DIVISEUR_MOITIE
        ecart_ligne: int = abs(ligne - centre_ligne)
        ecart_colonne: int = abs(colonne - centre_colonne)
        dans_zone: bool = (
            ecart_ligne <= RAYON_ZONE_CENTRALE_DEGAGEE
            and ecart_colonne <= RAYON_ZONE_CENTRALE_DEGAGEE
        )
        if dans_zone:
            return True
        else:
            return False

    def generer_riviere_sinueuse(self) -> None:
        """Trace une rivière sinueuse en CASE_EAU en préservant un gué central."""
        for indice_ligne in range(self.nb_lignes):
            est_dans_gue: bool = (
                LIGNE_GUE_RIVIERE_MIN
                <= indice_ligne
                <= LIGNE_GUE_RIVIERE_MAX
            )
            if est_dans_gue:
                continue
            else:
                pass

            decalage_sinus: float = (
                sin(float(indice_ligne) * FREQUENCE_SINUS_RIVIERE)
                * AMPLITUDE_SINUS_RIVIERE
            )
            colonne_centrale: int = int(
                round(float(COLONNE_BASE_RIVIERE) + decalage_sinus)
            )
            for decalage_largeur in range(LARGEUR_RIVIERE_CASES):
                colonne_eau: int = colonne_centrale + decalage_largeur
                if self.est_case_libre(indice_ligne, colonne_eau):
                    if not self.est_dans_zone_centrale_degagee(
                        indice_ligne,
                        colonne_eau,
                    ):
                        self.definir_etat_case(
                            indice_ligne,
                            colonne_eau,
                            CASE_EAU,
                        )
                    else:
                        pass
                else:
                    pass

    def generer_massifs_montagneux(self) -> None:
        """Place des amas de CASE_MONTAGNE autour de la vallée centrale."""
        for ligne_centre, colonne_centre, rayon in MASSIFS_MONTAGNEUX_DEFAUT:
            for indice_ligne in range(self.nb_lignes):
                for indice_colonne in range(self.nb_colonnes):
                    distance: float = hypot(
                        float(indice_ligne - ligne_centre),
                        float(indice_colonne - colonne_centre),
                    )
                    if distance <= float(rayon):
                        if self.est_case_libre(indice_ligne, indice_colonne):
                            if not self.est_dans_zone_centrale_degagee(
                                indice_ligne,
                                indice_colonne,
                            ):
                                self.definir_etat_case(
                                    indice_ligne,
                                    indice_colonne,
                                    CASE_MONTAGNE,
                                )
                            else:
                                pass
                        else:
                            pass
                    else:
                        pass

    def generer_relief_carte(
        self,
        nom_carte: str = CARTE_PLAINE,
    ) -> None:
        """Réinitialise la grille et génère le relief de la carte choisie.

        Args:
            nom_carte: Nom de la carte ("Plaine", "Rivière", "Montagnes").
        """
        self.reinitialiser()
        if nom_carte == CARTE_RIVIERE:
            self.generer_riviere_sinueuse()
        else:
            if nom_carte == CARTE_MONTAGNES:
                self.generer_massifs_montagneux()
            else:
                pass

    def obtenir_maison_a_coordonnee(
        self,
        ligne: int,
        colonne: int,
    ) -> Maison | None:
        """Retourne la maison située aux coordonnées données si elle existe.

        Args:
            ligne: Indice de la ligne.
            colonne: Indice de la colonne.

        Returns:
            Instance de Maison correspondante, ou None.
        """
        for maison in self.maisons:
            if maison.ligne == ligne and maison.colonne == colonne:
                return maison
            else:
                pass
        return None

    def obtenir_maison_proprietaire_sortie(
        self,
        ligne: int,
        colonne: int,
    ) -> Maison | None:
        """Retourne la maison dont la case_sortie correspond à (ligne, colonne).

        Args:
            ligne: Indice de la ligne de la route.
            colonne: Indice de la colonne de la route.

        Returns:
            Instance de Maison propriétaire de cette sortie, ou None.
        """
        coordonnee_cible: tuple[int, int] = (ligne, colonne)
        for maison in self.maisons:
            if maison.case_sortie == coordonnee_cible:
                return maison
            else:
                pass
        return None

    def est_case_sortie_de_maison(
        self,
        ligne: int,
        colonne: int,
    ) -> bool:
        """Indique si la case (ligne, colonne) est la sortie d'une maison.

        Args:
            ligne: Indice de la ligne.
            colonne: Indice de la colonne.

        Returns:
            True si une maison possède cette case comme case_sortie, False sinon.
        """
        maison_proprietaire: Maison | None = (
            self.obtenir_maison_proprietaire_sortie(ligne, colonne)
        )
        if maison_proprietaire is not None:
            return True
        else:
            return False

    def obtenir_usine_a_coordonnee(
        self,
        ligne: int,
        colonne: int,
    ) -> Usine | None:
        """Retourne l'usine située aux coordonnées données si elle existe.

        Args:
            ligne: Indice de la ligne.
            colonne: Indice de la colonne.

        Returns:
            Instance de Usine correspondante, ou None.
        """
        for usine in self.usines:
            if usine.ligne == ligne and usine.colonne == colonne:
                return usine
            else:
                pass
        return None

    def obtenir_usine_proprietaire_sortie(
        self,
        ligne: int,
        colonne: int,
    ) -> Usine | None:
        """Retourne l'usine dont la case_sortie correspond à (ligne, colonne).

        Args:
            ligne: Indice de la ligne de la route.
            colonne: Indice de la colonne de la route.

        Returns:
            Instance de Usine propriétaire de cette sortie, ou None.
        """
        coordonnee_cible: tuple[int, int] = (ligne, colonne)
        for usine in self.usines:
            if usine.case_sortie == coordonnee_cible:
                return usine
            else:
                pass
        return None

    def est_case_sortie_d_usine(
        self,
        ligne: int,
        colonne: int,
    ) -> bool:
        """Indique si la case (ligne, colonne) est la sortie d'une usine.

        Args:
            ligne: Indice de la ligne.
            colonne: Indice de la colonne.

        Returns:
            True si une usine possède cette case comme case_sortie, False sinon.
        """
        usine_proprietaire: Usine | None = (
            self.obtenir_usine_proprietaire_sortie(ligne, colonne)
        )
        if usine_proprietaire is not None:
            return True
        else:
            return False

    def est_case_sortie_de_batiment(
        self,
        ligne: int,
        colonne: int,
    ) -> bool:
        """Indique si la case est le bout de route d'une Maison ou d'une Usine.

        Args:
            ligne: Indice de la ligne.
            colonne: Indice de la colonne.

        Returns:
            True si la case est la case_sortie d'une maison ou d'une usine,
            False sinon.
        """
        if self.est_case_sortie_de_maison(ligne, colonne):
            return True
        else:
            if self.est_case_sortie_d_usine(ligne, colonne):
                return True
            else:
                return False

    def compter_routes_adjacentes_maison(
        self,
        maison: Maison,
        case_ignoree: tuple[int, int] | None = None,
    ) -> int:
        """Compte le nombre de CASE_ROUTE parmi les 8 voisins d'une maison.

        Args:
            maison: Instance de Maison à inspecter.
            case_ignoree: Coordonnée (ligne, colonne) optionnelle à ignorer.

        Returns:
            Nombre entier de cases de route adjacentes à la maison.
        """
        nb_routes: int = COMPTEUR_INITIAL_FRAMES
        for delta_colonne, delta_ligne in DIRECTIONS_HUIT_VOISINS:
            voisin_ligne: int = maison.ligne + delta_ligne
            voisin_colonne: int = maison.colonne + delta_colonne
            coordonnee_voisin: tuple[int, int] = (
                voisin_ligne,
                voisin_colonne,
            )
            if coordonnee_voisin != case_ignoree:
                if self.est_case_route(voisin_ligne, voisin_colonne):
                    nb_routes = nb_routes + PAS_INCREMENT_COMPTEUR
                else:
                    pass
            else:
                pass
        return nb_routes

    def peut_connecter_route_pres_des_maisons(
        self,
        ligne: int,
        colonne: int,
        maison_autorisee: Maison | None = None,
        ancienne_sortie_ignoree: tuple[int, int] | None = None,
    ) -> bool:
        """Vérifie qu'aucune maison voisine ne dépasse son unique route.

        Une maison ne peut être adjacente qu'à une seule CASE_ROUTE (sa
        case_sortie). Toute tentative de poser une deuxième route voisine
        d'une maison déjà connectée est refusée.

        Args:
            ligne: Ligne de la case où l'on souhaite poser une route.
            colonne: Colonne de la case où l'on souhaite poser une route.
            maison_autorisee: Maison en cours d'initialisation ou de
                réorientation de sa propre sortie.
            ancienne_sortie_ignoree: Coordonnée (ligne, colonne) de
                l'ancienne sortie en cours de déplacement.

        Returns:
            True si la règle d'unicité est respectée pour toutes les maisons,
            False sinon.
        """
        case_candidate_col_lig: tuple[int, int] = (colonne, ligne)
        case_candidate_lig_col: tuple[int, int] = (ligne, colonne)

        for maison in self.maisons:
            coordonnee_maison_col_lig: tuple[int, int] = (
                maison.colonne,
                maison.ligne,
            )
            if self.sont_cases_adjacentes_chebyshev(
                case_candidate_col_lig,
                coordonnee_maison_col_lig,
            ):
                if maison is maison_autorisee:
                    nb_autres_routes: int = (
                        self.compter_routes_adjacentes_maison(
                            maison,
                            ancienne_sortie_ignoree,
                        )
                    )
                    if nb_autres_routes >= NB_MAX_ROUTES_ADJACENTES_MAISON:
                        return False
                    else:
                        pass
                else:
                    if maison.case_sortie is not None:
                        if maison.case_sortie != case_candidate_lig_col:
                            return False
                        else:
                            pass
                    else:
                        nb_routes_existantes: int = (
                            self.compter_routes_adjacentes_maison(
                                maison,
                                ancienne_sortie_ignoree,
                            )
                        )
                        if (
                            nb_routes_existantes
                            >= NB_MAX_ROUTES_ADJACENTES_MAISON
                        ):
                            return False
                        else:
                            pass
            else:
                pass

        return True

    def obtenir_cible_orientation_maison(
        self,
        maison: Maison,
    ) -> tuple[float, float]:
        """Détermine le point (ligne, colonne) vers lequel orienter la sortie.

        Privilégie l'usine de même couleur la plus proche ; à défaut, vise
        le centre de la grille.

        Args:
            maison: Instance de Maison à orienter.

        Returns:
            Un tuple (ligne_cible, colonne_cible) flottant.
        """
        meilleure_usine: Usine | None = None
        meilleure_distance: float = float(self.nb_lignes + self.nb_colonnes)

        for usine in self.usines:
            if usine.couleur == maison.couleur:
                distance: float = hypot(
                    float(usine.ligne - maison.ligne),
                    float(usine.colonne - maison.colonne),
                )
                if meilleure_usine is None or distance < meilleure_distance:
                    meilleure_usine = usine
                    meilleure_distance = distance
                else:
                    pass
            else:
                pass

        if meilleure_usine is not None:
            return (
                float(meilleure_usine.ligne),
                float(meilleure_usine.colonne),
            )
        else:
            moitie: float = float(DIVISEUR_MOITIE)
            return (
                float(self.nb_lignes) / moitie,
                float(self.nb_colonnes) / moitie,
            )

    def initialiser_sortie_maison(self, maison: Maison) -> bool:
        """Attribue, pose gratuitement et connecte la case_sortie d'une maison.

        Si une route libre d'attache est déjà adjacente à la maison, elle
        devient la case_sortie et y est connectée. Sinon, choisit la
        meilleure case libre adjacente orientée vers l'usine cible, y pose
        gratuitement une CASE_ROUTE et la connecte à la maison.

        Args:
            maison: Instance de Maison nouvellement placée.

        Returns:
            True si une case_sortie a été associée et connectée, False sinon.
        """
        coordonnee_maison: tuple[int, int] = (maison.colonne, maison.ligne)

        if maison.case_sortie is not None:
            lig_sortie, col_sortie = maison.case_sortie
            if self.est_case_libre(lig_sortie, col_sortie):
                self.definir_etat_case(
                    lig_sortie,
                    col_sortie,
                    CASE_ROUTE,
                )
                self.connecter_cases(
                    coordonnee_maison,
                    (col_sortie, lig_sortie),
                )
                return True
            else:
                if self.est_case_route(lig_sortie, col_sortie):
                    self.connecter_cases(
                        coordonnee_maison,
                        (col_sortie, lig_sortie),
                    )
                    return True
                else:
                    pass

        routes_adjacentes: list[tuple[int, int]] = []
        for delta_colonne, delta_ligne in DIRECTIONS_HUIT_VOISINS:
            voisin_ligne: int = maison.ligne + delta_ligne
            voisin_colonne: int = maison.colonne + delta_colonne
            if self.est_case_route(voisin_ligne, voisin_colonne):
                if not self.est_case_sortie_de_batiment(
                    voisin_ligne,
                    voisin_colonne,
                ):
                    routes_adjacentes.append((voisin_ligne, voisin_colonne))
                else:
                    pass
            else:
                pass

        if len(routes_adjacentes) == NB_MAX_ROUTES_ADJACENTES_MAISON:
            sortie_existante: tuple[int, int] = routes_adjacentes[
                INDICE_MINIMUM_GRILLE
            ]
            maison.definir_case_sortie(sortie_existante)
            lig_existante, col_existante = sortie_existante
            self.connecter_cases(
                coordonnee_maison,
                (col_existante, lig_existante),
            )
            return True
        else:
            pass

        cible_ligne, cible_colonne = self.obtenir_cible_orientation_maison(
            maison
        )
        meilleure_case: tuple[int, int] | None = None
        meilleure_distance: float = float(self.nb_lignes + self.nb_colonnes)

        for delta_colonne, delta_ligne in DIRECTIONS_HUIT_VOISINS:
            voisin_ligne = maison.ligne + delta_ligne
            voisin_colonne = maison.colonne + delta_colonne
            if self.est_case_libre(voisin_ligne, voisin_colonne):
                distance_cible: float = hypot(
                    float(voisin_ligne) - cible_ligne,
                    float(voisin_colonne) - cible_colonne,
                )
                if (
                    meilleure_case is None
                    or distance_cible < meilleure_distance
                ):
                    meilleure_case = (voisin_ligne, voisin_colonne)
                    meilleure_distance = distance_cible
                else:
                    pass
            else:
                pass

        if meilleure_case is not None:
            lig_choisie, col_choisie = meilleure_case
            self.definir_etat_case(lig_choisie, col_choisie, CASE_ROUTE)
            maison.definir_case_sortie(meilleure_case)
            self.connecter_cases(
                coordonnee_maison,
                (col_choisie, lig_choisie),
            )
            return True
        else:
            return False

    def reorienter_sortie_maison(
        self,
        maison: Maison,
        nouvelle_ligne: int,
        nouvelle_colonne: int,
    ) -> bool:
        """Déplace gratuitement la case_sortie d'une maison vers une case voisine.

        Supprime l'ancienne case_sortie (et ses connexions) et place la
        nouvelle sur une case libre adjacente à la maison sans modifier le
        stock de routes, puis connecte uniquement la maison à cette sortie.

        Args:
            maison: Instance de Maison dont on réoriente la sortie.
            nouvelle_ligne: Ligne de la nouvelle case de sortie souhaitée.
            nouvelle_colonne: Colonne de la nouvelle case de sortie souhaitée.

        Returns:
            True si la sortie a été réorientée, False sinon.
        """
        coordonnee_maison: tuple[int, int] = (maison.colonne, maison.ligne)
        coordonnee_nouvelle: tuple[int, int] = (
            nouvelle_colonne,
            nouvelle_ligne,
        )
        if not self.sont_cases_adjacentes_chebyshev(
            coordonnee_maison,
            coordonnee_nouvelle,
        ):
            return False
        else:
            pass

        nouvelle_sortie: tuple[int, int] = (nouvelle_ligne, nouvelle_colonne)
        if maison.case_sortie == nouvelle_sortie:
            self.connecter_cases(coordonnee_maison, coordonnee_nouvelle)
            return True
        else:
            pass

        if not self.est_case_libre(nouvelle_ligne, nouvelle_colonne):
            return False
        else:
            pass

        ancienne_sortie: tuple[int, int] | None = maison.case_sortie
        if ancienne_sortie is not None:
            ancienne_ligne, ancienne_colonne = ancienne_sortie
            self.retirer_toutes_connexions_case(
                (ancienne_colonne, ancienne_ligne)
            )
            if self.est_case_route(ancienne_ligne, ancienne_colonne):
                self.definir_etat_case(
                    ancienne_ligne,
                    ancienne_colonne,
                    CASE_VIDE,
                )
            else:
                pass
        else:
            pass

        self.retirer_toutes_connexions_case(coordonnee_maison)
        self.definir_etat_case(nouvelle_ligne, nouvelle_colonne, CASE_ROUTE)
        maison.definir_case_sortie(nouvelle_sortie)
        self.connecter_cases(coordonnee_maison, coordonnee_nouvelle)
        return True

    def placer_maison(self, maison: Maison) -> bool:
        """Place une maison sur la grille et crée gratuitement sa case_sortie.

        Args:
            maison: Instance de Maison à placer.

        Returns:
            True si la maison a pu être placée, False sinon.
        """
        if self.est_case_libre(maison.ligne, maison.colonne):
            self.definir_etat_case(maison.ligne, maison.colonne, CASE_MAISON)
            self.maisons.append(maison)
            self.initialiser_sortie_maison(maison)
            return True
        else:
            return False

    def obtenir_cible_orientation_usine(
        self,
        usine: Usine,
    ) -> tuple[float, float]:
        """Détermine le point (ligne, colonne) vers lequel orienter l'usine.

        Privilégie la maison de même couleur la plus proche ; à défaut, vise
        le centre de la grille.

        Args:
            usine: Instance de Usine à orienter.

        Returns:
            Un tuple (ligne_cible, colonne_cible) flottant.
        """
        meilleure_maison: Maison | None = None
        meilleure_distance: float = float(self.nb_lignes + self.nb_colonnes)

        for maison in self.maisons:
            if maison.couleur == usine.couleur:
                distance: float = hypot(
                    float(maison.ligne - usine.ligne),
                    float(maison.colonne - usine.colonne),
                )
                if meilleure_maison is None or distance < meilleure_distance:
                    meilleure_maison = maison
                    meilleure_distance = distance
                else:
                    pass
            else:
                pass

        if meilleure_maison is not None:
            return (
                float(meilleure_maison.ligne),
                float(meilleure_maison.colonne),
            )
        else:
            moitie: float = float(DIVISEUR_MOITIE)
            return (
                float(self.nb_lignes) / moitie,
                float(self.nb_colonnes) / moitie,
            )

    def initialiser_sortie_usine(self, usine: Usine) -> bool:
        """Attribue, pose gratuitement et connecte la case_sortie d'une usine.

        Si une route libre d'attache est déjà adjacente à l'usine, elle
        devient la case_sortie et y est connectée. Sinon, choisit la
        meilleure case libre adjacente, y pose gratuitement une CASE_ROUTE
        et la connecte à l'usine.

        Args:
            usine: Instance de Usine nouvellement placée.

        Returns:
            True si une case_sortie a été associée et connectée, False sinon.
        """
        coordonnee_usine: tuple[int, int] = (usine.colonne, usine.ligne)

        if usine.case_sortie is not None:
            lig_sortie, col_sortie = usine.case_sortie
            if self.est_case_libre(lig_sortie, col_sortie):
                self.definir_etat_case(
                    lig_sortie,
                    col_sortie,
                    CASE_ROUTE,
                )
                self.connecter_cases(
                    coordonnee_usine,
                    (col_sortie, lig_sortie),
                )
                return True
            else:
                if self.est_case_route(lig_sortie, col_sortie):
                    self.connecter_cases(
                        coordonnee_usine,
                        (col_sortie, lig_sortie),
                    )
                    return True
                else:
                    pass

        routes_adjacentes: list[tuple[int, int]] = []
        for delta_colonne, delta_ligne in DIRECTIONS_HUIT_VOISINS:
            voisin_ligne: int = usine.ligne + delta_ligne
            voisin_colonne: int = usine.colonne + delta_colonne
            if self.est_case_route(voisin_ligne, voisin_colonne):
                if not self.est_case_sortie_de_batiment(
                    voisin_ligne,
                    voisin_colonne,
                ):
                    routes_adjacentes.append((voisin_ligne, voisin_colonne))
                else:
                    pass
            else:
                pass

        if len(routes_adjacentes) == NB_MAX_ROUTES_ADJACENTES_MAISON:
            sortie_existante: tuple[int, int] = routes_adjacentes[
                INDICE_MINIMUM_GRILLE
            ]
            usine.definir_case_sortie(sortie_existante)
            lig_existante, col_existante = sortie_existante
            self.connecter_cases(
                coordonnee_usine,
                (col_existante, lig_existante),
            )
            return True
        else:
            pass

        cible_ligne, cible_colonne = self.obtenir_cible_orientation_usine(
            usine
        )
        meilleure_case: tuple[int, int] | None = None
        meilleure_distance: float = float(self.nb_lignes + self.nb_colonnes)

        for delta_colonne, delta_ligne in DIRECTIONS_HUIT_VOISINS:
            voisin_ligne = usine.ligne + delta_ligne
            voisin_colonne = usine.colonne + delta_colonne
            if self.est_case_libre(voisin_ligne, voisin_colonne):
                distance_cible: float = hypot(
                    float(voisin_ligne) - cible_ligne,
                    float(voisin_colonne) - cible_colonne,
                )
                if (
                    meilleure_case is None
                    or distance_cible < meilleure_distance
                ):
                    meilleure_case = (voisin_ligne, voisin_colonne)
                    meilleure_distance = distance_cible
                else:
                    pass
            else:
                pass

        if meilleure_case is not None:
            lig_choisie, col_choisie = meilleure_case
            self.definir_etat_case(lig_choisie, col_choisie, CASE_ROUTE)
            usine.definir_case_sortie(meilleure_case)
            self.connecter_cases(
                coordonnee_usine,
                (col_choisie, lig_choisie),
            )
            return True
        else:
            return False

    def reorienter_sortie_usine(
        self,
        usine: Usine,
        nouvelle_ligne: int,
        nouvelle_colonne: int,
    ) -> bool:
        """Déplace gratuitement la case_sortie d'une usine vers une case voisine.

        Supprime l'ancienne case_sortie (et ses connexions) et place la
        nouvelle sur une case libre adjacente à l'usine sans modifier le
        stock de routes, puis connecte uniquement l'usine à cette sortie.

        Args:
            usine: Instance de Usine dont on réoriente la sortie.
            nouvelle_ligne: Ligne de la nouvelle case de sortie souhaitée.
            nouvelle_colonne: Colonne de la nouvelle case de sortie souhaitée.

        Returns:
            True si la sortie a été réorientée, False sinon.
        """
        coordonnee_usine: tuple[int, int] = (usine.colonne, usine.ligne)
        coordonnee_nouvelle: tuple[int, int] = (
            nouvelle_colonne,
            nouvelle_ligne,
        )
        if not self.sont_cases_adjacentes_chebyshev(
            coordonnee_usine,
            coordonnee_nouvelle,
        ):
            return False
        else:
            pass

        nouvelle_sortie: tuple[int, int] = (nouvelle_ligne, nouvelle_colonne)
        if usine.case_sortie == nouvelle_sortie:
            self.connecter_cases(coordonnee_usine, coordonnee_nouvelle)
            return True
        else:
            pass

        if not self.est_case_libre(nouvelle_ligne, nouvelle_colonne):
            return False
        else:
            pass

        ancienne_sortie: tuple[int, int] | None = usine.case_sortie
        if ancienne_sortie is not None:
            ancienne_ligne, ancienne_colonne = ancienne_sortie
            self.retirer_toutes_connexions_case(
                (ancienne_colonne, ancienne_ligne)
            )
            if self.est_case_route(ancienne_ligne, ancienne_colonne):
                self.definir_etat_case(
                    ancienne_ligne,
                    ancienne_colonne,
                    CASE_VIDE,
                )
            else:
                pass
        else:
            pass

        self.retirer_toutes_connexions_case(coordonnee_usine)
        self.definir_etat_case(nouvelle_ligne, nouvelle_colonne, CASE_ROUTE)
        usine.definir_case_sortie(nouvelle_sortie)
        self.connecter_cases(coordonnee_usine, coordonnee_nouvelle)
        return True

    def placer_usine(self, usine: Usine) -> bool:
        """Place une usine sur la grille et crée gratuitement sa case_sortie.

        Args:
            usine: Instance de Usine à placer.

        Returns:
            True si l'usine a pu être placée, False sinon.
        """
        if self.est_case_libre(usine.ligne, usine.colonne):
            self.definir_etat_case(usine.ligne, usine.colonne, CASE_USINE)
            self.usines.append(usine)
            self.initialiser_sortie_usine(usine)
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

    def autoriser_connexion_maison(
        self,
        ligne_maison: int,
        colonne_maison: int,
        ligne_autre: int,
        colonne_autre: int,
    ) -> bool:
        """Vérifie si une Maison peut être connectée à une case adjacente.

        Une Maison ne peut être connectée qu'à une CASE_ROUTE qui est son
        unique case_sortie, et ne peut jamais dépasser 1 liaison dans
        self.connexions.

        Args:
            ligne_maison: Ligne de la maison.
            colonne_maison: Colonne de la maison.
            ligne_autre: Ligne de l'autre case à connecter.
            colonne_autre: Colonne de l'autre case à connecter.

        Returns:
            True si la connexion avec cette maison est valide, False sinon.
        """
        if not self.est_case_route(ligne_autre, colonne_autre):
            return False
        else:
            pass

        maison: Maison | None = self.obtenir_maison_a_coordonnee(
            ligne_maison,
            colonne_maison,
        )
        if maison is None:
            return False
        else:
            pass

        coordonnee_autre_lig_col: tuple[int, int] = (
            ligne_autre,
            colonne_autre,
        )
        coordonnee_maison_col_lig: tuple[int, int] = (
            colonne_maison,
            ligne_maison,
        )
        coordonnee_autre_col_lig: tuple[int, int] = (
            colonne_autre,
            ligne_autre,
        )

        if maison.case_sortie is not None:
            if maison.case_sortie != coordonnee_autre_lig_col:
                return False
            else:
                voisins_actuels: set[tuple[int, int]] = (
                    self.obtenir_voisins_connectes(coordonnee_maison_col_lig)
                )
                if len(voisins_actuels) == LONGUEUR_LISTE_VIDE:
                    return True
                else:
                    if coordonnee_autre_col_lig in voisins_actuels:
                        return True
                    else:
                        return False
        else:
            voisins_existants: set[tuple[int, int]] = (
                self.obtenir_voisins_connectes(coordonnee_maison_col_lig)
            )
            if len(voisins_existants) == LONGUEUR_LISTE_VIDE:
                maison.definir_case_sortie(coordonnee_autre_lig_col)
                return True
            else:
                if coordonnee_autre_col_lig in voisins_existants:
                    maison.definir_case_sortie(coordonnee_autre_lig_col)
                    return True
                else:
                    return False

    def autoriser_connexion_usine(
        self,
        ligne_usine: int,
        colonne_usine: int,
        ligne_autre: int,
        colonne_autre: int,
    ) -> bool:
        """Vérifie si une Usine peut être connectée à une case adjacente.

        Une Usine ne peut être connectée qu'à une CASE_ROUTE qui est son
        unique case_sortie, et ne peut jamais dépasser 1 liaison dans
        self.connexions (interdiction de traverser une usine avec deux routes).

        Args:
            ligne_usine: Ligne de l'usine.
            colonne_usine: Colonne de l'usine.
            ligne_autre: Ligne de l'autre case à connecter.
            colonne_autre: Colonne de l'autre case à connecter.

        Returns:
            True si la connexion avec cette usine est valide, False sinon.
        """
        if not self.est_case_route(ligne_autre, colonne_autre):
            return False
        else:
            pass

        usine: Usine | None = self.obtenir_usine_a_coordonnee(
            ligne_usine,
            colonne_usine,
        )
        if usine is None:
            return False
        else:
            pass

        coordonnee_autre_lig_col: tuple[int, int] = (
            ligne_autre,
            colonne_autre,
        )
        coordonnee_usine_col_lig: tuple[int, int] = (
            colonne_usine,
            ligne_usine,
        )
        coordonnee_autre_col_lig: tuple[int, int] = (
            colonne_autre,
            ligne_autre,
        )

        if usine.case_sortie is not None:
            if usine.case_sortie != coordonnee_autre_lig_col:
                return False
            else:
                voisins_actuels: set[tuple[int, int]] = (
                    self.obtenir_voisins_connectes(coordonnee_usine_col_lig)
                )
                if len(voisins_actuels) == LONGUEUR_LISTE_VIDE:
                    return True
                else:
                    if coordonnee_autre_col_lig in voisins_actuels:
                        return True
                    else:
                        return False
        else:
            voisins_existants: set[tuple[int, int]] = (
                self.obtenir_voisins_connectes(coordonnee_usine_col_lig)
            )
            if len(voisins_existants) == LONGUEUR_LISTE_VIDE:
                usine.definir_case_sortie(coordonnee_autre_lig_col)
                return True
            else:
                if coordonnee_autre_col_lig in voisins_existants:
                    usine.definir_case_sortie(coordonnee_autre_lig_col)
                    return True
                else:
                    return False

    def connecter_cases(
        self,
        case_a: tuple[int, int],
        case_b: tuple[int, int],
    ) -> bool:
        """Crée une connexion explicite bidirectionnelle entre deux cases.

        Les coordonnées case_a et case_b sont au format (colonne, ligne).
        La liaison n'est enregistrée que si les cases sont adjacentes
        (distance de Chebyshev == 1) et respectent les règles métier :
        - Une Maison ne se connecte qu'à son unique case_sortie.
        - Une Usine ne se connecte qu'à son unique case_sortie.
        - Deux routes adjacentes se connectent explicitement.

        Args:
            case_a: Coordonnée (colonne, ligne) de la première case.
            case_b: Coordonnée (colonne, ligne) de la seconde case.

        Returns:
            True si la connexion a été créée (ou existait déjà), False sinon.
        """
        colonne_a, ligne_a = case_a
        colonne_b, ligne_b = case_b

        valides: bool = (
            self.est_coordonnee_valide(ligne_a, colonne_a)
            and self.est_coordonnee_valide(ligne_b, colonne_b)
        )
        if not valides:
            return False
        else:
            pass

        if not self.sont_cases_adjacentes_chebyshev(case_a, case_b):
            return False
        else:
            pass

        connectables: bool = (
            self.est_case_connectable_route(ligne_a, colonne_a)
            and self.est_case_connectable_route(ligne_b, colonne_b)
        )
        if not connectables:
            return False
        else:
            pass

        etat_a: int = self.matrice[ligne_a][colonne_a]
        etat_b: int = self.matrice[ligne_b][colonne_b]
        au_moins_une_route: bool = (
            etat_a == CASE_ROUTE or etat_b == CASE_ROUTE
        )
        if not au_moins_une_route:
            return False
        else:
            pass

        if etat_a == CASE_MAISON:
            if not self.autoriser_connexion_maison(
                ligne_a,
                colonne_a,
                ligne_b,
                colonne_b,
            ):
                return False
            else:
                pass
        else:
            pass

        if etat_b == CASE_MAISON:
            if not self.autoriser_connexion_maison(
                ligne_b,
                colonne_b,
                ligne_a,
                colonne_a,
            ):
                return False
            else:
                pass
        else:
            pass

        if etat_a == CASE_USINE:
            if not self.autoriser_connexion_usine(
                ligne_a,
                colonne_a,
                ligne_b,
                colonne_b,
            ):
                return False
            else:
                pass
        else:
            pass

        if etat_b == CASE_USINE:
            if not self.autoriser_connexion_usine(
                ligne_b,
                colonne_b,
                ligne_a,
                colonne_a,
            ):
                return False
            else:
                pass
        else:
            pass

        self.ajouter_arete_connexion(case_a, case_b)
        return True

    def sont_cases_connectees_visuellement(
        self,
        ligne_route: int,
        colonne_route: int,
        ligne_voisin: int,
        colonne_voisin: int,
    ) -> bool:
        """Vérifie si deux cases ont une arête explicite dans self.connexions.

        Args:
            ligne_route: Ligne de la première case.
            colonne_route: Colonne de la première case.
            ligne_voisin: Ligne de la case voisine.
            colonne_voisin: Colonne de la case voisine.

        Returns:
            True si les deux cases sont explicitement connectées, False sinon.
        """
        case_source: tuple[int, int] = (colonne_route, ligne_route)
        case_voisine: tuple[int, int] = (colonne_voisin, ligne_voisin)
        if self.sont_cases_connectees(case_source, case_voisine):
            return True
        else:
            return False

    def placer_route(self, ligne: int, colonne: int) -> bool:
        """Place un segment de route sur n'importe quelle CASE_VIDE.

        Autorise la pose d'une route même si elle est directement adjacente
        à une ou plusieurs Maisons (aucune connexion implicite n'est créée).

        Args:
            ligne: Indice de la ligne où poser la route.
            colonne: Indice de la colonne où poser la route.

        Returns:
            True si la route a été posée, False sinon.
        """
        stock_disponible: bool = self.stock_routes > STOCK_ROUTES_EPUISE
        if stock_disponible and self.est_case_libre(ligne, colonne):
            self.definir_etat_case(ligne, colonne, CASE_ROUTE)
            self.stock_routes = self.stock_routes - UNITE_STOCK_ROUTE
            return True
        else:
            return False

    def supprimer_route(self, ligne: int, colonne: int) -> bool:
        """Supprime un segment de route et retire ses arêtes dans connexions.

        Refuse la suppression du bout de route obligatoire (case_sortie)
        d'une Maison ou d'une Usine.

        Args:
            ligne: Indice de la ligne où supprimer la route.
            colonne: Indice de la colonne où supprimer la route.

        Returns:
            True si une route a été supprimée, False sinon.
        """
        if self.est_case_route(ligne, colonne):
            if self.est_case_sortie_de_batiment(ligne, colonne):
                return False
            else:
                coordonnee_col_lig: tuple[int, int] = (colonne, ligne)
                self.retirer_toutes_connexions_case(coordonnee_col_lig)
                self.definir_etat_case(ligne, colonne, CASE_VIDE)
                self.stock_routes = self.stock_routes + UNITE_STOCK_ROUTE
                return True
        else:
            return False

    def sont_cases_adjacentes_chebyshev(
        self,
        case_a: tuple[int, int],
        case_b: tuple[int, int],
    ) -> bool:
        """Vérifie si deux cases (col, lig) sont adjacentes (8 directions).

        Deux cases sont directement adjacentes si leur distance de Chebyshev
        est exactement égale à DISTANCE_CHEBYSHEV_ADJACENTE (1).

        Args:
            case_a: Coordonnée (colonne, ligne) de la première case.
            case_b: Coordonnée (colonne, ligne) de la seconde case.

        Returns:
            True si la distance de Chebyshev vaut 1, False sinon.
        """
        colonne_a, ligne_a = case_a
        colonne_b, ligne_b = case_b
        ecart_colonne: int = abs(colonne_a - colonne_b)
        ecart_ligne: int = abs(ligne_a - ligne_b)
        if ecart_colonne > ecart_ligne:
            distance_chebyshev: int = ecart_colonne
        else:
            distance_chebyshev = ecart_ligne

        if distance_chebyshev == DISTANCE_CHEBYSHEV_ADJACENTE:
            return True
        else:
            return False

    def a_connexion_externe_hors_ensemble(
        self,
        case_cible: tuple[int, int],
        cases_exclues: list[tuple[int, int]],
    ) -> bool:
        """Vérifie si une case est explicitement reliée à un voisin externe.

        Args:
            case_cible: Coordonnée (colonne, ligne) de la case à inspecter.
            cases_exclues: Liste des coordonnées (colonne, ligne) à ignorer.

        Returns:
            True si au moins un voisin explicitement connecté dans
            self.connexions n'est pas dans cases_exclues, False sinon.
        """
        voisins_connectes: set[tuple[int, int]] = (
            self.obtenir_voisins_connectes(case_cible)
        )
        for coordonnee_voisin in voisins_connectes:
            if coordonnee_voisin not in cases_exclues:
                return True
            else:
                pass
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

    def transition_respecte_sortie_maison(
        self,
        coordonnee_source: tuple[int, int],
        coordonnee_destination: tuple[int, int],
    ) -> bool:
        """Vérifie que l'entrée ou la sortie d'un bâtiment passe par sa case_sortie.

        S'applique aussi bien aux Maisons qu'aux Usines dotées d'une
        case_sortie.

        Args:
            coordonnee_source: Coordonnée (colonne, ligne) de départ du pas.
            coordonnee_destination: Coordonnée (colonne, ligne) d'arrivée du pas.

        Returns:
            True si la transition est valide vis-à-vis des bâtiments, False sinon.
        """
        col_src, lig_src = coordonnee_source
        col_dst, lig_dst = coordonnee_destination

        maison_src: Maison | None = self.obtenir_maison_a_coordonnee(
            lig_src,
            col_src,
        )
        if maison_src is not None and maison_src.case_sortie is not None:
            if (lig_dst, col_dst) != maison_src.case_sortie:
                return False
            else:
                pass
        else:
            pass

        maison_dst: Maison | None = self.obtenir_maison_a_coordonnee(
            lig_dst,
            col_dst,
        )
        if maison_dst is not None and maison_dst.case_sortie is not None:
            if (lig_src, col_src) != maison_dst.case_sortie:
                return False
            else:
                pass
        else:
            pass

        usine_src: Usine | None = self.obtenir_usine_a_coordonnee(
            lig_src,
            col_src,
        )
        if usine_src is not None and usine_src.case_sortie is not None:
            if (lig_dst, col_dst) != usine_src.case_sortie:
                return False
            else:
                pass
        else:
            pass

        usine_dst: Usine | None = self.obtenir_usine_a_coordonnee(
            lig_dst,
            col_dst,
        )
        if usine_dst is not None and usine_dst.case_sortie is not None:
            if (lig_src, col_src) != usine_dst.case_sortie:
                return False
            else:
                pass
        else:
            pass

        return True

    def obtenir_voisins_accessibles(
        self,
        coordonnee: tuple[int, int],
        depart: tuple[int, int],
        arrivee: tuple[int, int],
    ) -> list[tuple[int, int]]:
        """Retourne les voisins explicitement connectés et traversables.

        Explore uniquement les arêtes enregistrées dans self.connexions[coordonnee].

        Args:
            coordonnee: Coordonnée (colonne, ligne) de la case courante.
            depart: Coordonnée (colonne, ligne) de départ du trajet.
            arrivee: Coordonnée (colonne, ligne) d'arrivée du trajet.

        Returns:
            Liste des coordonnées (colonne, ligne) des voisins connectés
            et traversables.
        """
        voisins_accessibles: list[tuple[int, int]] = []
        voisins_connectes: set[tuple[int, int]] = (
            self.obtenir_voisins_connectes(coordonnee)
        )

        for coordonnee_voisin in voisins_connectes:
            if self.est_case_traversable(
                coordonnee_voisin,
                depart,
                arrivee,
            ):
                if self.transition_respecte_sortie_maison(
                    coordonnee,
                    coordonnee_voisin,
                ):
                    voisins_accessibles.append(coordonnee_voisin)
                else:
                    pass
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
                    if self.a_voisin_libre_pour_sortie(
                        indice_ligne,
                        indice_colonne,
                    ):
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

    def est_a_proximite_batiment_reference(
        self,
        ligne: int,
        colonne: int,
        distance_maximale: int,
        couleur_cible: tuple[int, int, int] | None = None,
    ) -> bool:
        """Vérifie si une case est à distance raisonnable d'un bâtiment actif.

        Args:
            ligne: Indice de la ligne candidate.
            colonne: Indice de la colonne candidate.
            distance_maximale: Écart maximal autorisé en lignes ou colonnes.
            couleur_cible: Couleur privilégiée des bâtiments de référence.

        Returns:
            True s'il n'y a aucun bâtiment sur la carte ou si au moins un
            bâtiment de référence se trouve dans le rayon distance_maximale.
        """
        aucun_batiment: bool = (
            len(self.maisons) == LONGUEUR_LISTE_VIDE
            and len(self.usines) == LONGUEUR_LISTE_VIDE
        )
        if aucun_batiment:
            return True
        else:
            pass

        coordonnees_reference: list[tuple[int, int]] = []

        if couleur_cible is not None:
            for usine in self.usines:
                if usine.couleur == couleur_cible:
                    coordonnees_reference.append(
                        (usine.ligne, usine.colonne)
                    )
                else:
                    pass
            for maison in self.maisons:
                if maison.couleur == couleur_cible:
                    coordonnees_reference.append(
                        (maison.ligne, maison.colonne)
                    )
                else:
                    pass
        else:
            pass

        if len(coordonnees_reference) == LONGUEUR_LISTE_VIDE:
            for usine in self.usines:
                coordonnees_reference.append((usine.ligne, usine.colonne))
            for maison in self.maisons:
                coordonnees_reference.append((maison.ligne, maison.colonne))
        else:
            pass

        for ref_ligne, ref_colonne in coordonnees_reference:
            ecart_ligne: int = abs(ligne - ref_ligne)
            ecart_colonne: int = abs(colonne - ref_colonne)
            dans_rayon: bool = (
                ecart_ligne <= distance_maximale
                and ecart_colonne <= distance_maximale
            )
            if dans_rayon:
                return True
            else:
                pass

        return False

    def obtenir_cases_libres_dans_zone(
        self,
        ligne_min: int,
        ligne_max: int,
        colonne_min: int,
        colonne_max: int,
        distance_minimale: int,
        distance_maximale: int,
        couleur_cible: tuple[int, int, int] | None = None,
    ) -> list[tuple[int, int]]:
        """Retourne les cases vides dans une fenêtre donnée proches du réseau.

        Args:
            ligne_min: Borne inférieure de ligne (incluse).
            ligne_max: Borne supérieure de ligne (exclue).
            colonne_min: Borne inférieure de colonne (incluse).
            colonne_max: Borne supérieure de colonne (exclue).
            distance_minimale: Écart minimum avec tout bâtiment existant.
            distance_maximale: Écart maximum avec un bâtiment de référence.
            couleur_cible: Couleur optionnelle pour cibler un réseau existant.

        Returns:
            Liste des coordonnées (ligne, colonne) éligibles.
        """
        cases_proches_dans_zone: list[tuple[int, int]] = []
        cases_dans_zone: list[tuple[int, int]] = []

        for indice_ligne in range(ligne_min, ligne_max):
            for indice_colonne in range(colonne_min, colonne_max):
                if self.est_case_libre(indice_ligne, indice_colonne):
                    if self.a_voisin_libre_pour_sortie(
                        indice_ligne,
                        indice_colonne,
                    ):
                        if self.est_eloignee_des_batiments(
                            indice_ligne,
                            indice_colonne,
                            distance_minimale,
                        ):
                            cases_dans_zone.append(
                                (indice_ligne, indice_colonne)
                            )
                            if self.est_a_proximite_batiment_reference(
                                indice_ligne,
                                indice_colonne,
                                distance_maximale,
                                couleur_cible,
                            ):
                                cases_proches_dans_zone.append(
                                    (indice_ligne, indice_colonne)
                                )
                            else:
                                pass
                        else:
                            pass
                    else:
                        pass
                else:
                    pass

        if len(cases_proches_dans_zone) > LONGUEUR_LISTE_VIDE:
            return cases_proches_dans_zone
        else:
            if len(cases_dans_zone) > LONGUEUR_LISTE_VIDE:
                return cases_dans_zone
            else:
                return self.obtenir_cases_libres_pour_apparition(
                    distance_minimale,
                    MARGE_BORDURE_APPARITION,
                )
