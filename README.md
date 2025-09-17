# Erdlinge Scripts - PDF-Verarbeitungstool

Dieses Repository enthält Skripte zur Verarbeitung verschiedener Arten von PDF-Dokumenten im Zusammenhang mit Lohnabrechnung und Erstattungen.

## Funktionen

- **AAG Erstattungen**: Verarbeitung von AAG-Erstattungs-PDFs und Generierung von CSV-Berichten mit U1/U2-Daten
- **Abrechnungen**: Verarbeitung von Lohnabrechnung-PDFs und Generierung von Excel-Berichten mit Zulagen, Arbeitszeiten und Gehaltsgruppen
- **AG Belastung**: Verarbeitung von Arbeitgeberbelastung-PDFs und Generierung von Excel-Berichten mit Kostenaufschlüsselungen
- **Lohnjournal**: Verarbeitung von Lohnjournal-PDFs und Generierung von Excel-Berichten mit Bruttolohndaten

## Installation

1. Installieren Sie die erforderlichen Abhängigkeiten:
```bash
pip install -r requirements.txt
```

## Verwendung

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

### Web-Interface (Gradio App)

Für eine benutzerfreundlichere Erfahrung verwenden Sie das Gradio-Web-Interface:

```bash
python gradio_app.py
```

Dies startet einen Webserver unter `http://localhost:7860` mit Registerkarten für jeden Dokumenttyp. Sie können:

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