"""Einstiegspunkt für das gebündelte Standalone-Programm.

Dieses Skript wird von PyInstaller als ausführbare Datei gebündelt. Es startet
die gemeinsame Gradio-Oberfläche (siehe :mod:`app`) und öffnet automatisch den
Standard-Browser, damit die Anwendung sich wie ein klassisches Desktop-Programm
verhält.
"""

import os
import sys


def _bundle_dir():
    """Verzeichnis, in dem die gebündelten Ressourcen liegen.

    Im PyInstaller-Bundle entpackt der Bootloader die Daten nach ``sys._MEIPASS``.
    Außerhalb des Bundles wird das Verzeichnis dieser Datei verwendet.
    """
    return getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))


def main():
    # Sicherstellen, dass die gebündelten Module gefunden werden, wenn das
    # Programm aus einem anderen Arbeitsverzeichnis gestartet wird.
    bundle_dir = _bundle_dir()
    if bundle_dir not in sys.path:
        sys.path.insert(0, bundle_dir)

    import app

    demo = app.build_app()
    # ``inbrowser=True`` öffnet den Standard-Browser, sobald der lokale Server
    # bereit ist. ``launch`` blockiert anschließend, bis das Programm beendet wird.
    demo.launch(inbrowser=True)


if __name__ == "__main__":
    main()
