@echo off
title Erdlinge Scripts - PDF Processing Desktop App

echo.
echo ========================================
echo  Erdlinge Scripts - Desktop Application
echo ========================================
echo.
echo Starte native Desktop-Anwendung...
echo.

python desktop_app.py

if %ERRORLEVEL% neq 0 (
    echo.
    echo Fehler beim Starten der Anwendung!
    echo Stellen Sie sicher, dass Python und PyWebView installiert sind.
    echo Installieren Sie PyWebView mit: pip install pywebview
    echo.
    pause
)