"""
Gradio Web Application for Erdlinge Scripts
Provides a web interface for the PDF processing scripts
"""

import gradio as gr
import tempfile
import os
from core_logic import (
    process_aag_erstattungen,
    process_abrechnungen, 
    process_ag_belastung,
    process_lohnjournal
)


def process_aag_files(files, year="2024"):
    """Process AAG Erstattungen files"""
    if not files:
        return "No files uploaded", None
    
    try:
        # Get file paths from uploaded files
        file_paths = [file.name for file in files]
        
        # Process files
        csv_content = process_aag_erstattungen(file_paths, year)
        
        # Save to temporary file for download
        temp_file = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.csv', encoding='utf-8-sig')
        temp_file.write(csv_content)
        temp_file.close()
        
        return f"Successfully processed {len(files)} files. CSV generated.", temp_file.name
        
    except Exception as e:
        return f"Error processing files: {str(e)}", None


def process_abrechnungen_files(files, year="2024"):
    """Process Abrechnungen files"""
    if not files:
        return "No files uploaded", None
    
    try:
        # Get file paths from uploaded files
        file_paths = [file.name for file in files]
        
        # Process files
        excel_path = process_abrechnungen(file_paths, year)
        
        return f"Successfully processed {len(files)} files. Excel generated.", excel_path
        
    except Exception as e:
        return f"Error processing files: {str(e)}", None


def process_ag_belastung_files(files, year="2024"):
    """Process AG Belastung files"""
    if not files:
        return "No files uploaded", None
    
    try:
        # Get file paths from uploaded files  
        file_paths = [file.name for file in files]
        
        # Process files
        excel_path = process_ag_belastung(file_paths, year)
        
        return f"Successfully processed {len(files)} files. Excel generated.", excel_path
        
    except Exception as e:
        return f"Error processing files: {str(e)}", None


def process_lohnjournal_files(files, year="2024"):
    """Process Lohnjournal files"""
    if not files:
        return "No files uploaded", None
    
    try:
        # Get file paths from uploaded files
        file_paths = [file.name for file in files]
        
        # Process files
        excel_path = process_lohnjournal(file_paths, year)
        
        return f"Successfully processed {len(files)} files. Excel generated.", excel_path
        
    except Exception as e:
        return f"Error processing files: {str(e)}", None


# Create Gradio interface
with gr.Blocks(title="Erdlinge Scripts - PDF Processing", theme=gr.themes.Soft()) as app:
    gr.Markdown("# Erdlinge Scripts - PDF Processing Tool")
    gr.Markdown("Upload PDF files and process them to generate Excel/CSV reports.")
    
    with gr.Tabs():
        # AAG Erstattungen Tab
        with gr.TabItem("AAG Erstattungen"):
            gr.Markdown("### AAG Reimbursements Processing")
            gr.Markdown("Upload AAG reimbursement PDF files to generate a CSV report with U1/U2 data.")
            
            with gr.Row():
                with gr.Column():
                    aag_files = gr.File(
                        label="Upload AAG PDF Files", 
                        file_count="multiple", 
                        file_types=[".pdf"]
                    )
                    aag_year = gr.Textbox(
                        label="Year", 
                        value="2024", 
                        placeholder="Enter year (e.g., 2024)"
                    )
                    aag_submit = gr.Button("Process AAG Files", variant="primary")
                
                with gr.Column():
                    aag_output = gr.Textbox(
                        label="Processing Status", 
                        lines=3, 
                        interactive=False
                    )
                    aag_download = gr.File(
                        label="Download Result", 
                        interactive=False
                    )
            
            aag_submit.click(
                fn=process_aag_files,
                inputs=[aag_files, aag_year],
                outputs=[aag_output, aag_download]
            )
        
        # Abrechnungen Tab
        with gr.TabItem("Abrechnungen"):
            gr.Markdown("### Payroll Processing")
            gr.Markdown("Upload payroll PDF files to generate Excel reports with allowances, working hours, and salary groups.")
            
            with gr.Row():
                with gr.Column():
                    abr_files = gr.File(
                        label="Upload Payroll PDF Files", 
                        file_count="multiple", 
                        file_types=[".pdf"]
                    )
                    abr_year = gr.Textbox(
                        label="Year", 
                        value="2024", 
                        placeholder="Enter year (e.g., 2024)"
                    )
                    abr_submit = gr.Button("Process Payroll Files", variant="primary")
                
                with gr.Column():
                    abr_output = gr.Textbox(
                        label="Processing Status", 
                        lines=3, 
                        interactive=False
                    )
                    abr_download = gr.File(
                        label="Download Result", 
                        interactive=False
                    )
            
            abr_submit.click(
                fn=process_abrechnungen_files,
                inputs=[abr_files, abr_year],
                outputs=[abr_output, abr_download]
            )
        
        # AG Belastung Tab
        with gr.TabItem("AG Belastung"):
            gr.Markdown("### Employer Burden Processing")
            gr.Markdown("Upload employer burden PDF file to generate Excel report with cost breakdowns.")
            
            with gr.Row():
                with gr.Column():
                    ag_files = gr.File(
                        label="Upload AG Belastung PDF File", 
                        file_count="single", 
                        file_types=[".pdf"]
                    )
                    ag_year = gr.Textbox(
                        label="Year", 
                        value="2024", 
                        placeholder="Enter year (e.g., 2024)"
                    )
                    ag_submit = gr.Button("Process AG Belastung File", variant="primary")
                
                with gr.Column():
                    ag_output = gr.Textbox(
                        label="Processing Status", 
                        lines=3, 
                        interactive=False
                    )
                    ag_download = gr.File(
                        label="Download Result", 
                        interactive=False
                    )
            
            ag_submit.click(
                fn=process_ag_belastung_files,
                inputs=[ag_files, ag_year],
                outputs=[ag_output, ag_download]
            )
        
        # Lohnjournal Tab
        with gr.TabItem("Lohnjournal"):
            gr.Markdown("### Payroll Journal Processing")
            gr.Markdown("Upload payroll journal PDF file to generate Excel report with gross salary data.")
            
            with gr.Row():
                with gr.Column():
                    lj_files = gr.File(
                        label="Upload Lohnjournal PDF File", 
                        file_count="single", 
                        file_types=[".pdf"]
                    )
                    lj_year = gr.Textbox(
                        label="Year", 
                        value="2024", 
                        placeholder="Enter year (e.g., 2024)"
                    )
                    lj_submit = gr.Button("Process Lohnjournal File", variant="primary")
                
                with gr.Column():
                    lj_output = gr.Textbox(
                        label="Processing Status", 
                        lines=3, 
                        interactive=False
                    )
                    lj_download = gr.File(
                        label="Download Result", 
                        interactive=False
                    )
            
            lj_submit.click(
                fn=process_lohnjournal_files,
                inputs=[lj_files, lj_year],
                outputs=[lj_output, lj_download]
            )


if __name__ == "__main__":
    app.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=False
    )