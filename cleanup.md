# MCPOSprint Cleanup Plan

## Overview
Convert TaskBlaster to MCPOSprint - a clean MCP server for thermal printer task card generation.

## Files/Directories to Remove

### Docker Components
- `Dockerfile` - Docker container configuration
- `docker-compose.yml` - Docker compose setup
- `docker-compose.override.yml.example` - Docker compose override example
- `docker-test.sh` - Docker testing script
- `docker/` - Docker-related directory

### Electron Application
- `electron-app/` - Entire Electron application directory and contents

### CLI Components
- `main.py` - CLI entry point (191 lines of CLI argument parsing and handling)

### Test/Output Directories (Legacy)
- `initial_files/` - Old implementation files
- `output/` - Generated output files
- `test_outputs/` - Test output directories
- `markdown/` - Sample markdown files
- `sample_cards.md` - Sample cards file (root level)
- `test_escpos.py` - Test script

## Files to Update

### pyproject.toml
- Change project name from "taskblaster" to "mcposprint"
- Remove CLI script entry: `taskblaster = "main:main"`
- Update description to "MCP server for thermal printer task card generation"
- Update keywords to reflect MCP server purpose
- Update classifiers to reflect MCP server purpose
- Remove console environment classifier
- Update package name in hatch config

### server.py
- Update MCP server name from "TaskBlaster" to "MCPOSprint"

### Package Directory
- Rename `taskblaster/` directory to `mcposprint/`
- Update all import statements from `taskblaster` to `mcposprint`

### Dependencies to Review
- Keep core functionality: pillow, qrcode, requests, python-dotenv, python-escpos, pyusb
- Keep MCP dependency: mcp[cli]>=1.10.1
- Review if all current dependencies are needed for MCP server only

## Files to Keep
- `server.py` - Main MCP server implementation (rename project reference)
- `mcposprint/` - Core library package (renamed from taskblaster/)
- `config/` - Configuration directory
- `README.md` - Update to reflect MCPOSprint MCP server focus
- `pyproject.toml` - Update as described above
- `uv.lock` - Dependency lock file (will need regeneration)
- `.env.example` - Environment configuration example

## Post-Cleanup Actions
1. Rename project directory from taskblaster to mcposprint
2. Update README.md to focus on MCPOSprint MCP server setup and usage
3. Update pyproject.toml metadata, name, and dependencies
4. Update server.py MCP server name
5. Update all import statements throughout codebase
6. Regenerate uv.lock after dependency changes
7. Test MCP server functionality
8. Remove any Docker/CLI references from documentation
9. Ensure all MCP tools work correctly without CLI dependencies

## Directory Structure After Cleanup
```
mcposprint/
├── server.py              # MCP server entry point
├── mcposprint/            # Core library (renamed)
│   ├── __init__.py
│   ├── core/
│   ├── generators/
│   ├── parsers/
│   └── printers/
├── config/                # Configuration files
├── pyproject.toml         # Updated project config
├── uv.lock               # Dependencies
├── README.md             # Updated documentation
└── .env.example          # Environment example
```

This cleanup will result in MCPOSprint - a focused MCP server for thermal printer task card generation without the complexity of multiple deployment methods and interfaces.