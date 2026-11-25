"""Contrôleur orchestrant la simulation du trafic, des demandes et du score."""

import math
import random

from src.config import (
    COMPTEUR_INITIAL_FRAMES,
    COMPTEUR_INITIAL_LIVRAISONS,
    DELAI_APPARITION_INITIALE_PAIRE,
    DISTANCE_MIN_SECURITE_VOITURE,
    ETAT_VOITURE_ALLER_USINE,
    ETAT_VOITURE_RETOUR_MAISON,
    FACTEUR_ACCELERATION_APPARITION,
    INTERVALLE_INITIAL_APPARITION_BATIMENT,
    INTERVALLE_MINIMUM_APPARITION_BATIMENT,
    LONGUEUR_LISTE_VIDE,
    LONGUEUR_MINIMALE_ITINERAIRE,
    PALETTE_COULEURS_BATIMENTS,
    PAS_INCREMENT_COMPTEUR,
    PROBABILITE_MAISON_SEULE,
)
from src.models.entity import Maison, Usine, Voiture
from src.models.grid import Grid
from src.models.pathfinding import trouver_chemin_a_etoile


class GameEngine:
    """Orchestre l'apparition procédurale, les demandes, le trafic et le score."""

    def __init__(self, grille: Grid) -> None:
        """Initialise le moteur de simulation avec la grille du jeu.

        Args:
            grille: Instance du modèle Grid contenant bâtiments et routes.
        """
        self.grille: Grid = grille
        self.voitures: list[Voiture] = []
        self.compteur_apparition_batiment: int = COMPTEUR_INITIAL_FRAMES
        self.intervalle_apparition_batiment: int = (
            DELAI_APPARITION_INITIALE_PAIRE
        )
        self.premiere_paire_apparue: bool = False
        self.score: int = COMPTEUR_INITIAL_LIVRAISONS
        self.partie_perdue: bool = False

    def choisir_case_libre_aleatoire(self) -> tuple[int, int] | None:
        """Sélectionne aléatoirement une case libre valide sur la grille.

        Returns:
            Un tuple (ligne, colonne) libre, ou None si la grille est pleine.
        """
        cases_disponibles: list[tuple[int, int]] = (
            self.grille.obtenir_cases_libres_pour_apparition()
        )
        if len(cases_disponibles) > LONGUEUR_LISTE_VIDE:
            case_choisie: tuple[int, int] = random.choice(cases_disponibles)
            return case_choisie
        else:
            return None

    def obtenir_couleurs_usines_actives(self) -> list[tuple[int, int, int]]:
        """Retourne la liste des couleurs des usines présentes sur la carte.

        Returns:
            Liste de tuples RGB correspondant aux usines existantes.
        """
        couleurs_actives: list[tuple[int, int, int]] = []
        for usine in self.grille.usines:
            if usine.couleur not in couleurs_actives:
                couleurs_actives.append(usine.couleur)
            else:
                pass
        return couleurs_actives

    def choisir_couleur_nouvelle_paire(self) -> tuple[int, int, int]:
        """Choisit aléatoirement une couleur de la palette pour une paire.

        Permet aussi bien l'apparition d'une nouvelle couleur que d'une
        nouvelle usine d'une couleur déjà présente sur la carte.

        Returns:
            Un tuple RGB issu de PALETTE_COULEURS_BATIMENTS.
        """
        return random.choice(PALETTE_COULEURS_BATIMENTS)

    def faire_apparaitre_maison_isolee(
        self,
        couleur: tuple[int, int, int],
    ) -> bool:
        """Fait apparaître une maison seule sur une case libre aléatoire.

        Args:
            couleur: Couleur RGB de la maison (rattachée à une usine active).

        Returns:
            True si la maison a pu être placée, False sinon.
        """
        case_maison: tuple[int, int] | None = (
            self.choisir_case_libre_aleatoire()
        )
        if case_maison is not None:
            ligne_maison, colonne_maison = case_maison
            nouvelle_maison: Maison = Maison(
                ligne_maison,
                colonne_maison,
                couleur,
            )
            return self.grille.placer_maison(nouvelle_maison)
        else:
            return False

    def faire_apparaitre_paire_maison_usine(
        self,
        couleur: tuple[int, int, int],
    ) -> bool:
        """Fait apparaître une paire (1 Usine + 1 Maison) de même couleur.

        Args:
            couleur: Couleur RGB commune à la maison et à l'usine.

        Returns:
            True si la paire a pu être placée, False sinon.
        """
        case_usine: tuple[int, int] | None = (
            self.choisir_case_libre_aleatoire()
        )
        if case_usine is None:
            return False
        else:
            pass

        ligne_usine, colonne_usine = case_usine
        nouvelle_usine: Usine = Usine(ligne_usine, colonne_usine, couleur)
        usine_placee: bool = self.grille.placer_usine(nouvelle_usine)

        if not usine_placee:
            return False
        else:
            pass

        maison_placee: bool = self.faire_apparaitre_maison_isolee(couleur)
        return maison_placee

    def reduire_intervalle_apparition(self) -> None:
        """Accélère progressivement la fréquence d'apparition des bâtiments."""
        if not self.premiere_paire_apparue:
            self.premiere_paire_apparue = True
            self.intervalle_apparition_batiment = (
                INTERVALLE_INITIAL_APPARITION_BATIMENT
            )
        else:
            nouvel_intervalle: int = int(
                self.intervalle_apparition_batiment
                * FACTEUR_ACCELERATION_APPARITION
            )
            if nouvel_intervalle < INTERVALLE_MINIMUM_APPARITION_BATIMENT:
                self.intervalle_apparition_batiment = (
                    INTERVALLE_MINIMUM_APPARITION_BATIMENT
                )
            else:
                self.intervalle_apparition_batiment = nouvel_intervalle

    def gerer_apparition_procedurale_batiments(self) -> None:
        """Gère le cycle d'apparition procédurale des Maisons et Usines."""
        if len(self.grille.usines) > LONGUEUR_LISTE_VIDE:
            self.premiere_paire_apparue = True
        else:
            pass

        self.compteur_apparition_batiment = (
            self.compteur_apparition_batiment + PAS_INCREMENT_COMPTEUR
        )

        if (
            self.compteur_apparition_batiment
            < self.intervalle_apparition_batiment
        ):
            return
        else:
            self.compteur_apparition_batiment = COMPTEUR_INITIAL_FRAMES

        couleurs_actives: list[tuple[int, int, int]] = (
            self.obtenir_couleurs_usines_actives()
        )
        aucune_usine_active: bool = (
            len(couleurs_actives) == LONGUEUR_LISTE_VIDE
        )

        if aucune_usine_active:
            couleur_initiale: tuple[int, int, int] = (
                self.choisir_couleur_nouvelle_paire()
            )
            self.faire_apparaitre_paire_maison_usine(couleur_initiale)
            self.reduire_intervalle_apparition()
        else:
            tirage_aleatoire: float = random.random()
            if tirage_aleatoire < PROBABILITE_MAISON_SEULE:
                couleur_existante: tuple[int, int, int] = random.choice(
                    couleurs_actives
                )
                self.faire_apparaitre_maison_isolee(couleur_existante)
            else:
                couleur_paire: tuple[int, int, int] = (
                    self.choisir_couleur_nouvelle_paire()
                )
                self.faire_apparaitre_paire_maison_usine(couleur_paire)
            self.reduire_intervalle_apparition()

    def mettre_a_jour_demandes_usines(self) -> None:
        """Génère les demandes des usines et vérifie la condition de défaite."""
        for usine in self.grille.usines:
            usine.mettre_a_jour_demandes()
            if usine.est_saturee():
                self.partie_perdue = True
            else:
                pass

    def est_sortie_maison_degagee(self, maison: Maison) -> bool:
        """Vérifie qu'aucune voiture n'occupe déjà la sortie de la maison.

        Args:
            maison: Instance de Maison souhaitant envoyer une voiture.

        Returns:
            True si aucune voiture en route n'est trop proche, False sinon.
        """
        maison_colonne: float = float(maison.colonne)
        maison_ligne: float = float(maison.ligne)

        for voiture in self.voitures:
            if voiture.etat == ETAT_VOITURE_ALLER_USINE:
                delta_colonne: float = (
                    voiture.position_colonne - maison_colonne
                )
                delta_ligne: float = voiture.position_ligne - maison_ligne
                distance: float = math.hypot(delta_colonne, delta_ligne)
                if distance < DISTANCE_MIN_SECURITE_VOITURE:
                    return False
                else:
                    pass
            else:
                pass

        return True

    def trouver_maison_disponible_pour_usine(
        self,
        usine: Usine,
    ) -> tuple[Maison | None, Voiture | None, list[tuple[int, int]]]:
        """Cherche la maison compatible la plus proche ayant une voiture libre.

        Args:
            usine: Instance de Usine ayant une demande non assignée.

        Returns:
            Un tuple (maison, voiture, itineraire) ou (None, None, []).
        """
        meilleure_maison: Maison | None = None
        meilleure_voiture: Voiture | None = None
        meilleur_itineraire: list[tuple[int, int]] = []
        coordonnee_usine: tuple[int, int] = usine.obtenir_coordonnee_grille()

        for maison in self.grille.maisons:
            if maison.couleur == usine.couleur:
                voiture_libre: Voiture | None = (
                    maison.obtenir_voiture_disponible()
                )
                if (
                    voiture_libre is not None
                    and self.est_sortie_maison_degagee(maison)
                ):
                    coordonnee_maison: tuple[int, int] = (
                        maison.obtenir_coordonnee_grille()
                    )
                    chemin_candidat: list[tuple[int, int]] = (
                        trouver_chemin_a_etoile(
                            self.grille,
                            coordonnee_maison,
                            coordonnee_usine,
                        )
                    )
                    if len(chemin_candidat) >= LONGUEUR_MINIMALE_ITINERAIRE:
                        aucun_trouve: bool = (
                            len(meilleur_itineraire)
                            < LONGUEUR_MINIMALE_ITINERAIRE
                        )
                        if aucun_trouve:
                            meilleure_maison = maison
                            meilleure_voiture = voiture_libre
                            meilleur_itineraire = chemin_candidat
                        else:
                            if len(chemin_candidat) < len(meilleur_itineraire):
                                meilleure_maison = maison
                                meilleure_voiture = voiture_libre
                                meilleur_itineraire = chemin_candidat
                            else:
                                pass
                    else:
                        pass
                else:
                    pass
            else:
                pass

        return (meilleure_maison, meilleure_voiture, meilleur_itineraire)

    def attribuer_demandes_aux_maisons(self) -> None:
        """Envoie les voitures disponibles des maisons vers les usines en demande."""
        for usine in self.grille.usines:
            recherche_possible: bool = True
            while usine.a_demande_non_assignee() and recherche_possible:
                maison_choisie, voiture_choisie, itineraire_aller = (
                    self.trouver_maison_disponible_pour_usine(usine)
                )
                if (
                    maison_choisie is not None
                    and voiture_choisie is not None
                    and len(itineraire_aller) >= LONGUEUR_MINIMALE_ITINERAIRE
                ):
                    usine.assigner_voiture()
                    voiture_choisie.lancer_trajet_aller(
                        usine,
                        itineraire_aller,
                    )
                    self.voitures.append(voiture_choisie)
                else:
                    recherche_possible = False

    def itineraire_restant_est_valide(self, voiture: Voiture) -> bool:
        """Vérifie si toutes les étapes restantes de la voiture existent encore.

        Args:
            voiture: Instance de Voiture à contrôler.

        Returns:
            True si l'itinéraire restant est toujours praticable, False sinon.
        """
        if len(voiture.itineraire) < LONGUEUR_MINIMALE_ITINERAIRE:
            return False
        else:
            pass

        depart_actuel: tuple[int, int] = voiture.obtenir_case_actuelle()
        arrivee_cible: tuple[int, int] = (
            voiture.obtenir_coordonnee_destination_actuelle()
        )

        for indice_etape in range(
            voiture.indice_etape_cible,
            len(voiture.itineraire),
        ):
            case_etape: tuple[int, int] = voiture.itineraire[indice_etape]
            if not self.grille.est_case_traversable(
                case_etape,
                depart_actuel,
                arrivee_cible,
            ):
                return False
            else:
                pass

        return True

    def trouver_itineraire_vers_usine_compatible(
        self,
        coordonnee_depart: tuple[int, int],
        couleur: tuple[int, int, int],
    ) -> tuple[Usine | None, list[tuple[int, int]]]:
        """Cherche n'importe quelle usine de même couleur atteignable via A*.

        Args:
            coordonnee_depart: Coordonnée (colonne, ligne) de départ.
            couleur: Couleur RGB recherchée.

        Returns:
            Un tuple (usine_cible, itineraire) ou (None, []).
        """
        meilleure_usine: Usine | None = None
        meilleur_itineraire: list[tuple[int, int]] = []

        for usine in self.grille.usines:
            if usine.couleur == couleur:
                coordonnee_usine: tuple[int, int] = (
                    usine.obtenir_coordonnee_grille()
                )
                chemin_candidat: list[tuple[int, int]] = (
                    trouver_chemin_a_etoile(
                        self.grille,
                        coordonnee_depart,
                        coordonnee_usine,
                    )
                )
                if len(chemin_candidat) >= LONGUEUR_MINIMALE_ITINERAIRE:
                    aucun_itineraire_trouve: bool = (
                        len(meilleur_itineraire)
                        < LONGUEUR_MINIMALE_ITINERAIRE
                    )
                    if aucun_itineraire_trouve:
                        meilleure_usine = usine
                        meilleur_itineraire = chemin_candidat
                    else:
                        if len(chemin_candidat) < len(meilleur_itineraire):
                            meilleure_usine = usine
                            meilleur_itineraire = chemin_candidat
                        else:
                            pass
                else:
                    pass
            else:
                pass

        return (meilleure_usine, meilleur_itineraire)

    def verifier_et_recalculer_itineraires(self) -> None:
        """Recalcule l'itinéraire aller ou retour si une route a été modifiée."""
        for voiture in self.voitures:
            if not self.itineraire_restant_est_valide(voiture):
                case_actuelle: tuple[int, int] = (
                    voiture.obtenir_case_actuelle()
                )
                if voiture.etat == ETAT_VOITURE_ALLER_USINE:
                    chemin_meme_usine: list[tuple[int, int]] = []
                    if voiture.usine_cible is not None:
                        chemin_meme_usine = trouver_chemin_a_etoile(
                            self.grille,
                            case_actuelle,
                            voiture.usine_cible.obtenir_coordonnee_grille(),
                        )
                    else:
                        pass

                    if len(chemin_meme_usine) >= LONGUEUR_MINIMALE_ITINERAIRE:
                        voiture.mettre_a_jour_itineraire(chemin_meme_usine)
                    else:
                        voiture.mettre_a_jour_itineraire([])
                else:
                    if voiture.etat == ETAT_VOITURE_RETOUR_MAISON:
                        coordonnee_maison: tuple[int, int] = (
                            voiture.maison_origine.obtenir_coordonnee_grille()
                        )
                        chemin_retour: list[tuple[int, int]] = (
                            trouver_chemin_a_etoile(
                                self.grille,
                                case_actuelle,
                                coordonnee_maison,
                            )
                        )
                        if len(chemin_retour) >= LONGUEUR_MINIMALE_ITINERAIRE:
                            voiture.mettre_a_jour_itineraire(chemin_retour)
                        else:
                            voiture.mettre_a_jour_itineraire([])
                    else:
                        pass
            else:
                pass

    def mettre_a_jour_deplacements_et_arrivees(self) -> None:
        """Fait avancer les voitures et gère les transitions Usine -> Maison."""
        voitures_en_route: list[Voiture] = []

        for voiture in self.voitures:
            voiture.avancer(self.voitures)

            if voiture.est_arrivee_destination_etape:
                if voiture.etat == ETAT_VOITURE_ALLER_USINE:
                    if voiture.usine_cible is not None:
                        voiture.usine_cible.enregistrer_livraison()
                        self.score = self.score + PAS_INCREMENT_COMPTEUR
                        depart_retour: tuple[int, int] = (
                            voiture.usine_cible.obtenir_coordonnee_grille()
                        )
                    else:
                        depart_retour = voiture.obtenir_case_actuelle()

                    arrivee_maison: tuple[int, int] = (
                        voiture.maison_origine.obtenir_coordonnee_grille()
                    )
                    itineraire_retour: list[tuple[int, int]] = (
                        trouver_chemin_a_etoile(
                            self.grille,
                            depart_retour,
                            arrivee_maison,
                        )
                    )
                    voiture.lancer_trajet_retour(itineraire_retour)
                    voitures_en_route.append(voiture)
                else:
                    if voiture.etat == ETAT_VOITURE_RETOUR_MAISON:
                        voiture.garer_a_la_maison()
                    else:
                        pass
            else:
                voitures_en_route.append(voiture)

        self.voitures = voitures_en_route

    def mettre_a_jour(self) -> None:
        """Exécute un cycle complet de simulation si la partie est en cours."""
        if self.partie_perdue:
            return
        else:
            pass

        self.gerer_apparition_procedurale_batiments()
        self.mettre_a_jour_demandes_usines()
        if self.partie_perdue:
            return
        else:
            pass

        self.verifier_et_recalculer_itineraires()
        self.attribuer_demandes_aux_maisons()
        self.mettre_a_jour_deplacements_et_arrivees()
