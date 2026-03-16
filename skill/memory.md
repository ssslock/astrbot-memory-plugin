---
name: memory
description: "Use this skill for storing, retrieving, removing, and listing memory content in files. This skill provides persistent storage for text content organized in a file system within the plugin's data directory. Use it when you need to save information for later retrieval, manage stored files, or browse existing memory entries. The skill ensures all operations stay within the plugin's designated data directory for security."
license: MIT
---

# Memory Management Skill

This skill provides four operations for managing text-based memory storage in files.

## Available Tools

### store_memory
Store memory content with a relative file path.

**Parameters:**
- `relative_path` (string): The relative file path where the content should be stored.
- `content` (string): The file content to store.

**Returns:**
- "OK" if successful, otherwise an error message.

**Security:** The path is validated to ensure it stays within the plugin's data directory.

### retrieve_memory
Retrieve stored memory content with a relative file path.

**Parameters:**
- `relative_path` (string): The relative file path to retrieve.

**Returns:**
- The stored file name and content if found, or "not found" if it does not exist.

**Security:** The path is validated to ensure it stays within the plugin's data directory.

### remove_memory
Remove memory content with a relative file path.

**Parameters:**
- `relative_path` (string): The relative file path to delete.

**Returns:**
- "deleted" if successfully deleted, "not found" if file doesn't exist, or an error message.

**Security:** The path is validated to ensure it stays within the plugin's data directory.

### list_memory
List stored memory entries in a directory with a relative path.

**Parameters:**
- `relative_path` (string, optional): The relative directory path to list. Defaults to current directory (".").

**Returns:**
- A formatted list of entries with type (file/folder) and file size for files.
- Returns "not found" if the directory doesn't exist, or an error message.

**Security:** The path is validated to ensure it stays within the plugin's data directory.

## Usage Guidelines

### When to Use This Skill
- When you need to persistently store text information for later use
- When you need to retrieve previously stored information
- When you need to manage (delete or list) stored memory files
- When organizing information in a hierarchical file structure

### Security Considerations
- All paths are restricted to the plugin's data directory
- Path traversal attempts are blocked
- Only text files are supported

### Error Handling
- All tools return descriptive error messages
- "not found" indicates the file or directory doesn't exist
- "Error:" prefix indicates other issues (permissions, invalid paths, etc.)

### Performance Notes
- Suitable for small to medium text files
- For large files, consider alternative storage methods
- Directory listings may be slow for directories with many files

## Examples

### Storing Information
```
store_memory(relative_path="notes/meeting.txt", content="Meeting notes from March 15...")
```

### Retrieving Information
```
retrieve_memory(relative_path="notes/meeting.txt")
```

### Removing Information
```
remove_memory(relative_path="notes/meeting.txt")
```

### Listing Contents
```
list_memory(relative_path="notes/")
```

## Implementation Details

The skill uses the plugin's data directory located at:
`<astrbot_data_path>/plugin_data/astrbot-memory-plugin/`

All file operations are performed with UTF-8 encoding. Parent directories are automatically created when needed.
---
name: memory
description: "Use this skill for storing, retrieving, removing, and listing memory content in files. This skill provides persistent storage for text content organized in a file system within the plugin's data directory. Use it when you need to save information for later retrieval, manage stored files, or browse existing memory entries. The skill ensures all operations stay within the plugin's designated data directory for security."
license: MIT
---

# Memory Management Skill

This skill provides four operations for managing text-based memory storage in files.

## Available Tools

### store_memory
Store memory content with a relative file path.

**Parameters:**
- `relative_path` (string): The relative file path where the content should be stored.
- `content` (string): The file content to store.

**Returns:**
- "OK" if successful, otherwise an error message.

**Security:** The path is validated to ensure it stays within the plugin's data directory.

### retrieve_memory
Retrieve stored memory content with a relative file path.

**Parameters:**
- `relative_path` (string): The relative file path to retrieve.

**Returns:**
- The stored file name and content if found, or "not found" if it does not exist.

**Security:** The path is validated to ensure it stays within the plugin's data directory.

### remove_memory
Remove memory content with a relative file path.

**Parameters:**
- `relative_path` (string): The relative file path to delete.

**Returns:**
- "deleted" if successfully deleted, "not found" if file doesn't exist, or an error message.

**Security:** The path is validated to ensure it stays within the plugin's data directory.

### list_memory
List stored memory entries in a directory with a relative path.

**Parameters:**
- `relative_path` (string, optional): The relative directory path to list. Defaults to current directory (".").

**Returns:**
- A formatted list of entries with type (file/folder) and file size for files.
- Returns "not found" if the directory doesn't exist, or an error message.

**Security:** The path is validated to ensure it stays within the plugin's data directory.

## Usage Guidelines

### When to Use This Skill
- When you need to persistently store text information for later use
- When you need to retrieve previously stored information
- When you need to manage (delete or list) stored memory files
- When organizing information in a hierarchical file structure

### Security Considerations
- All paths are restricted to the plugin's data directory
- Path traversal attempts are blocked
- Only text files are supported

### Error Handling
- All tools return descriptive error messages
- "not found" indicates the file or directory doesn't exist
- "Error:" prefix indicates other issues (permissions, invalid paths, etc.)

### Performance Notes
- Suitable for small to medium text files
- For large files, consider alternative storage methods
- Directory listings may be slow for directories with many files

## Examples

### Storing Information
```
store_memory(relative_path="notes/meeting.txt", content="Meeting notes from March 15...")
```

### Retrieving Information
```
retrieve_memory(relative_path="notes/meeting.txt")
```

### Removing Information
```
remove_memory(relative_path="notes/meeting.txt")
```

### Listing Contents
```
list_memory(relative_path="notes/")
```

## Implementation Details

The skill uses the plugin's data directory located at:
`<astrbot_data_path>/plugin_data/astrbot-memory-plugin/`

All file operations are performed with UTF-8 encoding. Parent directories are automatically created when needed.
