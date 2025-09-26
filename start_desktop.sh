#!/bin/bash

echo "========================================"
echo " Erdlinge Scripts - Desktop Application"
echo "========================================"
echo
echo "Starte native Desktop-Anwendung..."
echo

python3 desktop_app.py

if [ $? -ne 0 ]; then
    echo
    echo "Fehler beim Starten der Anwendung!"
    echo "Stellen Sie sicher, dass Python 3 und PyWebView installiert sind."
    echo "Installieren Sie PyWebView mit: pip install pywebview"
    echo
    read -p "Drücken Sie Enter zum Beenden..."
fi