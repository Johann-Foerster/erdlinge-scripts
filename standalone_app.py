"""
Standalone launcher for Erdlinge Scripts PDF Processing Tool
This script creates a desktop application that auto-opens the browser
"""

import gradio as gr
import tempfile
import os
import webbrowser
import socket
from threading import Timer
from core_logic import (
    process_aag_erstattungen,
    process_abrechnungen, 
    process_ag_belastung,
    process_lohnjournal
)


def find_free_port():
    """Find a free port on localhost"""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('', 0))
        s.listen(1)
        port = s.getsockname()[1]
    return port


def open_browser(port):
    """Open browser after a short delay"""
    webbrowser.open(f'http://localhost:{port}')


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
        
        return f"Erfolgreich {len(files)} Dateien verarbeiten. Excel erstellt.", excel_path
        
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


def main():
    """Main function for standalone application"""
    print("Starte Erdlinge Scripts PDF-Verarbeitungstool...")
    
    # Find free port
    port = find_free_port()
    
    # Create app
    app = create_app()
    
    # Schedule browser opening
    Timer(1.5, open_browser, [port]).start()
    
    print(f"Anwendung läuft auf: http://localhost:{port}")
    print("Der Browser wird automatisch geöffnet...")
    print("Zum Beenden drücken Sie Ctrl+C")
    
    # Launch app
    try:
        app.launch(
            server_name="127.0.0.1",
            server_port=port,
            share=False,
            show_error=True,
            quiet=False,
            show_tips=False,
            inbrowser=False  # We handle browser opening manually
        )
    except KeyboardInterrupt:
        print("\nAnwendung beendet.")
    except Exception as e:
        print(f"Fehler beim Starten der Anwendung: {e}")


if __name__ == "__main__":
    main()