#!/usr/bin/env python
"""
AbuLang - Main entry point with IDLE GUI
"""

import sys
from Module.idle_gui import AbuIDLEGUI
from Module import run_file


def main():
    """Main entry point"""
    
    if len(sys.argv) < 2:
        # Launch IDLE GUI if no arguments
        print("AbuLang v3.0.0")
        print("Launching IDLE GUI...\n")
        idle = AbuIDLEGUI()
        idle.run()
    else:
        # Run file if provided
        filename = sys.argv[1]
        try:
            run_file(filename)
        except FileNotFoundError:
            print(f"Error: File not found: {filename}")
            sys.exit(1)
        except Exception as e:
            print(f"Error: {e}")
            sys.exit(1)


if __name__ == "__main__":
    main()
