from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import sqlite3
import random

DB_PATH = "actions/restaurant.db"

class ActionObtenirAllergenes(Action):
    def name(self) -> Text:
        return "action_obtenir_allergenes"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # Connexion à la base de données SQLite
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        # Récupérer tous les allergènes
        cursor.execute("SELECT ingredient FROM allergens")
        allergenes = cursor.fetchall()

        # Fermer la connexion
        conn.close()

        # Préparer le message à envoyer
        if allergenes:
            allergenes_list = [allergen[0] for allergen in allergenes]
            message = "Les allergènes disponibles sont :\n" + "\n".join(allergenes_list)
        else:
            message = "Aucun allergène disponible."

        # Envoyer la réponse à l'utilisateur
        dispatcher.utter_message(text=message)

        return []

class ActionObtenirMenuDuJour(Action):
    def name(self) -> Text:
        return "action_obtenir_menu_du_jour"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # Connexion à la base de données SQLite
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        # Récupérer le menu du jour
        cursor.execute("SELECT date, menu FROM daily_menu WHERE date = DATE('now')")
        menu_du_jour = cursor.fetchone()

        # Fermer la connexion
        conn.close()

        # Préparer le message à envoyer
        if menu_du_jour:
            message = f"Menu du jour ({menu_du_jour[0]}) :\n{menu_du_jour[1]}"
        else:
            message = "Désolé, il n'y a pas de menu du jour disponible."

        # Envoyer la réponse à l'utilisateur
        dispatcher.utter_message(text=message)

        return []

class ActionVerification(Action):
    def name(self) -> Text:
        return "action_verification"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        date = tracker.get_slot("date")
        nombre = tracker.get_slot("nombre")
        nom = tracker.get_slot("nom")
        telephone = tracker.get_slot("telephone")

        if not all([date, nombre, nom, telephone]):
            dispatcher.utter_message(text="Il manque des informations pour valider la réservation.")
        else:
            booking_number = f"RES{random.randint(1000, 9999)}"
            tracker.slots["booking_number"] = booking_number
            dispatcher.utter_message(text=f"Votre réservation pour le {date} pour {nombre} personnes est confirmée. Votre code de réservation est : {booking_number}")

        return []

class ActionReservation(Action):
    def name(self) -> Text:
        return "action_reservation"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # Logique pour enregistrer la réservation dans la base de données
        return []

class ActionAnnulerReservation(Action):
    def name(self) -> Text:
        return "action_annuler_reservation"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # Logique pour annuler la réservation
        dispatcher.utter_message(text="Votre réservation a bien été annulée.")
        return []

class ActionModifierReservation(Action):
    def name(self) -> Text:
        return "action_modifier_reservation"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # Logique pour modifier la réservation
        dispatcher.utter_message(text="Votre réservation a bien été modifiée.")
        return []
