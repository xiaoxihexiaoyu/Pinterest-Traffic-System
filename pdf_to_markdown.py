#!/usr/bin/env python3
"""
PDF to Markdown Converter with Image Extraction
Converts PDF files to Markdown format, extracting images and adding document summaries.
"""

import os
import re
import sys
from pathlib import Path

try:
    import fitz  # PyMuPDF
    from PIL import Image
except ImportError as e:
    print(f"Error: Required library not found: {e}")
    print("Install with: pip install PyMuPDF Pillow")
    sys.exit(1)


class PDFToMarkdownConverter:
    """Convert PDF files to Markdown with image extraction."""

    # Step name mappings for better document summaries
    STEP_NAMES = {
        "10-1": ("1", "Profile Optimization", "Optimize Pinterest profile for maximum visibility"),
        "11-2": ("2", "Niche & Keyword Research", "Research profitable niches and keywords"),
        "12-3": ("3", "Article Creation", "Create SEO-optimized content articles"),
        "13-4": ("4", "Create Pin & Board Descriptions", "Write compelling descriptions with annotations"),
        "14-5": ("5", "Research Top-Ranking Pins", "Analyze successful pins in your niche"),
        "15-6": ("6", "Create Inspired Pins", "Design pins based on top-ranking examples"),
        "16-7": ("7", "Efficient Pin Upload", "Upload pins strategically for maximum reach"),
        "17-8": ("8", "Add Board Descriptions", "Optimize board descriptions for SEO"),
        "18-9": ("9", "In-Depth Monthly Review", "Review and analyze performance monthly"),
        "19-10": ("10", "Delete Underperforming Boards", "Clean up low-performing boards")
    }

    def __init__(self, source_dir, output_dir, assets_dir):
        self.source_dir = Path(source_dir)
        self.output_dir = Path(output_dir)
        self.assets_dir = Path(assets_dir)
        self.assets_dir.mkdir(parents=True, exist_ok=True)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def get_step_info(self, filename):
        """Extract step information from filename."""
        base_name = filename.replace(".pdf", "")
        for key, (step_num, step_name, goal) in self.STEP_NAMES.items():
            if base_name.startswith(key):
                return step_num, step_name, goal
        # Fallback: extract from filename
        match = re.search(r'(\d+)[-._]Step\s*__?\s*(.+?)_SOP', filename)
        if match:
            return match.group(1), match.group(2).replace('_', ' '), "Implement this step"
        return "N/A", "Unknown Step", "Complete this SOP step"

    def extract_images_from_page(self, page, pdf_name, page_num):
        """Extract images from a PDF page."""
        images = []
        image_list = page.get_images(full=True)

        for img_index, img in enumerate(image_list):
            xref = img[0]
            base_image = page.parent.extract_image(xref)

            if base_image:
                image_bytes = base_image["image"]
                image_ext = base_image.get("ext", "png")

                # Generate unique filename
                image_filename = f"{pdf_name}_page{page_num}_img{img_index}.{image_ext}"
                image_path = self.assets_dir / image_filename

                # Save image
                with open(image_path, "wb") as img_file:
                    img_file.write(image_bytes)

                images.append({
                    "filename": image_filename,
                    "index": img_index
                })

        return images

    def clean_text(self, text):
        """Clean up extracted text."""
        # Remove excessive whitespace
        text = re.sub(r'\n{3,}', '\n\n', text)
        # Clean up bullet points
        text = re.sub(r'[\u2022\u25cb]\s*', '- ', text)
        # Clean up quotes
        text = text.replace('"', '"').replace('"', '"').replace(''', "'").replace(''', "'")
        return text.strip()

    def pdf_to_markdown(self, pdf_path):
        """Convert a single PDF to Markdown."""
        pdf_path = Path(pdf_path)
        pdf_name = pdf_path.stem

        print(f"Processing: {pdf_path.name}")

        # Open PDF
        doc = fitz.open(pdf_path)

        # Get step info
        step_num, step_name, goal = self.get_step_info(pdf_path.name)

        # Build markdown content
        markdown_content = []
        all_images = {}  # page_num -> [images]

        # Add document summary at the top
        markdown_content.append("---")
        markdown_content.append(f"# Step {step_num}: {step_name}")
        markdown_content.append("")
        markdown_content.append("## Document Summary")
        markdown_content.append("")
        markdown_content.append(f"- **Step Number**: {step_num}")
        markdown_content.append(f"- **Step Name**: {step_name}")
        markdown_content.append(f"- **Core Objective**: {goal}")
        markdown_content.append(f"- **Source File**: {pdf_path.name}")
        markdown_content.append("")
        markdown_content.append("---")
        markdown_content.append("")
        markdown_content.append("## Content")
        markdown_content.append("")

        # Process each page
        for page_num in range(len(doc)):
            page = doc[page_num]

            # Extract images first
            page_images = self.extract_images_from_page(page, pdf_name, page_num + 1)
            if page_images:
                all_images[page_num] = page_images

            # Extract text with layout
            try:
                text = page.get_text()
                cleaned = self.clean_text(text)

                if page_num > 0:
                    markdown_content.append(f"\n### Page {page_num + 1}\n")

                if cleaned:
                    markdown_content.append(cleaned)

                # Add images for this page
                if page_num in all_images:
                    for img in all_images[page_num]:
                        img_path = f"assets/02-SOP_Steps/{img['filename']}"
                        markdown_content.append(f"\n![{img['filename']}]({img_path})\n")

            except Exception as e:
                print(f"  Warning: Error processing page {page_num + 1}: {e}")

        doc.close()

        # Save markdown file
        md_content = "\n".join(markdown_content)
        md_path = self.output_dir / f"{pdf_name}.md"

        with open(md_path, "w", encoding="utf-8") as f:
            f.write(md_content)

        print(f"  -> Converted to: {md_path.name}")
        print(f"  -> Extracted {sum(len(v) for v in all_images.values())} images")

        return md_path

    def convert_multiple(self, filenames):
        """Convert multiple PDF files."""
        results = []

        for filename in filenames:
            pdf_path = self.source_dir / filename
            if pdf_path.exists():
                try:
                    md_path = self.pdf_to_markdown(pdf_path)
                    results.append((filename, md_path, "Success"))
                except Exception as e:
                    results.append((filename, None, f"Error: {e}"))
                    print(f"  Error: {e}")
            else:
                results.append((filename, None, "File not found"))
                print(f"  File not found: {pdf_path}")

        return results


def main():
    """Main execution function."""
    source_dir = "/Users/xiaoyu/Downloads/NicheGrowNerd_Pin_Scale_System_SLENDERMAN_BBHF/"
    output_dir = "/Users/xiaoyu/Downloads/Pin_Scale_System_Converted/02-SOP_Steps/"
    assets_dir = "/Users/xiaoyu/Downloads/Pin_Scale_System_Converted/assets/02-SOP_Steps/"

    # Files to convert
    files_to_convert = [
        "10-1._Step__Profile_Optimization_SOP.pdf",
        "11-2._Step__Niche_&_Keyword_Research_SOP.pdf",
        "12-3._Step__Article_Creation_SOP.pdf",
        "13-4._Step__Create_Pin_&_Board_Descriptions_with_Annotations_SOP.pdf",
        "14-5._Step__Research_Current_Top-Ranking_Pins_SOP.pdf",
        "15-6._Step__Create_Pins_Inspired_By_the_Top-Ranking_Ones_SOP.pdf",
        "16-7._Step__Efficient_Pin_Upload_SOP.pdf",
        "17-8._Step__Add_Board_Descriptions_SOP.pdf",
        "18-9._Step__In-Depth_Review_Once_a_Month_SOP.pdf",
        "19-10._Step__Delete_Underperforming_Boards_SOP.pdf"
    ]

    converter = PDFToMarkdownConverter(source_dir, output_dir, assets_dir)

    print("=" * 60)
    print("PDF to Markdown Converter")
    print("=" * 60)
    print()

    results = converter.convert_multiple(files_to_convert)

    print()
    print("=" * 60)
    print("Conversion Summary")
    print("=" * 60)

    for filename, md_path, status in results:
        status_symbol = "OK" if "Success" in status else "XX"
        print(f"  [{status_symbol}] {filename}")
        if md_path:
            print(f"      -> {md_path}")

    print()
    success_count = sum(1 for _, _, s in results if "Success" in s)
    print(f"Converted: {success_count}/{len(files_to_convert)} files")
    print(f"Output directory: {output_dir}")
    print(f"Assets directory: {assets_dir}")


if __name__ == "__main__":
    main()
