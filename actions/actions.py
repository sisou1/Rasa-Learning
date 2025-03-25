from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import sqlite3

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
        return "action_obtenir_menu_du_jour"  # Nom de l'action pour récupérer le menu du jour

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
