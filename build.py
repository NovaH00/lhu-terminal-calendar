#!/usr/bin/env python3
"""
Build script for LHU Calendar application using Nuitka.

This script creates a standalone executable for the LHU Calendar application.
"""

import sys
from pathlib import Path
import subprocess
import argparse


def main():
    parser = argparse.ArgumentParser(description='Build LHU Calendar application with Nuitka')
    parser.add_argument('--output-dir', default='dist', help='Output directory for executables (default: dist)')
    parser.add_argument('--clean', action='store_true', help='Clean output directory before building')
    parser.add_argument('--verbose', '-v', action='store_true', help='Enable verbose output')

    args = parser.parse_args()

    # Define paths
    output_dir = Path(args.output_dir)
    main_script = Path('src/main.py')

    # Check if main script exists
    if not main_script.exists():
        print(f"Error: {main_script} not found!")
        sys.exit(1)

    # Clean output directory if requested
    if args.clean and output_dir.exists():
        print(f"Cleaning output directory: {output_dir}")
        import shutil
        shutil.rmtree(output_dir)

    # Create output directory
    output_dir.mkdir(exist_ok=True)
    
    # Build command
    cmd = [
        sys.executable,
        '-m', 'nuitka',
        '--onefile',  # Create a single executable file instead of standalone directory
        f'--output-dir={output_dir}',
        '--output-filename=calen',  # Set the executable name
        '--remove-output',
    ]

    if args.verbose:
        cmd.append('--verbose')
    else:
        cmd.append('--quiet')

    cmd.append(str(main_script))
    
    print(f"Building LHU Calendar application...")
    print(f"Command: {' '.join(cmd)}")
    
    try:
        result = subprocess.run(cmd, check=True)
        print(f"Build completed successfully! Executable is in {output_dir}/")
        
        # List the output files
        for file_path in output_dir.rglob('*'):
            if file_path.is_file():
                print(f"  - {file_path}")
                
    except subprocess.CalledProcessError as e:
        print(f"Build failed with return code {e.returncode}")
        sys.exit(e.returncode)
    except FileNotFoundError:
        print("Error: Nuitka is not installed. Please install it with 'pip install nuitka'")
        sys.exit(1)


if __name__ == '__main__':
    main()
