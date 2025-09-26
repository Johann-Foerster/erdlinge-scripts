#!/bin/bash

echo "========================================"
echo " Erdlinge Scripts - PDF Processing Tool"
echo "========================================"
echo
echo "Starte Anwendung..."
echo

python3 standalone_app.py

if [ $? -ne 0 ]; then
    echo
    echo "Fehler beim Starten der Anwendung!"
    echo "Stellen Sie sicher, dass Python 3 installiert ist."
    echo
    read -p "Drücken Sie Enter zum Beenden..."
fi