import os
import pymupdf

MODULES_DEF = [
    (1, "introduction-to-html", "Introduction to HTML & Web Structure", 2, 49),
    (2, "css-styling-and-layout", "CSS Styling, Selectors & The Box Model", 50, 83),
    (3, "advanced-css-flexbox-grid", "Advanced CSS, Flexbox, Grid & Media Queries", 84, 122),
    (4, "javascript-fundamentals", "JavaScript Fundamentals, Syntax & Operators", 123, 152),
    (5, "javascript-functions-arrays", "JavaScript Functions, Arrays & Objects", 153, 171),
    (6, "dom-and-event-handling", "DOM Manipulation & Event Handling", 172, 209),
    (7, "nodejs-and-backend", "Node.js & Backend Architecture", 210, 259),
    (8, "expressjs-web-framework", "Express.js Web Framework & Routing", 260, 266),
    (9, "mongodb-database", "MongoDB Database Development & Aggregations", 267, 289),
    (10, "reactjs-frontend-development", "React.js Frontend Development, Components & Hooks", 290, 326),
]

def split_pdf(cleaned_pdf_path, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    src_doc = pymupdf.open(cleaned_pdf_path)
    total_pages = len(src_doc)
    print(f"Source PDF has {total_pages} pages.")

    created_files = []
    for order, slug, title, start_p, end_p in MODULES_DEF:
        # 1-indexed to 0-indexed
        from_idx = start_p - 1
        to_idx = min(end_p - 1, total_pages - 1)
        
        mod_doc = pymupdf.open()
        
        # Include cover page (page 0) for each module, then the module's pages
        mod_doc.insert_pdf(src_doc, from_page=0, to_page=0)
        mod_doc.insert_pdf(src_doc, from_page=from_idx, to_page=to_idx)
        
        filename = f"module-{order:02d}-{slug}.pdf"
        out_path = os.path.join(output_dir, filename)
        mod_doc.save(out_path, garbage=4, deflate=True)
        mod_doc.close()
        
        page_count = (to_idx - from_idx + 1) + 1 # +1 for cover
        created_files.append((filename, title, page_count))
        print(f"Created: {filename} ({page_count} pages) -> '{title}'")

    src_doc.close()
    return created_files

if __name__ == "__main__":
    src = os.path.join("media", "source", "cleaned.pdf")
    
    # Save to media/courses/web-development/
    web_dir = os.path.join("media", "courses", "web-development")
    split_pdf(src, web_dir)
    print("All modules split successfully!")
