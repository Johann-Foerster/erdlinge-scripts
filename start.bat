@echo off
title Erdlinge Scripts - PDF Processing Tool

echo.
echo ========================================
echo  Erdlinge Scripts - PDF Processing Tool
echo ========================================
echo.
echo Starte Anwendung...
echo.

python standalone_app.py

if %ERRORLEVEL% neq 0 (
    echo.
    echo Fehler beim Starten der Anwendung!
    echo Stellen Sie sicher, dass Python installiert ist.
    echo.
    pause
)