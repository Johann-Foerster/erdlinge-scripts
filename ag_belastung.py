#!/usr/bin/env python3
"""
CLI script for processing AG Belastung (Employer Burden) documents.
Preserved original CLI functionality while using refactored core logic.
"""
import glob
import os
import sys
from core_processors import process_ag_belastung


def main():
    """Main CLI function for AG belastung processing."""
    YEAR = "2025"
    MON = "AUGUST"
    pdfs = glob.glob(f"ag_belastung/{YEAR}/August.pdf")
    
    if len(pdfs) != 1:
        raise OSError("expected one pdf")
    
    print(f"Reading {pdfs[0]}...")
    
    # Read PDF file
    with open(pdfs[0], 'rb') as f:
        file_content = f.read()
    
    # Process using core logic
    result_bytes = process_ag_belastung(file_content, YEAR, MON)
    
    # Save result
    OUT_FILENAME = f"ag_belastung_{YEAR}_{MON}.xlsx"
    print(f"\nCreating {OUT_FILENAME}")
    if os.path.exists(OUT_FILENAME):
        os.remove(OUT_FILENAME)
    
    with open(OUT_FILENAME, 'wb') as f:
        f.write(result_bytes)
    
    print("done")


if __name__ == "__main__":
    main()
