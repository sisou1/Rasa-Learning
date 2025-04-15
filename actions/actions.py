from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import sqlite3
import random
from rasa_sdk.events import SlotSet

DB_PATH = "actions/restaurant.db"

MAX_CAPACITY = 25

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

        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        cursor.execute("SELECT date, menu FROM daily_menu WHERE date = DATE('now')")
        menu_du_jour = cursor.fetchone()

        conn.close()

        if menu_du_jour:
            message = f"Menu du jour ({menu_du_jour[0]}) :\n{menu_du_jour[1]}"
        else:
            message = "Désolé, il n'y a pas de menu du jour disponible."

        dispatcher.utter_message(text=message)

        return []

class ActionVerification(Action):
    def name(self) -> Text:
        return "action_verification"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        date = tracker.get_slot("date_reservation")
        nombre = tracker.get_slot("nombre_personne")

        try:
            nombre = int(nombre)
        except (TypeError, ValueError):
            dispatcher.utter_message(text="Je n'ai pas compris le nombre de personnes.")
            return []

        # Vérification de la capacité totale pour la date donnée
        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            cursor.execute("""
                SELECT SUM(guests) FROM reservations WHERE date_time = ?
            """, (date,))
            total_reservations = cursor.fetchone()[0] or 0
            conn.close()

            if total_reservations + nombre > MAX_CAPACITY:
                dispatcher.utter_message(
                    text=f"Désolé, il n'y a plus assez de place pour {nombre} personnes à cette date. "
                )
                return []

        except Exception as e:
            print(">>> Erreur lors de la vérification des réservations :", e)
            dispatcher.utter_message(text="Une erreur est survenue lors de la vérification des disponibilités.")
            return []

        dispatcher.utter_message(text=f"Donc, pour le {date} pour {nombre} personnes, c’est bien ça ?")
        return []

class ActionReservation(Action):
    def name(self) -> Text:
        return "action_reservation"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        date = tracker.get_slot("date_reservation")
        nombre = tracker.get_slot("nombre_personne")
        nom = tracker.get_slot("nom_reservation")
        telephone = tracker.get_slot("numero_de_telephone")

        booking_number = f"RES{random.randint(1000, 9999)}"

        # Enregistrement en base de données
        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO reservations (name, phone, guests, date_time, comment, booking_number)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (nom, telephone, nombre, date, "", booking_number))
            conn.commit()
            conn.close()
            print(f">>> Réservation insérée avec succès : {booking_number}")
        except Exception as e:
            print(">>> Erreur lors de l'enregistrement :", e)
            dispatcher.utter_message(text="Une erreur est survenue lors de l'enregistrement de votre réservation.")
            return []

        dispatcher.utter_message(
            text=f"Merci {nom}. Votre réservation pour le {date} pour {nombre} personnes a été enregistrée.\n"
                 f"Nous vous contacterons au {telephone} si besoin.\n"
                 f"Voici votre code de réservation : {booking_number}"
        )

        return [SlotSet("code_reservation", booking_number)]

class ActionAnnulerReservation(Action):
    def name(self) -> Text:
        return "action_annuler_reservation"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # Logique pour annuler la réservation
        dispatcher.utter_message(text="Votre réservation a bien été annulée.")
        return []

class ActionAfficherReservation(Action):
    def name(self) -> Text:
        return "action_afficher_reservation"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        code = tracker.get_slot("code_reservation")

        if not code:
            dispatcher.utter_message(text="Je n'ai pas reçu de code de réservation.")
            return []

        try:
            conn = sqlite3.connect(DB_PATH)  # Change si ton chemin est différent
            cursor = conn.cursor()

            cursor.execute("""
                SELECT name, phone, guests, date_time, comment
                FROM reservations
                WHERE booking_number = ?
            """, (code,))

            result = cursor.fetchone()
            conn.close()

            if result:
                name, phone, guests, date_time, comment = result
                message = (
                    f"Voici les détails de la réservation :\n"
                    f"👤 Nom : {name}\n"
                    f"📞 Téléphone : {phone}\n"
                    f"👥 Nombre de personnes : {guests}\n"
                    f"📅 Date et heure : {date_time}\n"
                )
                if comment:
                    message += f"📝 Commentaire : {comment}"
                dispatcher.utter_message(text=message)
            else:
                dispatcher.utter_message(text="Aucune réservation trouvée avec ce code.")

        except Exception as e:
            dispatcher.utter_message(text=f"Erreur lors de la recherche : {str(e)}")

        return []