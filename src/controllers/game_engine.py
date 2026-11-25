"""Contrôleur orchestrant la simulation du trafic, du pathfinding et du temps."""

import math

from src.config import (
    DISTANCE_MIN_SECURITE_VOITURE,
    LONGUEUR_MINIMALE_ITINERAIRE,
)
from src.models.entity import Maison, Usine, Voiture
from src.models.grid import Grid
from src.models.pathfinding import trouver_chemin_a_etoile


class GameEngine:
    """Orchestre la génération des voitures, leurs itinéraires et le trafic."""

    def __init__(self, grille: Grid) -> None:
        """Initialise le moteur de simulation avec la grille du jeu.

        Args:
            grille: Instance du modèle Grid contenant bâtiments et routes.
        """
        self.grille: Grid = grille
        self.voitures: list[Voiture] = []

    def trouver_itineraire_vers_usine_compatible(
        self,
        coordonnee_depart: tuple[int, int],
        couleur: tuple[int, int, int],
    ) -> tuple[Usine | None, list[tuple[int, int]]]:
        """Cherche l'usine de même couleur la plus proche via le réseau routier.

        Args:
            coordonnee_depart: Coordonnée (colonne, ligne) de départ.
            couleur: Couleur RGB de la maison ou de la voiture.

        Returns:
            Un tuple (usine_cible, itineraire). Si aucune usine n'est
            accessible, retourne (None, []).
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

    def est_sortie_maison_degagee(self, maison: Maison) -> bool:
        """Vérifie qu'aucune voiture n'occupe déjà la sortie de la maison.

        Args:
            maison: Instance de Maison souhaitant générer une voiture.

        Returns:
            True si aucune voiture n'est trop proche de la maison, False sinon.
        """
        maison_colonne: float = float(maison.colonne)
        maison_ligne: float = float(maison.ligne)

        for voiture in self.voitures:
            delta_colonne: float = voiture.position_colonne - maison_colonne
            delta_ligne: float = voiture.position_ligne - maison_ligne
            distance: float = math.hypot(delta_colonne, delta_ligne)
            if distance < DISTANCE_MIN_SECURITE_VOITURE:
                return False
            else:
                pass

        return True

    def gerer_apparition_voitures(self) -> None:
        """Met à jour les compteurs des maisons et génère les voitures."""
        for maison in self.grille.maisons:
            maison.incrementer_timer_apparition()
            if maison.peut_generer_voiture():
                if self.est_sortie_maison_degagee(maison):
                    coordonnee_maison: tuple[int, int] = (
                        maison.obtenir_coordonnee_grille()
                    )
                    usine_cible, itineraire = (
                        self.trouver_itineraire_vers_usine_compatible(
                            coordonnee_maison,
                            maison.couleur,
                        )
                    )
                    if (
                        usine_cible is not None
                        and len(itineraire) >= LONGUEUR_MINIMALE_ITINERAIRE
                    ):
                        nouvelle_voiture: Voiture = maison.creer_voiture(
                            usine_cible,
                            itineraire,
                        )
                        self.voitures.append(nouvelle_voiture)
                    else:
                        pass
                else:
                    pass
            else:
                pass

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

        depart_initial: tuple[int, int] = (
            voiture.maison_origine.obtenir_coordonnee_grille()
        )
        arrivee_cible: tuple[int, int] = (
            voiture.usine_cible.obtenir_coordonnee_grille()
        )

        for indice_etape in range(
            voiture.indice_etape_cible,
            len(voiture.itineraire),
        ):
            case_etape: tuple[int, int] = voiture.itineraire[indice_etape]
            if not self.grille.est_case_traversable(
                case_etape,
                depart_initial,
                arrivee_cible,
            ):
                return False
            else:
                pass

        return True

    def verifier_et_recalculer_itineraires(self) -> None:
        """Recalcule l'itinéraire des voitures si une route a été modifiée."""
        for voiture in self.voitures:
            if not self.itineraire_restant_est_valide(voiture):
                case_actuelle: tuple[int, int] = (
                    voiture.obtenir_case_actuelle()
                )
                nouvelle_usine, nouvel_itineraire = (
                    self.trouver_itineraire_vers_usine_compatible(
                        case_actuelle,
                        voiture.couleur,
                    )
                )
                if (
                    nouvelle_usine is not None
                    and len(nouvel_itineraire) >= LONGUEUR_MINIMALE_ITINERAIRE
                ):
                    voiture.usine_cible = nouvelle_usine
                    voiture.mettre_a_jour_itineraire(nouvel_itineraire)
                else:
                    voiture.mettre_a_jour_itineraire([])
            else:
                pass

    def mettre_a_jour_deplacements_et_arrivees(self) -> None:
        """Fait avancer les voitures et retire celles arrivées à leur usine."""
        voitures_restantes: list[Voiture] = []

        for voiture in self.voitures:
            voiture.avancer(self.voitures)
            if voiture.est_arrivee:
                voiture.usine_cible.recevoir_voiture(voiture)
            else:
                voitures_restantes.append(voiture)

        self.voitures = voitures_restantes

    def mettre_a_jour(self) -> None:
        """Exécute un cycle complet de simulation pour la frame courante."""
        self.verifier_et_recalculer_itineraires()
        self.gerer_apparition_voitures()
        self.mettre_a_jour_deplacements_et_arrivees()
