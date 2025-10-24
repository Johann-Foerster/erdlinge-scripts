#!/usr/bin/env python3
"""
CLI script for processing AAG Erstattungen (Reimbursements) documents.
Preserved original CLI functionality while using refactored core logic.
"""
import glob
import os
import sys
from core_processors import process_aag_erstattungen


def main():
    """Main CLI function for AAG erstattungen processing."""
    YEAR = "2024"
    pdfs = glob.glob(f"aag_erstattungen/{YEAR}/*.pdf")
    
    if not pdfs:
        print(f"No PDF files found in aag_erstattungen/{YEAR}/")
        return
    
    print(f"Found {len(pdfs)} PDF files")
    
    # Read all PDF files
    file_contents = []
    for pdf in pdfs:
        print(f"Reading {pdf}...")
        with open(pdf, 'rb') as f:
            file_contents.append(f.read())
    
    # Process using core logic
    result_bytes = process_aag_erstattungen(file_contents, YEAR)
    
    # Save result
    outfile = f"AAG_Erstattungen_{YEAR}.csv"
    print(f"\nWriting {outfile}")
    
    with open(outfile, 'wb') as f:
        f.write(result_bytes)
    
    print("...written!")


if __name__ == "__main__":
    main()
