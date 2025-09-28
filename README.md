# Erdlinge Scripts - PDF-Verarbeitungstool

Dieses Repository enthält Skripte zur Verarbeitung verschiedener Arten von PDF-Dokumenten im Zusammenhang mit Lohnabrechnung und Erstattungen.

## Funktionen

- **AAG Erstattungen**: Verarbeitung von AAG-Erstattungs-PDFs und Generierung von CSV-Berichten mit U1/U2-Daten
- **Abrechnungen**: Verarbeitung von Lohnabrechnung-PDFs und Generierung von Excel-Berichten mit Zulagen, Arbeitszeiten und Gehaltsgruppen
- **AG Belastung**: Verarbeitung von Arbeitgeberbelastung-PDFs und Generierung von Excel-Berichten mit Kostenaufschlüsselungen
- **Lohnjournal**: Verarbeitung von Lohnjournal-PDFs und Generierung von Excel-Berichten mit Bruttolohndaten

## Installation

### Einfache Installation
```bash
pip install -r requirements.txt
```

## Nutzung

### 1. Standalone-Anwendung (Empfohlen für Endbenutzer)

**Ausführbare Datei erstellen:**
```bash
# Windows
build.bat

# Linux/macOS  
./build.sh
```

**Anwendung starten:**
- **Windows**: Doppelklick auf `dist/ErdlingeScripts.exe`
- **Linux/macOS**: `./dist/ErdlingeScripts` ausführen

Die Anwendung öffnet sich automatisch im Standard-Webbrowser.

### 2. Web-Interface (Für Entwickler)

```bash
# Standalone-Version (zufälliger Port + automatischer Browser-Start)
python standalone_app.py

# Entwickler-Version (fester Port 7860)
python gradio_app.py
```

### 3. Kommandozeilen-Skripte (Original-Funktionalität)

```bash
python aag_erstattungen.py
python abrechnungen.py
python ag_belastung.py
python lohnjournal.py
```

## Dateistruktur

Die Skripte erwarten folgende Verzeichnisstruktur:

```
aag_erstattungen/2024/*.pdf
abrechnungen/2024/*.pdf
ag_belastung/2024/Jan-Dez.pdf
lohnjournal/12.2024.pdf
```

## Ausgabedateien

- **AAG Erstattungen**: `AAG_Erstattungen_2024.csv`
- **Abrechnungen**: `abrechnungen_2024.xlsx`
- **AG Belastung**: `ag_belastung_2024_DEZ.xlsx`
- **Lohnjournal**: `lohnjournal_2024.xlsx`

## Funktionsweise

### Gemeinsame Kernlogik
- Alle Interfaces (CLI, Web, Standalone) nutzen identische Verarbeitungsfunktionen aus `core_logic.py`
- Gewährleistet konsistente Ergebnisse zwischen allen Nutzungsarten
- Bug-Fixes profitieren automatisch von allen Interfaces

### PDF-Verarbeitung
- Verwendet Apache Tika für Textextraktion
- Verarbeitet strukturierte deutsche Lohnabrechnung-Daten
- Unterstützt deutsche Zahlenformate (Komma als Dezimaltrennzeichen)

### Ausgabeformate
- **CSV**: Semicolon-getrennt (deutscher Standard)
- **Excel**: Mehrere Arbeitsblätter mit deutschen Spaltenüberschriften
- **Deutsche Zahlenformatierung**: Komma als Dezimaltrennzeichen

## Architektur

### Vereinfachte Struktur
- **Standalone-App**: Browser-basierte Anwendung mit automatischem Browser-Start
- **Web-Interface**: Gradio-basierte Benutzeroberfläche mit Tabbed Layout
- **CLI-Skripte**: Original-Kommandozeilen-Funktionalität (unverändert)
- **Kernlogik**: Geteilte Verarbeitungsfunktionen in `core_logic.py`

### Vorteile
- **Einfachheit**: Keine komplexen GUI-Abhängigkeiten
- **Zuverlässigkeit**: Browser-basierter Ansatz funktioniert universell
- **Wartbarkeit**: Einheitlicher Code-Pfad für alle Interfaces
- **Benutzerfreundlichkeit**: Automatischer Browser-Start für optimale Benutzererfahrung

## Unterstützte Plattformen

- **Windows**: .exe-Datei
- **Linux**: Standalone-Binary
- **macOS**: Standalone-Anwendung
- **WSL2**: Vollständige Unterstützung ohne zusätzliche Konfiguration

## Fehlerbehebung

### Build-Probleme
- **PyInstaller nicht gefunden**: `pip install pyinstaller`
- **Build schlägt fehl**: Stelle sicher, dass alle Abhängigkeiten installiert sind

### Laufzeit-Probleme  
- **Anwendung startet nicht**: Von Kommandozeile starten für Fehlermeldungen
- **Browser öffnet nicht automatisch**: Manuell die angezeigte URL im Browser öffnen
- **Port bereits belegt**: Anwendung findet automatisch freien Port

## Entwicklung

### Projekt-Setup
```bash
git clone <repository>
cd erdlinge-scripts
pip install -r requirements.txt
```

### Tests
```bash
# Web-Interface testen
python gradio_app.py

# Standalone-Version testen  
python standalone_app.py

# CLI-Skripte testen (mit entsprechenden PDF-Dateien)
python aag_erstattungen.py
```

### Neue Funktionen hinzufügen
1. Erweitere `core_logic.py` mit neuen Verarbeitungsfunktionen
2. Aktualisiere `gradio_app.py` und `standalone_app.py` für Web-Interface
3. Erstelle entsprechende CLI-Skripte falls benötigt
4. Teste alle Interfaces

## Beitragen

Bei Fehlern oder Verbesserungsvorschlägen bitte Issues erstellen oder Pull Requests einreichen. Alle Änderungen sollten:
- Deutsche Lokalisierung beibehalten
- CLI-Kompatibilität bewahren
- Einheitliche Verarbeitungsergebnisse sicherstellen
- Dokumentation aktualisieren