# TaskBlaster - ADHD Task Card Printer

A modular system for generating and printing task cards from markdown and Notion. Optimized for thermal printers with direct USB ESC/POS printing and Docker containerization.

## Features

✅ **Static Cards**: Generate cards from markdown files  
✅ **Notion Integration**: Fetch and print today's tasks from Notion  
✅ **Thermal Printer Support**: Direct USB printing via ESC/POS protocol  
✅ **Docker Ready**: Full containerization with direct USB printer support  
✅ **Modular Architecture**: Clean separation of concerns  
✅ **QR Code Support**: Notion tasks include QR codes for quick access  

## 🚀 Installation

### Native Installation (Recommended for Printing)

For full printing functionality, install TaskBlaster natively on your system:

```bash
# Clone the repository
git clone https://github.com/your-username/taskblaster.git
cd taskblaster

# Install with uv
uv sync
uv run taskblaster --setup
```

### System Requirements
- **Python 3.11+**
- **Direct USB printing** via ESC/POS protocol
- **PIL/Pillow** for image generation
- **libusb** for USB printer access
  - macOS: `brew install libusb`
  - Ubuntu/Debian: `sudo apt install libusb-1.0-0-dev`
  - Windows: Included with python-escpos
- **Notion API access** (optional, for Notion integration)

## 🐳 Docker Usage (Full Support)

TaskBlaster supports **full printing functionality in Docker** using direct USB communication via ESC/POS protocol.

### Docker with USB Printer Support

```bash
# Build the container
docker-compose build

# Print cards directly from Docker
docker-compose run --rm printer uv run taskblaster --static markdown/sample_cards.md
docker-compose run --rm printer uv run taskblaster --notion

# Generate cards without printing
docker-compose run --rm printer uv run taskblaster --static markdown/sample_cards.md --no-print
```

### Docker Configuration for USB Printers

The `docker-compose.yml` includes:
- **privileged: true** - Required for USB device access
- **devices: /dev/bus/usb:/dev/bus/usb** - USB device mounting
- **Direct ESC/POS printing** - No additional setup required

### Printing Mode

**ESC/POS Direct USB**: Direct USB communication, no additional drivers required

```bash
# Print cards with ESC/POS
docker-compose run --rm printer uv run taskblaster --static cards.md
```

## 🖨️ Printer Setup

### Supported Printers

#### ESC/POS Compatible Thermal Printers
- **EPSON**: TM-T20III, TM-T88V, TM-T82, TM-T70
- **Star Micronics**: TSP143, TSP654, TSP100
- **Citizen**: CT-S310II, CT-S4000
- **Most USB thermal printers** supporting ESC/POS protocol

### Printer Setup

#### ESC/POS (Direct USB)
```bash
# Auto-detection (recommended)
uv run taskblaster --test-print

# List USB devices
lsusb

# Docker usage
docker-compose run --rm printer uv run taskblaster --test-print
```

## Architecture

The application is modularized into clean components:

```
taskblaster/
├── core/
│   ├── config.py      # Configuration management
│   └── printer.py     # Main orchestration class
├── parsers/
│   ├── markdown.py    # Markdown file parser
│   └── notion.py      # Notion API integration
├── generators/
│   └── card.py        # PIL-based card image generation
└── printers/
    └── escpos_printer.py  # ESC/POS direct USB interface
```

## Configuration

### Environment Variables

Create a `.env` file based on `.env.example`:

```bash
# Printer Configuration
PRINTER_NAME=EPSON_TM_T20III-17

# Notion Configuration (optional)
NOTION_API_KEY=your_notion_api_key_here
TASKS_DATABASE_ID=your_database_id_here

# Application Settings
DEBUG=false
OUTPUT_DIR=./output
```

### Notion Setup

1. Create a Notion integration at https://www.notion.so/my-integrations
2. Copy the API key to your `.env` file
3. Share your tasks database with the integration
4. Copy the database ID to your `.env` file

Database should have these properties:
- **Name** or **Task** (title)
- **Due Date** (date)
- **Priority** (select: High, Medium, Low)
- **Status** (status: Not Started, In Progress, Done)
- **Description** (rich text, optional)

## Docker Configuration

### Printer Setup

#### USB Printers (Linux hosts)
```yaml
# docker-compose.yml includes:
volumes:
  - /dev/bus/usb:/dev/bus/usb:rw
privileged: true
```

#### Printer Configuration in Container
```bash
# Enter container and test printer detection
docker-compose run taskblaster bash

# Test USB printer detection
uv run taskblaster --test-print
```

### Volume Mounts

The Docker setup includes these mounted directories:

- `./config:/app/config` - Configuration files
- `./output:/app/output` - Generated card images
- `./markdown:/app/markdown` - Markdown input files

## Usage Examples

### Command Line Options

```bash
# Basic commands (after uv sync)
uv run taskblaster --static cards.md       # Print markdown cards
uv run taskblaster --notion                # Print Notion tasks
uv run taskblaster --setup                 # Create sample files
uv run taskblaster --test-print            # Test printer
uv run taskblaster --diagnose              # Run diagnostics

# Options
uv run taskblaster --static cards.md --no-print       # Generate without printing
uv run taskblaster --output-dir /custom/path          # Custom output directory
uv run taskblaster --printer-name MY_PRINTER          # Override printer name
uv run taskblaster --debug                            # Enable debug output
```

### Markdown Format

```markdown
## Morning Routine
- *Get dressed
- Brush teeth
- Make coffee
- Check calendar

## Work Tasks
- *Review emails
- Update project status
- *Prepare for 2pm meeting
- Submit timesheet
```

- Use `## Title` for card headers
- Use `- Task` for regular tasks
- Use `- *Task` for priority tasks (marked with ★)

### Docker Commands

```bash
# One-time setup
docker-compose build
docker-compose run taskblaster taskblaster --setup

# Daily usage
docker-compose run taskblaster taskblaster --notion
docker-compose run taskblaster taskblaster --static /app/markdown/my_cards.md

# Maintenance
docker-compose run taskblaster taskblaster --diagnose
docker-compose run taskblaster bash  # Interactive shell
```

## Troubleshooting

### Common Issues

1. **Printer not found**
   ```bash
   # Test USB printer detection
uv run taskblaster --test-print

# Run full diagnostics
uv run taskblaster --diagnose
   
   # List USB devices (Linux/macOS)
   lsusb
   ```

2. **Notion connection fails**
   ```bash
   # Verify API key and database ID
   uv run taskblaster --diagnose
   
   # Check database permissions in Notion
   ```

3. **Docker printer access**
   ```bash
   # Ensure privileged mode and USB device mounting
   # Check printer detection in container:
   docker-compose run taskblaster uv run taskblaster --test-print
   ```

### Debug Mode

Enable detailed error output:
```bash
uv run taskblaster --debug --diagnose
```

### Health Check

The Docker container includes a health check:
```bash
docker-compose ps  # Check container health
```

## Development

### Local Development
```bash
# Install in development mode with dev dependencies
uv sync --all-extras

# Run tests (when available)
pytest

# Format code
black taskblaster/
isort taskblaster/

# Type checking
mypy taskblaster/
```

### Building Docker Image
```bash
# Build locally
docker build -t taskblaster .

# Build with compose
docker-compose build

# Multi-platform build
docker buildx build --platform linux/amd64,linux/arm64 -t taskblaster .
```

## License

MIT License - see LICENSE file for details.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## Changelog

### v2.0.0 (Phase 3&4)
- ✅ Modular architecture with clean separation
- ✅ Docker containerization with USB printer support
- ✅ Enhanced configuration management
- ✅ Improved error handling and diagnostics
- ✅ Comprehensive documentation
- ✅ ESC/POS direct USB printing

### v1.0.0 (Phase 1&2)
- ✅ Static markdown card generation
- ✅ Notion API integration
- ✅ Basic CLI interface
