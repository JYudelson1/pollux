# Files Tool

Secure file operations within a reserved directory, providing read, write, and listing capabilities with path traversal protection.

## Usage

### XML Interface
```xml
<!-- Write to file -->
<file_write path="example.txt" mode="overwrite">content</file_write>

<!-- Read from file -->
<file_read path="example.txt"></file_read>

<!-- List files -->
<file_list path="subdirectory"></file_list>
```

### Attributes

#### file_write
- `path`: String (required) - Relative path within reserved directory
- `mode`: String (optional, default="overwrite")
  - "overwrite": Replace existing content
  - "append": Add to existing content

#### file_read
- `path`: String (required) - Relative path within reserved directory

#### file_list
- `path`: String (optional) - Subdirectory to list, defaults to root

### Examples
```xml
<!-- Write new file -->
<file_write path="notes/todo.txt">- First item
- Second item</file_write>

<!-- Append to file -->
<file_write path="notes/todo.txt" mode="append">- New item</file_write>

<!-- List directory contents -->
<file_list path="notes"></file_list>
```

## Implementation Details

### Security Features
- Path traversal prevention
- Operations restricted to base directory
- Parent directory verification

### Base Directory
- Located at ROOT/data/files
- All paths are relative to this directory
- Automatic parent directory creation

### Error Handling
- ValueError for path traversal attempts
- FileNotFoundError for missing files/directories
- Clear error messages with path information

## Development Notes

### Testing Considerations
- Path traversal prevention
- Directory creation
- File modes (append vs overwrite)
- Unicode content handling

### Future Improvements
- File deletion capability
- File move/rename operations
- Directory operations
- Metadata operations