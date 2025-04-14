# Fonction de nettoyage pour terminer tous les processus quand on fait CTRL+C
cleanup() {
    echo "Arrêt des processus..."
    kill 0  # Tue tous les processus du même groupe
    exit
}

# Intercepte le CTRL+C (SIGINT)
trap cleanup SIGINT

rasa run --enable-api --cors="*" & 
rasa run actions & 
python -m http.server 8000 &

wait
