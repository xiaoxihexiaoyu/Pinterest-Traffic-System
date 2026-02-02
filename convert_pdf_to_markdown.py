#!/usr/bin/env python3
"""
PDF to Markdown Converter
Converts PDF files to Markdown format with image extraction
"""

import os
import sys
import re
import json
from pathlib import Path
from typing import List, Dict, Tuple
from dataclasses import dataclass

try:
    import fitz  # PyMuPDF
except ImportError:
    print("Installing PyMuPDF...")
    os.system("pip3 install PyMuPDF -q")
    import fitz


@dataclass
class DocumentInfo:
    """Document information for summary"""
    title: str
    page_count: int
    has_images: bool
    image_count: int = 0
    word_count: int = 0


class PDFToMarkdownConverter:
    """Convert PDF to Markdown with image extraction"""
    
    def __init__(self, source_dir: str, output_dir: str, assets_dir: str):
        self.source_dir = Path(source_dir)
        self.output_dir = Path(output_dir)
        self.assets_dir = Path(assets_dir)
        self.assets_dir.mkdir(parents=True, exist_ok=True)
        
    def sanitize_filename(self, filename: str) -> str:
        """Sanitize filename for markdown output"""
        # Remove .pdf extension
        name = filename.replace('.pdf', '')
        # Replace problematic characters
        name = name.replace('–', '-').replace('—', '-')
        name = name.replace('_', ' ')
        # Clean up multiple spaces
        name = re.sub(r'\s+', ' ', name)
        return name.strip()
    
    def extract_images_from_page(self, page, doc_name: str, page_num: int) -> List[str]:
        """Extract images from a page and return their relative paths"""
        image_list = page.get_images()
        image_paths = []
        
        for img_index, img in enumerate(image_list):
            try:
                xref = img[0]
                base_image = doc_name.replace(' ', '_').replace('/', '_')
                img_filename = f"{base_image}_page{page_num+1}_img{img_index+1}.png"
                img_path = self.assets_dir / img_filename
                
                # Extract image
                pix = fitz.Pixmap(page.parent, xref)
                
                # Handle CMYK images
                if pix.n >= 5:
                    pix = fitz.Pixmap(fitz.csRGB, pix)
                
                # Save image
                pix.save(str(img_path))
                pix = None
                
                # Relative path for markdown
                rel_path = f"assets/06-Automation_Tools/{img_filename}"
                image_paths.append(rel_path)
                
            except Exception as e:
                print(f"    Warning: Could not extract image {img_index} from page {page_num+1}: {e}")
                continue
        
        return image_paths
    
    def analyze_document(self, doc: fitz.Document) -> DocumentInfo:
        """Analyze document and return summary info"""
        total_images = 0
        total_words = 0
        
        for page in doc:
            images = page.get_images()
            total_images += len(images)
            text = page.get_text()
            total_words += len(text.split())
        
        # Try to get title from first page
        first_page_text = doc[0].get_text()
        lines = first_page_text.split('\n')
        title = lines[0][:100] if lines else "Untitled"
        
        return DocumentInfo(
            title=title.strip(),
            page_count=len(doc),
            has_images=total_images > 0,
            image_count=total_images,
            word_count=total_words
        )
    
    def convert_pdf(self, pdf_path: Path) -> Tuple[bool, str]:
        """Convert a single PDF to Markdown"""
        print(f"  Converting: {pdf_path.name}")
        
        try:
            # Open PDF
            doc = fitz.open(str(pdf_path))
            
            # Analyze document
            doc_info = self.analyze_document(doc)
            
            # Generate output filename
            md_filename = self.sanitize_filename(pdf_path.name) + ".md"
            md_path = self.output_dir / md_filename
            
            # Prepare markdown content
            md_content = []
            
            # Add document summary at the top
            md_content.append(f"# {doc_info.title}\n")
            md_content.append("---\n")
            md_content.append("## Document Summary\n\n")
            md_content.append(f"- **Pages**: {doc_info.page_count}\n")
            md_content.append(f"- **Images**: {doc_info.image_count}\n")
            md_content.append(f"- **Words**: {doc_info.word_count}\n")
            md_content.append(f"- **Source**: {pdf_path.name}\n")
            md_content.append("\n---\n\n")
            
            # Extract content page by page
            all_images = {}
            
            for page_num, page in enumerate(doc):
                # Extract images first
                images = self.extract_images_from_page(page, md_filename.replace('.md', ''), page_num)
                if images:
                    all_images[page_num] = images
                
                # Get text blocks with positions
                blocks = page.get_text("blocks")
                
                # Sort blocks by vertical position (top to bottom)
                blocks.sort(key=lambda b: (b[1], b[0]))
                
                # Process each block
                for block in blocks:
                    if block[6] == 0:  # Text block
                        text = block[4].strip()
                        if text:
                            # Add to markdown
                            md_content.append(text + "\n")
            
            # Close document
            doc.close()
            
            # Write markdown file
            with open(md_path, 'w', encoding='utf-8') as f:
                f.write(''.join(md_content))
            
            print(f"    -> Saved: {md_filename} ({doc_info.page_count} pages, {doc_info.image_count} images)")
            return True, str(md_path)
            
        except Exception as e:
            error_msg = f"Error converting {pdf_path.name}: {e}"
            print(f"    ERROR: {error_msg}")
            return False, error_msg


def main():
    """Main conversion function"""
    source_dir = "/Users/xiaoyu/Downloads/NicheGrowNerd_Pin_Scale_System_SLENDERMAN_BBHF"
    output_dir = "/Users/xiaoyu/Downloads/Pin_Scale_System_Converted/06-Automation_Tools"
    assets_dir = "/Users/xiaoyu/Downloads/Pin_Scale_System_Converted/assets/06-Automation_Tools"
    
    # Files to convert
    files_to_convert = [
        "67-1._The_Ugly_Truth_About_Underperforming_Pins.pdf",
        "68-2._The_3_Automations_–_Choose_Your_Weapon.pdf",
        "69-2.a_The_Quick_Fix_–_Simple_Version.pdf",
        "70-2.b_The_Power_Scrubber_-_Delete_Pins_Across_All_Boards.pdf",
        "71-2.c_The_Precision_Cleaner_-_Delete_Pins_in_One_Specific_Board.pdf",
        "72-3._How_to_Set_It_Up_in_make.com.pdf",
        "73-4._For_Pros_Only__Mastering_the_Filters.pdf",
        "74-5._Automate_with_Intention.pdf",
        "75-The_Quick_Fix_–_Simple_Version_(Limited_to_250_pins_-_board).blueprint.json.pdf",
        "76-The_Power_Scrubber_-_Delete_Pins_Across_All_Boards.blueprint.json.pdf",
        "77-The_Precision_Cleaner_-_Delete_Pins_in_One_Board.blueprint.json.pdf",
        "78-Third-Party_Tools_vs._Native.pdf",
    ]
    
    # Create converter
    converter = PDFToMarkdownConverter(source_dir, output_dir, assets_dir)
    
    # Convert each file
    results = {"success": [], "failed": []}
    
    print(f"\n=== PDF to Markdown Converter ===")
    print(f"Output directory: {output_dir}")
    print(f"Assets directory: {assets_dir}")
    print(f"\nConverting {len(files_to_convert)} files...\n")
    
    for filename in files_to_convert:
        pdf_path = Path(source_dir) / filename
        
        if not pdf_path.exists():
            print(f"  WARNING: File not found: {filename}")
            results["failed"].append((filename, "File not found"))
            continue
        
        success, result = converter.convert_pdf(pdf_path)
        
        if success:
            results["success"].append((filename, result))
        else:
            results["failed"].append((filename, result))
    
    # Print summary
    print("\n=== Conversion Summary ===")
    print(f"Successful: {len(results['success'])}")
    print(f"Failed: {len(results['failed'])}")
    
    if results['failed']:
        print("\nFailed files:")
        for filename, error in results['failed']:
            print(f"  - {filename}: {error}")
    
    print(f"\nOutput files saved to: {output_dir}")
    print(f"Images saved to: {assets_dir}")


if __name__ == "__main__":
    main()
