# Source Tool

Tool for reading the AI's own source code, enabling self-inspection and documentation capabilities.

## Usage

### XML Interface
```xml
<!-- Read source file -->
<src_read path="tools/memory/__init__.py"></src_read>

<!-- List source files -->
<src_list path="tools"></src_list>
```

### Attributes

#### src_read
- `path`: String (required) - Relative path within source directory

#### src_list
- `path`: String (optional) - Directory to list, defaults to root

### Examples
```xml
<!-- Read implementation file -->
<src_read path="scaffolding/xml_parser.py"></src_read>

<!-- List tool implementations -->
<src_list path="tools"></src_list>
```

## Implementation Details

### Base Directory
- Located at ROOT/src
- All paths are relative to this directory

### Error Handling
- FileNotFoundError for missing files
- ValueError for invalid paths
- Clear error messages

## Development Notes

### Security Considerations
- Read-only operations
- No execution capabilities
- Path validation

### Future Improvements
- Code search capabilities
- Documentation generation
- Implementation analysis tools
- Dependency mapping