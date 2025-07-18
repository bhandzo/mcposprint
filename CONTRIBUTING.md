# Contributing to MCPOSprint

Thank you for your interest in contributing to MCPOSprint! This document provides guidelines for contributing to this MCP server for thermal printer task card generation.

## Development Setup

### Prerequisites
- Python 3.10+
- [uv](https://docs.astral.sh/uv/) for dependency management
- USB thermal printer (optional, for testing)
- Notion API access (optional, for Notion integration testing)

### Getting Started

1. **Fork and clone the repository**
   ```bash
   git clone https://github.com/your-username/mcposprint.git
   cd mcposprint
   ```

2. **Install dependencies**
   ```bash
   uv sync --all-extras
   ```

3. **Set up environment**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

4. **Run the MCP server**
   ```bash
   uv run mcposprint
   ```

## Project Structure

```
mcposprint/
   mcposprint/           # Main package
      core/            # Core functionality
      parsers/         # Input parsers (markdown, Notion)
      generators/      # Card image generation
      printers/        # Printer interfaces
   server.py           # MCP server entry point
   tests/              # Test suite (future)
   docs/               # Documentation (future)
```

## Code Style

### Python Code Standards
- Follow PEP 8
- Use type hints where possible
- Keep functions focused and small
- Add docstrings for public functions

### Formatting Tools
```bash
# Format code
black mcposprint/
isort mcposprint/

# Type checking
mypy mcposprint/
```

## MCP Tool Development

When adding new MCP tools:

1. **Define in server.py**
   ```python
   @mcp.tool()
   async def your_new_tool(param: str, ctx: Context = None) -> str:
       """Tool description"""
       if ctx:
           ctx.info("Starting operation...")
       # Implementation
       return "result"
   ```

2. **Add progress tracking for long operations**
   ```python
   for i, item in enumerate(items):
       if ctx:
           await ctx.report_progress(i, len(items))
           ctx.info(f"Processing {item}")
   ```

3. **Handle errors gracefully**
   ```python
   try:
       # operation
   except Exception as e:
       if ctx:
           ctx.info(f"L Error: {str(e)}")
       raise
   ```

## Testing

### Running Tests
```bash
# Run all tests (when available)
pytest

# Run with coverage
pytest --cov=mcposprint
```

### Testing MCP Tools
- Test each tool individually
- Verify progress reporting works
- Test error handling
- Check timeout behavior

## Pull Request Process

1. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes**
   - Follow the code style guidelines
   - Add tests if applicable
   - Update documentation

3. **Test your changes**
   ```bash
   # Run the MCP server
   uv run mcposprint
   
   # Test with an MCP client
   # Verify your changes work as expected
   ```

4. **Commit and push**
   ```bash
   git add .
   git commit -m "Add: your feature description"
   git push origin feature/your-feature-name
   ```

5. **Create a pull request**
   - Provide a clear description of your changes
   - Reference any related issues
   - Include testing instructions

## Issue Reporting

When reporting issues:

1. **Use the run_diagnostics tool** to gather system information
2. **Include your environment details** (OS, Python version, printer model)
3. **Provide reproduction steps**
4. **Include relevant error messages**

## Areas for Contribution

### High Priority
- **Test suite development** - Add comprehensive tests
- **Error handling improvements** - Better error messages and recovery
- **Documentation** - API docs, examples, tutorials

### Medium Priority
- **New printer support** - Additional ESC/POS printer models
- **Card templates** - More design options
- **Performance optimizations** - Faster image generation

### Low Priority
- **Additional parsers** - Support for other task sources
- **Export formats** - PDF, SVG output options
- **UI tools** - Configuration helpers

## Questions?

- **Documentation**: Check the README.md
- **Issues**: Create a GitHub issue
- **Discussions**: Use GitHub Discussions for general questions

## Code of Conduct

- Be respectful and inclusive
- Focus on constructive feedback
- Help others learn and contribute
- Follow the project's technical standards

Thank you for contributing to MCPOSprint!