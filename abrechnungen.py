from core_logic import process_abrechnungen
import glob, os

YEAR = "2024"

# CLI script functionality preserved  
if __name__ == "__main__":
    pdfs = glob.glob(f"abrechnungen/{YEAR}/*.pdf")
    
    if not pdfs:
        print(f"No PDF files found in abrechnungen/{YEAR}/ directory")
        exit(1)
    
    print(f"Processing {len(pdfs)} PDF files...")
    
    # Use the extracted core logic
    temp_excel_path = process_abrechnungen(pdfs, YEAR)
    
    # Move to final location
    OUT_FILENAME = f"abrechnungen_{YEAR}.xlsx"
    print(f"\nCreating {OUT_FILENAME}")
    if os.path.exists(OUT_FILENAME):
        os.remove(OUT_FILENAME)
    
    # Copy the temp file to the final location
    import shutil
    shutil.move(temp_excel_path, OUT_FILENAME)
    
    print("done")
