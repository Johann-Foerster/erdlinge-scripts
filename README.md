# Erdlinge Scripts - PDF-Verarbeitungstool

Dieses Repository enthält Skripte zur Verarbeitung verschiedener Arten von PDF-Dokumenten im Zusammenhang mit Lohnabrechnung und Erstattungen.

## Funktionen

- **AAG Erstattungen**: Verarbeitung von AAG-Erstattungs-PDFs und Generierung von CSV-Berichten mit U1/U2-Daten
- **Abrechnungen**: Verarbeitung von Lohnabrechnung-PDFs und Generierung von Excel-Berichten mit Zulagen, Arbeitszeiten und Gehaltsgruppen
- **AG Belastung**: Verarbeitung von Arbeitgeberbelastung-PDFs und Generierung von Excel-Berichten mit Kostenaufschlüsselungen
- **Lohnjournal**: Verarbeitung von Lohnjournal-PDFs und Generierung von Excel-Berichten mit Bruttolohndaten

## Installation

### Vollinstallation (Empfohlen)
Für alle Funktionen einschließlich nativer Desktop-Anwendung:
```bash
pip install -r requirements.txt
```

### Minimalinstallation
Nur für CLI und Web-Interface (ohne native Desktop-App):
```bash
pip install -r requirements-minimal.txt
```

### Manuelle Installation der Desktop-Abhängigkeiten
Falls PyWebView-Fehler auftreten:

**Windows/Linux:**
```bash
pip install PyQt5
# Oder: pip install PyQt6
```

**Linux (Alternative mit GTK):**
```bash
sudo apt-get install python3-gi python3-gi-cairo gir1.2-webkit2-4.0
```

**macOS:**
```bash
# Keine zusätzlichen Abhängigkeiten erforderlich
# PyWebView nutzt das System-WebView
pip install pywebview
```

## Verwendung

### Standalone-Anwendung (Empfohlen für Endbenutzer)

Für Benutzer ohne Python-Kenntnisse bieten wir vorgefertigte ausführbare Dateien:

**Verfügbare Downloads:**
- `ErdlingeScriptsDesktop-Windows.exe` - **Native Desktop App** für Windows 10/11
- `ErdlingeScriptsDesktop-MacOS` - **Native Desktop App** für macOS 10.15+  
- `ErdlingeScriptsDesktop-Linux` - **Native Desktop App** für Ubuntu/Debian/CentOS
- `ErdlingeScripts-Windows.exe` - Browser-basierte Version für Windows 10/11
- `ErdlingeScripts-MacOS` - Browser-basierte Version für macOS 10.15+
- `ErdlingeScripts-Linux` - Browser-basierte Version für Ubuntu/Debian/CentOS

**Installation:**
1. Laden Sie die entsprechende Datei für Ihr Betriebssystem herunter
2. Doppelklicken Sie die Datei
3. **Desktop-Version**: Öffnet sich in nativer Desktop-Anwendung
4. **Browser-Version**: Öffnet sich automatisch im Webbrowser
5. Verwenden Sie die benutzerfreundliche Oberfläche zum Hochladen und Verarbeiten von PDF-Dateien

**Vorteile der Desktop-Anwendung:**
- ✅ **Native Desktop-Erfahrung** mit eigenem Fenster
- ✅ **Keine Browser-Abhängigkeit** - funktioniert offline
- ✅ **Bessere Integration** in das Betriebssystem
- ✅ **Professionelles Erscheinungsbild** für Geschäftsumgebungen
- ✅ **Einfachere Dateiverwaltung** mit nativen Dialogen
- ✅ **Keine Python-Installation erforderlich**
- ✅ **Alle Abhängigkeiten sind enthalten**

### Standalone-Anwendung selbst erstellen

Falls Sie die Anwendung selbst kompilieren möchten:

```bash
# Abhängigkeiten installieren (einschließlich PyWebView für native Desktop-App)
pip install -r requirements.txt

# Beide Versionen erstellen:
# Für Windows:
build.bat

# Für Linux/Mac:
chmod +x build.sh
./build.sh
```

**Zwei Build-Ausgaben:**
- `ErdlingeScriptsDesktop` - Native Desktop-Anwendung mit PyWebView
- `ErdlingeScripts` - Browser-basierte Anwendung

### Desktop-Anwendung (Entwickler)

Für die beste Benutzererfahrung mit nativer Desktop-App:

```bash
python desktop_app.py
```

**Oder mit Startskripten:**
```bash
# Windows:
start_desktop.bat

# Linux/Mac:
./start_desktop.sh
```

### Kommandozeilen-Interface (CLI)

Die ursprünglichen CLI-Skripte bleiben erhalten und können wie zuvor verwendet werden:

```bash
# AAG Erstattungen verarbeiten
python aag_erstattungen.py

# Abrechnungen verarbeiten
python abrechnungen.py

# AG Belastung verarbeiten
python ag_belastung.py

# Lohnjournal verarbeiten
python lohnjournal.py
```

Jedes Skript erwartet PDF-Dateien in spezifischen Verzeichnisstrukturen:
- `aag_erstattungen/2024/*.pdf`
- `abrechnungen/2024/*.pdf`
- `ag_belastung/2024/Jan-Dez.pdf`
- `lohnjournal/12.2024.pdf`

### Web-Interface (Entwickler)

Für eine benutzerfreundlichere Erfahrung verwenden Sie das Gradio-Web-Interface:

```bash
python gradio_app.py
```

### Standalone Web-Interface (Automatischer Browser-Start)

Für eine bessere Benutzererfahrung mit automatischer Browser-Öffnung:

```bash
python standalone_app.py
```

Dies startet einen Webserver auf einem zufälligen freien Port und öffnet automatisch Ihren Webbrowser. Sie können:

1. PDF-Dateien über das Web-Interface hochladen
2. Das Jahr für die Verarbeitung angeben
3. Auf den Verarbeitungsbutton klicken
4. Die generierten CSV/Excel-Ergebnisse herunterladen

#### Funktionen des Web-Interfaces:

- **Registerkarten-Interface**: Separate Registerkarten für jeden Dokumenttyp
- **Datei-Upload**: Drag-and-Drop oder Klick zum Hochladen von PDF-Dateien
- **Echtzeitverarbeitung**: Verarbeitungsstatus anzeigen und Ergebnisse sofort herunterladen
- **Mehrere Dateien unterstützt**: Mehrere Dateien hochladen wo unterstützt (AAG, Abrechnungen)
- **Einzeldatei unterstützt**: Einzeldatei hochladen wo erforderlich (AG Belastung, Lohnjournal)

## Dateiformate

### Eingabe
- PDF-Dateien mit den entsprechenden Dokumenttypen

### Ausgabe
- **AAG Erstattungen**: CSV-Datei mit Semikolon-getrennten Werten
- **Abrechnungen**: Excel-Datei mit mehreren Arbeitsblättern für verschiedene Datenkategorien
- **AG Belastung**: Excel-Datei mit Arbeitgeberkostenaufschlüsselung
- **Lohnjournal**: Excel-Datei mit Lohnzusammenfassungsdaten

## Abhängigkeiten

- `gradio` - Web-Interface-Framework
- `tika` - PDF-Textextraktion
- `pandas` - Datenmanipulation und Excel-Export
- `openpyxl` - Excel-Dateibehandlung
- `numpy` - Numerische Berechnungen

## Architektur

Der Code ist strukturiert, um die Wiederverwendbarkeit zu maximieren:

- `core_logic.py` - Enthält die Kernverarbeitungsfunktionen, die aus den ursprünglichen CLI-Skripten extrahiert wurden
- `gradio_app.py` - Web-Interface-Implementierung unter Verwendung der Kernlogik
- `aag_erstattungen.py`, `abrechnungen.py`, `ag_belastung.py`, `lohnjournal.py` - CLI-Skripte, die die Kernlogik verwenden

Dieses Design stellt sicher, dass:
1. Die ursprüngliche CLI-Funktionalität erhalten bleibt
2. Code nicht dupliziert wird
3. Fehlerbehebungen und Verbesserungen sowohl CLI- als auch Web-Interfaces zugutekommen
4. Die Kernlogik einfach getestet und gewartet werden kann