"""Modèles des entités du jeu (Maison, Usine, Voiture) sans Pygame."""

import math

from src.config import (
    COMPTEUR_INITIAL_DEMANDES,
    COMPTEUR_INITIAL_FRAMES,
    COMPTEUR_INITIAL_LIVRAISONS,
    DIRECTION_INITIALE_NULLE,
    DISTANCE_MIN_SECURITE_VOITURE,
    DISTANCE_NULLE,
    ETAT_VOITURE_A_LA_MAISON,
    ETAT_VOITURE_ALLER_USINE,
    ETAT_VOITURE_RETOUR_MAISON,
    INDICE_PREMIERE_ETAPE_ITINERAIRE,
    INTERVALLE_DEMANDE_USINE,
    LONGUEUR_MINIMALE_ITINERAIRE,
    NB_VOITURES_PAR_MAISON,
    PAS_INCREMENT_COMPTEUR,
    SEUIL_ARRIVEE_ETAPE,
    SEUIL_CRITIQUE_DEMANDES_USINE,
    SEUIL_MEME_DIRECTION,
    VITESSE_VOITURE,
)


class Maison:
    """Représente une maison dotée d'une flotte fixe de voitures."""

    def __init__(
        self,
        ligne: int,
        colonne: int,
        couleur: tuple[int, int, int],
    ) -> None:
        """Initialise une maison avec ses coordonnées, sa couleur et sa flotte.

        Args:
            ligne: Indice de la ligne sur la grille.
            colonne: Indice de la colonne sur la grille.
            couleur: Tuple RGB représentant la couleur de la maison.
        """
        self.ligne: int = ligne
        self.colonne: int = colonne
        self.couleur: tuple[int, int, int] = couleur
        self.flotte_voitures: list[Voiture] = []
        for _ in range(NB_VOITURES_PAR_MAISON):
            voiture_maison: Voiture = Voiture(maison_origine=self)
            self.flotte_voitures.append(voiture_maison)

    def obtenir_coordonnee_grille(self) -> tuple[int, int]:
        """Retourne la coordonnée (colonne, ligne) de la maison.

        Returns:
            Un tuple (colonne, ligne).
        """
        return (self.colonne, self.ligne)

    def obtenir_voiture_disponible(self) -> "Voiture | None":
        """Retourne une voiture actuellement garée à la maison si disponible.

        Returns:
            Une instance de Voiture disponible, ou None si toutes sont dehors.
        """
        for voiture in self.flotte_voitures:
            if voiture.etat == ETAT_VOITURE_A_LA_MAISON:
                return voiture
            else:
                pass
        return None

    def compter_voitures_disponibles(self) -> int:
        """Compte le nombre de voitures actuellement garées à la maison.

        Returns:
            Nombre entier de voitures dans l'état ETAT_VOITURE_A_LA_MAISON.
        """
        nb_disponibles: int = COMPTEUR_INITIAL_FRAMES
        for voiture in self.flotte_voitures:
            if voiture.etat == ETAT_VOITURE_A_LA_MAISON:
                nb_disponibles = nb_disponibles + PAS_INCREMENT_COMPTEUR
            else:
                pass
        return nb_disponibles


class Usine:
    """Représente une usine générant périodiquement des demandes."""

    def __init__(
        self,
        ligne: int,
        colonne: int,
        couleur: tuple[int, int, int],
    ) -> None:
        """Initialise une usine avec ses coordonnées, sa couleur et ses demandes.

        Args:
            ligne: Indice de la ligne sur la grille.
            colonne: Indice de la colonne sur la grille.
            couleur: Tuple RGB représentant la couleur de l'usine.
        """
        self.ligne: int = ligne
        self.colonne: int = colonne
        self.couleur: tuple[int, int, int] = couleur
        self.voitures_recues: int = COMPTEUR_INITIAL_LIVRAISONS
        self.demandes_actives: int = COMPTEUR_INITIAL_DEMANDES
        self.demandes_assignees: int = COMPTEUR_INITIAL_DEMANDES
        self.compteur_generation_demande: int = COMPTEUR_INITIAL_FRAMES

    def obtenir_coordonnee_grille(self) -> tuple[int, int]:
        """Retourne la coordonnée (colonne, ligne) de l'usine.

        Returns:
            Un tuple (colonne, ligne).
        """
        return (self.colonne, self.ligne)

    def mettre_a_jour_demandes(self) -> None:
        """Incrémente le timer et génère une nouvelle demande périodiquement."""
        self.compteur_generation_demande = (
            self.compteur_generation_demande + PAS_INCREMENT_COMPTEUR
        )
        if self.compteur_generation_demande >= INTERVALLE_DEMANDE_USINE:
            self.compteur_generation_demande = COMPTEUR_INITIAL_FRAMES
            self.demandes_actives = (
                self.demandes_actives + PAS_INCREMENT_COMPTEUR
            )
        else:
            pass

    def obtenir_demandes_non_assignees(self) -> int:
        """Retourne le nombre de demandes actives sans voiture assignée.

        Returns:
            Entier supérieur ou égal à zéro.
        """
        ecart_demandes: int = self.demandes_actives - self.demandes_assignees
        if ecart_demandes > COMPTEUR_INITIAL_DEMANDES:
            return ecart_demandes
        else:
            return COMPTEUR_INITIAL_DEMANDES

    def a_demande_non_assignee(self) -> bool:
        """Indique si l'usine attend l'envoi d'au moins une voiture.

        Returns:
            True s'il existe au moins une demande non assignée, False sinon.
        """
        if self.obtenir_demandes_non_assignees() > COMPTEUR_INITIAL_DEMANDES:
            return True
        else:
            return False

    def assigner_voiture(self) -> None:
        """Réserve une demande active pour une voiture qui prend la route."""
        self.demandes_assignees = (
            self.demandes_assignees + PAS_INCREMENT_COMPTEUR
        )

    def liberer_assignation(self) -> None:
        """Annule l'assignation d'une voiture qui ne peut plus rejoindre l'usine."""
        if self.demandes_assignees > COMPTEUR_INITIAL_DEMANDES:
            self.demandes_assignees = (
                self.demandes_assignees - PAS_INCREMENT_COMPTEUR
            )
        else:
            self.demandes_assignees = COMPTEUR_INITIAL_DEMANDES

    def enregistrer_livraison(self) -> None:
        """Valide la livraison d'une voiture et consomme une demande active."""
        self.voitures_recues = (
            self.voitures_recues + PAS_INCREMENT_COMPTEUR
        )
        if self.demandes_actives > COMPTEUR_INITIAL_DEMANDES:
            self.demandes_actives = (
                self.demandes_actives - PAS_INCREMENT_COMPTEUR
            )
        else:
            self.demandes_actives = COMPTEUR_INITIAL_DEMANDES

        if self.demandes_assignees > COMPTEUR_INITIAL_DEMANDES:
            self.demandes_assignees = (
                self.demandes_assignees - PAS_INCREMENT_COMPTEUR
            )
        else:
            self.demandes_assignees = COMPTEUR_INITIAL_DEMANDES

    def est_saturee(self) -> bool:
        """Vérifie si l'usine a atteint le seuil critique de défaite.

        Returns:
            True si demandes_actives >= SEUIL_CRITIQUE_DEMANDES_USINE,
            False sinon.
        """
        if self.demandes_actives >= SEUIL_CRITIQUE_DEMANDES_USINE:
            return True
        else:
            return False


class Voiture:
    """Représente un véhicule autonome effectuant des allers-retours."""

    def __init__(
        self,
        maison_origine: Maison,
        usine_cible: Usine | None = None,
        itineraire: list[tuple[int, int]] | None = None,
    ) -> None:
        """Initialise une voiture rattachée à sa maison d'origine.

        Args:
            maison_origine: Maison propriétaire de la voiture.
            usine_cible: Usine cible optionnelle.
            itineraire: Chemin initial optionnel.
        """
        self.maison_origine: Maison = maison_origine
        self.usine_cible: Usine | None = usine_cible
        self.couleur: tuple[int, int, int] = maison_origine.couleur
        self.position_colonne: float = float(maison_origine.colonne)
        self.position_ligne: float = float(maison_origine.ligne)
        self.direction_colonne: float = DIRECTION_INITIALE_NULLE
        self.direction_ligne: float = DIRECTION_INITIALE_NULLE
        self.itineraire: list[tuple[int, int]] = []
        self.indice_etape_cible: int = INDICE_PREMIERE_ETAPE_ITINERAIRE
        self.vitesse: float = VITESSE_VOITURE
        self.etat: int = ETAT_VOITURE_A_LA_MAISON
        self.est_arrivee_destination_etape: bool = False

        if itineraire is not None and usine_cible is not None:
            self.lancer_trajet_aller(usine_cible, itineraire)
        else:
            pass

    def est_en_circulation(self) -> bool:
        """Indique si la voiture est actuellement sur la route (aller ou retour).

        Returns:
            True si la voiture n'est pas garée à la maison, False sinon.
        """
        if self.etat != ETAT_VOITURE_A_LA_MAISON:
            return True
        else:
            return False

    def obtenir_case_actuelle(self) -> tuple[int, int]:
        """Retourne la case entière (colonne, ligne) la plus proche.

        Returns:
            Un tuple (colonne, ligne) d'entiers.
        """
        colonne_entiere: int = int(round(self.position_colonne))
        ligne_entiere: int = int(round(self.position_ligne))
        return (colonne_entiere, ligne_entiere)

    def obtenir_coordonnee_destination_actuelle(self) -> tuple[int, int]:
        """Retourne la coordonnée finale visée selon l'état (Usine ou Maison).

        Returns:
            Un tuple (colonne, ligne) du bâtiment de destination.
        """
        if (
            self.etat == ETAT_VOITURE_ALLER_USINE
            and self.usine_cible is not None
        ):
            return self.usine_cible.obtenir_coordonnee_grille()
        else:
            return self.maison_origine.obtenir_coordonnee_grille()

    def obtenir_prochaine_case_cible(self) -> tuple[int, int]:
        """Retourne la prochaine case (colonne, ligne) visée sur l'itinéraire.

        Returns:
            La coordonnée (colonne, ligne) de l'étape cible courante.
        """
        if self.indice_etape_cible < len(self.itineraire):
            return self.itineraire[self.indice_etape_cible]
        else:
            return self.obtenir_coordonnee_destination_actuelle()

    def actualiser_vecteur_direction(self) -> None:
        """Met à jour le vecteur unitaire de direction vers la prochaine étape."""
        if self.indice_etape_cible < len(self.itineraire):
            cible_colonne, cible_ligne = (
                self.itineraire[self.indice_etape_cible]
            )
            delta_colonne: float = float(cible_colonne) - self.position_colonne
            delta_ligne: float = float(cible_ligne) - self.position_ligne
            norme: float = math.hypot(delta_colonne, delta_ligne)
            if norme > SEUIL_ARRIVEE_ETAPE:
                self.direction_colonne = delta_colonne / norme
                self.direction_ligne = delta_ligne / norme
            else:
                pass
        else:
            pass

    def obtenir_vecteur_decalage_droite(self) -> tuple[float, float]:
        """Calcule le vecteur normal unitaire pointant à droite de la voiture.

        En coordonnées écran (X vers la droite, Y vers le bas), la rotation
        de +90 degrés vers la droite d'un vecteur (dx, dy) est (-dy, dx).

        Returns:
            Un tuple (decalage_x, decalage_y) pour placer la voiture à droite.
        """
        decalage_x: float = -self.direction_ligne
        decalage_y: float = self.direction_colonne
        return (decalage_x, decalage_y)

    def mettre_a_jour_itineraire(
        self,
        nouvel_itineraire: list[tuple[int, int]],
    ) -> None:
        """Affecte un nouvel itinéraire et ajuste l'indice de la prochaine case.

        Args:
            nouvel_itineraire: Liste ordonnée des coordonnées (col, lig).
        """
        self.itineraire = list(nouvel_itineraire)
        self.est_arrivee_destination_etape = False
        if len(self.itineraire) >= LONGUEUR_MINIMALE_ITINERAIRE:
            self.indice_etape_cible = INDICE_PREMIERE_ETAPE_ITINERAIRE
            self.actualiser_vecteur_direction()
        else:
            self.indice_etape_cible = COMPTEUR_INITIAL_FRAMES

    def lancer_trajet_aller(
        self,
        usine_cible: Usine,
        itineraire: list[tuple[int, int]],
    ) -> None:
        """Démarre un trajet aller depuis la maison vers l'usine cible.

        Args:
            usine_cible: Instance de Usine à livrer.
            itineraire: Chemin A* de la maison vers l'usine.
        """
        self.position_colonne = float(self.maison_origine.colonne)
        self.position_ligne = float(self.maison_origine.ligne)
        self.usine_cible = usine_cible
        self.etat = ETAT_VOITURE_ALLER_USINE
        self.mettre_a_jour_itineraire(itineraire)

    def lancer_trajet_retour(
        self,
        itineraire_retour: list[tuple[int, int]],
    ) -> None:
        """Démarre le trajet retour depuis l'usine vers la maison d'origine.

        Args:
            itineraire_retour: Chemin A* de l'usine vers la maison.
        """
        if self.usine_cible is not None:
            self.position_colonne = float(self.usine_cible.colonne)
            self.position_ligne = float(self.usine_cible.ligne)
        else:
            pass
        self.etat = ETAT_VOITURE_RETOUR_MAISON
        self.mettre_a_jour_itineraire(itineraire_retour)

    def garer_a_la_maison(self) -> None:
        """Remet la voiture en stationnement disponible dans sa maison."""
        self.position_colonne = float(self.maison_origine.colonne)
        self.position_ligne = float(self.maison_origine.ligne)
        self.direction_colonne = DIRECTION_INITIALE_NULLE
        self.direction_ligne = DIRECTION_INITIALE_NULLE
        self.usine_cible = None
        self.itineraire = []
        self.indice_etape_cible = COMPTEUR_INITIAL_FRAMES
        self.etat = ETAT_VOITURE_A_LA_MAISON
        self.est_arrivee_destination_etape = False

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

    def circule_dans_meme_sens(self, autre_voiture: "Voiture") -> bool:
        """Vérifie si une autre voiture circule dans la même direction.

        Deux voitures en sens opposé sur une route à double sens ont un
        produit scalaire négatif et ne se bloquent jamais.

        Args:
            autre_voiture: Autre véhicule en circulation.

        Returns:
            True si les deux véhicules vont dans le même sens, False sinon.
        """
        produit_scalaire: float = (
            self.direction_colonne * autre_voiture.direction_colonne
            + self.direction_ligne * autre_voiture.direction_ligne
        )
        if produit_scalaire > SEUIL_MEME_DIRECTION:
            return True
        else:
            return False

    def est_bloquee_par_trafic(
        self,
        autres_voitures: list["Voiture"],
    ) -> bool:
        """Vérifie si une voiture allant dans le même sens bloque la voie.

        Args:
            autres_voitures: Liste de toutes les voitures en circulation.

        Returns:
            True si la voiture doit s'arrêter, False si sa voie est libre.
        """
        if not self.est_en_circulation():
            return False
        else:
            pass

        if self.indice_etape_cible >= len(self.itineraire):
            return False
        else:
            pass

        self.actualiser_vecteur_direction()
        prochaine_case: tuple[int, int] = self.obtenir_prochaine_case_cible()
        cible_colonne_float: float = float(prochaine_case[0])
        cible_ligne_float: float = float(prochaine_case[1])
        ma_distance_vers_cible: float = self.calculer_distance_vers_point(
            cible_colonne_float,
            cible_ligne_float,
        )

        for autre_voiture in autres_voitures:
            if (
                autre_voiture is self
                or not autre_voiture.est_en_circulation()
                or autre_voiture.est_arrivee_destination_etape
            ):
                continue
            else:
                pass

            if not self.circule_dans_meme_sens(autre_voiture):
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

            if autre_occupe_cible or autre_vise_meme_cible:
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
                pass

        return False

    def avancer(self, autres_voitures: list["Voiture"]) -> None:
        """Déplace la voiture d'un pas sur sa voie de droite si elle est libre.

        Args:
            autres_voitures: Liste des voitures actives pour gérer le trafic.
        """
        if not self.est_en_circulation():
            return
        else:
            pass

        if self.est_arrivee_destination_etape:
            return
        else:
            pass

        if len(self.itineraire) < LONGUEUR_MINIMALE_ITINERAIRE:
            return
        else:
            pass

        if self.indice_etape_cible >= len(self.itineraire):
            self.est_arrivee_destination_etape = True
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

        if distance_restante > SEUIL_ARRIVEE_ETAPE:
            self.direction_colonne = delta_colonne / distance_restante
            self.direction_ligne = delta_ligne / distance_restante
        else:
            pass

        if distance_restante <= self.vitesse + SEUIL_ARRIVEE_ETAPE:
            self.position_colonne = cible_colonne
            self.position_ligne = cible_ligne
            self.indice_etape_cible = (
                self.indice_etape_cible + PAS_INCREMENT_COMPTEUR
            )
            if self.indice_etape_cible >= len(self.itineraire):
                self.est_arrivee_destination_etape = True
            else:
                self.est_arrivee_destination_etape = False
                self.actualiser_vecteur_direction()
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
