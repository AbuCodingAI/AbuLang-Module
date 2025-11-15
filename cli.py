#!/usr/bin/env python
"""
AbuLang Command Line Interface
"""

import sys
import os
from essentials.python.runner import AbuRunner

def main():
    """Main CLI entry point"""
    
    if len(sys.argv) < 2:
        print("AbuLang v3.0.0")
        print("Usage: abulang <file.abu>")
        print("\nExamples:")
        print("  abulang myprogram.abu")
        print("  abulang example.abu")
        sys.exit(1)
    
    filename = sys.argv[1]
    
    # Check if file exists
    if not os.path.exists(filename):
        print(f"Error: File not found: {filename}")
        sys.exit(1)
    
    # Check if it's an .abu file
    if not filename.endswith('.abu'):
        print(f"Warning: File should have .abu extension")
    
    # Read and run the file
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            code = f.read()
        
        runner = AbuRunner()
        runner.run(code)
        
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
