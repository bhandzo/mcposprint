"""Main TaskCardPrinter class that orchestrates all components"""

from typing import List, Dict, Any, Optional
from pathlib import Path
from .config import Config
from ..parsers.markdown import MarkdownParser
from ..parsers.notion import NotionParser
from ..generators.card import CardGenerator
from ..printers.escpos_printer import EscposPrinter

class TaskCardPrinter:
    """Main class for generating and printing task cards"""
    
    def __init__(self, config: Optional[Config] = None):
        self.config = config or Config()
        
        # Initialize components
        self.markdown_parser = MarkdownParser()
        self.card_generator = CardGenerator(self.config)
        
        # Initialize ESC/POS printer
        self.printer = EscposPrinter(self.config)
        print("🖨️ Using ESC/POS direct USB printing")
        
        # Initialize Notion parser only if configured
        self.notion_parser = None
        if self.config.has_notion_config:
            try:
                self.notion_parser = NotionParser(self.config)
            except ValueError as e:
                print(f"⚠️ Notion not configured: {e}")
    
    def process_static_cards(self, markdown_file: str, print_cards: bool = True) -> List[str]:
        """Process static markdown cards and optionally print them"""
        print(f"📖 Processing static cards from: {markdown_file}")
        
        try:
            # Parse markdown file
            cards = self.markdown_parser.parse_file(markdown_file)
            print(f"📋 Found {len(cards)} cards")
            
            generated_files = []
            
            for i, card in enumerate(cards):
                print(f"\n🎨 Generating card {i+1}/{len(cards)}: {card['title']}")
                
                # Generate card image
                img = self.card_generator.create_static_card_image(card)
                
                # Save image
                output_path = Path(self.config.output_dir) / f"card_{i+1:02d}_{card['title'][:20].replace(' ', '_')}.png"
                img.save(output_path, 'PNG', dpi=(203, 203))
                generated_files.append(str(output_path))
                print(f"💾 Saved: {output_path}")
                
                # Print if requested
                if print_cards:
                    is_last = (i == len(cards) - 1)
                    success = self.printer.print_image(img, cut_after=True, is_last_card=is_last)
                    if not success:
                        print(f"❌ Failed to print card {i+1}")
            
            print(f"\n✅ Processed {len(cards)} static cards")
            return generated_files
            
        except Exception as e:
            print(f"❌ Error processing static cards: {e}")
            raise
    
    def process_notion_tasks(self, print_cards: bool = True) -> List[str]:
        """Process Notion tasks and optionally print them"""
        if not self.notion_parser:
            raise ValueError("Notion not configured")
        
        print("🔄 Fetching today's tasks from Notion...")
        
        try:
            # Fetch tasks from Notion
            tasks = self.notion_parser.get_todays_tasks()
            print(f"📋 Found {len(tasks)} tasks for today")
            
            if not tasks:
                print("ℹ️ No tasks found for today")
                return []
            
            generated_files = []
            
            for i, task in enumerate(tasks):
                print(f"\n🎨 Generating card {i+1}/{len(tasks)}: {task['title']}")
                
                # Generate card image
                img = self.card_generator.create_notion_card_image(task)
                
                # Save image
                output_path = Path(self.config.output_dir) / f"notion_task_{i+1:02d}_{task['title'][:20].replace(' ', '_')}.png"
                img.save(output_path, 'PNG', dpi=(203, 203))
                generated_files.append(str(output_path))
                print(f"💾 Saved: {output_path}")
                
                # Print if requested
                if print_cards:
                    is_last = (i == len(tasks) - 1)
                    success = self.printer.print_image(img, cut_after=True, is_last_card=is_last)
                    if not success:
                        print(f"❌ Failed to print task {i+1}")
            
            print(f"\n✅ Processed {len(tasks)} Notion tasks")
            return generated_files
            
        except Exception as e:
            print(f"❌ Error processing Notion tasks: {e}")
            raise
    
    def test_printer_connection(self) -> bool:
        """Test printer connection"""
        print("🔧 Testing printer connection...")
        return self.printer.test_connection()
    
    def test_notion_connection(self) -> bool:
        """Test Notion API connection"""
        if not self.notion_parser:
            print("❌ Notion not configured")
            return False
        
        print("🔧 Testing Notion connection...")
        return self.notion_parser.test_connection()
    
    def run_diagnostics(self) -> Dict[str, Any]:
        """Run comprehensive diagnostics"""
        print("🔍 Running diagnostics...")
        
        diagnostics = {
            'config': self.config.validate(),
            'printer': self.printer.get_printer_status(),
            'notion': None,
            'output_dir': Path(self.config.output_dir).exists()
        }
        
        # Test Notion if configured
        if self.notion_parser:
            diagnostics['notion'] = {
                'configured': True,
                'connection': self.notion_parser.test_connection()
            }
        else:
            diagnostics['notion'] = {
                'configured': False,
                'connection': False
            }
        
        # Print diagnostics
        print("\n📊 Diagnostic Results:")
        print(f"✅ Config errors: {len(diagnostics['config'])}")
        if diagnostics['config']:
            for error in diagnostics['config']:
                print(f"  ❌ {error}")
        
        print(f"✅ Output directory: {'✅' if diagnostics['output_dir'] else '❌'}")
        
        printer_status = diagnostics['printer']
        print(f"✅ USB device found: {'✅' if printer_status['usb_device_found'] else '❌'}")
        print(f"✅ Printer exists: {'✅' if printer_status['printer_exists'] else '❌'}")
        print(f"✅ Printer ready: {'✅' if printer_status['printer_ready'] else '❌'}")
        
        # Show printer error messages if any
        if printer_status['error_messages']:
            for error in printer_status['error_messages']:
                print(f"  ⚠️  {error}")
        
        notion_status = diagnostics['notion']
        print(f"✅ Notion configured: {'✅' if notion_status['configured'] else '❌'}")
        print(f"✅ Notion connection: {'✅' if notion_status['connection'] else '❌'}")
        
        # Overall status
        has_issues = (
            bool(diagnostics['config']) or 
            not diagnostics['output_dir'] or
            not printer_status['usb_device_found'] or
            (notion_status['configured'] and not notion_status['connection'])
        )
        
        print(f"\n🎯 Overall Status: {'❌ ISSUES FOUND' if has_issues else '✅ ALL SYSTEMS GO'}")
        
        return diagnostics
    
    def create_sample_files(self):
        """Create sample markdown file for testing card generation"""
        print("📝 Creating sample markdown file...")
        
        # Create sample markdown file
        markdown_content = self.markdown_parser.create_sample_markdown()
        markdown_path = Path("sample_cards.md")
        markdown_path.write_text(markdown_content)
        print(f"💾 Created: {markdown_path}")
        
        print("✅ Sample markdown file created successfully")
        print("ℹ️  Configuration is handled via environment variables in your Claude Desktop MCP configuration") 