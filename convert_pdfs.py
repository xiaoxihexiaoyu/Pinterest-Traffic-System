#!/usr/bin/env python3
"""
PDF to Markdown Converter
Converts PDF files to Markdown format with image extraction
"""

import os
import re
import fitz  # PyMuPDF
from pathlib import Path
from typing import List, Tuple

# Smart quote characters
LEFT_SINGLE_QUOTE = '\u2018'
RIGHT_SINGLE_QUOTE = '\u2019'
LEFT_DOUBLE_QUOTE = '\u201c'
RIGHT_DOUBLE_QUOTE = '\u201d'
EM_DASH = '\u2014'
EN_DASH = '\u2013'


class PDFToMarkdownConverter:
    def __init__(self, source_dir: str, output_dir: str, assets_dir: str):
        self.source_dir = source_dir
        self.output_dir = output_dir
        self.assets_dir = assets_dir
        Path(self.output_dir).mkdir(parents=True, exist_ok=True)
        Path(self.assets_dir).mkdir(parents=True, exist_ok=True)

    def sanitize_filename(self, filename: str) -> str:
        """Sanitize filename for safe use"""
        # Remove or replace problematic characters
        filename = re.sub(r'[<>:"|?*]', '', filename)
        filename = filename.replace("'", "")
        filename = filename.replace('"', '')
        # Replace smart quotes
        filename = filename.replace(LEFT_DOUBLE_QUOTE, '').replace(RIGHT_DOUBLE_QUOTE, '')
        filename = filename.replace(LEFT_SINGLE_QUOTE, "'").replace(RIGHT_SINGLE_QUOTE, "'")
        filename = filename.replace(EM_DASH, '-').replace(EN_DASH, '-')
        return filename

    def extract_images_from_page(self, page, doc_name: str, page_num: int) -> List[Tuple[str, str]]:
        """Extract images from a PDF page"""
        image_list = []
        
        try:
            # Get list of images on the page
            images = page.get_images(full=True)
            
            for img_index, img in enumerate(images):
                try:
                    xref = img[0]
                    base_image = page.parent.extract_image(xref)
                    
                    if base_image:
                        image_bytes = base_image["image"]
                        image_ext = base_image["ext"]
                        
                        # Generate filename
                        image_filename = f"{doc_name}_page{page_num + 1}_img{img_index + 1}.{image_ext}"
                        image_path = os.path.join(self.assets_dir, image_filename)
                        
                        # Save image
                        with open(image_path, "wb") as img_file:
                            img_file.write(image_bytes)
                        
                        image_list.append((image_filename, f"assets/09-FAQ_Advanced/{image_filename}"))
                except Exception:
                    continue
        except Exception:
            pass
        
        return image_list

    def extract_text_with_structure(self, page) -> str:
        """Extract text while preserving structure"""
        try:
            # Get text blocks
            blocks = page.get_text("blocks")
            
            if not blocks:
                return page.get_text()
            
            markdown_lines = []
            
            for block in blocks:
                if len(block) < 4:
                    continue
                
                bbox = block[0:4]  # x0, y0, x1, y1
                text = block[4]
                
                if not text or not text.strip():
                    continue
                
                text = text.strip()
                
                # Detect headings (all caps or ends with colon, usually larger)
                lines = text.split('\n')
                for line in lines:
                    line = line.strip()
                    if not line:
                        continue
                    
                    # Skip very short lines (likely artifacts)
                    if len(line) < 2:
                        continue
                    
                    # Detect potential headings
                    if line.isupper() and len(line) < 50:
                        markdown_lines.append(f"\n### {line}\n")
                    elif line.endswith(':') and len(line) < 80:
                        markdown_lines.append(f"\n#### {line}\n")
                    else:
                        markdown_lines.append(line + " ")
            
            return "\n".join(markdown_lines)
        except Exception:
            return page.get_text()

    def convert_pdf_to_markdown(self, pdf_filename: str) -> str:
        """Convert a single PDF file to Markdown"""
        pdf_path = os.path.join(self.source_dir, pdf_filename)
        
        if not os.path.exists(pdf_path):
            print(f"  File not found: {pdf_path}")
            return ""
        
        # Generate output filename
        base_name = os.path.splitext(pdf_filename)[0]
        doc_name = self.sanitize_filename(base_name)
        md_filename = f"{base_name}.md"
        md_path = os.path.join(self.output_dir, md_filename)
        
        print(f"Converting: {pdf_filename}")
        
        try:
            doc = fitz.open(pdf_path)
            page_count = len(doc)
            markdown_content = []
            
            # Add document title
            title = doc_name.replace("_", " ").strip()
            markdown_content.append(f"# {title}\n\n")
            
            # Process each page
            for page_num in range(page_count):
                page = doc[page_num]
                
                # Add page marker
                markdown_content.append(f"\n---\n## Page {page_num + 1}\n\n")
                
                # Extract images first
                images = self.extract_images_from_page(page, doc_name.replace(' ', '_'), page_num)
                
                # Extract text
                text = self.extract_text_with_structure(page)
                markdown_content.append(text)
                
                # Add images after text
                if images:
                    markdown_content.append("\n\n### Images\n\n")
                    for img_filename, img_path in images:
                        markdown_content.append(f"![{img_filename}]({img_path})\n\n")
            
            doc.close()
            
            # Write markdown file
            full_content = "".join(markdown_content)
            
            # Clean up extra whitespace
            full_content = re.sub(r'\n{3,}', '\n\n', full_content)
            full_content = re.sub(r' +', ' ', full_content)
            
            with open(md_path, "w", encoding="utf-8") as f:
                f.write(full_content)
            
            print(f"  -> Success: {md_filename} ({page_count} pages)")
            
            return md_path
            
        except Exception as e:
            print(f"  Error converting {pdf_filename}: {e}")
            import traceback
            traceback.print_exc()
            return ""

    def convert_multiple(self, filenames: List[str]):
        """Convert multiple PDF files"""
        results = []
        for filename in filenames:
            result = self.convert_pdf_to_markdown(filename)
            if result:
                results.append(result)
        return results


def find_pdf_files(source_dir: str, pattern: str) -> List[str]:
    """Find PDF files matching a pattern in source directory"""
    import glob
    return glob.glob(os.path.join(source_dir, pattern))


def main():
    source_dir = "/Users/xiaoyu/Downloads/NicheGrowNerd_Pin_Scale_System_SLENDERMAN_BBHF"
    output_dir = "/Users/xiaoyu/Downloads/Pin_Scale_System_Converted/09-FAQ_Advanced"
    assets_dir = "/Users/xiaoyu/Downloads/Pin_Scale_System_Converted/09-FAQ_Advanced/assets/09-FAQ_Advanced"
    
    # Use glob to find all matching PDF files
    import glob
    
    patterns = [
        "96-*.pdf",
        "97-*.pdf", 
        "98-*.pdf",
        "99-*.pdf",
        "100-*.pdf",
        "101-*.pdf",
        "102-*.pdf",
        "103-*.pdf",
        "104-*.pdf",
        "105-*.pdf",
        "106-*.pdf",
        "107-*.pdf",
        "108-*.pdf",
        "109-*.pdf",
        "110-*.pdf",
    ]
    
    files_to_convert = []
    for pattern in patterns:
        matched = glob.glob(os.path.join(source_dir, pattern))
        files_to_convert.extend([os.path.basename(f) for f in matched])
    
    # Sort files for consistent processing
    files_to_convert = sorted(set(files_to_convert))
    
    print(f"Found {len(files_to_convert)} files to convert:")
    for f in files_to_convert:
        print(f"  - {f}")
    print()
    
    converter = PDFToMarkdownConverter(source_dir, output_dir, assets_dir)
    results = converter.convert_multiple(files_to_convert)
    
    print(f"\n=== Conversion Complete ===")
    print(f"Successfully converted: {len(results)}/{len(files_to_convert)} files")
    print(f"Output directory: {output_dir}")
    print(f"Assets directory: {assets_dir}")


if __name__ == "__main__":
    main()
