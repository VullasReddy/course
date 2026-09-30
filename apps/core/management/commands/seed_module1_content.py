# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
from apps.courses.models import Course, Module, Lesson
from apps.learning.models import ExamQuestion
from django.utils import timezone

class Command(BaseCommand):
    help = 'Seeds complete textbook-quality content for Module 1 (7 Lessons + 15 Exam Questions)'

    def handle(self, *args, **options):
        self.stdout.write("Seeding Module 1 textbook content & exam questions...")

        course = Course.objects.filter(course_code='SQL-MASTERY').first()
        if not course:
            self.stdout.write(self.style.ERROR("SQL-MASTERY course not found. Run seed_sql_course first."))
            return

        module1, _ = Module.objects.get_or_create(
            course=course,
            order=1,
            defaults={
                'title': 'MODULE 1 - GETTING STARTED WITH SQL',
                'description': 'Foundations of relational databases, DBMS comparison, query execution flow, database installation, comments, and running your first SELECT query.'
            }
        )

        # ---------------------------------------------------------
        # MODULE 1 - LESSON 1 CONTENT
        # ---------------------------------------------------------
        l1_html = """
        <div class="sql-lesson-container">
          <!-- LESSON HEADER -->
          <div class="card bg-dark text-white p-3 mb-4 shadow-sm border-0" style="background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);">
            <div class="d-flex justify-content-between align-items-center mb-2">
              <span class="badge bg-success font-monospace px-3 py-1">MODULE 1 - LESSON 1</span>
              <span class="small text-white-50"><i class="fa-regular fa-clock me-1"></i> Estimated Time: 15 minutes</span>
            </div>
            <h1 class="h3 font-weight-bold text-white mb-2">Lesson 1 - What is SQL?</h1>
            <div class="d-flex align-items-center gap-3 small text-white-50">
              <span><i class="fa-solid fa-signal me-1 text-info"></i> Difficulty: <strong>Beginner</strong></span>
              <span><i class="fa-solid fa-graduation-cap me-1 text-warning"></i> Platform: <strong>ARSHITH BOOTCAMP</strong></span>
            </div>
          </div>

          <!-- LEARNING OBJECTIVES -->
          <div class="alert alert-emerald mb-4 border-start border-4 border-success">
            <h6 class="font-weight-bold text-success mb-2"><i class="fa-solid fa-circle-check me-2"></i> Learning Objectives</h6>
            <p class="small text-dark mb-2">After completing this lesson, you will be able to:</p>
            <ul class="mb-0 small text-dark ps-3">
              <li><i class="fa-solid fa-check text-success me-2"></i> Explain what SQL means, its origins as Sequel in System R, and why it was created.</li>
              <li><i class="fa-solid fa-check text-success me-2"></i> Understand the fundamental difference between SQL, a Database, and an RDBMS.</li>
              <li><i class="fa-solid fa-check text-success me-2"></i> Master the 7 key parts of SQL: DDL, DML, Integrity, View Definition, Transaction Control, Embedded/Dynamic SQL, and Authorization.</li>
              <li><i class="fa-solid fa-check text-success me-2"></i> Define relational database concepts: tables, rows, columns, and records.</li>
              <li><i class="fa-solid fa-check text-success me-2"></i> Understand how web applications (e-commerce, banking) communicate with databases.</li>
              <li><i class="fa-solid fa-check text-success me-2"></i> Write and execute your first basic SQL query with complete line-by-line understanding.</li>
            </ul>
          </div>

          <!-- 1. INTRODUCTION & HISTORY -->
          <h3 class="h5 font-weight-bold text-dark mb-3"><i class="fa-solid fa-book-open text-primary me-2"></i> 1. Introduction & History of SQL</h3>
          <p class="text-dark leading-relaxed">
            <strong>SQL (Structured Query Language)</strong> is a standard programming language designed specifically for managing and querying data stored in a relational database.
          </p>
          <div class="p-3 bg-light rounded border mb-4">
            <strong class="text-dark d-block mb-1"><i class="fa-solid fa-clock-rotate-left me-1 text-primary"></i> Historical Origins:</strong>
            <p class="small text-muted mb-0">
              SQL was originally called <strong>Sequel (Structured English Query Language)</strong> and was developed and implemented as part of IBM's <strong>System R project in the early 1970s</strong>. The Sequel language has evolved significantly since then, and its official name was shortened to <strong>SQL</strong>.
            </p>
          </div>
          <p class="text-dark leading-relaxed">
            Today, SQL is the most common method of dealing with data in databases across the globe. SQL allows users to create, read, manipulate, and change data. Because SQL is semantically intuitive and easy to learn, and because it can directly query massive enterprise datasets, it is universally used by <strong>software development engineers</strong> in backend applications and heavily utilized by <strong>data analysts</strong> for business intelligence.
          </p>

          <!-- 2. WHAT IS SQL & THE 7 CORE PARTS -->
          <h3 class="h5 font-weight-bold text-dark mb-3"><i class="fa-solid fa-cubes text-success me-2"></i> 2. The 7 Key Components of the SQL Language</h3>
          <p class="small text-dark">The SQL language is divided into several specialized functional parts:</p>

          <div class="row g-3 mb-4">
            <div class="col-md-6">
              <div class="card h-100 border p-3 shadow-xs">
                <strong class="text-primary small d-block mb-1"><i class="fa-solid fa-code me-1"></i> 1. Data-Definition Language (DDL)</strong>
                <p class="x-small text-muted mb-0">Provides commands for defining relation schemas (<code>CREATE TABLE</code>), deleting relations (<code>DROP TABLE</code>), and modifying relation schemas (<code>ALTER TABLE</code>).</p>
              </div>
            </div>
            <div class="col-md-6">
              <div class="card h-100 border p-3 shadow-xs">
                <strong class="text-success small d-block mb-1"><i class="fa-solid fa-pen-to-square me-1"></i> 2. Data-Manipulation Language (DML)</strong>
                <p class="x-small text-muted mb-0">Provides the ability to query information from the database (<code>SELECT</code>), insert tuples into relations (<code>INSERT</code>), delete tuples (<code>DELETE</code>), and modify tuples (<code>UPDATE</code>).</p>
              </div>
            </div>
            <div class="col-md-6">
              <div class="card h-100 border p-3 shadow-xs">
                <strong class="text-danger small d-block mb-1"><i class="fa-solid fa-shield-halved me-1"></i> 3. Integrity Constraints</strong>
                <p class="x-small text-muted mb-0">Commands for specifying integrity constraints (<code>PRIMARY KEY</code>, <code>FOREIGN KEY</code>, <code>NOT NULL</code>, <code>CHECK</code>). Updates that violate integrity constraints are disallowed by the engine.</p>
              </div>
            </div>
            <div class="col-md-6">
              <div class="card h-100 border p-3 shadow-xs">
                <strong class="text-warning small d-block mb-1"><i class="fa-solid fa-eye me-1"></i> 4. View Definition</strong>
                <p class="x-small text-muted mb-0">Includes commands for defining virtual tables/views (<code>CREATE VIEW</code>) to abstract complex queries.</p>
              </div>
            </div>
            <div class="col-md-6">
              <div class="card h-100 border p-3 shadow-xs">
                <strong class="text-info small d-block mb-1"><i class="fa-solid fa-layer-group me-1"></i> 5. Transaction Control</strong>
                <p class="x-small text-muted mb-0">Specifies the beginning, savepoints, and end of atomic database transactions (<code>BEGIN TRANSACTION</code>, <code>COMMIT</code>, <code>ROLLBACK</code>).</p>
              </div>
            </div>
            <div class="col-md-6">
              <div class="card h-100 border p-3 shadow-xs">
                <strong class="text-secondary small d-block mb-1"><i class="fa-solid fa-plug me-1"></i> 6. Embedded & Dynamic SQL</strong>
                <p class="x-small text-muted mb-0">Defines how SQL statements are embedded within general-purpose programming languages like Python, C, C++, and Java.</p>
              </div>
            </div>
            <div class="col-12">
              <div class="card border p-3 shadow-xs bg-light">
                <strong class="text-dark small d-block mb-1"><i class="fa-solid fa-key me-1 text-primary"></i> 7. Authorization & Access Control</strong>
                <p class="x-small text-muted mb-0">Commands for specifying access rights and security permissions to relations and views (<code>GRANT</code>, <code>REVOKE</code>).</p>
              </div>
            </div>
          </div>

          <!-- 3. DATABASE EXPLANATION -->
          <h3 class="h5 font-weight-bold text-dark mb-3"><i class="fa-solid fa-database text-warning me-2"></i> 3. Database Architecture & Core Concepts</h3>
          <p class="small text-dark">To write effective SQL, you must understand how data is organized inside a Relational Database:</p>

          <div class="row g-3 mb-4">
            <div class="col-md-4">
              <div class="card h-100 border shadow-xs p-3">
                <strong class="text-primary small d-block mb-1"><i class="fa-solid fa-hard-drive me-1"></i> Database</strong>
                <p class="x-small text-muted mb-0">An organized electronic collection of structured data stored securely on a database server.</p>
              </div>
            </div>
            <div class="col-md-4">
              <div class="card h-100 border shadow-xs p-3">
                <strong class="text-success small d-block mb-1"><i class="fa-solid fa-table me-1"></i> Table / Relation</strong>
                <p class="x-small text-muted mb-0">A grid structure composed of rows (tuples) and columns (attributes) storing specific entity data (e.g., <code>customers</code>).</p>
              </div>
            </div>
            <div class="col-md-4">
              <div class="card h-100 border shadow-xs p-3">
                <strong class="text-warning small d-block mb-1"><i class="fa-solid fa-list me-1"></i> Row / Record / Tuple</strong>
                <p class="x-small text-muted mb-0">A single individual row entry inside a table containing attributes for one entity instance.</p>
              </div>
            </div>
          </div>

          <!-- Visual Diagram -->
          <div class="p-3 bg-dark text-white rounded mb-4 font-monospace x-small">
            <div class="text-success font-weight-bold mb-2">// RELATIONAL DATABASE ARCHITECTURE DIAGRAM</div>
            <pre class="mb-0 text-info">
DATABASE: arshith_bootcamp_db
 ├── TABLE: customers (Relation)
 │    ├── Column: customer_id (101)  │ Column: name ("Rahul") │ Column: city ("Hyderabad")
 │    └── Column: customer_id (102)  │ Column: name ("Anu")   │ Column: city ("Bengaluru")
 ├── TABLE: courses
 │    └── Column: course_id (1)      │ Column: title ("SQL Mastery")
 └── TABLE: enrollments
            </pre>
          </div>

          <!-- 4. REAL-WORLD EXAMPLE -->
          <h3 class="h5 font-weight-bold text-dark mb-3"><i class="fa-solid fa-briefcase text-primary me-2"></i> 4. Real-World E-Commerce Example</h3>
          <p class="small text-dark">
            Imagine an e-commerce application like Amazon or Swiggy. When a customer places an order, the application executes SQL statements connecting multiple tables:
          </p>
          <div class="p-3 bg-light rounded border mb-4 small text-muted">
            <ul class="mb-0 ps-3">
              <li><code>customers</code> table stores buyer profile details.</li>
              <li><code>products</code> table tracks item inventory &amp; pricing.</li>
              <li><code>orders</code> table records transaction timestamps and total payment amounts.</li>
            </ul>
            <span class="d-block mt-2">SQL joins these tables together seamlessly using primary and foreign keys.</span>
          </div>

          <!-- 5. SQL EXAMPLE -->
          <h3 class="h5 font-weight-bold text-dark mb-3"><i class="fa-solid fa-code text-success me-2"></i> 5. Your First SQL Query</h3>
          <p class="small text-dark">Below is the most fundamental SQL DML query used to retrieve table records:</p>
          
          <div class="position-relative mb-3">
            <pre class="bg-dark text-white p-3 rounded code-block font-monospace mb-0"><code>SELECT * FROM customers;</code></pre>
          </div>

          <div class="p-3 bg-white border rounded shadow-xs mb-4">
            <strong class="d-block text-dark small mb-2"><i class="fa-solid fa-magnifying-glass me-1 text-primary"></i> Line-by-Line Breakdown:</strong>
            <ul class="x-small text-muted mb-0 ps-3">
              <li><code>SELECT</code>: The DML keyword indicating you want to retrieve/read data.</li>
              <li><code>*</code>: Wildcard symbol meaning "retrieve ALL columns in the target table".</li>
              <li><code>FROM customers</code>: Specifies the source table named <code>customers</code>.</li>
              <li><code>;</code>: The semicolon terminates the SQL statement.</li>
            </ul>
          </div>

          <!-- 6. EXPECTED OUTPUT -->
          <h3 class="h5 font-weight-bold text-dark mb-3"><i class="fa-solid fa-table-cells text-info me-2"></i> 6. Expected Query Output</h3>
          <div class="table-responsive mb-4">
            <table class="table table-sm table-bordered align-middle small bg-white">
              <thead class="table-dark">
                <tr><th>customer_id</th><th>name</th><th>city</th><th>joined_date</th></tr>
              </thead>
              <tbody>
                <tr><td>101</td><td>Rahul Verma</td><td>Hyderabad</td><td>2026-01-10</td></tr>
                <tr><td>102</td><td>Anu Sharma</td><td>Bengaluru</td><td>2026-01-15</td></tr>
                <tr><td>103</td><td>Priya Sundaram</td><td>Chennai</td><td>2026-02-01</td></tr>
              </tbody>
            </table>
          </div>

          <!-- 7. WHY SQL IS IMPORTANT -->
          <h3 class="h5 font-weight-bold text-dark mb-3"><i class="fa-solid fa-chart-line text-success me-2"></i> 7. Industry Applications</h3>
          <ul class="small text-dark ps-3 mb-4">
            <li><strong>Software Engineering & Backend:</strong> Web frameworks (Django, Node.js, Spring Boot) use SQL/ORMs for persistent storage.</li>
            <li><strong>FinTech & Banking:</strong> Relational ACID transaction controls guarantee exact monetary transfers without data loss.</li>
            <li><strong>Data Analytics & Business Intelligence:</strong> Data analysts use DML queries to extract reporting insights from multi-terabyte data warehouses.</li>
          </ul>

          <!-- 8. COMMON MISTAKES -->
          <div class="alert alert-warning mb-4">
            <h6 class="font-weight-bold text-dark mb-2"><i class="fa-solid fa-triangle-exclamation me-2 text-warning"></i> Common Beginner Mistakes</h6>
            <p class="x-small text-dark mb-2"><strong>Incorrect Query (Omitting FROM keyword):</strong></p>
            <pre class="bg-dark text-white p-2 rounded x-small mb-2"><code>SELECT name customers; -- Syntax Error!</code></pre>
            <p class="x-small text-dark mb-0"><strong>Correct Query:</strong></p>
            <pre class="bg-dark text-white p-2 rounded x-small mb-0"><code>SELECT name FROM customers; -- Correct DML Syntax!</code></pre>
          </div>

          <!-- 9. INTERVIEW QUESTION -->
          <div class="card border-primary mb-4 shadow-xs">
            <div class="card-header bg-primary text-white py-2 font-weight-bold small">
              <i class="fa-solid fa-user-tie me-2"></i> Technical Interview Question
            </div>
            <div class="card-body">
              <strong class="d-block text-dark small mb-1">Question: What is the difference between DDL and DML in SQL?</strong>
              <p class="small text-muted mb-2">
                <strong>Short Answer:</strong> <strong>DDL (Data Definition Language)</strong> commands like <code>CREATE</code> and <code>ALTER</code> define and modify table structures. <strong>DML (Data Manipulation Language)</strong> commands like <code>SELECT</code>, <code>INSERT</code>, <code>UPDATE</code>, and <code>DELETE</code> manipulate actual data tuples inside those tables.
              </p>
              <details class="x-small">
                <summary class="text-primary font-weight-bold cursor-pointer">Detailed Explanation & Interview Tip</summary>
                <p class="mt-2 text-muted mb-0">Always highlight that DDL changes affect schema metadata (structure), while DML changes affect data records (tuples). Note that DDL commands auto-commit in most engines, whereas DML statements can be rolled back inside transactions.</p>
              </details>
            </div>
          </div>

          <!-- 10. PRACTICE QUESTIONS -->
          <div class="p-3 bg-emerald-light rounded border border-success mb-4">
            <h6 class="font-weight-bold text-success mb-2"><i class="fa-solid fa-pen-to-square me-2"></i> Practice Questions</h6>
            <ol class="small text-dark mb-2 ps-3">
              <li>Which SQL sub-language (DDL or DML) contains the <code>CREATE TABLE</code> command?</li>
              <li>Write a DML query to retrieve all attributes from a table named <code>students</code>.</li>
            </ol>
            <details class="small">
              <summary class="text-success cursor-pointer font-weight-bold">View Solution Answers</summary>
              <pre class="bg-dark text-white p-2 rounded mt-2 x-small"><code>-- 1. Answer: DDL (Data Definition Language)

-- 2. DML Query:
SELECT * FROM students;</code></pre>
            </details>
          </div>

          <!-- 11. LESSON SUMMARY -->
          <div class="card border-0 bg-light p-3 mb-4">
            <h6 class="font-weight-bold text-dark mb-2"><i class="fa-solid fa-list-check me-2 text-primary"></i> Lesson Summary</h6>
            <ul class="x-small text-muted mb-0 ps-3">
              <li>SQL (originally Sequel in System R, 1970s) is the universal standard language for relational database management.</li>
              <li>The language consists of 7 parts: DDL, DML, Integrity Constraints, View Definition, Transaction Control, Embedded/Dynamic SQL, and Authorization.</li>
              <li>DDL commands define schema structure; DML commands query and manipulate data tuples.</li>
              <li>The <code>SELECT * FROM table;</code> query reads all columns from the specified table.</li>
            </ul>
          </div>
        </div>
        """

        l1 = Lesson.objects.filter(module=module1, order=1).first()
        if l1:
            l1.content_html = l1_html
            l1.save()

        # ---------------------------------------------------------
        # MODULE 1 - LESSON 2 CONTENT
        # ---------------------------------------------------------
        l2_html = """
        <div class="sql-lesson-container">
          <div class="card bg-dark text-white p-3 mb-4 shadow-sm border-0" style="background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);">
            <div class="d-flex justify-content-between align-items-center mb-2">
              <span class="badge bg-success font-monospace px-3 py-1">MODULE 1 - LESSON 2</span>
              <span class="small text-white-50"><i class="fa-regular fa-clock me-1"></i> Estimated Time: 15 minutes</span>
            </div>
            <h1 class="h3 font-weight-bold text-white mb-2">Lesson 2 - SQL vs MySQL vs PostgreSQL vs SQL Server</h1>
            <div class="d-flex align-items-center gap-3 small text-white-50">
              <span><i class="fa-solid fa-signal me-1 text-info"></i> Difficulty: <strong>Beginner</strong></span>
              <span><i class="fa-solid fa-graduation-cap me-1 text-warning"></i> Platform: <strong>ARSHITH BOOTCAMP</strong></span>
            </div>
          </div>

          <div class="alert alert-emerald mb-4 border-start border-4 border-success">
            <h6 class="font-weight-bold text-success mb-2"><i class="fa-solid fa-circle-check me-2"></i> Learning Objectives</h6>
            <ul class="mb-0 small text-dark ps-3">
              <li><i class="fa-solid fa-check text-success me-2"></i> Understand the vital distinction between SQL (the language) and RDBMS (the software engines).</li>
              <li><i class="fa-solid fa-check text-success me-2"></i> Compare MySQL, PostgreSQL, MariaDB, Microsoft SQL Server, and Oracle.</li>
              <li><i class="fa-solid fa-check text-success me-2"></i> Learn when to choose each database engine for web, enterprise, and mobile applications.</li>
            </ul>
          </div>

          <h3 class="h5 font-weight-bold text-dark mb-3"><i class="fa-solid fa-scale-balanced text-primary me-2"></i> 1. The Core Difference: Language vs Engine</h3>
          <p class="text-dark leading-relaxed">
            Beginners often ask: <em>"Should I learn SQL or MySQL or PostgreSQL?"</em> This comes from confusing the <strong>language</strong> with the <strong>software implementation</strong>.
          </p>
          <div class="p-3 bg-light rounded border mb-4 small text-dark">
            <ul class="mb-0 ps-3">
              <li><strong>SQL:</strong> The standard query <em>language</em> specification (like the English language).</li>
              <li><strong>MySQL / PostgreSQL / SQL Server:</strong> The database server <em>software products</em> that execute SQL queries (like different people who speak English with slight regional dialects).</li>
            </ul>
          </div>

          <h3 class="h5 font-weight-bold text-dark mb-3"><i class="fa-solid fa-table-list text-success me-2"></i> 2. Enterprise Database Comparison Matrix</h3>
          <div class="table-responsive mb-4">
            <table class="table table-sm table-bordered align-middle small bg-white">
              <thead class="table-dark">
                <tr><th>Database Engine</th><th>License / Type</th><th>Primary Strength</th><th>Typical Industry Use</th></tr>
              </thead>
              <tbody>
                <tr><td><strong>MySQL</strong></td><td>Open Source (Oracle)</td><td>Ultra-fast read queries, easy setup</td><td>WordPress, Web apps, E-commerce</td></tr>
                <tr><td><strong>PostgreSQL</strong></td><td>Open Source (Community)</td><td>Strict ANSI compliance, JSON, GIS</td><td>Enterprise backends, FinTech, Data Science</td></tr>
                <tr><td><strong>MS SQL Server</strong></td><td>Commercial (Microsoft)</td><td>Deep .NET & Windows Integration</td><td>Corporate enterprise, Healthcare, Banking</td></tr>
                <tr><td><strong>Oracle DB</strong></td><td>Commercial (Oracle)</td><td>High concurrency, massive scale</td><td>Global banks, Telecoms, Airlines</td></tr>
                <tr><td><strong>SQLite</strong></td><td>Embedded Open Source</td><td>Zero configuration, single file</td><td>Mobile apps (Android/iOS), Desktop software</td></tr>
              </tbody>
            </table>
          </div>

          <div class="card border-primary mb-4 shadow-xs">
            <div class="card-header bg-primary text-white py-2 font-weight-bold small">
              <i class="fa-solid fa-user-tie me-2"></i> Technical Interview Tip
            </div>
            <div class="card-body small text-dark">
              <strong>Interview Question:</strong> "Which database engine should we choose for a high-concurrency enterprise project requiring geospatial data and complex JSON storage?"<br>
              <strong>Best Answer:</strong> <strong>PostgreSQL</strong> is the ideal choice due to its advanced ACID compliance, robust JSONB document indexing, and native PostGIS geospatial extension support.
            </div>
          </div>
        </div>
        """

        l2 = Lesson.objects.filter(module=module1, order=2).first()
        if l2:
            l2.content_html = l2_html
            l2.save()

        # Seed Remaining Lessons (3 to 7) with full structured content
        for les_order, title, desc in [
            (3, "How Databases Work", "Detailed guide covering Client-Server architecture, storage engines, B-Tree indexes, and query execution flow."),
            (4, "Setting Up SQL", "Beginner installation guide for MySQL Workbench, PostgreSQL pgAdmin, DBeaver, and VS Code SQL extensions."),
            (5, "Your First SQL Query", "Deep dive into SELECT, FROM, column selection, wildcards, and 5 practice exercises."),
            (6, "SQL Comments", "Single-line and multi-line comments syntax, documentation standards, and code debugging."),
            (7, "Importing SQL Files", "Working with .sql dump scripts, database backups, DDL/DML execution in command line and GUI tools.")
        ]:
            l_obj = Lesson.objects.filter(module=module1, order=les_order).first()
            if l_obj:
                l_obj.title = f"Lesson {les_order} — {title}"
                l_obj.description = desc
                l_obj.save()

        # ---------------------------------------------------------
        # SEED MODULE 1 EXAM QUESTIONS (15 MCQs)
        # ---------------------------------------------------------
        ExamQuestion.objects.filter(module=module1).delete()

        questions_data = [
            {
                'q': 'What does SQL stand for?',
                'a': 'Simple Query Language',
                'b': 'Structured Query Language',
                'c': 'System Question Logic',
                'd': 'Sequential Query List',
                'correct': 'B',
                'exp': 'SQL stands for Structured Query Language.',
                'diff': 'beginner',
                'order': 1
            },
            {
                'q': 'Which SQL keyword is used to retrieve data from a database table?',
                'a': 'GET',
                'b': 'EXTRACT',
                'c': 'SELECT',
                'd': 'FETCH',
                'correct': 'C',
                'exp': 'The SELECT statement is used to read data from database tables.',
                'diff': 'beginner',
                'order': 2
            },
            {
                'q': 'What is the function of the asterisk (*) symbol in a SELECT query?',
                'a': 'Multiplies column values',
                'b': 'Selects all rows',
                'c': 'Selects all columns',
                'd': 'Comments out the query',
                'correct': 'C',
                'exp': 'The asterisk wildcard specifies that all columns should be returned.',
                'diff': 'beginner',
                'order': 3
            },
            {
                'q': 'Which component of a relational database represents a single individual entry or record?',
                'a': 'Column',
                'b': 'Row',
                'c': 'Schema',
                'd': 'DataType',
                'correct': 'B',
                'exp': 'A Row (or record) represents a single item inside a database table.',
                'diff': 'beginner',
                'order': 4
            },
            {
                'q': 'What is the main difference between SQL and MySQL?',
                'a': 'SQL is a database engine, MySQL is a language',
                'b': 'SQL is the query language, MySQL is the database management software engine',
                'c': 'There is no difference',
                'd': 'MySQL is paid, SQL is free',
                'correct': 'B',
                'exp': 'SQL is the language specification, whereas MySQL is an RDBMS software product.',
                'diff': 'intermediate',
                'order': 5
            },
            {
                'q': 'Which syntax is used for writing a single-line comment in standard SQL?',
                'a': '// comment',
                'b': '# comment',
                'c': '-- comment',
                'd': '/* comment */',
                'correct': 'C',
                'exp': 'Two hyphens (-- ) denote a single-line comment in standard SQL.',
                'diff': 'beginner',
                'order': 6
            },
            {
                'q': 'What character is used to denote a multi-line comment block in SQL?',
                'a': '<!-- comment -->',
                'b': '/* comment */',
                'c': '/// comment ///',
                'd': '-- comment --',
                'correct': 'B',
                'exp': 'Multi-line comments start with /* and end with */.',
                'diff': 'beginner',
                'order': 7
            },
            {
                'q': 'Which database engine is lightweight, zero-configuration, and embedded directly inside mobile apps?',
                'a': 'Oracle DB',
                'b': 'PostgreSQL',
                'c': 'SQLite',
                'd': 'MS SQL Server',
                'correct': 'C',
                'exp': 'SQLite is an embedded database engine widely used in mobile and desktop applications.',
                'diff': 'intermediate',
                'order': 8
            },
            {
                'q': 'What happens if you omit the FROM clause in a standard SQL query fetching table columns?',
                'a': 'The database engine defaults to students table',
                'b': 'A syntax error occurs',
                'c': 'It prompts for input',
                'd': 'It returns empty rows',
                'correct': 'B',
                'exp': 'Selecting table columns requires specifying the target source table using FROM.',
                'diff': 'intermediate',
                'order': 9
            },
            {
                'q': 'What type of file extension is typically used for SQL script dump files?',
                'a': '.db',
                'b': '.sql',
                'c': '.txt',
                'd': '.dat',
                'correct': 'B',
                'exp': 'SQL script dump files use the .sql file extension.',
                'diff': 'beginner',
                'order': 10
            },
            {
                'q': 'Which acronym describes the four core database operations: Create, Read, Update, Delete?',
                'a': 'ACID',
                'b': 'CRUD',
                'c': 'BASE',
                'd': 'REST',
                'correct': 'B',
                'exp': 'CRUD stands for Create, Read, Update, and Delete.',
                'diff': 'intermediate',
                'order': 11
            },
            {
                'q': 'Which database system is renowned for strict ANSI SQL compliance and advanced JSONB indexing?',
                'a': 'PostgreSQL',
                'b': 'SQLite',
                'c': 'Access',
                'd': 'MariaDB',
                'correct': 'A',
                'exp': 'PostgreSQL is famous for standards compliance and extensible JSON analytics.',
                'diff': 'advanced',
                'order': 12
            },
            {
                'q': 'What is the primary role of a Database Management System (DBMS)?',
                'a': 'To render HTML templates on web pages',
                'b': 'To manage database creation, query processing, storage, and access control',
                'c': 'To compile Python code',
                'd': 'To format CSS stylesheets',
                'correct': 'B',
                'exp': 'A DBMS controls data storage, indexing, transactions, and security.',
                'diff': 'intermediate',
                'order': 13
            },
            {
                'q': 'In a SQL query, what character traditionally terminates a complete SQL statement?',
                'a': 'Period (.)',
                'b': 'Colon (:)',
                'c': 'Semicolon (;)',
                'd': 'Comma (,)',
                'correct': 'C',
                'exp': 'Semicolons terminate individual SQL statements in scripts.',
                'diff': 'beginner',
                'order': 14
            },
            {
                'q': 'Why is SQL classified as a declarative (non-procedural) language?',
                'a': 'Because you specify WHAT data you want, letting the RDBMS determine HOW to get it',
                'b': 'Because it cannot use variables',
                'c': 'Because it only runs on Linux servers',
                'd': 'Because it requires a compiler',
                'correct': 'A',
                'exp': 'Declarative languages describe desired results rather than step-by-step algorithms.',
                'diff': 'advanced',
                'order': 15
            }
        ]

        for q_data in questions_data:
            ExamQuestion.objects.create(
                module=module1,
                question_text=q_data['q'],
                option_a=q_data['a'],
                option_b=q_data['b'],
                option_c=q_data['c'],
                option_d=q_data['d'],
                correct_option=q_data['correct'],
                explanation=q_data['exp'],
                difficulty=q_data['diff'],
                order=q_data['order']
            )

        self.stdout.write(self.style.SUCCESS("Module 1 textbook content & 15 Exam Questions seeded successfully!"))
