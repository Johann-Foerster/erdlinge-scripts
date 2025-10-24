#!/usr/bin/env python3
"""
CLI script for processing Lohnjournal (Payroll Journal) documents.
Preserved original CLI functionality while using refactored core logic.
"""
import glob
import os
import sys
from core_processors import process_lohnjournal


def main():
    """Main CLI function for lohnjournal processing."""
    YEAR = "2024"
    pdfs = glob.glob(f"lohnjournal/12.2024.pdf")
    
    if len(pdfs) != 1:
        raise OSError("expected one pdf")
    
    print(f"Reading {pdfs[0]}...")
    
    # Read PDF file
    with open(pdfs[0], 'rb') as f:
        file_content = f.read()
    
    # Process using core logic
    result_bytes = process_lohnjournal(file_content, YEAR)
    
    # Save result
    OUT_FILENAME = f"lohnjournal_{YEAR}.xlsx"
    print(f"\nCreating {OUT_FILENAME}")
    if os.path.exists(OUT_FILENAME):
        os.remove(OUT_FILENAME)
    
    with open(OUT_FILENAME, 'wb') as f:
        f.write(result_bytes)
    
    print("done")


if __name__ == "__main__":
    main()
