import os
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable, PageBreak
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY

W, H = A4
DARK_BG = colors.HexColor("#0D1B2A")
ACCENT  = colors.HexColor("#00C9A7")
WHITE   = colors.white
CARD_BG = colors.HexColor("#1B2A3B")
LIGHT_BG = colors.HexColor("#F8FAFC")
TEXT_DARK = colors.HexColor("#2D3748")
CODE_BG   = colors.HexColor("#EDF2F7")
TEXT_LIGHT = colors.HexColor("#E8F0FE")

# ---------- styles ----------
badge_s = ParagraphStyle("Badge", fontName="Helvetica-Bold", fontSize=12,
    textColor=DARK_BG, alignment=1)
title_s = ParagraphStyle("Title", fontName="Helvetica-Bold", fontSize=26,
    textColor=WHITE, alignment=1, leading=34)
sub_s   = ParagraphStyle("Sub",   fontName="Helvetica", fontSize=12,
    textColor=ACCENT, alignment=1)
sm_s    = ParagraphStyle("Sm",    fontName="Helvetica", fontSize=9,
    textColor=TEXT_LIGHT, alignment=1)
ph_s    = ParagraphStyle("PH",    fontName="Helvetica-Bold", fontSize=16,
    textColor=DARK_BG, spaceAfter=4)
hdr_s   = ParagraphStyle("Hdr",   fontName="Helvetica-Bold", fontSize=11,
    textColor=WHITE)
body_s  = ParagraphStyle("Body",  fontName="Helvetica", fontSize=10.5,
    textColor=TEXT_DARK, leading=16, spaceAfter=8, alignment=TA_JUSTIFY)
code_s  = ParagraphStyle("Code",  fontName="Courier", fontSize=9,
    textColor=DARK_BG, backColor=CODE_BG,
    leading=14, spaceAfter=6, leftIndent=10, rightIndent=10, borderPad=6)

CODE_STARTS = ("SELECT","CREATE","INSERT","UPDATE","DELETE","WITH","DELIMITER",
               "CALL","SET ","--","GRANT","REVOKE","SHOW","ALTER","DROP",
               "IF ","UNION","START","TRUNCATE","mysqldump","mysql ")


def is_code_block(text):
    for line in text.split("\n"):
        s = line.strip()
        if s.startswith("  ") or any(s.startswith(k) for k in CODE_STARTS):
            return True
    return False


def cover_page(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(DARK_BG);  canvas.rect(0, 0, W, H, fill=1, stroke=0)
    canvas.setFillColor(ACCENT);   canvas.rect(0, H-8, W, 8, fill=1, stroke=0)
    canvas.setFillColor(CARD_BG);  canvas.rect(0, 0, W, 90, fill=1, stroke=0)
    canvas.setFillColor(ACCENT);   canvas.rect(0, 0, W, 4,  fill=1, stroke=0)
    canvas.restoreState()


def content_page(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(LIGHT_BG); canvas.rect(0, 0, W, H,    fill=1, stroke=0)
    canvas.setFillColor(ACCENT);   canvas.rect(0, 0, 6, H,    fill=1, stroke=0)
    canvas.setFillColor(DARK_BG);  canvas.rect(0, H-50, W, 50, fill=1, stroke=0)
    canvas.setFillColor(DARK_BG);  canvas.rect(0, 0,  W, 35,  fill=1, stroke=0)
    canvas.setFillColor(WHITE);    canvas.setFont("Helvetica", 8)
    canvas.drawString(20, 12, "ARSHITH LMS  -  DBMS with SQL")
    canvas.drawRightString(W-20, 12, f"Page {canvas.getPageNumber()}")
    canvas.restoreState()


def build_pdf(num, slug, title, sections, out_dir):
    os.makedirs(out_dir, exist_ok=True)
    fname = f"module-{num:02d}-{slug}.pdf"
    fpath = os.path.join(out_dir, fname)

    doc = SimpleDocTemplate(fpath, pagesize=A4,
        leftMargin=2*cm, rightMargin=1.5*cm,
        topMargin=1.5*cm, bottomMargin=1.8*cm)
    story = []

    # — COVER PAGE —
    story.append(Spacer(1, 3.5*cm))
    bt = Table([[Paragraph(f"MODULE {num:02d}", badge_s)]], colWidths=[5*cm])
    bt.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,-1), ACCENT),
        ("TOPPADDING", (0,0), (-1,-1), 10),
        ("BOTTOMPADDING", (0,0), (-1,-1), 10),
        ("ALIGN", (0,0), (-1,-1), "CENTER"),
    ]))
    story.append(Table([[bt]], colWidths=[W - 3.5*cm]))
    story.append(Spacer(1, 1.2*cm))
    story.append(Paragraph(title, title_s))
    story.append(Spacer(1, 0.8*cm))
    story.append(HRFlowable(width="80%", thickness=2, color=ACCENT, spaceAfter=20))
    story.append(Paragraph("DBMS with SQL  -  Enterprise Learning Series", sub_s))
    story.append(Spacer(1, 0.4*cm))
    story.append(Paragraph("ARSHITH LMS  |  Professional Edition", sm_s))
    story.append(PageBreak())

    # — CONTENT PAGES —
    story.append(Spacer(1, 1.5*cm))
    story.append(Paragraph(title, ph_s))
    story.append(HRFlowable(width="100%", thickness=2, color=ACCENT, spaceAfter=16))

    for sec_title, sec_content in sections:
        hd = Table([[Paragraph(sec_title, hdr_s)]], colWidths=[W - 3.5*cm])
        hd.setStyle(TableStyle([
            ("BACKGROUND", (0,0), (-1,-1), DARK_BG),
            ("TOPPADDING", (0,0), (-1,-1), 8),
            ("BOTTOMPADDING", (0,0), (-1,-1), 8),
            ("LEFTPADDING", (0,0), (-1,-1), 14),
        ]))
        story.append(hd)
        story.append(Spacer(1, 0.2*cm))

        safe = (sec_content
                .replace("&", "&amp;")
                .replace("<", "&lt;")
                .replace(">", "&gt;"))

        if is_code_block(sec_content):
            for chunk in safe.split("\n\n"):
                if chunk.strip():
                    story.append(Paragraph(chunk.replace("\n", "<br/>"), code_s))
        else:
            story.append(Paragraph(safe.replace("\n", "<br/>"), body_s))

        story.append(Spacer(1, 0.3*cm))

    doc.build(story, onFirstPage=cover_page, onLaterPages=content_page)
    print(f"  Created: {fname}")
    return fpath


# ============================================================
# 25 SQL MODULE DEFINITIONS
# ============================================================
MODULES = [
  (1, "introduction-to-sql", "Introduction to SQL and Databases", [
    ("What is SQL?",
     "SQL (Structured Query Language) is the standard language for relational databases.\n"
     "Powers MySQL, PostgreSQL, Oracle, and SQL Server.\n"
     "Used by developers, analysts, and data scientists worldwide."),
    ("Key Concepts",
     "Database: organised collection of data\n"
     "Table: data in rows and columns\n"
     "Row: a single record\n"
     "Column: an attribute/field\n"
     "Primary Key: unique identifier per row\n"
     "Query: request to retrieve or change data"),
    ("Basic Example",
     "SELECT first_name, last_name, gpa\n"
     "FROM students\n"
     "WHERE gpa > 3.5\n"
     "ORDER BY gpa DESC\n"
     "LIMIT 10;"),
    ("SQL vs NoSQL",
     "SQL: structured schema, ACID, complex queries (MySQL, PostgreSQL)\n"
     "NoSQL: flexible schema, horizontal scale (MongoDB, Redis, Cassandra)\n"
     "SQL: banking, ERP, e-commerce\n"
     "NoSQL: social media, IoT, real-time"),
    ("Why Learn SQL?",
     "SQL is the most in-demand data skill globally.\n"
     "Powers every major database system.\n"
     "Essential for backend dev, data analysis, and data engineering."),
  ]),

  (2, "rdbms-concepts", "RDBMS Concepts and Architecture", [
    ("What is RDBMS?",
     "Relational Database Management System stores data in tables with defined relationships.\n"
     "Enforces ACID properties and data integrity through constraints."),
    ("ACID Properties",
     "Atomicity: all operations succeed or all fail\n"
     "Consistency: database stays in a valid state\n"
     "Isolation: concurrent transactions do not interfere\n"
     "Durability: committed data survives crashes"),
    ("Popular Systems",
     "MySQL: open-source web databases\n"
     "PostgreSQL: advanced open-source\n"
     "Oracle: enterprise grade\n"
     "SQL Server: Microsoft enterprise\n"
     "SQLite: lightweight embedded"),
    ("3-Tier Architecture",
     "External Level: user views\n"
     "Conceptual Level: schema definitions\n"
     "Internal Level: physical disk storage"),
    ("Table Example",
     "CREATE TABLE students (\n"
     "  id INT PRIMARY KEY,\n"
     "  name VARCHAR(100) NOT NULL,\n"
     "  dept_id INT REFERENCES departments(id)\n"
     ");"),
  ]),

  (3, "data-types-and-constraints", "SQL Data Types and Constraints", [
    ("Numeric Types",
     "INT: whole numbers\n"
     "DECIMAL(p,s): exact decimals e.g. salary DECIMAL(10,2)\n"
     "FLOAT: approximate floating-point\n"
     "BIGINT: very large integers"),
    ("String Types",
     "CHAR(n): fixed-length string\n"
     "VARCHAR(n): variable-length (most common)\n"
     "TEXT: large text blocks\n"
     "NVARCHAR: unicode variable-length"),
    ("Date and Time Types",
     "DATE: YYYY-MM-DD\n"
     "TIME: HH:MM:SS\n"
     "DATETIME: date and time combined\n"
     "TIMESTAMP: with timezone support"),
    ("Constraints",
     "NOT NULL: column cannot be empty\n"
     "UNIQUE: all values must differ\n"
     "PRIMARY KEY: NOT NULL + UNIQUE\n"
     "FOREIGN KEY: links to another table\n"
     "CHECK: validates a condition\n"
     "DEFAULT: sets a fallback value"),
    ("Full Example",
     "CREATE TABLE employees (\n"
     "  id INT PRIMARY KEY,\n"
     "  name VARCHAR(100) NOT NULL,\n"
     "  email VARCHAR(150) UNIQUE,\n"
     "  salary DECIMAL(10,2) CHECK (salary > 0),\n"
     "  dept_id INT REFERENCES departments(id)\n"
     ");"),
  ]),

  (4, "ddl-create-alter-drop", "SQL DDL - CREATE ALTER DROP", [
    ("DDL Commands",
     "CREATE: build new objects\n"
     "ALTER: modify existing objects\n"
     "DROP: delete objects permanently\n"
     "TRUNCATE: remove all rows fast\n"
     "RENAME: rename objects"),
    ("CREATE TABLE",
     "CREATE TABLE students (\n"
     "  student_id INT PRIMARY KEY AUTO_INCREMENT,\n"
     "  first_name VARCHAR(50) NOT NULL,\n"
     "  email VARCHAR(100) UNIQUE,\n"
     "  gpa DECIMAL(3,2)\n"
     ");"),
    ("ALTER TABLE",
     "-- Add column\n"
     "ALTER TABLE students ADD phone VARCHAR(15);\n"
     "-- Modify column\n"
     "ALTER TABLE students MODIFY email VARCHAR(200);\n"
     "-- Drop column\n"
     "ALTER TABLE students DROP COLUMN phone;"),
    ("DROP vs TRUNCATE",
     "DROP TABLE students;      -- removes table completely\n"
     "TRUNCATE TABLE students;  -- empties data, keeps structure\n"
     "DROP DATABASE school;     -- removes entire database"),
    ("Create Index",
     "CREATE INDEX idx_email ON students(email);\n"
     "CREATE UNIQUE INDEX idx_u ON students(email);\n"
     "DROP INDEX idx_email ON students;"),
  ]),

  (5, "dml-insert-update-delete", "SQL DML - INSERT UPDATE DELETE", [
    ("DML Commands",
     "INSERT: add new records\n"
     "UPDATE: modify existing records\n"
     "DELETE: remove records\n"
     "SELECT: retrieve records\n"
     "All DML operations can be rolled back."),
    ("INSERT",
     "INSERT INTO students (first_name, gpa)\n"
     "VALUES ('Arshith', 3.9);\n\n"
     "-- Multiple rows\n"
     "INSERT INTO students (first_name, gpa)\n"
     "VALUES ('Rahul', 3.7), ('Priya', 3.8);"),
    ("UPDATE",
     "UPDATE students\n"
     "SET gpa = 4.0\n"
     "WHERE student_id = 1;\n\n"
     "-- ALWAYS use WHERE clause!\n"
     "-- Without WHERE, ALL rows are updated!"),
    ("DELETE",
     "DELETE FROM students WHERE student_id = 5;\n"
     "DELETE FROM students WHERE gpa < 2.0;\n\n"
     "-- Remove all rows (use TRUNCATE instead)\n"
     "DELETE FROM students;"),
    ("INSERT SELECT",
     "-- Copy data between tables\n"
     "INSERT INTO archive_students\n"
     "SELECT * FROM students\n"
     "WHERE enrollment_date < '2020-01-01';"),
  ]),

  (6, "select-and-filtering", "SQL SELECT and Filtering Data", [
    ("SELECT Basics",
     "SELECT * FROM students;\n"
     "SELECT first_name, gpa FROM students;\n"
     "SELECT first_name AS Name FROM students;\n"
     "SELECT DISTINCT department FROM employees;"),
    ("WHERE Clause",
     "SELECT * FROM students WHERE gpa > 3.5;\n"
     "SELECT * FROM students WHERE gpa > 3.0 AND dept = 'CS';\n"
     "SELECT * FROM students WHERE dept = 'CS' OR dept = 'IT';"),
    ("Operators",
     "Comparison: = != < > <= >=\n"
     "Range:      BETWEEN 3.0 AND 4.0\n"
     "List:       IN ('CS', 'IT', 'ECE')\n"
     "Null:       IS NULL  /  IS NOT NULL\n"
     "Pattern:    LIKE '%pattern%'"),
    ("LIKE Patterns",
     "WHERE name LIKE 'A%'      -- starts with A\n"
     "WHERE name LIKE '%kumar'  -- ends with kumar\n"
     "WHERE name LIKE '%sh%'    -- contains sh\n"
     "WHERE name LIKE '_____'   -- exactly 5 chars"),
    ("ORDER BY and LIMIT",
     "SELECT * FROM students ORDER BY gpa DESC;\n"
     "SELECT * FROM students ORDER BY dept ASC, gpa DESC;\n"
     "SELECT * FROM students LIMIT 10;\n"
     "-- Pagination (skip 10, get next 10)\n"
     "SELECT * FROM students LIMIT 10 OFFSET 10;"),
  ]),

  (7, "aggregate-functions", "SQL Aggregate Functions", [
    ("Aggregate Functions",
     "COUNT():  count rows\n"
     "SUM():    total of values\n"
     "AVG():    average value\n"
     "MIN():    minimum value\n"
     "MAX():    maximum value"),
    ("COUNT",
     "SELECT COUNT(*) AS total FROM students;\n"
     "SELECT COUNT(email) AS has_email FROM students;\n"
     "SELECT COUNT(DISTINCT dept) AS depts FROM students;"),
    ("SUM and AVG",
     "SELECT SUM(salary) AS payroll FROM employees;\n"
     "SELECT ROUND(AVG(gpa), 2) AS avg_gpa FROM students;\n"
     "SELECT SUM(salary) FROM employees WHERE dept = 'Eng';"),
    ("MIN and MAX",
     "SELECT MAX(salary), MIN(salary) FROM employees;\n"
     "SELECT MIN(enrollment_date) FROM students;\n"
     "-- Name with highest GPA\n"
     "SELECT * FROM students\n"
     "WHERE gpa = (SELECT MAX(gpa) FROM students);"),
    ("GROUP BY and HAVING",
     "SELECT dept, COUNT(*), ROUND(AVG(gpa),2) AS avg\n"
     "FROM students\n"
     "GROUP BY dept\n"
     "HAVING AVG(gpa) > 3.0\n"
     "ORDER BY avg DESC;\n\n"
     "-- WHERE filters rows (before grouping)\n"
     "-- HAVING filters groups (after grouping)"),
  ]),

  (8, "joins-inner-left-right", "SQL JOINs - INNER LEFT RIGHT FULL", [
    ("JOIN Types",
     "INNER JOIN:      only matching rows from both tables\n"
     "LEFT JOIN:       all left rows + matching right rows\n"
     "RIGHT JOIN:      all right rows + matching left rows\n"
     "FULL OUTER JOIN: all rows from both tables\n"
     "SELF JOIN:       table joined with itself"),
    ("INNER JOIN",
     "SELECT s.first_name, d.dept_name\n"
     "FROM students s\n"
     "INNER JOIN departments d ON s.dept_id = d.dept_id;\n\n"
     "-- Three-table join\n"
     "SELECT s.name, c.course_name, e.grade\n"
     "FROM students s\n"
     "JOIN enrollments e ON s.id = e.student_id\n"
     "JOIN courses c ON e.course_id = c.id;"),
    ("LEFT JOIN",
     "SELECT s.first_name, d.dept_name\n"
     "FROM students s\n"
     "LEFT JOIN departments d ON s.dept_id = d.dept_id;\n\n"
     "-- Students with NO department:\n"
     "WHERE d.dept_id IS NULL;"),
    ("RIGHT JOIN",
     "SELECT s.first_name, d.dept_name\n"
     "FROM students s\n"
     "RIGHT JOIN departments d ON s.dept_id = d.dept_id;\n"
     "-- All departments even without students"),
    ("SELF JOIN",
     "-- Employee and their manager\n"
     "SELECT e.name AS employee, m.name AS manager\n"
     "FROM employees e\n"
     "JOIN employees m ON e.manager_id = m.emp_id;"),
  ]),

  (9, "subqueries-nested", "SQL Subqueries and Nested Queries", [
    ("What is a Subquery?",
     "A SELECT nested inside another SQL statement.\n"
     "Types: Scalar (one value), Row (one row),\n"
     "Table (many rows), Correlated (references outer query)."),
    ("WHERE Subquery",
     "-- Students with above-average GPA\n"
     "SELECT first_name, gpa FROM students\n"
     "WHERE gpa > (SELECT AVG(gpa) FROM students);"),
    ("IN vs EXISTS",
     "-- IN\n"
     "WHERE student_id IN (\n"
     "  SELECT student_id FROM enrollments WHERE course_id = 101\n"
     ");\n\n"
     "-- EXISTS (faster for large data)\n"
     "WHERE EXISTS (\n"
     "  SELECT 1 FROM enrollments e\n"
     "  WHERE e.student_id = s.student_id AND course_id = 101\n"
     ");"),
    ("Correlated Subquery",
     "-- GPA above department average\n"
     "SELECT s.first_name, s.gpa FROM students s\n"
     "WHERE s.gpa > (\n"
     "  SELECT AVG(s2.gpa) FROM students s2\n"
     "  WHERE s2.department = s.department\n"
     ");\n"
     "-- Runs once per outer row"),
    ("FROM Subquery",
     "SELECT dept, avg_gpa FROM (\n"
     "  SELECT department AS dept, AVG(gpa) AS avg_gpa\n"
     "  FROM students\n"
     "  GROUP BY department\n"
     ") AS stats\n"
     "WHERE avg_gpa > 3.0;"),
  ]),

  (10, "indexes-performance", "SQL Indexes and Performance", [
    ("What is an Index?",
     "Speeds up data retrieval dramatically.\n"
     "Without index: full table scan (slow).\n"
     "With index: direct access (fast).\n"
     "Trade-off: faster reads, slower writes."),
    ("Index Types",
     "PRIMARY KEY:    automatic clustered index\n"
     "UNIQUE INDEX:   enforces uniqueness + fast lookup\n"
     "REGULAR INDEX:  speeds up queries\n"
     "COMPOSITE:      index on multiple columns\n"
     "FULLTEXT INDEX: for text search"),
    ("Creating Indexes",
     "CREATE INDEX idx_name ON students(last_name);\n"
     "CREATE UNIQUE INDEX idx_email ON students(email);\n"
     "CREATE INDEX idx_dg ON students(department, gpa);\n"
     "DROP INDEX idx_name ON students;"),
    ("EXPLAIN",
     "EXPLAIN SELECT * FROM students WHERE email = 'a@b.com';\n\n"
     "type = ref/const  -->  index used (good)\n"
     "type = ALL        -->  full scan (bad, add index!)\n"
     "key               -->  which index was used\n"
     "rows              -->  estimated rows scanned"),
    ("Best Practices",
     "Index WHERE, JOIN ON, ORDER BY columns\n"
     "Index high-cardinality columns\n"
     "Use composite indexes for common query patterns\n\n"
     "Do NOT index every column\n"
     "Do NOT index rarely-used columns"),
  ]),

  (11, "views-virtual-tables", "SQL Views and Virtual Tables", [
    ("What is a View?",
     "A saved query acting as a virtual table.\n"
     "Does NOT store data itself.\n"
     "Benefits: simplify queries, improve security, consistent interface."),
    ("Create View",
     "CREATE VIEW student_summary AS\n"
     "SELECT first_name, department, gpa\n"
     "FROM students WHERE status = 'active';\n\n"
     "SELECT * FROM student_summary WHERE gpa > 3.5;"),
    ("Replace and Drop",
     "CREATE OR REPLACE VIEW student_summary AS\n"
     "SELECT first_name, gpa FROM students;\n\n"
     "DROP VIEW IF EXISTS student_summary;"),
    ("Updatable Views",
     "Single base table, no GROUP BY, no aggregates.\n\n"
     "UPDATE student_summary\n"
     "SET gpa = 3.9 WHERE last_name = 'Kumar';\n"
     "-- Updates underlying students table"),
    ("Security with Views",
     "CREATE VIEW public_emp AS\n"
     "SELECT emp_id, name, department FROM employees;\n"
     "-- salary column is hidden!\n\n"
     "GRANT SELECT ON public_emp TO 'hr'@'localhost';"),
  ]),

  (12, "stored-procedures", "SQL Stored Procedures and Functions", [
    ("Stored Procedures",
     "Saved SQL code executed repeatedly.\n"
     "Benefits: reduce network traffic,\n"
     "improve performance, enforce business logic."),
    ("Create Procedure",
     "DELIMITER //\n"
     "CREATE PROCEDURE GetStudents(IN dept VARCHAR(50))\n"
     "BEGIN\n"
     "  SELECT first_name, gpa FROM students\n"
     "  WHERE department = dept ORDER BY gpa DESC;\n"
     "END //\n"
     "DELIMITER ;\n\n"
     "CALL GetStudents('Computer Science');"),
    ("OUT Parameters",
     "DELIMITER //\n"
     "CREATE PROCEDURE DeptStats(\n"
     "  IN dept VARCHAR(50), OUT avg_gpa DECIMAL(3,2)\n"
     ")\n"
     "BEGIN\n"
     "  SELECT AVG(gpa) INTO avg_gpa\n"
     "  FROM students WHERE department = dept;\n"
     "END //\n"
     "DELIMITER ;\n"
     "CALL DeptStats('CS', @avg); SELECT @avg;"),
    ("User Functions",
     "DELIMITER //\n"
     "CREATE FUNCTION Grade(gpa DECIMAL(3,2))\n"
     "RETURNS VARCHAR(2) DETERMINISTIC\n"
     "BEGIN\n"
     "  IF gpa >= 3.7 THEN RETURN 'A+';\n"
     "  ELSEIF gpa >= 3.0 THEN RETURN 'B+';\n"
     "  ELSE RETURN 'B';\n"
     "  END IF;\n"
     "END //\n"
     "DELIMITER ;\n"
     "SELECT first_name, Grade(gpa) FROM students;"),
    ("Control Flow",
     "IF cond THEN ... ELSEIF cond THEN ... ELSE ... END IF;\n\n"
     "WHILE i <= 10 DO\n"
     "  SET total = total + i;\n"
     "  SET i = i + 1;\n"
     "END WHILE;\n\n"
     "CASE x WHEN 'A' THEN ... ELSE ... END CASE;"),
  ]),

  (13, "triggers-automation", "SQL Triggers and Automation", [
    ("What is a Trigger?",
     "Auto-executes SQL in response to INSERT, UPDATE, or DELETE.\n"
     "BEFORE: runs before the operation.\n"
     "AFTER:  runs after the operation.\n"
     "Uses: audit logging, validation, auto-calculations."),
    ("AFTER UPDATE Trigger",
     "DELIMITER //\n"
     "CREATE TRIGGER log_update\n"
     "AFTER UPDATE ON students FOR EACH ROW\n"
     "BEGIN\n"
     "  INSERT INTO audit(action, old_v, new_v, ts)\n"
     "  VALUES('UPDATE', OLD.gpa, NEW.gpa, NOW());\n"
     "END //\n"
     "DELIMITER ;\n\n"
     "-- OLD = values before change\n"
     "-- NEW = values after change"),
    ("BEFORE Trigger Validation",
     "DELIMITER //\n"
     "CREATE TRIGGER check_salary\n"
     "BEFORE UPDATE ON employees FOR EACH ROW\n"
     "BEGIN\n"
     "  IF NEW.salary < OLD.salary * 0.9 THEN\n"
     "    SIGNAL SQLSTATE '45000'\n"
     "    SET MESSAGE_TEXT = 'Cannot cut salary more than 10%';\n"
     "  END IF;\n"
     "END //\n"
     "DELIMITER ;"),
    ("INSERT Trigger",
     "CREATE TRIGGER after_insert\n"
     "AFTER INSERT ON students FOR EACH ROW\n"
     "INSERT INTO profiles(student_id, created_at)\n"
     "VALUES(NEW.student_id, NOW());"),
    ("Manage Triggers",
     "SHOW TRIGGERS;\n"
     "SHOW CREATE TRIGGER log_update;\n"
     "DROP TRIGGER IF EXISTS log_update;\n\n"
     "Best practice: keep simple, document behavior,\n"
     "avoid cascading triggers."),
  ]),

  (14, "transactions-acid", "SQL Transactions and ACID Properties", [
    ("What is a Transaction?",
     "Sequence of SQL operations treated as one unit.\n"
     "All succeed (COMMIT) or all fail (ROLLBACK).\n"
     "Classic example: bank transfer must be atomic."),
    ("COMMIT and ROLLBACK",
     "START TRANSACTION;\n\n"
     "UPDATE accounts SET balance = balance - 1000 WHERE id = 1;\n"
     "UPDATE accounts SET balance = balance + 1000 WHERE id = 2;\n\n"
     "COMMIT;     -- save changes\n"
     "-- OR\n"
     "ROLLBACK;   -- undo everything\n\n"
     "SAVEPOINT sp1;\n"
     "ROLLBACK TO sp1;"),
    ("ACID",
     "Atomicity:    all or nothing\n"
     "Consistency:  database moves between valid states\n"
     "Isolation:    transactions do not see each other's work\n"
     "Durability:   committed data survives crashes"),
    ("Isolation Levels",
     "READ UNCOMMITTED: dirty reads possible\n"
     "READ COMMITTED:   only committed data visible\n"
     "REPEATABLE READ:  stable results per query (MySQL default)\n"
     "SERIALIZABLE:     fully isolated, strictest\n\n"
     "SET TRANSACTION ISOLATION LEVEL REPEATABLE READ;"),
    ("Transaction Procedure",
     "DELIMITER //\n"
     "CREATE PROCEDURE Transfer(IN fid INT, IN tid INT, IN amt DECIMAL)\n"
     "BEGIN\n"
     "  DECLARE CONTINUE HANDLER FOR SQLEXCEPTION ROLLBACK;\n"
     "  START TRANSACTION;\n"
     "    UPDATE accounts SET balance = balance - amt WHERE id = fid;\n"
     "    UPDATE accounts SET balance = balance + amt WHERE id = tid;\n"
     "  COMMIT;\n"
     "END //"),
  ]),

  (15, "normalization-1nf-2nf-3nf", "Database Normalization 1NF 2NF 3NF", [
    ("What is Normalization?",
     "Organising data to reduce redundancy and improve integrity.\n"
     "Splits large tables into smaller related ones.\n"
     "Normal forms: 1NF, 2NF, 3NF, BCNF."),
    ("First Normal Form 1NF",
     "Each column has atomic (indivisible) values.\n"
     "No repeating groups.\n\n"
     "Wrong:\n"
     "id | name    | courses\n"
     "1  | Arshith | SQL, Python\n\n"
     "Right 1NF:\n"
     "id | name    | course\n"
     "1  | Arshith | SQL\n"
     "1  | Arshith | Python"),
    ("Second Normal Form 2NF",
     "1NF + no partial dependencies.\n\n"
     "Wrong: order_id, product_id | qty | product_name\n"
     "(product_name depends only on product_id)\n\n"
     "Fix: split into Orders(order_id, product_id, qty)\n"
     "and Products(product_id, product_name)"),
    ("Third Normal Form 3NF",
     "2NF + no transitive dependencies.\n\n"
     "Wrong: student_id | dept_id | dept_name | dept_head\n"
     "(dept_name depends on dept_id, not student_id)\n\n"
     "Fix: Students(student_id, dept_id)\n"
     "and Departments(dept_id, dept_name, dept_head)"),
    ("Denormalization",
     "Adding redundancy intentionally for read performance.\n"
     "When: read-heavy apps, analytics, costly JOINs.\n\n"
     "Balance: normalize for data integrity,\n"
     "denormalize for read speed."),
  ]),

  (16, "window-functions", "SQL Window Functions", [
    ("What are Window Functions?",
     "Calculations over related rows without GROUP BY collapse.\n\n"
     "Syntax:\n"
     "function() OVER (PARTITION BY col ORDER BY col)"),
    ("ROW_NUMBER RANK DENSE_RANK",
     "SELECT first_name, gpa,\n"
     "  ROW_NUMBER() OVER(PARTITION BY dept ORDER BY gpa DESC) rn,\n"
     "  RANK()       OVER(PARTITION BY dept ORDER BY gpa DESC) rnk,\n"
     "  DENSE_RANK() OVER(PARTITION BY dept ORDER BY gpa DESC) dr\n"
     "FROM students;\n\n"
     "ROW_NUMBER: 1,2,3,4 unique\n"
     "RANK:       1,2,2,4 skips after tie\n"
     "DENSE_RANK: 1,2,2,3 no skip"),
    ("LAG and LEAD",
     "SELECT month, revenue,\n"
     "  LAG(revenue)  OVER(ORDER BY month) AS prev_month,\n"
     "  LEAD(revenue) OVER(ORDER BY month) AS next_month,\n"
     "  revenue - LAG(revenue) OVER(ORDER BY month) AS growth\n"
     "FROM monthly_sales;\n\n"
     "LAG = look backward   LEAD = look forward"),
    ("NTILE and PERCENT_RANK",
     "SELECT first_name, gpa,\n"
     "  NTILE(4) OVER(ORDER BY gpa DESC) AS quartile,\n"
     "  ROUND(PERCENT_RANK() OVER(ORDER BY gpa), 2) AS pct\n"
     "FROM students;"),
    ("Running Total",
     "SELECT month, revenue,\n"
     "  SUM(revenue) OVER(\n"
     "    ORDER BY month ROWS UNBOUNDED PRECEDING\n"
     "  ) AS running_total,\n"
     "  AVG(revenue) OVER(\n"
     "    ORDER BY month\n"
     "    ROWS BETWEEN 2 PRECEDING AND CURRENT ROW\n"
     "  ) AS moving_avg_3\n"
     "FROM monthly_sales;"),
  ]),

  (17, "cte-expressions", "SQL Common Table Expressions CTE", [
    ("What is a CTE?",
     "Temporary named result using WITH.\n"
     "Exists only during query execution.\n"
     "Benefits: readable, recursive, reusable within query.\n\n"
     "WITH name AS (SELECT ...) SELECT * FROM name;"),
    ("Simple CTE",
     "WITH avg_gpa AS (\n"
     "  SELECT AVG(gpa) AS average FROM students\n"
     ")\n"
     "SELECT s.first_name, s.gpa\n"
     "FROM students s, avg_gpa\n"
     "WHERE s.gpa > avg_gpa.average;"),
    ("Multiple CTEs",
     "WITH\n"
     "  dept_avg AS (\n"
     "    SELECT dept, AVG(gpa) avg FROM students GROUP BY dept\n"
     "  ),\n"
     "  top AS (\n"
     "    SELECT * FROM students WHERE gpa > 3.8\n"
     "  )\n"
     "SELECT t.name, d.avg\n"
     "FROM top t JOIN dept_avg d ON t.dept = d.dept;"),
    ("Recursive CTE",
     "WITH RECURSIVE org AS (\n"
     "  SELECT emp_id, name, manager_id, 0 AS level\n"
     "  FROM employees WHERE manager_id IS NULL\n"
     "  UNION ALL\n"
     "  SELECT e.emp_id, e.name, e.manager_id, o.level+1\n"
     "  FROM employees e JOIN org o ON e.manager_id = o.emp_id\n"
     ")\n"
     "SELECT * FROM org ORDER BY level;"),
    ("CTE vs View vs Subquery",
     "CTE:      query-scoped, readable, recursive capable\n"
     "Subquery: inline, not reusable\n"
     "View:     persistent, reusable across sessions\n\n"
     "Use CTE for complex single-query logic.\n"
     "Use View for multi-session reusable logic."),
  ]),

  (18, "string-date-functions", "SQL String and Date Functions", [
    ("String Functions",
     "LENGTH('Hello')      -- 5\n"
     "UPPER('hello')       -- HELLO\n"
     "LOWER('HELLO')       -- hello\n"
     "TRIM('  hi  ')       -- hi\n"
     "LPAD('5', 3, '0')    -- 005\n"
     "REPEAT('SQL ', 3)    -- SQL SQL SQL"),
    ("String Manipulation",
     "CONCAT(first_name, ' ', last_name)\n"
     "SUBSTRING('Hello World', 7, 5)  -- World\n"
     "LEFT('Hello', 3)                -- Hel\n"
     "RIGHT('Hello', 3)               -- llo\n"
     "REPLACE('Hello World', 'World', 'SQL')"),
    ("Search Functions",
     "INSTR('Hello World', 'World')  -- 7\n"
     "FORMAT(1234567.89, 2)          -- 1,234,567.89\n"
     "-- REGEXP pattern matching\n"
     "WHERE email REGEXP '^[a-z]+@gmail\\.com$'"),
    ("Date Functions",
     "NOW()          -- 2024-01-15 10:30:45\n"
     "CURDATE()      -- 2024-01-15\n"
     "YEAR(NOW())  MONTH(NOW())  DAY(NOW())\n"
     "DAYNAME(NOW())   -- Monday\n"
     "MONTHNAME(NOW()) -- January"),
    ("Date Arithmetic",
     "DATE_ADD('2024-01-15', INTERVAL 30 DAY)   -- 2024-02-14\n"
     "DATE_SUB('2024-01-15', INTERVAL 1 MONTH)\n"
     "DATEDIFF('2024-12-31', '2024-01-01')       -- 365\n"
     "DATE_FORMAT(NOW(), '%d/%m/%Y')             -- 15/01/2024"),
  ]),

  (19, "null-handling-case", "SQL NULL Handling and CASE Expressions", [
    ("Understanding NULL",
     "NULL = unknown or missing value.\n"
     "NOT zero, NOT empty string.\n\n"
     "NULL = NULL  is FALSE\n"
     "NULL != NULL is FALSE\n"
     "Any math with NULL = NULL\n"
     "Use IS NULL, never = NULL"),
    ("IS NULL Queries",
     "SELECT * FROM students WHERE email IS NULL;\n"
     "SELECT * FROM students WHERE email IS NOT NULL;\n\n"
     "-- Count missing emails\n"
     "SELECT COUNT(*) - COUNT(email) AS no_email FROM students;"),
    ("COALESCE and IFNULL",
     "COALESCE(NULL, NULL, 'default')  -- returns 'default'\n\n"
     "SELECT first_name,\n"
     "  COALESCE(phone, email, 'No contact') AS contact\n"
     "FROM students;\n\n"
     "IFNULL(phone, 'N/A')    -- NULL becomes N/A\n"
     "NULLIF(gpa, 0)          -- returns NULL if gpa = 0"),
    ("CASE Expression",
     "SELECT first_name,\n"
     "  CASE\n"
     "    WHEN gpa >= 3.7 THEN 'A+ Distinction'\n"
     "    WHEN gpa >= 3.3 THEN 'A  Excellent'\n"
     "    WHEN gpa >= 3.0 THEN 'B+ Good'\n"
     "    ELSE                 'B  Average'\n"
     "  END AS grade_label\n"
     "FROM students;"),
    ("CASE in Aggregates",
     "SELECT\n"
     "  COUNT(CASE WHEN gpa >= 3.5 THEN 1 END) AS honor_roll,\n"
     "  COUNT(CASE WHEN gpa <  2.0 THEN 1 END) AS at_risk,\n"
     "  COUNT(*) AS total\n"
     "FROM students;"),
  ]),

  (20, "er-diagrams-schema", "ER Diagrams and Schema Design", [
    ("ER Diagram Components",
     "Entity:       real-world object (Students, Courses)\n"
     "Attribute:    property of entity (name, age, gpa)\n"
     "Relationship: how entities connect (enrolls in)\n"
     "Cardinality:  how many (1:1, 1:N, M:N)"),
    ("Cardinality Types",
     "One-to-One  1:1   Person --- Passport\n"
     "One-to-Many 1:N   Department --- Students\n"
     "                  (one dept has many students)\n"
     "Many-to-Many M:N  Students --- Courses\n"
     "                  (requires a junction table!)"),
    ("University Schema",
     "departments(dept_id PK, name, head_id)\n"
     "instructors(inst_id PK, name, dept_id FK)\n"
     "courses(course_id PK, title, credits, inst_id FK)\n"
     "students(student_id PK, name, dept_id FK)\n"
     "enrollments(student_id FK, course_id FK, grade, semester)"),
    ("Design Best Practices",
     "Every table needs a PRIMARY KEY\n"
     "Use FOREIGN KEYS for relationships\n"
     "Plural table names: students, not student\n"
     "Consistent snake_case naming\n"
     "Add created_at / updated_at timestamps\n"
     "Normalize to at least 3NF"),
    ("Blog Schema Example",
     "CREATE TABLE users (\n"
     "  user_id INT AUTO_INCREMENT PRIMARY KEY,\n"
     "  username VARCHAR(50) UNIQUE NOT NULL,\n"
     "  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP\n"
     ");\n"
     "CREATE TABLE posts (\n"
     "  post_id INT AUTO_INCREMENT PRIMARY KEY,\n"
     "  user_id INT NOT NULL,\n"
     "  title VARCHAR(200),\n"
     "  FOREIGN KEY(user_id) REFERENCES users(user_id)\n"
     "    ON DELETE CASCADE\n"
     ");"),
  ]),

  (21, "advanced-queries", "Advanced Queries and Optimization", [
    ("Query Execution Order",
     "1. FROM / JOIN\n"
     "2. WHERE\n"
     "3. GROUP BY\n"
     "4. HAVING\n"
     "5. SELECT\n"
     "6. DISTINCT\n"
     "7. ORDER BY\n"
     "8. LIMIT / OFFSET"),
    ("Optimization Tips",
     "Use specific columns, not SELECT *\n"
     "Filter early with WHERE before joins\n"
     "Index JOIN and WHERE columns\n"
     "Use LIMIT when you do not need all rows\n"
     "Use EXISTS over IN for large subqueries\n"
     "Prefer JOINs over correlated subqueries"),
    ("Common Mistakes",
     "-- Wrong: breaks index!\n"
     "WHERE YEAR(date) = 2024\n\n"
     "-- Right: uses index\n"
     "WHERE date BETWEEN '2024-01-01' AND '2024-12-31'\n\n"
     "-- Wrong: leading wildcard, no index\n"
     "WHERE name LIKE '%Kumar'\n\n"
     "-- Right: uses index\n"
     "WHERE name LIKE 'Kumar%'"),
    ("UNION and UNION ALL",
     "UNION:     removes duplicates (slower)\n"
     "UNION ALL: keeps all rows (faster)\n\n"
     "SELECT name FROM students\n"
     "UNION ALL\n"
     "SELECT name FROM alumni;\n\n"
     "Rules: same column count and compatible types"),
    ("EXPLAIN Analysis",
     "EXPLAIN SELECT * FROM students WHERE email = 'a@b.com';\n\n"
     "type = ref or const  --> good (index used)\n"
     "type = ALL           --> bad  (full table scan!)\n"
     "key                  --> which index was used\n"
     "rows                 --> estimated rows examined"),
  ]),

  (22, "security-user-management", "SQL Security and User Management", [
    ("User Management",
     "CREATE USER 'arshith'@'localhost' IDENTIFIED BY 'Pass123!';\n"
     "ALTER USER  'arshith'@'localhost' IDENTIFIED BY 'New!';\n"
     "DROP USER   'arshith'@'localhost';\n"
     "SELECT user, host FROM mysql.user;"),
    ("GRANT Privileges",
     "GRANT ALL PRIVILEGES ON school.* TO 'arshith'@'localhost';\n"
     "GRANT SELECT, INSERT ON school.students TO 'teacher'@'localhost';\n"
     "GRANT SELECT ON school.* TO 'reporter'@'localhost';\n"
     "FLUSH PRIVILEGES;"),
    ("REVOKE Privileges",
     "REVOKE DELETE ON school.students FROM 'teacher'@'localhost';\n"
     "REVOKE ALL PRIVILEGES ON school.* FROM 'teacher'@'localhost';\n"
     "SHOW GRANTS FOR 'arshith'@'localhost';"),
    ("SQL Injection",
     "Vulnerability: WHERE user = '\" + input + \"'\n"
     "Attack input:  admin' OR '1'='1  --> bypasses login!\n\n"
     "Prevention:\n"
     "Use prepared statements / parameterized queries\n"
     "Validate and sanitize all user input\n"
     "Least-privilege database accounts\n"
     "Escape special characters"),
    ("Security Best Practices",
     "Never store plain-text passwords (use bcrypt)\n"
     "Encrypt sensitive columns at rest\n"
     "Regular automated backups\n"
     "Audit logging on sensitive tables\n"
     "Use VIEWS to limit data exposure\n"
     "Principle of least privilege for every user"),
  ]),

  (23, "backup-recovery", "SQL Backup Recovery and Maintenance", [
    ("Backup Types",
     "Full:        complete copy of everything\n"
     "Incremental: only changes since last backup\n"
     "Differential: changes since last FULL backup\n"
     "Logical:     SQL dump file (portable)\n"
     "Physical:    raw database files"),
    ("mysqldump",
     "-- Backup single database\n"
     "mysqldump -u root -p school_db > backup.sql\n\n"
     "-- Backup all databases\n"
     "mysqldump -u root -p --all-databases > all.sql\n\n"
     "-- Restore from backup\n"
     "mysql -u root -p school_db < backup.sql\n\n"
     "-- Compressed backup\n"
     "mysqldump -u root -p school_db | gzip > backup.sql.gz"),
    ("Maintenance Commands",
     "CHECK TABLE students;       -- check for errors\n"
     "REPAIR TABLE students;      -- repair corrupted table\n"
     "OPTIMIZE TABLE students;    -- reclaim space\n"
     "ANALYZE TABLE students;     -- update key stats\n"
     "SHOW TABLE STATUS LIKE 'students';"),
    ("Performance Monitoring",
     "SHOW PROCESSLIST;\n"
     "SHOW STATUS LIKE 'Connections';\n"
     "SHOW VARIABLES LIKE 'slow_query_log%';\n"
     "SET GLOBAL slow_query_log = 'ON';\n"
     "SET GLOBAL long_query_time = 2;"),
    ("Replication Basics",
     "Master: handles all writes\n"
     "Slave:  handles reads (improves performance)\n\n"
     "Benefits: high availability, load balancing,\n"
     "backups without downtime, geographic distribution\n\n"
     "Types:\n"
     "Asynchronous: master does not wait\n"
     "Synchronous:  master waits for confirmation"),
  ]),

  (24, "real-world-projects", "SQL Real World Projects", [
    ("E-Commerce Schema",
     "products(id, name, price, stock)\n"
     "orders(id, customer_id, total, status)\n"
     "order_items(order_id, product_id, qty)\n\n"
     "-- Top selling products\n"
     "SELECT p.name, SUM(oi.qty) AS sold\n"
     "FROM products p\n"
     "JOIN order_items oi ON p.id = oi.product_id\n"
     "GROUP BY p.id ORDER BY sold DESC LIMIT 10;"),
    ("HR Hierarchy",
     "WITH RECURSIVE tree AS (\n"
     "  SELECT emp_id, name, manager_id, 0 AS level\n"
     "  FROM employees WHERE manager_id IS NULL\n"
     "  UNION ALL\n"
     "  SELECT e.emp_id, e.name, e.manager_id, t.level+1\n"
     "  FROM employees e JOIN tree t ON e.manager_id = t.emp_id\n"
     ")\n"
     "SELECT REPEAT('  ', level), name FROM tree;"),
    ("School Analytics",
     "SELECT d.dept_name,\n"
     "  COUNT(*) AS students,\n"
     "  ROUND(AVG(gpa), 2) AS avg_gpa,\n"
     "  COUNT(CASE WHEN gpa >= 3.5 THEN 1 END) AS honor_roll\n"
     "FROM students s\n"
     "JOIN departments d ON s.dept_id = d.dept_id\n"
     "GROUP BY d.dept_id ORDER BY avg_gpa DESC;"),
    ("Inventory Alert",
     "SELECT name, stock,\n"
     "  CASE\n"
     "    WHEN stock = 0              THEN 'OUT OF STOCK'\n"
     "    WHEN stock < reorder_level  THEN 'REORDER NOW'\n"
     "    ELSE                             'OK'\n"
     "  END AS status\n"
     "FROM products\n"
     "WHERE stock <= reorder_level;"),
    ("Interview Q and A",
     "1. DELETE vs TRUNCATE vs DROP?\n"
     "   DELETE:   rollback-able, triggers fire\n"
     "   TRUNCATE: fast, no rollback, no triggers\n"
     "   DROP:     removes table entirely\n\n"
     "2. HAVING vs WHERE?\n"
     "   WHERE:  filters rows before GROUP BY\n"
     "   HAVING: filters groups after GROUP BY\n\n"
     "3. Clustered vs Non-clustered index?\n"
     "   Clustered:     data physically sorted by key\n"
     "   Non-clustered: separate pointer structure"),
  ]),

  (25, "nosql-future-databases", "SQL vs NoSQL and Future of Databases", [
    ("SQL vs NoSQL",
     "SQL:   fixed schema, ACID, complex queries\n"
     "       MySQL, PostgreSQL, Oracle, SQL Server\n\n"
     "NoSQL: flexible schema, horizontal scale\n"
     "       MongoDB, Redis, Cassandra, DynamoDB\n\n"
     "SQL: banking, ERP, e-commerce\n"
     "NoSQL: social media, IoT, real-time analytics"),
    ("NewSQL Databases",
     "Combines SQL ACID guarantees + NoSQL scalability:\n\n"
     "Google Spanner:   globally distributed SQL\n"
     "CockroachDB:      resilient distributed SQL\n"
     "TiDB:             MySQL-compatible distributed\n"
     "YugabyteDB:       high-performance distributed"),
    ("Cloud Databases",
     "AWS RDS:          managed MySQL, PostgreSQL, Oracle\n"
     "AWS Aurora:       5x faster MySQL compatible\n"
     "Google BigQuery:  serverless analytics warehouse\n"
     "Azure SQL:        managed SQL Server\n"
     "PlanetScale:      serverless MySQL"),
    ("OLTP vs OLAP",
     "OLTP: many small transactions, normalized, fast reads/writes\n"
     "      Examples: MySQL, PostgreSQL\n\n"
     "OLAP: complex analytics, denormalized, large scans\n"
     "      Examples: BigQuery, Snowflake, Redshift\n\n"
     "ETL:  Extract from OLTP, Transform, Load into OLAP"),
    ("Career Paths",
     "SQL opens paths to:\n"
     "Database Administrator (DBA)\n"
     "Data Analyst\n"
     "Data Engineer\n"
     "Data Scientist\n"
     "Backend Developer\n\n"
     "Next steps: Python, data modeling,\n"
     "certifications, Kaggle datasets,\n"
     "data warehouses (Snowflake, BigQuery)"),
  ]),
]


if __name__ == "__main__":
    output_dir = os.path.join("media", "courses", "sql-dbms")
    print(f"Generating 25 SQL modules in: {output_dir}")
    print("=" * 60)
    for num, slug, title, sections in MODULES:
        build_pdf(num, slug, title, sections, output_dir)
    print("=" * 60)
    print("All 25 SQL/DBMS modules generated successfully!")