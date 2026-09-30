import os
import pymupdf

MODULES_25 = [
    # --- HTML SECTION (Modules 1 - 5) ---
    (1, "html-basics-and-structure", "HTML5 Basics, Document Structure & Headings", 2, 9),
    (2, "html-text-formatting-and-links", "HTML Formatting, Comments, Links & Anchors", 10, 16),
    (3, "html-media-images-audio-video", "HTML Images, Audio, Video & Embeds", 17, 21),
    (4, "html-tables-and-lists", "HTML Tables, Rows, Cells & Nested Lists", 22, 24),
    (5, "html-forms-semantics-and-seo", "HTML Forms, Inputs, HTML5 Semantics & SEO", 25, 49),

    # --- CSS SECTION (Modules 6 - 11) ---
    (6, "css-fundamentals-and-selectors", "CSS Introduction, Syntax & Selectors", 50, 57),
    (7, "css-colors-backgrounds-and-borders", "CSS Colors, Backgrounds, Borders & Radius", 58, 61),
    (8, "css-box-model-margin-and-padding", "CSS Box Model, Sizing, Margins & Padding", 62, 69),
    (9, "css-typography-and-units", "CSS Typography, Fonts, Units & Calcs", 70, 83),
    (10, "css-display-and-positioning", "CSS Display, Flow & Positioning Schemes", 84, 94),
    (11, "css-flexbox-grid-and-responsive", "CSS Flexbox, CSS Grid & Media Queries", 95, 122),

    # --- JAVASCRIPT FUNDAMENTALS (Modules 12 - 17) ---
    (12, "javascript-syntax-and-variables", "JavaScript Syntax, Variables, Data Types & Console", 123, 132),
    (13, "javascript-operators-and-control-flow", "JavaScript Operators, Expressions & If-Else", 133, 138),
    (14, "javascript-objects-and-properties", "JavaScript Objects Deep-Dive & Methods", 139, 142),
    (15, "javascript-loops-and-iterations", "JavaScript Loops, Break, Continue & Iterations", 143, 152),
    (16, "javascript-functions-and-scope", "JavaScript Functions, Arrow Functions & Scope", 153, 155),
    (17, "javascript-arrays-and-strings", "JavaScript Arrays, Strings, Methods & Templates", 156, 171),

    # --- DOM & BROWSER APIS (Modules 18 - 20) ---
    (18, "dom-architecture-and-selectors", "DOM Architecture, Node Tree & Element Selection", 172, 177),
    (19, "dom-manipulation-styles-and-events", "DOM Manipulation, Classes, Attributes & Events", 178, 191),
    (20, "event-bubbling-storage-and-errors", "Event Bubbling, Delegation, LocalStorage & Error Handling", 192, 209),

    # --- BACKEND & DATABASE (Modules 21 - 23) ---
    (21, "nodejs-architecture-and-modules", "Node.js Runtime, Modules (CJS/ESM) & Server", 210, 228),
    (22, "async-javascript-promises-and-express", "Asynchronous JS, Promises, Async/Await & Express.js", 229, 266),
    (23, "mongodb-database-and-crud", "MongoDB NoSQL Database, Compass & CRUD Operations", 267, 289),

    # --- REACT.JS (Modules 24 - 25) ---
    (24, "react-fundamentals-and-components", "React.js Setup with Vite, Components & JSX", 290, 300),
    (25, "react-state-hooks-and-router", "React State, Props, Hooks (useState/useEffect) & Router", 301, 326),
]

def split_into_25_modules(cleaned_pdf_path, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    src_doc = pymupdf.open(cleaned_pdf_path)
    total_pages = len(src_doc)
    print(f"Source PDF has {total_pages} pages.")

    # Remove existing older split PDFs in output directory
    for f in os.listdir(output_dir):
        if f.endswith('.pdf'):
            os.remove(os.path.join(output_dir, f))

    created_files = []
    for order, slug, title, start_p, end_p in MODULES_25:
        from_idx = start_p - 1
        to_idx = min(end_p - 1, total_pages - 1)
        
        mod_doc = pymupdf.open()
        
        # Include cover page (page 0) for each module
        mod_doc.insert_pdf(src_doc, from_page=0, to_page=0)
        # Include module body pages
        mod_doc.insert_pdf(src_doc, from_page=from_idx, to_page=to_idx)
        
        filename = f"module-{order:02d}-{slug}.pdf"
        out_path = os.path.join(output_dir, filename)
        mod_doc.save(out_path, garbage=4, deflate=True)
        mod_doc.close()
        
        page_count = (to_idx - from_idx + 1) + 1 # +1 cover
        created_files.append((order, filename, title, page_count))
        print(f"Created: {filename} ({page_count} pages) -> '{title}'")

    src_doc.close()
    return created_files

if __name__ == "__main__":
    src = os.path.join("media", "source", "cleaned.pdf")
    web_dir = os.path.join("media", "courses", "web-development")
    split_into_25_modules(src, web_dir)
    print("All 25 modules generated successfully!")
