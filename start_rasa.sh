source ./venv/bin/activate

rasa run --enable-api --cors="*" & 
rasa run actions & 
python -m http.server 8000 &