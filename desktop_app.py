"""
PyWebView-based Desktop Application for Erdlinge Scripts
This creates a native desktop window instead of opening in browser
"""

import gradio as gr
import tempfile
import os
import socket
import threading
import time
import sys
from core_logic import (
    process_aag_erstattungen,
    process_abrechnungen, 
    process_ag_belastung,
    process_lohnjournal
)

def check_gui_requirements():
    """Prüfe GUI-Anforderungen und gebe hilfreiche Fehlermeldungen aus."""
    import platform
    import os
    
    system = platform.system()
    
    if system == "Darwin":
        return True, "macOS WebView verfügbar"
    
    if system == "Windows":
        # Unter Windows sollte PyQt normalerweise funktionieren
        return True, "Windows GUI verfügbar"
    
    # Linux/WSL2 spezifische Prüfungen
    if system == "Linux":
        has_display = bool(os.environ.get('DISPLAY') or os.environ.get('WAYLAND_DISPLAY'))
        
        # WSL2 Detection
        is_wsl = False
        try:
            with open('/proc/version', 'r') as f:
                if 'WSL' in f.read().upper():
                    is_wsl = True
        except:
            pass
        
        if is_wsl and not has_display:
            error_msg = """
WSL2 erkannt ohne GUI-Unterstützung. Lösungen:

1. Windows 11 WSLg (empfohlen):
   - Bereits integriert, sollte automatisch funktionieren
   
2. X11-Weiterleitung einrichten:
   export DISPLAY=:0
   
3. System-GUI-Pakete installieren:
   sudo apt-get install python3-pyqt5 python3-pyqt5.qtwebkit
   sudo apt-get install python3-gi python3-gi-cairo gir1.2-webkit2-4.0

Fallback: Browser-Version wird verwendet.
"""
            return False, error_msg.strip()
        
        if not has_display:
            return False, "Keine Display-Umgebung erkannt. Headless-System?"
    
    return True, "GUI-Umgebung verfügbar"


try:
    import webview
    WEBVIEW_AVAILABLE = True
    WEBVIEW_ERROR = None
    
    # Zusätzliche GUI-Prüfungen
    gui_ok, gui_msg = check_gui_requirements()
    if not gui_ok:
        WEBVIEW_AVAILABLE = False
        WEBVIEW_ERROR = gui_msg
        
except ImportError as e:
    WEBVIEW_AVAILABLE = False
    WEBVIEW_ERROR = f"PyWebView nicht installiert: {str(e)}\n\nInstallation:\npip install pywebview PyQt5"
    import webbrowser
except Exception as e:
    WEBVIEW_AVAILABLE = False
    WEBVIEW_ERROR = f"PyWebView Initialisierungsfehler: {str(e)}"
    import webbrowser


def find_free_port():
    """Find a free port on localhost"""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('', 0))
        s.listen(1)
        port = s.getsockname()[1]
    return port


def process_aag_files(files, year="2024"):
    """AAG Erstattungen Dateien verarbeiten"""
    if not files:
        return "Keine Dateien hochgeladen", None
    
    try:
        # Get file paths from uploaded files
        file_paths = [file.name for file in files]
        
        # Process files
        csv_content = process_aag_erstattungen(file_paths, year)
        
        # Save to temporary file for download
        temp_file = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.csv', encoding='utf-8-sig')
        temp_file.write(csv_content)
        temp_file.close()
        
        return f"Erfolgreich {len(files)} Dateien verarbeitet. CSV erstellt.", temp_file.name
        
    except Exception as e:
        return f"Fehler beim Verarbeiten der Dateien: {str(e)}", None


def process_abrechnungen_files(files, year="2024"):
    """Abrechnungen Dateien verarbeiten"""
    if not files:
        return "Keine Dateien hochgeladen", None
    
    try:
        # Get file paths from uploaded files
        file_paths = [file.name for file in files]
        
        # Process files
        excel_path = process_abrechnungen(file_paths, year)
        
        return f"Erfolgreich {len(files)} Dateien verarbeitet. Excel erstellt.", excel_path
        
    except Exception as e:
        return f"Fehler beim Verarbeiten der Dateien: {str(e)}", None


def process_ag_belastung_files(files, year="2024"):
    """AG Belastung Dateien verarbeiten"""
    if not files:
        return "Keine Dateien hochgeladen", None
    
    try:
        # Get file paths from uploaded files  
        file_paths = [file.name for file in files]
        
        # Process files
        excel_path = process_ag_belastung(file_paths, year)
        
        return f"Erfolgreich {len(files)} Dateien verarbeitet. Excel erstellt.", excel_path
        
    except Exception as e:
        return f"Fehler beim Verarbeiten der Dateien: {str(e)}", None


def process_lohnjournal_files(files, year="2024"):
    """Lohnjournal Dateien verarbeiten"""
    if not files:
        return "Keine Dateien hochgeladen", None
    
    try:
        # Get file paths from uploaded files
        file_paths = [file.name for file in files]
        
        # Process files
        excel_path = process_lohnjournal(file_paths, year)
        
        return f"Erfolgreich {len(files)} Dateien verarbeitet. Excel erstellt.", excel_path
        
    except Exception as e:
        return f"Fehler beim Verarbeiten der Dateien: {str(e)}", None


def create_app():
    """Create and configure the Gradio app"""
    with gr.Blocks(title="Erdlinge Scripts - PDF-Verarbeitung", theme=gr.themes.Soft()) as app:
        gr.Markdown("# Erdlinge Scripts - PDF-Verarbeitungstool")
        gr.Markdown("Laden Sie PDF-Dateien hoch und verarbeiten Sie sie, um Excel/CSV-Berichte zu erstellen.")
        
        with gr.Tabs():
            # AAG Erstattungen Tab
            with gr.TabItem("AAG Erstattungen"):
                gr.Markdown("### AAG Erstattungen Verarbeitung")
                gr.Markdown("Laden Sie AAG Erstattungs-PDF-Dateien hoch, um einen CSV-Bericht mit U1/U2-Daten zu erstellen.")
                
                with gr.Row():
                    with gr.Column():
                        aag_files = gr.File(
                            label="AAG PDF-Dateien hochladen", 
                            file_count="multiple", 
                            file_types=[".pdf"]
                        )
                        aag_year = gr.Textbox(
                            label="Jahr", 
                            value="2024", 
                            placeholder="Jahr eingeben (z.B. 2024)"
                        )
                        aag_submit = gr.Button("AAG Dateien verarbeiten", variant="primary")
                    
                    with gr.Column():
                        aag_output = gr.Textbox(
                            label="Verarbeitungsstatus", 
                            lines=3, 
                            interactive=False
                        )
                        aag_download = gr.File(
                            label="Ergebnis herunterladen", 
                            interactive=False
                        )
                
                aag_submit.click(
                    fn=process_aag_files,
                    inputs=[aag_files, aag_year],
                    outputs=[aag_output, aag_download]
                )
            
            # Abrechnungen Tab
            with gr.TabItem("Abrechnungen"):
                gr.Markdown("### Lohnabrechnung Verarbeitung")
                gr.Markdown("Laden Sie Lohnabrechnung-PDF-Dateien hoch, um Excel-Berichte mit Zulagen, Arbeitszeiten und Gehaltsgruppen zu erstellen.")
                
                with gr.Row():
                    with gr.Column():
                        abr_files = gr.File(
                            label="Lohnabrechnung PDF-Dateien hochladen", 
                            file_count="multiple", 
                            file_types=[".pdf"]
                        )
                        abr_year = gr.Textbox(
                            label="Jahr", 
                            value="2024", 
                            placeholder="Jahr eingeben (z.B. 2024)"
                        )
                        abr_submit = gr.Button("Lohnabrechnung Dateien verarbeiten", variant="primary")
                    
                    with gr.Column():
                        abr_output = gr.Textbox(
                            label="Verarbeitungsstatus", 
                            lines=3, 
                            interactive=False
                        )
                        abr_download = gr.File(
                            label="Ergebnis herunterladen", 
                            interactive=False
                        )
                
                abr_submit.click(
                    fn=process_abrechnungen_files,
                    inputs=[abr_files, abr_year],
                    outputs=[abr_output, abr_download]
                )
            
            # AG Belastung Tab
            with gr.TabItem("AG Belastung"):
                gr.Markdown("### Arbeitgeberbelastung Verarbeitung")
                gr.Markdown("Laden Sie eine Arbeitgeberbelastung-PDF-Datei hoch, um einen Excel-Bericht mit Kostenaufschlüsselungen zu erstellen.")
                
                with gr.Row():
                    with gr.Column():
                        ag_files = gr.File(
                            label="AG Belastung PDF-Datei hochladen", 
                            file_count="single", 
                            file_types=[".pdf"]
                        )
                        ag_year = gr.Textbox(
                            label="Jahr", 
                            value="2024", 
                            placeholder="Jahr eingeben (z.B. 2024)"
                        )
                        ag_submit = gr.Button("AG Belastung Datei verarbeiten", variant="primary")
                    
                    with gr.Column():
                        ag_output = gr.Textbox(
                            label="Verarbeitungsstatus", 
                            lines=3, 
                            interactive=False
                        )
                        ag_download = gr.File(
                            label="Ergebnis herunterladen", 
                            interactive=False
                        )
                
                ag_submit.click(
                    fn=process_ag_belastung_files,
                    inputs=[ag_files, ag_year],
                    outputs=[ag_output, ag_download]
                )
            
            # Lohnjournal Tab
            with gr.TabItem("Lohnjournal"):
                gr.Markdown("### Lohnjournal Verarbeitung")
                gr.Markdown("Laden Sie eine Lohnjournal-PDF-Datei hoch, um einen Excel-Bericht mit Bruttolohndaten zu erstellen.")
                
                with gr.Row():
                    with gr.Column():
                        lj_files = gr.File(
                            label="Lohnjournal PDF-Datei hochladen", 
                            file_count="single", 
                            file_types=[".pdf"]
                        )
                        lj_year = gr.Textbox(
                            label="Jahr", 
                            value="2024", 
                            placeholder="Jahr eingeben (z.B. 2024)"
                        )
                        lj_submit = gr.Button("Lohnjournal Datei verarbeiten", variant="primary")
                    
                    with gr.Column():
                        lj_output = gr.Textbox(
                            label="Verarbeitungsstatus", 
                            lines=3, 
                            interactive=False
                        )
                        lj_download = gr.File(
                            label="Ergebnis herunterladen", 
                            interactive=False
                        )
                
                lj_submit.click(
                    fn=process_lohnjournal_files,
                    inputs=[lj_files, lj_year],
                    outputs=[lj_output, lj_download]
                )
    
    return app


def start_gradio_server(app, port):
    """Start Gradio server in a separate thread"""
    # Build launch parameters compatible with different Gradio versions
    launch_params = {
        "server_name": "127.0.0.1",
        "server_port": port,
        "share": False,
        "show_error": True,
        "quiet": True,
        "inbrowser": False,
        "prevent_thread_lock": True
    }
    
    # Check if show_tips parameter is supported (newer Gradio versions)
    import inspect
    launch_signature = inspect.signature(app.launch)
    if 'show_tips' in launch_signature.parameters:
        launch_params['show_tips'] = False
    
    app.launch(**launch_params)


def start_browser_fallback(port):
    """Fallback auf Browser-Version wenn PyWebView nicht verfügbar ist."""
    try:
        import webbrowser
        webbrowser.open(f"http://localhost:{port}")
        print(f"✓ Browser geöffnet unter: http://localhost:{port}")
        print("\nDie Anwendung läuft im Browser-Modus.")
        print("Drücken Sie Strg+C um das Programm zu beenden.")
        
        # Keep the server running
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\nProgramm beendet.")
            
    except Exception as browser_error:
        print(f"Fehler beim Öffnen des Browsers: {browser_error}")
        print(f"Manuell öffnen: http://localhost:{port}")
        print("Drücken Sie Strg+C um das Programm zu beenden.")
        
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\nProgramm beendet.")


def main():
    """Main function for native desktop application"""
    print("Starte Erdlinge Scripts PDF-Verarbeitungstool...")
    
    if not WEBVIEW_AVAILABLE:
        print("PyWebView nicht verfügbar. Fallback auf Browser-Version...")
        print(f"Fehler: {WEBVIEW_ERROR}")
        print("")
        print("Für die native Desktop-Anwendung installieren Sie die erforderlichen Abhängigkeiten:")
        print("1. Für Windows/Linux: pip install PyQt5 oder pip install PyQt6")
        print("2. Für Linux (alternative): sudo apt-get install python3-gi python3-gi-cairo gir1.2-webkit2-4.0")
        print("3. Für macOS: PyWebView nutzt das System-WebView (keine zusätzlichen Abhängigkeiten erforderlich)")
        print("")
        print("Vollständige Installation: pip install -r requirements.txt")
        print("")
        
        # Fallback to browser version
        from standalone_app import main as browser_main
        browser_main()
        return
    
    # Find free port
    port = find_free_port()
    url = f"http://127.0.0.1:{port}"
    
    # Create app
    app = create_app()
    
    print(f"Starte Web-Server auf Port {port}...")
    
    # Start Gradio server in background thread
    server_thread = threading.Thread(target=start_gradio_server, args=(app, port))
    server_thread.daemon = True
    
    try:
        server_thread.start()
    except Exception as e:
        print(f"Fehler beim Starten des Server-Threads: {e}")
        return
    
    # Wait for server to start
    print("Warte auf Server-Start...")
    time.sleep(3)  # Give more time for server startup
    
    # Test if server is running
    try:
        import urllib.request
        urllib.request.urlopen(url, timeout=10)
        print("Server erfolgreich gestartet.")
    except Exception as e:
        print(f"Fehler beim Verbinden zum Server: {e}")
        print("Mögliche Lösungen:")
        print("1. Stellen Sie sicher, dass alle Abhängigkeiten installiert sind: pip install -r requirements.txt")
        print("2. Prüfen Sie, ob der Port bereits verwendet wird")
        print("3. Versuchen Sie die Browser-Version: python standalone_app.py")
        return
    
    print("Öffne native Desktop-Anwendung...")
    
    # Create and show webview window
    try:
        webview.create_window(
            title="Erdlinge Scripts - PDF-Verarbeitungstool",
            url=url,
            width=1200,
            height=800,
            min_size=(800, 600),
            resizable=True,
            fullscreen=False,
            minimized=False,
            on_top=False,
            shadow=True,
            maximized=False
        )
        
        # Show debug info in console mode only
        debug_mode = '--debug' in sys.argv
        
        # Start the webview
        webview.start(debug=debug_mode, http_server=False)
        
    except Exception as e:
        error_msg = str(e).lower()
        print(f"Fehler beim Starten der Desktop-Anwendung: {e}")
        
        if "qtpy" in error_msg or "qt" in error_msg:
            print("")
            print("PyWebView benötigt Qt-Bibliotheken:")
            print("WSL2/Linux: sudo apt-get install python3-pyqt5 python3-pyqt5.qtwebkit")
            print("Windows/Linux: pip install PyQt5")
            print("")
            print("WSL2 zusätzlich benötigt:")
            print("export DISPLAY=:0  # oder Windows 11 WSLg verwenden")
        elif "gtk" in error_msg:
            print("")
            print("GTK-Bibliotheken fehlen:")
            print("sudo apt-get install python3-gi python3-gi-cairo gir1.2-webkit2-4.0")
        elif "display" in error_msg or "wayland" in error_msg or "x11" in error_msg:
            print("")
            print("GUI-Display nicht verfügbar (WSL2/Headless):")
            print("1. Windows 11: WSLg sollte automatisch funktionieren")
            print("2. Ältere Versionen: export DISPLAY=:0")
            print("3. X11-Server auf Windows installieren (VcXsrv, Xming)")
        else:
            print("")
            print("Mögliche Lösungen:")
            print("1. Windows/Linux: pip install PyQt5")
            print("2. Linux (alternative): sudo apt-get install python3-gi python3-gi-cairo gir1.2-webkit2-4.0")
            print("3. Vollständige Neuinstallation: pip install -r requirements.txt")
        
        print("")
        print("Fallback: Öffne im Browser...")
        import webbrowser
        webbrowser.open(url)
        
        try:
            # Keep the server running
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\nAnwendung beendet.")


if __name__ == "__main__":
    main()