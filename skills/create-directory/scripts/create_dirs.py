#!/usr/bin/env python3
"""Directory creation utility script."""

import os
import sys
import argparse

def create_directory_structure(base_path, structure):
    """
    Create a directory structure from a list of paths.
    
    Args:
        base_path: Base directory path
        structure: List of directory paths relative to base_path
    """
    created = []
    errors = []
    
    for rel_path in structure:
        full_path = os.path.join(base_path, rel_path)
        try:
            os.makedirs(full_path, exist_ok=True)
            created.append(full_path)
        except Exception as e:
            errors.append((full_path, str(e)))
    
    return created, errors

def main():
    parser = argparse.ArgumentParser(description='Create directory structure')
    parser.add_argument('base', help='Base directory path')
    parser.add_argument('directories', nargs='+', help='Directories to create')
    
    args = parser.parse_args()
    
    created, errors = create_directory_structure(args.base, args.directories)
    
    if created:
        print("Created directories:")
        for path in created:
            print(f"  {path}")
    
    if errors:
        print("
Errors:")
        for path, error in errors:
            print(f"  {path}: {error}")
        sys.exit(1)

if __name__ == '__main__':
    main()
