import os
import re
import io
import pymupdf
from PIL import Image, ImageDraw

def clean_pdf(input_path, output_path):
    print(f"Opening original: {input_path}")
    doc = pymupdf.open(input_path)
    total_pages = len(doc)
    print(f"Total pages: {total_pages}")

    # --- 1. CLEAN COVER PAGE (PAGE 1) ---
    p1 = doc[0]
    images = p1.get_images()
    clean_cover_doc = None
    if images:
        xref = images[0][0]
        base_img = doc.extract_image(xref)
        pil_img = Image.open(io.BytesIO(base_img["image"])).convert("RGB")
        
        # Patch the watermark badge with exact matching dark navy blue
        draw = ImageDraw.Draw(pil_img)
        bg_color = (0, 28, 57)
        draw.rectangle([580, 1280, 1020, 1370], fill=bg_color)
        
        buf = io.BytesIO()
        pil_img.save(buf, format="JPEG", quality=95)
        jpeg_bytes = buf.getvalue()
        
        # Build clean single-page doc for cover
        clean_cover_doc = pymupdf.open()
        cov_page = clean_cover_doc.new_page(width=p1.rect.width, height=p1.rect.height)
        cov_page.insert_image(p1.rect, stream=jpeg_bytes)
        print("Page 1 (Cover) cleaned and built seamlessly.")

    # --- 2. CLEAN INTERIOR PAGES (PAGES 2-326) VIA STREAM EDITING ---
    pattern_interior = re.compile(
        r'q\s+/GS-\d+\s+gs\s+BT\s+.*?\([^\)]*CodeWithHarry[^\)]*\)\s+Tj\s+ET\s+Q',
        re.DOTALL
    )
    pattern_interior_fallback = re.compile(
        r'BT\s+.*?\([^\)]*CodeWithHarry[^\)]*\)\s+Tj\s+ET',
        re.DOTALL
    )

    cleaned_count = 0
    for page_num in range(1, total_pages):
        page = doc[page_num]
        for xref in page.get_contents():
            stream_str = doc.xref_stream(xref).decode('latin1')
            if "CodeWithHarry" in stream_str:
                new_str, count = pattern_interior.subn('', stream_str)
                if count == 0:
                    new_str, count = pattern_interior_fallback.subn('', stream_str)
                if count > 0:
                    doc.update_stream(xref, new_str.encode('latin1'))
                    cleaned_count += 1
                    
        if page_num % 50 == 0 or page_num == total_pages - 1:
            print(f"Processed {page_num + 1}/{total_pages} pages...")

    print(f"Cleaned interior watermark on {cleaned_count} pages.")

    # --- 3. COMBINE CLEAN COVER + CLEANED PAGES INTO FINAL CLEANED PDF ---
    final_doc = pymupdf.open()
    if clean_cover_doc:
        final_doc.insert_pdf(clean_cover_doc)
    else:
        final_doc.insert_pdf(doc, from_page=0, to_page=0)
        
    final_doc.insert_pdf(doc, from_page=1, to_page=total_pages - 1)
    
    print(f"Saving final cleaned PDF to: {output_path} ...")
    final_doc.save(output_path, garbage=4, deflate=True)
    
    doc.close()
    if clean_cover_doc:
        clean_cover_doc.close()
    final_doc.close()
    print("Cleaned PDF saved successfully!")

def render_previews(pdf_path, page_numbers, output_dir):
    doc = pymupdf.open(pdf_path)
    os.makedirs(output_dir, exist_ok=True)
    for p_num in page_numbers:
        page_idx = p_num - 1
        page = doc[page_idx]
        pix = page.get_pixmap(dpi=150)
        out_file = os.path.join(output_dir, f"page_{p_num}_preview.png")
        pix.save(out_file)
        print(f"Saved preview: {out_file}")
    doc.close()

if __name__ == "__main__":
    src = os.path.join("media", "source", "python-full-stack-full.pdf")
    dst = os.path.join("media", "source", "cleaned.pdf")
    previews = os.path.join("media", "preview")
    
    clean_pdf(src, dst)
    render_previews(dst, [1, 10, 20], previews)
