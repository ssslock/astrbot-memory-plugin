# Directory Creation Reference

## Cross-Platform Considerations

### Path Separators
- Unix/Linux/macOS: `/`
- Windows: `\` (but Python handles both)
- Always use `os.path.join()` for cross-platform compatibility

### Special Characters to Avoid
Avoid these characters in directory names:
- `< > : " | ? *` (Windows restrictions)
- `/` and `\` (path separators)
- Null character `\0`
- Leading/trailing spaces

### Maximum Path Lengths
- Windows: 260 characters (MAX_PATH)
- Linux/macOS: Typically much longer (4096 characters)
- Consider using relative paths for deep nesting

## Python Functions Comparison

### os.mkdir() vs os.makedirs()
- `os.mkdir(path)`: Creates single directory, parent must exist
- `os.makedirs(path, exist_ok=True)`: Creates intermediate directories, handles existing

### pathlib (Modern Alternative)
```python
from pathlib import Path

# Create directory
Path("my_directory").mkdir(parents=True, exist_ok=True)

# Create nested structure
Path("a/b/c").mkdir(parents=True, exist_ok=True)
```

## Common Use Cases

### 1. Temporary Directories
```python
import tempfile
import shutil

# Create temporary directory
temp_dir = tempfile.mkdtemp()
print(f"Created temp directory: {temp_dir}")

# Clean up when done
shutil.rmtree(temp_dir)
```

### 2. User-Specific Directories
```python
import os
from pathlib import Path

# Get user home directory
home = Path.home()

# Create application directory
app_dir = home / ".myapp" / "data"
app_dir.mkdir(parents=True, exist_ok=True)
```

### 3. Project Template Structure
```python
def create_python_project(project_name):
    structure = [
        f"{project_name}/",
        f"{project_name}/__init__.py",
        f"{project_name}/src/",
        f"{project_name}/tests/",
        f"{project_name}/docs/",
        f"{project_name}/requirements.txt",
        f"{project_name}/README.md",
        f"{project_name}/.gitignore",
    ]
    
    for item in structure:
        if item.endswith('/'):
            os.makedirs(item, exist_ok=True)
        else:
            # Create empty file
            with open(item, 'w') as f:
                pass
```

## Error Codes and Handling

### Common Exceptions
1. `FileExistsError`: Directory already exists (without `exist_ok=True`)
2. `PermissionError`: Insufficient permissions
3. `FileNotFoundError`: Parent directory doesn't exist
4. `OSError`: General filesystem error

### Recovery Strategies
1. Check permissions first
2. Use `exist_ok=True` to ignore existing directories
3. Create parent directories if needed
4. Provide user-friendly error messages

## Performance Considerations

1. **Batch Operations**: Create multiple directories at once when possible
2. **Exist Check**: `os.path.exists()` is fast, but `exist_ok=True` handles it internally
3. **Network Drives**: Be aware of latency on network filesystems
4. **Symbolic Links**: Handle symlinks appropriately in your use case
