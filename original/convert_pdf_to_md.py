#!/usr/bin/env python3
"""
Convert PDF files to Markdown format with image extraction.
"""

import os
import re
import fitz  # PyMuPDF
from pathlib import Path
from datetime import datetime

# Configuration
SOURCE_DIR = "/Users/xiaoyu/Downloads/NicheGrowNerd_Pin_Scale_System_SLENDERMAN_BBHF/"
OUTPUT_DIR = "/Users/xiaoyu/Downloads/Pin_Scale_System_Converted/05-Image_Design/"
ASSETS_DIR = os.path.join(OUTPUT_DIR, "assets")

# Files to convert (note: file 63 has _min not –10 min)
PDF_FILES = [
    "51-Always_Do_This_Before_You_Create_Images!.pdf",
    "52-How_to_Create_Better_AI_Images.pdf",
    "53-How_to_Create_Ultra-Realistic_Humanized_AI_Images_(Added_Aug_25).pdf",
    "54-Midjourney.pdf",
    "55-Automate_Text_Overlays_(Added_Aug_25).pdf",
    "56-Systemize_Ideogram_(Added_Aug_25).pdf",
    "57-Automate_Ideogram_(Added_Aug_25).pdf",
    "58-What_pin_designs_perform_best_by_niche_(from_our_years_of_data).pdf",
    "59-Create_Templates_with_Ideogram_(Added_Oct_25).pdf",
    "60-Pinterest's_Own_Images.pdf",
    "61-Instagram_Images.pdf",
    "62-My_Stock_Image_Workflow_(added_October_25).pdf",
    "63-Preparations_(5–10_min).pdf",  # Corrected filename
    "64-AI_Images_on_Autopilot.pdf",
    "65-Real_Image_Workflow.pdf",
    "66-The_Complete_AI_Image_Workflow_SOP.pdf",
]


def sanitize_filename(name):
    """Sanitize filename for use as image name."""
    name = re.sub(r'[<>:"/\\|?*]', '', name)
    name = name.replace(' ', '_')
    return name


def extract_text_from_blocks(blocks):
    """Extract text from PDF blocks with formatting preservation."""
    text_parts = []
    current_line = ""
    prev_y = None

    for block in blocks:
        if block.get("type") == 0:  # Text block
            for line in block.get("lines", []):
                for span in line.get("spans", []):
                    text = span.get("text", "")
                    if not text.strip():
                        continue

                    flags = span.get("flags", 0)
                    font_size = span.get("size", 12)
                    is_bold = (flags & 2**4) != 0
                    is_italic = (flags & 1) != 0

                    bbox = span.get("bbox", [0, 0, 0, 0])
                    y = bbox[1]

                    # Format based on font size and style
                    formatted_text = text
                    if is_bold:
                        formatted_text = f"**{text}**"
                    if is_italic:
                        formatted_text = f"*{formatted_text}*"

                    # Handle different size text as headers
                    if font_size > 20 and text.strip():
                        # Large text might be a heading
                        pass

                    current_line += formatted_text

                if current_line:
                    text_parts.append(current_line)
                    current_line = ""

    return text_parts


def extract_page_content(doc, page_num, output_base_name):
    """Extract text and images from a page."""
    page = doc[page_num]
    content = {
        "text": [],
        "images": []
    }

    # Get page dimensions
    rect = page.rect
    width, height = rect.width, rect.height

    # Extract text blocks
    try:
        blocks = page.get_text("dict")["blocks"]
        text_content = page.get_text("text")

        # Get structured text with layout
        text_content = page.get_text("text")
        content["text"].append(text_content)

    except Exception as e:
        print(f"Error extracting text from page {page_num}: {e}")

    # Extract images
    try:
        image_list = page.get_images(full=True)
        for img_index, img in enumerate(image_list):
            xref = img[0]
            base_image = doc.extract_image(xref)

            if base_image:
                image_bytes = base_image["image"]
                image_ext = base_image.get("ext", "png")

                # Get image position
                try:
                    img_rect = page.get_image_rects(xref)[0] if page.get_image_rects(xref) else None
                except:
                    img_rect = None

                # Save image
                image_filename = f"{output_base_name}_page{page_num + 1}_img{img_index + 1}.{image_ext}"
                image_path = os.path.join(ASSETS_DIR, image_filename)

                with open(image_path, "wb") as img_file:
                    img_file.write(image_bytes)

                content["images"].append({
                    "filename": image_filename,
                    "index": img_index,
                    "page": page_num + 1
                })
    except Exception as e:
        print(f"Error extracting images from page {page_num}: {e}")

    return content


def pdf_to_markdown(pdf_path, output_path):
    """Convert a PDF file to Markdown format."""

    pdf_name = os.path.basename(pdf_path)
    base_name = os.path.splitext(pdf_name)[0]
    asset_base_name = sanitize_filename(base_name)

    print(f"\nProcessing: {pdf_name}")

    # Open PDF
    doc = fitz.open(pdf_path)

    # Metadata
    metadata = {
        "title": base_name.replace('_', ' '),
        "pages": len(doc),
        "file": pdf_name,
        "date": datetime.now().strftime("%Y-%m-%d")
    }

    # Collect all page content
    all_pages_content = []
    all_images = []

    for page_num in range(len(doc)):
        print(f"  Processing page {page_num + 1}/{len(doc)}...")
        page_content = extract_page_content(doc, page_num, asset_base_name)
        all_pages_content.append(page_content)
        all_images.extend([img for img in page_content["images"]])

    # Generate markdown
    markdown_lines = []

    # Frontmatter with summary
    markdown_lines.append("---")
    markdown_lines.append(f"title: {metadata['title']}")
    markdown_lines.append(f"source_file: {metadata['file']}")
    markdown_lines.append(f"total_pages: {metadata['pages']}")
    markdown_lines.append(f"total_images: {len(all_images)}")
    markdown_lines.append(f"conversion_date: {metadata['date']}")
    markdown_lines.append("---")
    markdown_lines.append("")
    markdown_lines.append(f"# {metadata['title']}")
    markdown_lines.append("")
    markdown_lines.append("## Document Summary")
    markdown_lines.append("")
    markdown_lines.append(f"This document contains **{metadata['pages']} pages** with **{len(all_images)} images**.")
    markdown_lines.append("")
    markdown_lines.append("---")
    markdown_lines.append("")

    # Page by page content
    current_page = 1
    for page_content in all_pages_content:
        # Page header
        markdown_lines.append(f"## Page {current_page}")
        markdown_lines.append("")

        # Text content
        text = "\n".join(page_content["text"])
        if text.strip():
            # Clean up text
            text = text.strip()
            # Add paragraph breaks
            lines = text.split('\n')
            paragraph_buffer = []
            for line in lines:
                line = line.strip()
                if not line:
                    if paragraph_buffer:
                        markdown_lines.append(" ".join(paragraph_buffer))
                        markdown_lines.append("")
                        paragraph_buffer = []
                else:
                    # Check if it's a heading (all caps or ends with colon)
                    if line.isupper() and len(line) < 50:
                        if paragraph_buffer:
                            markdown_lines.append(" ".join(paragraph_buffer))
                            markdown_lines.append("")
                            paragraph_buffer = []
                        markdown_lines.append(f"### {line}")
                        markdown_lines.append("")
                    elif line.endswith(':') and len(line) < 60:
                        if paragraph_buffer:
                            markdown_lines.append(" ".join(paragraph_buffer))
                            markdown_lines.append("")
                            paragraph_buffer = []
                        markdown_lines.append(f"### {line}")
                        markdown_lines.append("")
                    else:
                        paragraph_buffer.append(line)

            if paragraph_buffer:
                markdown_lines.append(" ".join(paragraph_buffer))
                markdown_lines.append("")

        # Images for this page
        page_images = [img for img in page_content["images"] if img["page"] == current_page]
        for img in page_images:
            markdown_lines.append(f"![Image](assets/{img['filename']})")
            markdown_lines.append("")

        markdown_lines.append("---")
        markdown_lines.append("")
        current_page += 1

    # Write markdown file
    markdown_content = "\n".join(markdown_lines)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(markdown_content)

    doc.close()

    print(f"  Saved to: {output_path}")
    print(f"  Extracted {len(all_images)} images")

    return len(all_images)


def main():
    """Main conversion function."""
    # Create directories
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    os.makedirs(ASSETS_DIR, exist_ok=True)

    total_files = 0
    total_images = 0

    for pdf_file in PDF_FILES:
        source_path = os.path.join(SOURCE_DIR, pdf_file)

        if not os.path.exists(source_path):
            print(f"WARNING: File not found: {pdf_file}")
            continue

        # Output markdown filename
        base_name = os.path.splitext(pdf_file)[0]
        output_filename = f"{base_name}.md"
        output_path = os.path.join(OUTPUT_DIR, output_filename)

        # Convert
        try:
            num_images = pdf_to_markdown(source_path, output_path)
            total_files += 1
            total_images += num_images
        except Exception as e:
            print(f"ERROR converting {pdf_file}: {e}")
            import traceback
            traceback.print_exc()

    print(f"\n" + "="*50)
    print(f"Conversion Complete!")
    print(f"Files processed: {total_files}")
    print(f"Total images extracted: {total_images}")
    print(f"Output directory: {OUTPUT_DIR}")
    print(f"Assets directory: {ASSETS_DIR}")
    print("="*50)


if __name__ == "__main__":
    main()
