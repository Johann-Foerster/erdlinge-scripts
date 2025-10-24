"""
Gradio App for Erdlinge Scripts
A web interface for processing different types of documents with the existing CLI logic.
"""
import gradio as gr
import sys
import os
import tempfile
import shutil
from pathlib import Path
from core_processors import (
    process_abrechnungen,
    process_ag_belastung, 
    process_aag_erstattungen,
    process_lohnjournal
)


def safe_read_file(gradio_file_path):
    """Safely read a file uploaded via gradio."""
    # Validate that the file exists and is readable
    if not os.path.exists(gradio_file_path):
        raise ValueError("File does not exist")
    
    # Check file size (limit to 100MB)
    file_size = os.path.getsize(gradio_file_path)
    if file_size > 100 * 1024 * 1024:  # 100MB
        raise ValueError("File too large")
    
    with open(gradio_file_path, 'rb') as f:
        return f.read()


def process_abrechnungen_ui(files, year):
    """Process Abrechnungen files through gradio interface."""
    if not files:
        return None, "Bitte mindestens eine PDF-Datei hochladen."
    
    try:
        file_contents = []
        for file in files:
            # Use only basename to prevent path traversal
            safe_filename = os.path.basename(file.name)
            if not safe_filename.lower().endswith('.pdf'):
                return None, "❌ Nur PDF-Dateien sind erlaubt."
            
            file_contents.append(safe_read_file(file.name))
        
        result_bytes = process_abrechnungen(file_contents, year)
        
        # Save to temporary file for download with sanitized name
        # This is safe as output_filename is constructed by us, not user input
        output_filename = f"abrechnungen_{year}.xlsx"
        with open(output_filename, 'wb') as f:
            f.write(result_bytes)
        
        return output_filename, f"✅ Erfolgreich verarbeitet! {len(files)} Datei(en) zu Excel konvertiert."
        
    except Exception as e:
        return None, f"❌ Fehler beim Verarbeiten: {str(e)}"


def process_ag_belastung_ui(file, year, month):
    """Process AG Belastung file through gradio interface."""
    if not file:
        return None, "Bitte eine PDF-Datei hochladen."
    
    try:
        # Use only basename to prevent path traversal
        safe_filename = os.path.basename(file.name)
        if not safe_filename.lower().endswith('.pdf'):
            return None, "❌ Nur PDF-Dateien sind erlaubt."
        
        file_content = safe_read_file(file.name)
        
        result_bytes = process_ag_belastung(file_content, year, month)
        
        # Save to temporary file for download with sanitized name
        output_filename = f"ag_belastung_{year}_{month}.xlsx"
        with open(output_filename, 'wb') as f:
            f.write(result_bytes)
        
        return output_filename, f"✅ Erfolgreich verarbeitet! AG Belastung für {month} {year} zu Excel konvertiert."
        
    except Exception as e:
        return None, f"❌ Fehler beim Verarbeiten: {str(e)}"


def process_aag_erstattungen_ui(files, year):
    """Process AAG Erstattungen files through gradio interface."""
    if not files:
        return None, "Bitte mindestens eine PDF-Datei hochladen."
    
    try:
        file_contents = []
        for file in files:
            # Use only basename to prevent path traversal
            safe_filename = os.path.basename(file.name)
            if not safe_filename.lower().endswith('.pdf'):
                return None, "❌ Nur PDF-Dateien sind erlaubt."
            
            file_contents.append(safe_read_file(file.name))
        
        result_bytes = process_aag_erstattungen(file_contents, year)
        
        # Save to temporary file for download with sanitized name
        output_filename = f"AAG_Erstattungen_{year}.csv"
        with open(output_filename, 'wb') as f:
            f.write(result_bytes)
        
        return output_filename, f"✅ Erfolgreich verarbeitet! {len(files)} Datei(en) zu CSV konvertiert."
        
    except Exception as e:
        return None, f"❌ Fehler beim Verarbeiten: {str(e)}"


def process_lohnjournal_ui(file, year):
    """Process Lohnjournal file through gradio interface."""
    if not file:
        return None, "Bitte eine PDF-Datei hochladen."
    
    try:
        # Use only basename to prevent path traversal
        safe_filename = os.path.basename(file.name)
        if not safe_filename.lower().endswith('.pdf'):
            return None, "❌ Nur PDF-Dateien sind erlaubt."
        
        file_content = safe_read_file(file.name)
        
        result_bytes = process_lohnjournal(file_content, year)
        
        # Save to temporary file for download with sanitized name
        output_filename = f"lohnjournal_{year}.xlsx"
        with open(output_filename, 'wb') as f:
            f.write(result_bytes)
        
        return output_filename, f"✅ Erfolgreich verarbeitet! Lohnjournal für {year} zu Excel konvertiert."
        
    except Exception as e:
        return None, f"❌ Fehler beim Verarbeiten: {str(e)}"


def create_gradio_app():
    """Create and configure the gradio interface."""
    
    with gr.Blocks(title="Erdlinge Scripts", theme=gr.themes.Soft()) as app:
        gr.Markdown("""
        # 🏢 Erdlinge Scripts - Document Processing Tool
        
        Verarbeitung verschiedener Dokument-Typen zu Excel/CSV-Dateien.
        Wählen Sie einen Tab für den gewünschten Dokumenttyp.
        """)
        
        with gr.Tabs():
            # Abrechnungen Tab
            with gr.Tab("📊 Abrechnungen (Gehaltsabrechnungen)"):
                gr.Markdown("### Gehaltsabrechnungen verarbeiten")
                gr.Markdown("Lädt PDF-Dateien von Gehaltsabrechnungen und erstellt Excel-Tabellen mit Zulagen, Fahrtkosten etc.")
                
                with gr.Row():
                    with gr.Column():
                        abr_files = gr.File(
                            label="PDF-Dateien hochladen", 
                            file_count="multiple",
                            file_types=[".pdf"],
                            height=150
                        )
                        abr_year = gr.Textbox(
                            label="Jahr", 
                            value="2024",
                            placeholder="z.B. 2024"
                        )
                        abr_submit = gr.Button("🚀 Verarbeiten", variant="primary", size="lg")
                    
                    with gr.Column():
                        abr_status = gr.Textbox(label="Status", interactive=False, lines=3)
                        abr_download = gr.File(label="Download Excel-Datei")
                
                abr_submit.click(
                    process_abrechnungen_ui,
                    inputs=[abr_files, abr_year],
                    outputs=[abr_download, abr_status]
                )
            
            # AG Belastung Tab
            with gr.Tab("💰 AG Belastung (Arbeitgeber-Belastung)"):
                gr.Markdown("### Arbeitgeber-Belastung verarbeiten")
                gr.Markdown("Verarbeitet eine PDF-Datei der Arbeitgeber-Belastung und erstellt eine Excel-Tabelle.")
                
                with gr.Row():
                    with gr.Column():
                        agb_file = gr.File(
                            label="PDF-Datei hochladen",
                            file_count="single", 
                            file_types=[".pdf"],
                            height=150
                        )
                        agb_year = gr.Textbox(
                            label="Jahr",
                            value="2025", 
                            placeholder="z.B. 2025"
                        )
                        agb_month = gr.Textbox(
                            label="Monat",
                            value="AUGUST",
                            placeholder="z.B. AUGUST"
                        )
                        agb_submit = gr.Button("🚀 Verarbeiten", variant="primary", size="lg")
                    
                    with gr.Column():
                        agb_status = gr.Textbox(label="Status", interactive=False, lines=3)
                        agb_download = gr.File(label="Download Excel-Datei")
                
                agb_submit.click(
                    process_ag_belastung_ui,
                    inputs=[agb_file, agb_year, agb_month],
                    outputs=[agb_download, agb_status]
                )
            
            # AAG Erstattungen Tab
            with gr.Tab("📄 AAG Erstattungen"):
                gr.Markdown("### AAG Erstattungen verarbeiten")
                gr.Markdown("Verarbeitet PDF-Dateien von AAG-Erstattungen (U1/U2) und erstellt eine CSV-Datei.")
                
                with gr.Row():
                    with gr.Column():
                        aag_files = gr.File(
                            label="PDF-Dateien hochladen",
                            file_count="multiple",
                            file_types=[".pdf"],
                            height=150
                        )
                        aag_year = gr.Textbox(
                            label="Jahr",
                            value="2024",
                            placeholder="z.B. 2024"
                        )
                        aag_submit = gr.Button("🚀 Verarbeiten", variant="primary", size="lg")
                    
                    with gr.Column():
                        aag_status = gr.Textbox(label="Status", interactive=False, lines=3)
                        aag_download = gr.File(label="Download CSV-Datei")
                
                aag_submit.click(
                    process_aag_erstattungen_ui,
                    inputs=[aag_files, aag_year],
                    outputs=[aag_download, aag_status]
                )
            
            # Lohnjournal Tab
            with gr.Tab("📋 Lohnjournal"):
                gr.Markdown("### Lohnjournal verarbeiten")
                gr.Markdown("Verarbeitet eine PDF-Datei des Lohnjournals und erstellt eine Excel-Tabelle.")
                
                with gr.Row():
                    with gr.Column():
                        lj_file = gr.File(
                            label="PDF-Datei hochladen",
                            file_count="single",
                            file_types=[".pdf"],
                            height=150
                        )
                        lj_year = gr.Textbox(
                            label="Jahr",
                            value="2024",
                            placeholder="z.B. 2024"
                        )
                        lj_submit = gr.Button("🚀 Verarbeiten", variant="primary", size="lg")
                    
                    with gr.Column():
                        lj_status = gr.Textbox(label="Status", interactive=False, lines=3)
                        lj_download = gr.File(label="Download Excel-Datei")
                
                lj_submit.click(
                    process_lohnjournal_ui,
                    inputs=[lj_file, lj_year],
                    outputs=[lj_download, lj_status]
                )
        
        gr.Markdown("""
        ---
        ### 📝 Hinweise:
        - **Abrechnungen**: Mehrere PDF-Dateien möglich, erstellt Excel mit verschiedenen Tabellenblättern
        - **AG Belastung**: Eine PDF-Datei, Jahr und Monat angeben
        - **AAG Erstattungen**: Mehrere PDF-Dateien möglich, erstellt CSV mit U1/U2 Daten  
        - **Lohnjournal**: Eine PDF-Datei, erstellt Excel mit Steuer- und Gesamtbrutto-Daten
        
        🔧 **Entwickelt für die Erdlinge-Verwaltung**
        """)
    
    return app


def main():
    """Main function to run the gradio app."""
    app = create_gradio_app()
    
    # Check if running in share mode
    share = "--share" in sys.argv
    port = 7860
    
    if "--port" in sys.argv:
        try:
            port_idx = sys.argv.index("--port")
            port = int(sys.argv[port_idx + 1])
        except (IndexError, ValueError):
            print("Warning: Invalid port specified, using default 7860")
    
    print("🚀 Starting Erdlinge Scripts Gradio App...")
    print(f"📍 Local URL: http://localhost:{port}")
    if share:
        print("🌐 Public URL will be generated...")
    
    app.launch(
        server_name="0.0.0.0",
        server_port=port,
        share=share,
        show_error=True
    )


if __name__ == "__main__":
    main()