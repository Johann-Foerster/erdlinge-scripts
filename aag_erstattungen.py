from core_logic import process_aag_erstattungen
import glob

YEAR = "2024"

# CLI script functionality preserved
if __name__ == "__main__":
    pdfs = glob.glob(f"aag_erstattungen/{YEAR}/*.pdf")
    
    if not pdfs:
        print(f"No PDF files found in aag_erstattungen/{YEAR}/ directory")
        exit(1)
    
    print(f"Processing {len(pdfs)} PDF files...")
    
    # Use the extracted core logic
    csv_content = process_aag_erstattungen(pdfs, YEAR)
    
    # Write to file
    outfile = f"AAG_Erstattungen_{YEAR}.csv"
    print(f"\nWriting {outfile}")
    
    with open(outfile, "w", encoding="utf-8-sig") as file:
        file.write(csv_content)
    
    print("...written!")
