"""Modèles des entités du jeu (Maison, Usine, Voiture) sans Pygame."""

import math

from src.config import (
    COMPTEUR_INITIAL_FRAMES,
    COMPTEUR_INITIAL_LIVRAISONS,
    DISTANCE_MIN_SECURITE_VOITURE,
    DISTANCE_NULLE,
    INDICE_PREMIERE_ETAPE_ITINERAIRE,
    INTERVALLE_APPARITION_VOITURE,
    LONGUEUR_MINIMALE_ITINERAIRE,
    NB_MAX_VOITURES_PAR_MAISON,
    PAS_INCREMENT_COMPTEUR,
    SEUIL_ARRIVEE_ETAPE,
    VITESSE_VOITURE,
)


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
        self.compteur_apparition: int = COMPTEUR_INITIAL_FRAMES
        self.nb_voitures_actives: int = COMPTEUR_INITIAL_FRAMES

    def obtenir_coordonnee_grille(self) -> tuple[int, int]:
        """Retourne la coordonnée (colonne, ligne) de la maison.

        Returns:
            Un tuple (colonne, ligne).
        """
        return (self.colonne, self.ligne)

    def incrementer_timer_apparition(self) -> None:
        """Incrémente le compteur de frames avant la prochaine génération."""
        self.compteur_apparition = (
            self.compteur_apparition + PAS_INCREMENT_COMPTEUR
        )

    def peut_generer_voiture(self) -> bool:
        """Indique si la maison peut faire apparaître une nouvelle voiture.

        Returns:
            True si le délai est écoulé et le quota non atteint, False sinon.
        """
        quota_disponible: bool = (
            self.nb_voitures_actives < NB_MAX_VOITURES_PAR_MAISON
        )
        delai_ecoule: bool = (
            self.compteur_apparition >= INTERVALLE_APPARITION_VOITURE
        )
        if quota_disponible and delai_ecoule:
            return True
        else:
            return False

    def creer_voiture(
        self,
        usine_cible: "Usine",
        itineraire: list[tuple[int, int]],
    ) -> "Voiture":
        """Génère une nouvelle voiture rattachée à cette maison.

        Args:
            usine_cible: Instance de l'Usine de destination.
            itineraire: Liste ordonnée des coordonnées (col, lig) à suivre.

        Returns:
            La nouvelle instance de Voiture créée.
        """
        self.compteur_apparition = COMPTEUR_INITIAL_FRAMES
        self.nb_voitures_actives = (
            self.nb_voitures_actives + PAS_INCREMENT_COMPTEUR
        )
        nouvelle_voiture: Voiture = Voiture(
            maison_origine=self,
            usine_cible=usine_cible,
            itineraire=itineraire,
        )
        return nouvelle_voiture

    def notifier_arrivee_voiture(self) -> None:
        """Libère une place dans le quota de voitures actives de la maison."""
        if self.nb_voitures_actives > COMPTEUR_INITIAL_FRAMES:
            self.nb_voitures_actives = (
                self.nb_voitures_actives - PAS_INCREMENT_COMPTEUR
            )
        else:
            self.nb_voitures_actives = COMPTEUR_INITIAL_FRAMES


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
        self.voitures_recues: int = COMPTEUR_INITIAL_LIVRAISONS

    def obtenir_coordonnee_grille(self) -> tuple[int, int]:
        """Retourne la coordonnée (colonne, ligne) de l'usine.

        Returns:
            Un tuple (colonne, ligne).
        """
        return (self.colonne, self.ligne)

    def recevoir_voiture(self, voiture: "Voiture") -> None:
        """Enregistre l'arrivée d'une voiture à l'usine et notifie sa maison.

        Args:
            voiture: Instance de Voiture arrivée à destination.
        """
        self.voitures_recues = (
            self.voitures_recues + PAS_INCREMENT_COMPTEUR
        )
        voiture.maison_origine.notifier_arrivee_voiture()


class Voiture:
    """Représente un véhicule autonome se déplaçant sur les routes."""

    def __init__(
        self,
        maison_origine: Maison,
        usine_cible: Usine,
        itineraire: list[tuple[int, int]],
    ) -> None:
        """Initialise une voiture au départ de sa maison d'origine.

        Args:
            maison_origine: Maison ayant généré la voiture.
            usine_cible: Usine cible de même couleur.
            itineraire: Chemin initial (liste de tuples (colonne, ligne)).
        """
        self.maison_origine: Maison = maison_origine
        self.usine_cible: Usine = usine_cible
        self.couleur: tuple[int, int, int] = maison_origine.couleur
        self.position_colonne: float = float(maison_origine.colonne)
        self.position_ligne: float = float(maison_origine.ligne)
        self.itineraire: list[tuple[int, int]] = []
        self.indice_etape_cible: int = INDICE_PREMIERE_ETAPE_ITINERAIRE
        self.vitesse: float = VITESSE_VOITURE
        self.est_arrivee: bool = False
        self.mettre_a_jour_itineraire(itineraire)

    def obtenir_case_actuelle(self) -> tuple[int, int]:
        """Retourne la case entière (colonne, ligne) la plus proche.

        Returns:
            Un tuple (colonne, ligne) d'entiers.
        """
        colonne_entiere: int = int(round(self.position_colonne))
        ligne_entiere: int = int(round(self.position_ligne))
        return (colonne_entiere, ligne_entiere)

    def obtenir_prochaine_case_cible(self) -> tuple[int, int]:
        """Retourne la prochaine case (colonne, ligne) visée sur l'itinéraire.

        Returns:
            La coordonnée (colonne, ligne) de l'étape cible courante.
        """
        if self.indice_etape_cible < len(self.itineraire):
            return self.itineraire[self.indice_etape_cible]
        else:
            return self.usine_cible.obtenir_coordonnee_grille()

    def mettre_a_jour_itineraire(
        self,
        nouvel_itineraire: list[tuple[int, int]],
    ) -> None:
        """Affecte un nouvel itinéraire et ajuste l'indice de la prochaine case.

        Args:
            nouvel_itineraire: Liste ordonnée des coordonnées (col, lig).
        """
        self.itineraire = list(nouvel_itineraire)
        if len(self.itineraire) >= LONGUEUR_MINIMALE_ITINERAIRE:
            self.indice_etape_cible = INDICE_PREMIERE_ETAPE_ITINERAIRE
        else:
            self.indice_etape_cible = COMPTEUR_INITIAL_FRAMES

    def calculer_distance_vers_point(
        self,
        cible_colonne: float,
        cible_ligne: float,
    ) -> float:
        """Calcule la distance euclidienne entre la voiture et un point.

        Args:
            cible_colonne: Coordonnée colonne du point cible.
            cible_ligne: Coordonnée ligne du point cible.

        Returns:
            Distance flottante en unités de cases.
        """
        delta_colonne: float = cible_colonne - self.position_colonne
        delta_ligne: float = cible_ligne - self.position_ligne
        return math.hypot(delta_colonne, delta_ligne)

    def est_bloquee_par_trafic(
        self,
        autres_voitures: list["Voiture"],
    ) -> bool:
        """Vérifie si une autre voiture bloque la case suivante de l'itinéraire.

        Args:
            autres_voitures: Liste de toutes les voitures actives.

        Returns:
            True si la voiture doit s'arrêter, False si la voie est libre.
        """
        if self.indice_etape_cible >= len(self.itineraire):
            return False
        else:
            pass

        prochaine_case: tuple[int, int] = self.obtenir_prochaine_case_cible()
        cible_colonne_float: float = float(prochaine_case[0])
        cible_ligne_float: float = float(prochaine_case[1])
        ma_distance_vers_cible: float = self.calculer_distance_vers_point(
            cible_colonne_float,
            cible_ligne_float,
        )

        for autre_voiture in autres_voitures:
            if autre_voiture is self or autre_voiture.est_arrivee:
                continue
            else:
                pass

            distance_entre_voitures: float = self.calculer_distance_vers_point(
                autre_voiture.position_colonne,
                autre_voiture.position_ligne,
            )

            if distance_entre_voitures >= DISTANCE_MIN_SECURITE_VOITURE:
                continue
            else:
                pass

            case_actuelle_autre: tuple[int, int] = (
                autre_voiture.obtenir_case_actuelle()
            )
            prochaine_case_autre: tuple[int, int] = (
                autre_voiture.obtenir_prochaine_case_cible()
            )

            autre_occupe_cible: bool = case_actuelle_autre == prochaine_case
            autre_vise_meme_cible: bool = (
                prochaine_case_autre == prochaine_case
            )

            if autre_occupe_cible:
                autre_distance_cible: float = (
                    autre_voiture.calculer_distance_vers_point(
                        cible_colonne_float,
                        cible_ligne_float,
                    )
                )
                if autre_distance_cible < ma_distance_vers_cible:
                    return True
                else:
                    pass
            else:
                if autre_vise_meme_cible:
                    autre_distance_cible = (
                        autre_voiture.calculer_distance_vers_point(
                            cible_colonne_float,
                            cible_ligne_float,
                        )
                    )
                    if autre_distance_cible < ma_distance_vers_cible:
                        return True
                    else:
                        pass
                else:
                    pass

        return False

    def avancer(self, autres_voitures: list["Voiture"]) -> None:
        """Déplace la voiture d'un pas vers sa prochaine étape si la voie est libre.

        Args:
            autres_voitures: Liste des voitures actives pour gérer le trafic.
        """
        if self.est_arrivee:
            return
        else:
            pass

        if len(self.itineraire) < LONGUEUR_MINIMALE_ITINERAIRE:
            return
        else:
            pass

        if self.indice_etape_cible >= len(self.itineraire):
            self.est_arrivee = True
            return
        else:
            pass

        if self.est_bloquee_par_trafic(autres_voitures):
            return
        else:
            pass

        cible_colonne_int, cible_ligne_int = (
            self.itineraire[self.indice_etape_cible]
        )
        cible_colonne: float = float(cible_colonne_int)
        cible_ligne: float = float(cible_ligne_int)

        delta_colonne: float = cible_colonne - self.position_colonne
        delta_ligne: float = cible_ligne - self.position_ligne
        distance_restante: float = math.hypot(delta_colonne, delta_ligne)

        if distance_restante <= self.vitesse + SEUIL_ARRIVEE_ETAPE:
            self.position_colonne = cible_colonne
            self.position_ligne = cible_ligne
            self.indice_etape_cible = (
                self.indice_etape_cible + PAS_INCREMENT_COMPTEUR
            )
            if self.indice_etape_cible >= len(self.itineraire):
                self.est_arrivee = True
            else:
                self.est_arrivee = False
        else:
            if distance_restante > DISTANCE_NULLE:
                ratio_deplacement: float = self.vitesse / distance_restante
                self.position_colonne = (
                    self.position_colonne + delta_colonne * ratio_deplacement
                )
                self.position_ligne = (
                    self.position_ligne + delta_ligne * ratio_deplacement
                )
            else:
                pass
