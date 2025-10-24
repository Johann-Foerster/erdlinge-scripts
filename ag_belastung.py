from core_logic import process_ag_belastung
import glob, os

YEAR = "2024"
MON = "August"

# CLI script functionality preserved
if __name__ == "__main__":
    pdfs = glob.glob(f"ag_belastung/{YEAR}/{MON}.pdf")
    
    if len(pdfs) != 1:
        raise OSError("expected one pdf")
    
    print(f"Processing {pdfs[0]}...")
    
    # Use the extracted core logic
    temp_excel_path = process_ag_belastung(pdfs, YEAR)
    
    # Move to final location
    OUT_FILENAME = f"ag_belastung_{YEAR}_{MON}.xlsx"
    print(f"\nCreating {OUT_FILENAME}")
    if os.path.exists(OUT_FILENAME):
        os.remove(OUT_FILENAME)
    
    # Copy the temp file to the final location
    import shutil
    shutil.move(temp_excel_path, OUT_FILENAME)
    
    print("done")
