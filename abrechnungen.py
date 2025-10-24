#!/usr/bin/env python3
"""
CLI script for processing Abrechnungen (Payroll) documents.
Preserved original CLI functionality while using refactored core logic.
"""
import glob
import os
import sys
from core_processors import process_abrechnungen


def main():
    """Main CLI function for abrechnungen processing."""
    YEAR = "2024"
    pdfs = glob.glob(f"abrechnungen/{YEAR}/*.pdf")
    
    if not pdfs:
        print(f"No PDF files found in abrechnungen/{YEAR}/")
        return
    
    print(f"Found {len(pdfs)} PDF files")
    
    # Read all PDF files
    file_contents = []
    for pdf in pdfs:
        print(f"Reading {pdf}...")
        with open(pdf, 'rb') as f:
            file_contents.append(f.read())
    
    # Process using core logic
    result_bytes = process_abrechnungen(file_contents, YEAR)
    
    # Save result
    OUT_FILENAME = f"abrechnungen_{YEAR}.xlsx"
    print(f"\nCreating {OUT_FILENAME}")
    if os.path.exists(OUT_FILENAME):
        os.remove(OUT_FILENAME)
    
    with open(OUT_FILENAME, 'wb') as f:
        f.write(result_bytes)
    
    print("done")


if __name__ == "__main__":
    main()
