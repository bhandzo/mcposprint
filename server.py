
#!/usr/bin/env python3
from mcp.server.fastmcp import FastMCP, Context
from mcposprint import TaskCardPrinter, Config
from pathlib import Path

mcp = FastMCP("MCPOSprint")

@mcp.tool()
def process_static_cards(file: str, no_print: bool = False) -> list[str]:
    """Process static markdown cards"""
    config = Config()
    printer = TaskCardPrinter(config)
    print_cards = not no_print
    generated_files = printer.process_static_cards(file, print_cards=print_cards)
    return generated_files

@mcp.tool()
async def process_notion_tasks(no_print: bool = False, ctx: Context = None) -> list[str]:
    """Process today's Notion tasks with progress tracking"""
    config = Config()
    if not config.has_notion_config:
        raise ValueError("Notion not configured. Run --setup to create configuration files.")
    
    if ctx:
        ctx.info("Initializing Notion task processing...")
    
    printer = TaskCardPrinter(config)
    print_cards = not no_print
    
    try:
        if ctx:
            ctx.info("Fetching tasks from Notion API...")
        
        # Get tasks from Notion
        from mcposprint.parsers.notion import NotionParser
        notion_parser = NotionParser(config)
        tasks = notion_parser.get_todays_tasks()
        
        if ctx:
            ctx.info(f"✅ API Success: Found {len(tasks)} tasks")
            if len(tasks) == 0:
                ctx.info("No tasks found for today")
                return []
        
        generated_files = []
        
        # Process each task with progress reporting
        for i, task in enumerate(tasks):
            if ctx:
                await ctx.report_progress(i, len(tasks))
                ctx.info(f"Processing task {i+1}/{len(tasks)}: {task.get('title', 'Unknown')}")
            
            # Generate card for this task
            from mcposprint.generators.card import CardGenerator
            card_gen = CardGenerator(config)
            image_path = card_gen.generate_card(task, f"notion_task_{i+1:02d}")
            generated_files.append(str(image_path))
            
            if ctx:
                ctx.info(f"✅ Generated: {image_path}")
            
            # Print if requested
            if print_cards:
                try:
                    from PIL import Image
                    img = Image.open(image_path)
                    is_last = (i == len(tasks) - 1)
                    success = printer.printer.print_image(img, cut_after=True, is_last_card=is_last)
                    
                    if ctx:
                        if success:
                            ctx.info(f"✅ Print Success: {task.get('title', 'Unknown')}")
                        else:
                            ctx.info(f"❌ Print Failed: {task.get('title', 'Unknown')}")
                except Exception as e:
                    if ctx:
                        ctx.info(f"❌ Print Error: {task.get('title', 'Unknown')} - {str(e)}")
        
        if ctx:
            ctx.info(f"✅ Processing complete: {len(generated_files)} cards generated")
            if print_cards:
                ctx.info("All cards sent to printer")
        
        return generated_files
        
    except Exception as e:
        if ctx:
            ctx.info(f"❌ Error: {str(e)}")
        raise

@mcp.tool()
def print_only(directory: str) -> str:
    """Print existing images from directory"""
    import glob
    config = Config()
    printer = TaskCardPrinter(config)
    print_dir = Path(directory)
    if not print_dir.exists():
        return f"Directory not found: {directory}"
    
    image_files = []
    for pattern in ['*.png', '*.jpg', '*.jpeg']:
        image_files.extend(glob.glob(str(print_dir / pattern)))
    
    if not image_files:
        return f"No image files found in: {directory}"
    
    image_files.sort()
    
    success_count = 0
    for i, image_file in enumerate(image_files):
        from PIL import Image
        try:
            img = Image.open(image_file)
            is_last = (i == len(image_files) - 1)
            success = printer.printer.print_image(img, cut_after=True, is_last_card=is_last)
            if success:
                success_count += 1
        except Exception as e:
            return f"Error printing {Path(image_file).name}: {e}"
            
    return f"Successfully printed {success_count}/{len(image_files)} images"

@mcp.tool()
def test_printer_connection() -> str:
    """Test printer connection"""
    config = Config()
    printer = TaskCardPrinter(config)
    success = printer.test_printer_connection()
    return "Printer connection successful" if success else "Printer connection failed"

@mcp.tool()
def run_diagnostics() -> dict:
    """Run full diagnostics"""
    config = Config()
    printer = TaskCardPrinter(config)
    diagnostics = printer.run_diagnostics()
    return diagnostics

@mcp.tool()
def create_sample_files() -> str:
    """Create sample configuration files"""
    config = Config()
    printer = TaskCardPrinter(config)
    printer.create_sample_files()
    return "Sample files created"

@mcp.resource("image://thermal-card-size")
def get_thermal_card_size() -> str:
    """Get thermal printer card size specifications"""
    return """Thermal Card Size Specifications:
- Width: 384 pixels (48mm at 203 DPI)
- Height: Variable (typically 200-400 pixels)
- DPI: 203 (8 dots/mm)
- Format: PNG recommended
- Color: Monochrome (black and white)
- Margins: 8px on all sides recommended"""

def main():
    """Entry point for script execution"""
    mcp.run()

if __name__ == "__main__":
    main()
