---
name: create-directory
description: Use this skill whenever you need to create directories or folder structures. This includes creating single directories, nested directory structures, project folder layouts, or organizing files into directories. If the user mentions creating folders, directories, organizing files, or setting up project structures, use this skill.
---

# Directory Creation Skill

## Overview

This skill provides guidance and tools for creating directories and folder structures in a safe and efficient manner. It includes best practices for directory creation, error handling, and cross-platform compatibility.

## Quick Start

### Basic Directory Creation

```python
import os

# Create a single directory
os.makedirs("my_directory", exist_ok=True)

# Create nested directories
os.makedirs("parent/child/grandchild", exist_ok=True)
```

### Safe Directory Creation Function

```python
import os
import shutil

def create_directory_safe(path, clean_existing=False):
    """
    Safely create a directory.
    
    Args:
        path: Directory path to create
        clean_existing: If True, remove existing directory and recreate
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        if clean_existing and os.path.exists(path):
            shutil.rmtree(path)
            print(f"Removed existing directory: {path}")
        
        os.makedirs(path, exist_ok=True)
        print(f"Created directory: {path}")
        return True
    except Exception as e:
        print(f"Error creating directory {path}: {e}")
        return False
```

## Best Practices

### 1. Use `exist_ok=True`
Always use `exist_ok=True` with `os.makedirs()` to avoid errors if the directory already exists.

### 2. Handle Special Characters
Avoid special characters in directory names that might cause issues on different operating systems.

### 3. Check Permissions
Ensure you have write permissions in the parent directory before attempting to create subdirectories.

### 4. Cross-Platform Paths
Use `os.path.join()` for cross-platform compatibility:

```python
import os

# Good - cross-platform
path = os.path.join("parent", "child", "grandchild")

# Bad - platform-specific
path = "parent/child/grandchild"  # Works on Unix, not Windows
```

## Common Patterns

### Create Project Structure

```python
def create_project_structure(base_path):
    """Create a standard project directory structure."""
    directories = [
        "src",
        "tests",
        "docs",
        "data/raw",
        "data/processed",
        "notebooks",
        "scripts",
        "config",
        "logs",
        "reports"
    ]
    
    for directory in directories:
        full_path = os.path.join(base_path, directory)
        os.makedirs(full_path, exist_ok=True)
        print(f"Created: {full_path}")
    
    return True
```

### Create Directory with Initial Files

```python
def create_directory_with_files(dir_path, files_content=None):
    """Create directory and optionally initialize with files."""
    os.makedirs(dir_path, exist_ok=True)
    
    if files_content:
        for filename, content in files_content.items():
            filepath = os.path.join(dir_path, filename)
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Created file: {filepath}")
    
    return True
```

## Error Handling

### Check Before Creating

```python
import os

def create_directory_safe_with_checks(path):
    """Create directory with comprehensive checks."""
    # Check if path is absolute or relative
    if os.path.isabs(path):
        print(f"Creating absolute path: {path}")
    else:
        print(f"Creating relative path: {path}")
    
    # Check parent directory permissions
    parent_dir = os.path.dirname(os.path.abspath(path))
    if not os.path.exists(parent_dir):
        print(f"Warning: Parent directory does not exist: {parent_dir}")
        return False
    
    # Check if it's a file, not a directory
    if os.path.isfile(path):
        print(f"Error: Path exists as a file: {path}")
        return False
    
    # Create directory
    try:
        os.makedirs(path, exist_ok=True)
        print(f"Successfully created directory: {path}")
        return True
    except PermissionError:
        print(f"Permission denied: {path}")
        return False
    except Exception as e:
        print(f"Unexpected error: {e}")
        return False
```

## Scripts

For reusable directory creation patterns, see the `scripts/` directory.

## References

For more advanced file system operations, see the references directory.
