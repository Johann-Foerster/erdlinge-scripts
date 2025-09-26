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

try:
    import webview
    WEBVIEW_AVAILABLE = True
except ImportError:
    WEBVIEW_AVAILABLE = False
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
    app.launch(
        server_name="127.0.0.1",
        server_port=port,
        share=False,
        show_error=True,
        quiet=True,
        show_tips=False,
        inbrowser=False,
        prevent_thread_lock=True
    )


def main():
    """Main function for native desktop application"""
    print("Starte Erdlinge Scripts PDF-Verarbeitungstool...")
    
    if not WEBVIEW_AVAILABLE:
        print("PyWebView nicht verfügbar. Fallback auf Browser-Version...")
        print("Installieren Sie PyWebView für native Desktop-Erfahrung: pip install pywebview")
        
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
    server_thread.start()
    
    # Wait for server to start
    print("Warte auf Server-Start...")
    time.sleep(2)
    
    # Test if server is running
    try:
        import urllib.request
        urllib.request.urlopen(url, timeout=5)
        print("Server erfolgreich gestartet.")
    except Exception as e:
        print(f"Fehler beim Verbinden zum Server: {e}")
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
        print(f"Fehler beim Starten der Desktop-Anwendung: {e}")
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