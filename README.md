# Projet rasa restaurant 

Groupe : Lucas ROGARD et Fabien KIEFER

# Lancer le projet

Cloner le projet

source ./venv/bin/activate

rasa train

chmod +x start_rasa.sh

./start_rasa.sh

attendre bien une minute le dernier message attentu est : **root  - Rasa server is up and running.**

aller sur **localhost:8000**

# Intergration dans un site web

Vidéo source : https://www.youtube.com/watch?v=ZhRo3gfLk90

L'idée viens de Ilyas Hessab, d'ou la ressemblance avec sa version complétement assumé.


# Problème majeur du projet

Il y a un souci évident et connu.

Les stories sont exécuté grâce a une suite de rules et non pas graçe à une suite de rules et non pas grâce à une suite d'une stories.
Si on a fait ça, c'est à cause d'un souci incompris que j'ai abordé rapidement en fin de cours,
Lors d'un appel d'un slot et de l'utilisation d'une action en Python, un fallback s'exécute pour une raison inconnue.
On a beaucoup utilisé Rasa interactive pour résoudre le souci.

## Tests réalisé :

- Rajouter des elements au intent, voir si l'IA comprend bien ce qu'il se passe, avec un RSA shell nlu et un rasa interactive on comprend que ce n'est pas ça
- Config de base de rasa venant de l'installation, sauf que le bug survient même sur d'autres PC avec le même code
- Les slots, le type des données et la compréhension de l'intent donné, sauf que tout est bon lors d'un rasa interactive, on voit bien qu'il comprend bien tout.
- vérifier les actions en elles-mêmes, oui bah j'ai fait plusieurs tests ça n'a rien donné

## Solution utilisé :

Utiliser des rules pour forcer l'action d'après, graçe a ça l'action se fait bien, et aucun fallback ne survient.
On est bien conscient que ce n'est pas optimal mais il fallait bien trouver une solution, même si c'est un bout de scotch, on a fini par faire comme ça pour que ça fonctionne.