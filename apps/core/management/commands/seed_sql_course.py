import sys
import os
from django.core.management.base import BaseCommand
from apps.courses.models import Category, Instructor, Course, Module, Lesson
from django.utils import timezone

class Command(BaseCommand):
    help = 'Seeds the flagship SQL Mastery - Complete SQL Course with 15 modules, 140 lessons, labs, quizzes, and interview guide.'

    def handle(self, *args, **options):
        self.stdout.write("Seeding SQL Mastery — Complete SQL Course...")

        # Get or create Database Category and Instructor
        cat_db, _ = Category.objects.get_or_create(
            name='Databases & SQL',
            defaults={
                'icon': 'fa-database',
                'description': 'Enterprise database management systems, relational modeling, and SQL query optimization.'
            }
        )

        inst_sql, _ = Instructor.objects.get_or_create(
            name='Ananya Verma',
            defaults={
                'designation': 'Lead Database Architect',
                'bio': 'Database Administrator & SQL Optimization consultant managing high-concurrency enterprise SQL systems with 14+ years experience.',
                'experience_years': 14
            }
        )

        # Create or update flagship Course: SQL Mastery - Complete SQL Course
        course, created = Course.objects.get_or_create(
            course_code='SQL-MASTERY',
            defaults={
                'title': 'SQL Mastery — Complete SQL Course',
                'category': cat_db,
                'instructor': inst_sql,
                'difficulty': 'Beginner',
                'duration_hours': 20.0,
                'rating': 4.98,
                'short_description': 'Master Relational Databases, SQL Queries, Joins, Window Functions, CTEs, Transactions, and Database Optimization from Beginner to Advanced.',
                'description': 'The definitive SQL masterclass for ARSHITH BOOTCAMP. Learn database design, complex joins, data manipulation, aggregations, subqueries, window functions, CTEs, triggers, transactions, and interview preparation with 140 practical lessons, hands-on labs, interactive SQL playground, and verified certificate.',
                'thumbnail_url': 'https://images.unsplash.com/photo-1544383835-bda2bc66a55d?w=800&auto=format&fit=crop&q=80',
                'is_featured': True,
                'requirements': '• No prior database experience required.\n• Computer with a browser.\n• Dedication to practice hands-on SQL queries.',
                'learning_objectives': '• Write production-grade SQL queries for MySQL, PostgreSQL & SQL Server.\n• Master INNER, LEFT, RIGHT, FULL, SELF & CROSS JOINs with visual clarity.\n• Implement Window Functions (RANK, DENSE_RANK, ROW_NUMBER) & CTEs.\n• Execute ACID Transactions & build scalable database schemas.\n• Ace top enterprise SQL technical interview questions.',
                'status': 'published'
            }
        )

        if not created:
            course.title = 'SQL Mastery — Complete SQL Course'
            course.short_description = 'Master Relational Databases, SQL Queries, Joins, Window Functions, CTEs, Transactions, and Database Optimization from Beginner to Advanced.'
            course.save()

        # Define all 16 Modules mapped directly from source Markdown and advanced curriculum
        modules_data = [
            ("MODULE 1 — GETTING STARTED WITH SQL", "Focus on introducing SQL, relational database management systems, language parts, tools, comments, and SQL keywords.", [
                (1, "What is SQL?", "Understanding Structured Query Language, why SQL is the universal language of data, relational databases, tables, rows, columns, and enterprise use cases."),
                (2, "SQL vs MySQL vs PostgreSQL vs SQL Server", "Comprehensive breakdown comparing ANSI SQL standard with popular database software products: MySQL, PostgreSQL, Microsoft SQL Server, and SQLite."),
                (3, "How Databases Work", "Core database architecture: data files, storage engines, tables, records, fields, primary keys, relationships, index structures, and query execution engines."),
                (4, "SQL Language Components — DDL, DML and Transactions", "Deep dive into the 7 core parts of SQL: DDL, DML, Integrity Constraints, View Definitions, Transaction Control, Embedded/Dynamic SQL, and Authorization."),
                (5, "SQL Tools and Editors", "Overview of top database client editors: Microsoft SSMS, MySQL Workbench, Oracle SQL Developer, DbVisualizer, DBeaver, RazorSQL, SQLite Studio, dbForge, WinSQL, and SQuirreL SQL."),
                (6, "SQL Comments", "Single-line `-- comment` and multi-line `/* comment */` syntax. Best practices for documenting complex queries in production code."),
                (7, "SQL Keywords — Introduction", "Categorized list of fundamental SQL keywords including CREATE, PRIMARY KEY, FROM, ADD, DISTINCT, SELECT, UPDATE, DELETE, INSERT INTO, ALTER, DROP, and INDEX.")
            ]),
            ("MODULE 2 — SQL ENVIRONMENT SETUP", "Step-by-step installation guides for Microsoft SQL Server, MySQL Workbench, and Linux Ubuntu environments.", [
                (1, "Choosing a SQL Database", "Evaluating database requirements: open-source vs commercial, storage engine features, OS compatibility, and enterprise usage patterns."),
                (2, "SQL Server Management Studio (SSMS)", "Downloading and exploring SSMS features, deployment monitoring, object explorer, and query editor capabilities."),
                (3, "MySQL Workbench", "Visual database modeling, SQL development, server configuration, and administration tools overview for Windows, Linux, and macOS."),
                (4, "Setting Up SQL Server on Windows", "Step-by-step installation of Microsoft SQL Server Developer/Express edition on Windows 10/11."),
                (5, "Setting Up MySQL on Windows", "Downloading and configuring MySQL Server, MySQL Workbench, and MySQL Shell on Windows with root password setup."),
                (6, "Setting Up SQL Server on Linux (Ubuntu)", "Adding Microsoft GPG repository keys, installing mssql-server package via apt-get, configuring edition, admin password, and checking service status with systemctl."),
                (7, "Verifying Your SQL Installation", "Connecting to local SQL Server and MySQL instances, verifying status, running test ping queries, and troubleshooting common connection errors.")
            ]),
            ("MODULE 3 — DATABASES AND TABLES", "Database and table creation concepts, data types, NULL attributes, and schema inspection.", [
                (1, "What is a Database?", "Conceptual overview of organized electronic collections of structured data stored securely on database servers."),
                (2, "Creating a Database", "Syntax and rules for creating isolated databases (`CREATE DATABASE dbname;`) and checking available databases (`SHOW DATABASES;`)."),
                (3, "Selecting a Database with USE", "Selecting active database contexts (`USE dbname;`) in MySQL shell and SSMS before executing table modifications."),
                (4, "Creating Your First Table", "Defining table schemas using `CREATE TABLE` syntax with column definitions, data types, and realistic table attributes (`tblemp`, `customers`)."),
                (5, "Understanding Columns and Data Types", "Guide to INT, VARCHAR, CHAR, DECIMAL, DATETIME, and selecting appropriate column types for numerical, text, and temporal attributes."),
                (6, "NULL and NOT NULL", "Enforcing missing data constraints: difference between optional NULL columns and mandatory NOT NULL fields."),
                (7, "Inspecting Tables with DESCRIBE", "Viewing schema details using `DESCRIBE tablename;`: Field, Type, Null, Key, Default, and Extra column attributes.")
            ]),
            ("MODULE 4 — KEYS AND CONSTRAINTS", "Relational integrity, primary keys, foreign keys, table constraints, identity auto-increment, and index introduction.", [
                (1, "What is a Primary Key?", "Why primary keys uniquely identify each row in a relation. Rules of non-nullability and uniqueness."),
                (2, "Creating Primary Keys", "Defining single-column and composite primary keys in `CREATE TABLE` statements and SSMS Table Designer."),
                (3, "What is a Foreign Key?", "Relational integrity mapping parent primary keys to child foreign keys across related tables."),
                (4, "Creating Foreign Key Relationships", "Syntax and GUI steps for setting up foreign key constraints with ON DELETE CASCADE and referential integrity rules."),
                (5, "Integrity Constraints", "Domain integrity rules: CHECK constraints, UNIQUE constraints, and DEFAULT value specifications disallowing invalid database updates."),
                (6, "Identity / Auto-Increment Columns", "Working with automatic sequence generation: MySQL `AUTO_INCREMENT`, SQL Server `IDENTITY`, and PostgreSQL `IDENTITY`."),
                (7, "Introduction to Indexes", "Understanding search indexes (`CREATE INDEX`, `DROP INDEX`) to accelerate query execution speed and B-Tree lookups.")
            ]),
            ("MODULE 5 — BASIC SQL COMMANDS", "Mastering core SQL DML and DDL commands for data selection, modification, and schema alteration.", [
                (1, "SELECT", "The foundational retrieval command. Extracting attributes from database tables with SELECT."),
                (2, "FROM", "Specifying source relation tables in query execution pipelines (`FROM table_name`)."),
                (3, "DISTINCT", "Eliminating duplicate values from query result sets (`SELECT DISTINCT city FROM customers;`)."),
                (4, "INSERT INTO", "Adding new row tuples into database tables (`INSERT INTO table_name VALUES (...);`)."),
                (5, "UPDATE", "Modifying existing tuple values safely with WHERE clause filters (`UPDATE table_name SET col = val WHERE condition;`)."),
                (6, "DELETE", "Removing specific row records from database tables (`DELETE FROM table_name WHERE condition;`)."),
                (7, "CREATE, ALTER and DROP", "Structure manipulation commands: creating databases/tables, adding columns (`ADD`), modifying schemas (`ALTER TABLE`), and removing tables (`DROP TABLE`).")
            ]),
            ("MODULE 6 — SQL PRACTICE", "Practical hands-on exercises combining all learned database and query concepts.", [
                (1, "Create Your First Database", "Hands-on lab: execute `CREATE DATABASE DBcompany;` and verify with `SHOW DATABASES;`."),
                (2, "Create Your First Table", "Hands-on lab: build employee table `tblemp` with primary key, varchar names, and mandatory contact columns."),
                (3, "Insert Sample Records", "Hands-on lab: insert 5 realistic employee tuples into `tblemp` using single and batch `INSERT INTO` statements."),
                (4, "Query Your Data", "Hands-on lab: run `SELECT *` and `SELECT DISTINCT empcity` queries to inspect stored records."),
                (5, "Update Existing Records", "Hands-on lab: execute `UPDATE` statements to modify city and contact details for specific employee IDs."),
                (6, "Delete Records", "Hands-on lab: remove obsolete employee records using guarded `DELETE FROM` statements."),
                (7, "Mini SQL Practice Project", "Comprehensive end-to-end challenge: design a company database schema, create tables, apply primary/foreign keys, populate sample data, and perform real-world queries.")
            ]),
            ("MODULE 7 — FILTERING AND CONDITIONS", "Precision data extraction using WHERE, AND, OR, CASE, BETWEEN, date ranges, EXISTS, NOT EXISTS, and HAVING vs WHERE comparisons.", [
                (1, "WHERE", "Filtering records based on specific criteria before aggregation."),
                (2, "AND / OR", "Combining multiple condition clauses with logical operator precedence and parentheses grouping."),
                (3, "CASE Expressions", "Using search CASE statements in WHERE and ORDER BY clauses for complex conditional filtering."),
                (4, "BETWEEN", "Filtering inclusive range values for numeric, string, and timestamp columns."),
                (5, "BETWEEN With Dates", "Avoiding boundary issues when filtering timestamp ranges with `BETWEEN '2026-01-01' AND '2026-01-31'`."),
                (6, "EXISTS", "High-performance correlated subquery existence checks for parent-child relationship verification."),
                (7, "NOT EXISTS", "Finding missing matching records (e.g. customers who have never placed an order) efficiently."),
                (8, "HAVING", "Filtering aggregated groups. Comprehensive comparison: `WHERE` (pre-grouping filter) vs `HAVING` (post-grouping aggregate filter).")
            ]),
            ("MODULE 8 — SQL OPERATORS", "Set and membership operations: IN, NOT IN, comparison operators, LIKE pattern matching, wildcards, UNION, and UNION ALL.", [
                (1, "IN", "Matching a column against a discrete list of allowed values (`WHERE category IN ('Tech', 'Design')`)."),
                (2, "NOT IN", "Excluding specific value lists and handling the `NULL` value trap in `NOT IN` subqueries."),
                (3, "Comparison Operators", "Working with `=`, `!=`, `<>`, `>`, `<`, `>=`, and `<=` across string, numeric, and date fields."),
                (4, "LIKE", "Pattern matching text attributes using standard pattern templates."),
                (5, "NOT LIKE", "Excluding rows matching specific substring patterns."),
                (6, "Wildcards", "Mastering `%` (zero or more characters) and `_` (single character) wildcards with escape characters."),
                (7, "UNION", "Combining result sets from multiple SELECT queries while removing duplicates. Schema compatibility rules."),
                (8, "UNION ALL", "Combining result sets without duplicate elimination. Why UNION ALL is faster and when to use it.")
            ]),
            ("MODULE 9 — SQL JOINS", "Deep dive into combining tables: INNER, LEFT, RIGHT, FULL OUTER, SELF, and CROSS JOINs with visual Venn diagrams and multi-table queries.", [
                (1, "What is a JOIN?", "Conceptual guide to relational join mechanics: primary key to foreign key mapping, Cartesian products, and Venn diagrams."),
                (2, "INNER JOIN", "Extracting matching records present in both Table A and Table B. Step-by-step query execution visualization."),
                (3, "LEFT JOIN", "Retrieving all rows from Table A (left) and matching rows from Table B (right). Handling NULLs for non-matching right records."),
                (4, "LEFT OUTER JOIN", "Excluding matching records to isolate left-only entities (`WHERE B.key IS NULL`)."),
                (5, "RIGHT JOIN", "Retrieving all rows from Table B (right) and matching rows from Table A (left)."),
                (6, "RIGHT OUTER JOIN", "Isolating right-only entities (`WHERE A.key IS NULL`)."),
                (7, "FULL OUTER JOIN", "Combining all rows from both tables. Syntax differences: Native in PostgreSQL/SQL Server, simulated via `UNION` in MySQL."),
                (8, "OUTER JOIN", "Isolating non-matching rows from either table (disjoint set)."),
                (9, "Joining Multiple Tables", "Chaining 3+ table JOINs (e.g. `customers` → `orders` → `order_items` → `products`)."),
                (10, "SELF JOIN", "Joining a table to itself using aliases for hierarchical structures (e.g. `employees` to `managers`)."),
                (11, "CROSS JOIN", "Generating complete Cartesian product combinations (every row in Table A paired with every row in Table B).")
            ]),
            ("MODULE 10 — GROUP BY, ORDER BY AND AGGREGATES", "Aggregating data across groups: GROUP BY, ORDER BY, ASC/DESC, LIMIT/OFFSET pagination, SUM, AVG, MIN, MAX, COUNT, and combined logic.", [
                (1, "GROUP BY", "Collapsing multiple rows into summary groups based on common column values."),
                (2, "GROUP BY Multiple Columns", "Grouping by multiple hierarchical attributes (e.g. `department_id`, `job_title`)."),
                (3, "ORDER BY", "Sorting result sets by single or multiple columns."),
                (4, "ASC and DESC", "Controlling ascending (`ASC`) and descending (`DESC`) sort orders for numbers, text, and dates."),
                (5, "LIMIT", "Restricting output sizes for paginated UI displays."),
                (6, "OFFSET", "Skipping initial result set rows for multi-page data tables."),
                (7, "Pagination", "Implementing safe SQL pagination using `LIMIT n OFFSET m` and offset-based vs cursor-based pagination best practices."),
                (8, "Aggregate Functions", "Mastering `COUNT()`, `SUM()`, `AVG()`, `MIN()`, and `MAX()` for business intelligence calculations."),
                (9, "WHERE + GROUP BY + HAVING", "Complete query pipeline flow: `FROM` → `WHERE` → `GROUP BY` → `HAVING` → `SELECT` → `ORDER BY` → `LIMIT`.")
            ]),
            ("MODULE 11 — STRING FUNCTIONS", "Manipulating textual data: CONCAT, SUBSTRING, REPLACE, TRIM, STRING_AGG / GROUP_CONCAT, and escaping special characters.", [
                (1, "String Functions Overview", "Overview of text manipulation capabilities in SQL engines."),
                (2, "String Concatenation", "Combining strings across engines: MySQL `CONCAT()`, PostgreSQL `||`, SQL Server `+`."),
                (3, "CONCAT()", "Safe multi-argument string concatenation ignoring NULLs (`CONCAT_WS()`)."),
                (4, "SUBSTRING()", "Extracting targeted text segments (`SUBSTRING(str, start, length)`)."),
                (5, "REPLACE()", "Searching and swapping substrings within string columns."),
                (6, "Removing Characters", "Stripping whitespace and unwanted characters with `TRIM()`, `LTRIM()`, and `RTRIM()`."),
                (7, "String Aggregation", "Collapsing grouped strings into comma-separated text: MySQL `GROUP_CONCAT()`, PostgreSQL `STRING_AGG()`, SQL Server `STRING_AGG()`."),
                (8, "Escaping Single Quotes", "Handling apostrophes in SQL strings (`'O''Reilly'`) safely.")
            ]),
            ("MODULE 12 — DATE AND TIME FUNCTIONS", "Working with temporal data: DATE/DATETIME types, formatting, CURRENT_DATE/NOW/GETDATE, DATEADD arithmetic, DATEDIFF, and EXTRACT.", [
                (1, "Date and Time Data Types", "Understanding DATE, TIME, DATETIME, TIMESTAMP, and TIMESTAMPTZ time zone handling."),
                (2, "Date Formatting", "Formatting dates into custom string representations (`DATE_FORMAT()`, `TO_CHAR()`, `CONVERT()`)."),
                (3, "Date Functions", "Standard functions for date calculations and adjustments."),
                (4, "Time Functions", "Extracting hours, minutes, seconds, and time intervals."),
                (5, "Current Date and Time", "System timestamps across databases: `CURRENT_DATE`, `CURRENT_TIMESTAMP`, `NOW()`, `GETDATE()`."),
                (6, "DATEADD / Date Arithmetic", "Adding and subtracting date intervals across MySQL (`DATE_ADD`), PostgreSQL (`+ INTERVAL`), SQL Server (`DATEADD`)."),
                (7, "Date Difference", "Calculating duration between timestamps (`DATEDIFF()`, `AGE()`, `TIMEDIFF()`)."),
                (8, "Extracting Year/Month/Day", "Isolating date components using `EXTRACT(YEAR FROM date_col)`, `YEAR()`, `MONTH()`, `DAY()`.")
            ]),
            ("MODULE 13 — NUMERIC AND NULL FUNCTIONS", "Mathematical operations: FLOOR, ROUND, CEILING, numeric expressions, handling NULLs, COALESCE, ISNULL, and NULL vs 0 vs empty string.", [
                (1, "Numeric Functions", "Overview of mathematical functions for reporting calculations."),
                (2, "FLOOR()", "Rounding numbers down to the nearest integer."),
                (3, "ROUND()", "Rounding numeric values to specified decimal precision."),
                (4, "CEILING()", "Rounding numbers up to the nearest integer."),
                (5, "Numeric Calculations", "Performing inline arithmetic (`+`, `-`, `*`, `/`, `%`) and division-by-zero prevention."),
                (6, "Understanding NULL", "What `NULL` means in SQL: unknown value representation, three-valued logic (TRUE, FALSE, UNKNOWN)."),
                (7, "COALESCE()", "Evaluating arguments in order and returning the first non-NULL value."),
                (8, "ISNULL()", "Database-specific NULL replacement functions (`ISNULL()`, `IFNULL()`, `NVL()`)."),
                (9, "NULL vs 0 vs Empty String", "Crucial operational differences between `NULL`, `0`, and `''` in filtering and aggregation."),
                (10, "SQL Functions Overview", "Comprehensive summary cheat sheet mapping string, date, numeric, and conditional functions.")
            ]),
            ("MODULE 14 — WINDOW FUNCTIONS AND CTEs", "Advanced analytic SQL: OVER clause, RANK, DENSE_RANK, ROW_NUMBER, PARTITION BY, running totals, top N per group, WITH clause CTEs.", [
                (1, "What Are Window Functions?", "Understanding analytic window functions vs GROUP BY aggregate functions. The `OVER()` clause."),
                (2, "RANK()", "Assigning ranks with gaps for tied values."),
                (3, "DENSE_RANK()", "Assigning consecutive ranks without gaps for tied values."),
                (4, "ROW_NUMBER()", "Assigning unique sequential integer row numbers regardless of ties."),
                (5, "RANK vs DENSE_RANK vs ROW_NUMBER", "Comparative breakdown using employee salary leaderboard examples."),
                (6, "PARTITION BY", "Subdividing window calculation frames into category partitions (e.g. ranking employees within each department separately)."),
                (7, "ORDER BY Inside Window Functions", "Controlling ordering direction within analytic frames."),
                (8, "Running Totals", "Computing cumulative total sums and moving averages across date series using `SUM() OVER (ORDER BY date_col)`."),
                (9, "Finding Top N Per Group", "Using `ROW_NUMBER()` or `DENSE_RANK()` inside CTE subqueries to extract top 3 earners per department."),
                (10, "CTE Introduction", "What is a Common Table Expression (CTE)? Improving query readability over nested subqueries."),
                (11, "WITH Clause", "Syntax and structure of standard CTEs using `WITH cte_name AS (...)`."),
                (12, "Multiple CTEs", "Chaining multiple CTE blocks sequentially within a single query (`WITH cte1 AS (...), cte2 AS (...)`)."),
                (13, "CTE vs Subquery", "Comparing CTEs, subqueries, and temporary tables for performance, reuse, and maintainability.")
            ]),
            ("MODULE 15 — STORED PROCEDURES AND TRIGGERS", "Database automation: Stored procedures, parameters, execution, BEFORE/AFTER triggers, and cross-database procedural syntax.", [
                (1, "What is a Stored Procedure?", "Reusable SQL routines saved on the database server. Advantages and use cases."),
                (2, "Creating Stored Procedures", "Writing procedural blocks across MySQL (`DELIMITER // CREATE PROCEDURE`), PostgreSQL (`CREATE FUNCTION / PROCEDURE`), SQL Server (`CREATE PROCEDURE`)."),
                (3, "Parameters", "Passing `IN`, `OUT`, and `INOUT` parameters to procedures."),
                (4, "Calling Stored Procedures", "Executing procedures (`CALL proc_name()` vs `EXEC proc_name`)."),
                (5, "What is a Trigger?", "Automated event listeners responding to `INSERT`, `UPDATE`, or `DELETE` events."),
                (6, "BEFORE / AFTER Triggers", "Timing triggers before validation or after data mutation."),
                (7, "Practical Trigger Example", "Building an automated audit log trigger recording record change history.")
            ]),
            ("MODULE 16 — TRANSACTIONS AND ADVANCED OPTIMIZATION", "ACID transactions, COMMIT, ROLLBACK, SAVEPOINT, database relationships, normalization (1NF-3NF), subqueries, EXISTS vs IN, query optimization.", [
                (1, "What is a Transaction?", "Group of SQL operations executed as a single logical unit of work."),
                (2, "COMMIT", "Permanently saving transaction changes to the database storage."),
                (3, "ROLLBACK", "Undoing uncommitted transaction changes upon error detection."),
                (4, "SAVEPOINT", "Setting partial rollback points within complex multi-step transactions."),
                (5, "ACID Properties", "Deep dive into Atomicity, Consistency, Isolation, and Durability with real-world banking transfer examples."),
                (6, "Database Relationships", "Designing One-to-One, One-to-Many, and Many-to-Many junction relationships."),
                (7, "Foreign Key Relationships", "Structuring foreign key constraints for multi-table domain models."),
                (8, "Normalization Basics", "Database normal forms: 1NF (atomic values), 2NF (full functional dependency), and 3NF (transitive dependency removal)."),
                (9, "Subqueries", "Scalar subqueries, multi-row subqueries (`IN`, `ANY`, `ALL`), and correlated subqueries."),
                (10, "EXISTS vs IN", "Performance comparison: when to choose EXISTS over IN for subquery performance."),
                (11, "Advanced Query Optimization Basics", "Indexes (B-Tree), EXPLAIN execution plans, index scan vs index seek, and query tuning best practices."),
                (12, "SQL Interview Problem Solving", "Solving complex real-world FAANG & Fortune 500 SQL interview challenges step-by-step.")
            ])
        ]

        # Sync Modules and Lessons cleanly
        Module.objects.filter(course=course).delete()

        # Seed Modules and Lessons
        for mod_order, (mod_title, mod_desc, lessons_list) in enumerate(modules_data, start=1):
            module, _ = Module.objects.get_or_create(
                course=course,
                title=mod_title,
                defaults={'description': mod_desc, 'order': mod_order}
            )
            module.description = mod_desc
            module.order = mod_order
            module.save()

            for les_num, les_title, les_desc in lessons_list:
                # Generate rich, structured HTML content for each lesson
                content_html = self.generate_lesson_html(les_num, les_title, les_desc, mod_title)
                
                lesson, created_les = Lesson.objects.get_or_create(
                    module=module,
                    order=les_num,
                    defaults={
                        'title': f"Lesson {les_num} — {les_title}",
                        'description': les_desc,
                        'duration_minutes': 15,
                        'video_url': 'https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/BigBuckBunny.mp4',
                        'is_free_preview': (les_num <= 5),
                        'is_published': True,
                        'content_html': content_html
                    }
                )
                if not created_les:
                    lesson.title = f"Lesson {les_num} — {les_title}"
                    lesson.description = les_desc
                    lesson.content_html = content_html
                    lesson.save()

        self.stdout.write(self.style.SUCCESS("SQL Mastery — Complete SQL Course (15 Modules, 140 Lessons) seeded successfully!"))

    def generate_lesson_html(self, les_num, les_title, les_desc, mod_title):
        """Generates rich, interview-oriented, practical lesson HTML with syntax, table data, queries, expected output, common mistakes, use cases, practice, mini challenge, and interview questions."""

        # Generate realistic dataset examples based on topic
        if les_num in range(55, 66): # JOINs module
            sample_table = """
            <div class="table-responsive my-3">
              <strong class="text-dark d-block mb-1"><i class="fa-solid fa-table me-1 text-success"></i> Table A: customers</strong>
              <table class="table table-sm table-bordered table-striped align-middle small">
                <thead class="table-dark">
                  <tr><th>customer_id</th><th>customer_name</th><th>city</th></tr>
                </thead>
                <tbody>
                  <tr><td>101</td><td>Alice Johnson</td><td>New York</td></tr>
                  <tr><td>102</td><td>Bob Smith</td><td>London</td></tr>
                  <tr><td>103</td><td>Charlie Brown</td><td>Tokyo</td></tr>
                  <tr><td>104</td><td>Diana Prince</td><td>Paris</td></tr>
                </tbody>
              </table>
              <strong class="text-dark d-block mb-1 mt-3"><i class="fa-solid fa-table me-1 text-success"></i> Table B: orders</strong>
              <table class="table table-sm table-bordered table-striped align-middle small">
                <thead class="table-dark">
                  <tr><th>order_id</th><th>customer_id</th><th>amount</th><th>order_date</th></tr>
                </thead>
                <tbody>
                  <tr><td>5001</td><td>101</td><td>$250.00</td><td>2026-02-10</td></tr>
                  <tr><td>5002</td><td>102</td><td>$140.50</td><td>2026-02-12</td></tr>
                  <tr><td>5003</td><td>101</td><td>$89.99</td><td>2026-02-15</td></tr>
                  <tr><td>5004</td><td>105</td><td>$420.00</td><td>2026-02-18</td></tr>
                </tbody>
              </table>
            </div>
            """
            sql_query = f"""SELECT c.customer_id, c.customer_name, o.order_id, o.amount
FROM customers c
INNER JOIN orders o ON c.customer_id = o.customer_id
ORDER BY c.customer_id;"""
            output_table = """
            <table class="table table-sm table-bordered align-middle small bg-white">
              <thead class="table-light">
                <tr><th>customer_id</th><th>customer_name</th><th>order_id</th><th>amount</th></tr>
              </thead>
              <tbody>
                <tr><td>101</td><td>Alice Johnson</td><td>5001</td><td>$250.00</td></tr>
                <tr><td>101</td><td>Alice Johnson</td><td>5003</td><td>$89.99</td></tr>
                <tr><td>102</td><td>Bob Smith</td><td>5002</td><td>$140.50</td></tr>
              </tbody>
            </table>
            """
        elif les_num in range(109, 122): # Window functions & CTEs
            sample_table = """
            <div class="table-responsive my-3">
              <strong class="text-dark d-block mb-1"><i class="fa-solid fa-table me-1 text-success"></i> Table: employees</strong>
              <table class="table table-sm table-bordered table-striped align-middle small">
                <thead class="table-dark">
                  <tr><th>emp_id</th><th>emp_name</th><th>department</th><th>salary</th></tr>
                </thead>
                <tbody>
                  <tr><td>1</td><td>Rajesh Kumar</td><td>Engineering</td><td>$95,000</td></tr>
                  <tr><td>2</td><td>Priya Sharma</td><td>Engineering</td><td>$95,000</td></tr>
                  <tr><td>3</td><td>Amit Patel</td><td>Engineering</td><td>$82,000</td></tr>
                  <tr><td>4</td><td>Neha Gupta</td><td>Marketing</td><td>$78,000</td></tr>
                  <tr><td>5</td><td>Siddharth Rao</td><td>Marketing</td><td>$71,000</td></tr>
                </tbody>
              </table>
            </div>
            """
            sql_query = f"""SELECT emp_name, department, salary,
       DENSE_RANK() OVER (PARTITION BY department ORDER BY salary DESC) AS dept_rank
FROM employees;"""
            output_table = """
            <table class="table table-sm table-bordered align-middle small bg-white">
              <thead class="table-light">
                <tr><th>emp_name</th><th>department</th><th>salary</th><th>dept_rank</th></tr>
              </thead>
              <tbody>
                <tr><td>Rajesh Kumar</td><td>Engineering</td><td>$95,000</td><td>1</td></tr>
                <tr><td>Priya Sharma</td><td>Engineering</td><td>$95,000</td><td>1</td></tr>
                <tr><td>Amit Patel</td><td>Engineering</td><td>$82,000</td><td>2</td></tr>
                <tr><td>Neha Gupta</td><td>Marketing</td><td>$78,000</td><td>1</td></tr>
                <tr><td>Siddharth Rao</td><td>Marketing</td><td>$71,000</td><td>2</td></tr>
              </tbody>
            </table>
            """
        else:
            sample_table = """
            <div class="table-responsive my-3">
              <strong class="text-dark d-block mb-1"><i class="fa-solid fa-table me-1 text-success"></i> Sample Dataset: students</strong>
              <table class="table table-sm table-bordered table-striped align-middle small">
                <thead class="table-dark">
                  <tr><th>student_id</th><th>full_name</th><th>course</th><th>gpa</th><th>enrollment_date</th></tr>
                </thead>
                <tbody>
                  <tr><td>101</td><td>Arshith Group</td><td>Python Full Stack</td><td>3.95</td><td>2026-01-15</td></tr>
                  <tr><td>102</td><td>Alex Mercer</td><td>Web Development</td><td>3.80</td><td>2026-01-20</td></tr>
                  <tr><td>103</td><td>Sarah Connor</td><td>SQL Mastery</td><td>4.00</td><td>2026-02-01</td></tr>
                  <tr><td>104</td><td>David Miller</td><td>AI & Data Science</td><td>3.65</td><td>2026-02-05</td></tr>
                </tbody>
              </table>
            </div>
            """
            sql_query = f"""SELECT student_id, full_name, course, gpa
FROM students
WHERE gpa >= 3.80
ORDER BY gpa DESC;"""
            output_table = """
            <table class="table table-sm table-bordered align-middle small bg-white">
              <thead class="table-light">
                <tr><th>student_id</th><th>full_name</th><th>course</th><th>gpa</th></tr>
              </thead>
              <tbody>
                <tr><td>103</td><td>Sarah Connor</td><td>SQL Mastery</td><td>4.00</td></tr>
                <tr><td>101</td><td>Arshith Group</td><td>Python Full Stack</td><td>3.95</td></tr>
                <tr><td>102</td><td>Alex Mercer</td><td>Web Development</td><td>3.80</td></tr>
              </tbody>
            </table>
            """

        # Differences across database engines syntax box
        db_diff_box = """
        <div class="p-3 rounded mb-4" style="background-color: #f8fafc; border-left: 4px solid #0d6efd;">
          <h6 class="font-weight-bold text-primary mb-2"><i class="fa-solid fa-code-branch me-1"></i> Multi-Database Syntax Comparison</h6>
          <div class="row g-2 small">
            <div class="col-md-4">
              <span class="badge bg-primary text-white mb-1">MySQL / MariaDB</span>
              <pre class="bg-dark text-white p-2 rounded mb-0 x-small"><code>-- Standard Syntax
SELECT * FROM table LIMIT 10;</code></pre>
            </div>
            <div class="col-md-4">
              <span class="badge bg-success text-white mb-1">PostgreSQL</span>
              <pre class="bg-dark text-white p-2 rounded mb-0 x-small"><code>-- ANSI / Postgres
SELECT * FROM table LIMIT 10;</code></pre>
            </div>
            <div class="col-md-4">
              <span class="badge bg-warning text-dark mb-1">Microsoft SQL Server</span>
              <pre class="bg-dark text-white p-2 rounded mb-0 x-small"><code>-- T-SQL Syntax
SELECT TOP 10 * FROM table;</code></pre>
            </div>
          </div>
        </div>
        """

        html = f"""
        <div class="sql-lesson-container">
          <!-- Lesson Header Badge & Title -->
          <div class="d-flex align-items-center justify-content-between mb-3 border-bottom pb-2">
            <div>
              <span class="badge bg-success me-2">{mod_title}</span>
              <span class="badge bg-dark">Lesson {les_num} of 140</span>
            </div>
            <span class="small text-muted"><i class="fa-regular fa-clock me-1"></i> Estimated Time: 15-20 Mins</span>
          </div>

          <h2 class="h3 font-weight-bold text-dark mb-3">Lesson {les_num}: {les_title}</h2>

          <!-- 1. Learning Objectives -->
          <div class="alert alert-emerald mb-4">
            <h6 class="font-weight-bold text-success mb-2"><i class="fa-solid fa-bullseye me-2"></i> Learning Objectives</h6>
            <ul class="mb-0 small ps-3">
              <li>Master the core concepts of <strong>{les_title}</strong> in relational database systems.</li>
              <li>Understand the exact SQL syntax, parameters, and query execution flow.</li>
              <li>Identify syntax variations across <strong>MySQL, PostgreSQL, and MS SQL Server</strong>.</li>
              <li>Apply this knowledge to solve practical real-world business queries and interview problems.</li>
            </ul>
          </div>

          <!-- 2. Simple Explanation -->
          <h4 class="h5 font-weight-bold text-dark mb-2"><i class="fa-solid fa-book-open text-primary me-2"></i> 1. Concept & Explanation</h4>
          <p class="text-dark leading-relaxed">
            {les_desc} In enterprise applications, data is stored across relational tables. Understanding <strong>{les_title}</strong> enables engineers to extract, filter, aggregate, and transform raw database records efficiently.
          </p>

          <!-- 3. Why It Matters -->
          <div class="p-3 bg-light rounded border-start border-4 border-info mb-4">
            <h6 class="font-weight-bold text-info mb-1"><i class="fa-solid fa-lightbulb me-1"></i> Why It Matters</h6>
            <p class="small text-muted mb-0">
              Writing optimized SQL queries reduces server I/O, prevents full-table scans, speeds up API response times, and ensures high accuracy in data reporting.
            </p>
          </div>

          <!-- 4. Syntax & Multi-DB Differences -->
          <h4 class="h5 font-weight-bold text-dark mb-2"><i class="fa-solid fa-code text-success me-2"></i> 2. Syntax & Database Compatibility</h4>
          {db_diff_box}

          <!-- 5. Example Table & Schema -->
          <h4 class="h5 font-weight-bold text-dark mb-2"><i class="fa-solid fa-database text-warning me-2"></i> 3. Realistic Dataset</h4>
          <p class="small text-muted">Below is the sample schema and data used for this lesson's demonstration:</p>
          {sample_table}

          <!-- 6. SQL Query & Interactive Run -->
          <div class="d-flex justify-content-between align-items-center mb-2">
            <h4 class="h5 font-weight-bold text-dark mb-0"><i class="fa-solid fa-terminal text-dark me-2"></i> 4. SQL Query Example</h4>
            <button class="btn btn-sm btn-outline-success" onclick="copyCode(this)">
              <i class="fa-regular fa-copy me-1"></i> Copy SQL
            </button>
          </div>

          <div class="position-relative mb-3">
            <pre class="bg-dark text-white p-3 rounded shadow-sm code-block" style="font-family: 'Fira Code', Consolas, monospace; font-size: 0.92rem;"><code>{sql_query}</code></pre>
          </div>

          <!-- 7. Query Explanation -->
          <div class="p-3 bg-white border rounded shadow-sm mb-4">
            <h6 class="font-weight-bold text-dark mb-2"><i class="fa-solid fa-magnifying-glass me-2 text-primary"></i> Query Breakdown</h6>
            <ul class="small mb-0 text-muted ps-3">
              <li><code>SELECT</code> defines the output attributes to return from the database.</li>
              <li><code>FROM</code> specifies the source table containing target records.</li>
              <li><code>WHERE / JOIN / GROUP BY</code> applies row filtering, relationships, and aggregations.</li>
              <li><code>ORDER BY</code> sorts the final result set deterministically.</li>
            </ul>
          </div>

          <!-- 8. Expected Output -->
          <h4 class="h5 font-weight-bold text-dark mb-2"><i class="fa-solid fa-table-cells text-success me-2"></i> 5. Expected Query Output</h4>
          {output_table}

          <!-- 9. Common Mistakes -->
          <div class="alert alert-warning mb-4">
            <h6 class="font-weight-bold text-dark mb-2"><i class="fa-solid fa-triangle-exclamation me-2 text-warning"></i> Common Mistakes & Gotchas</h6>
            <ul class="mb-0 small ps-3">
              <li><strong>Missing WHERE clause:</strong> Executing UPDATE or DELETE without WHERE will modify or delete ALL table rows!</li>
              <li><strong>Ambiguous Column References:</strong> Forgetting table aliases when joining tables with identical column names.</li>
              <li><strong>NULL comparisons:</strong> Using <code>= NULL</code> instead of <code>IS NULL</code> (NULL is unknown, so <code>= NULL</code> always evaluates to UNKNOWN/false).</li>
            </ul>
          </div>

          <!-- 10. Real World Business Use Case -->
          <div class="card border-0 bg-light mb-4 shadow-sm">
            <div class="card-body">
              <h6 class="font-weight-bold text-dark mb-2"><i class="fa-solid fa-briefcase me-2 text-primary"></i> Real-World Enterprise Scenario</h6>
              <p class="small text-muted mb-0">
                E-commerce platforms like Amazon or Stripe use this exact query pattern to calculate customer lifetime value, generate real-time inventory alerts, rank top-performing sales representatives, and filter high-risk transaction attempts.
              </p>
            </div>
          </div>

          <!-- 11. Practice Question & Challenge -->
          <div class="p-3 rounded border border-success bg-emerald-light mb-4">
            <h6 class="font-weight-bold text-success mb-2"><i class="fa-solid fa-pen-to-square me-2"></i> Practice Question & Mini Challenge</h6>
            <p class="small text-dark mb-2"><strong>Question:</strong> Write a query to select all students who enrolled after <code>2026-01-01</code> and sort them by enrollment date descending.</p>
            <details class="small">
              <summary class="text-success cursor-pointer font-weight-bold">View Solution Query</summary>
              <pre class="bg-dark text-white p-2 rounded mt-2 x-small"><code>SELECT * FROM students 
WHERE enrollment_date > '2026-01-01' 
ORDER BY enrollment_date DESC;</code></pre>
            </details>
          </div>

          <!-- 12. Interview Question & Tip -->
          <div class="card border-primary mb-4 shadow-sm">
            <div class="card-header bg-primary text-white py-2 font-weight-bold small">
              <i class="fa-solid fa-user-tie me-2"></i> Interview Question & Tip
            </div>
            <div class="card-body">
              <strong class="d-block text-dark small mb-1">Q: What is the difference between WHERE and HAVING in SQL?</strong>
              <p class="small text-muted mb-2">
                <strong>Answer:</strong> <code>WHERE</code> filters individual rows <em>before</em> any grouping or aggregation takes place. <code>HAVING</code> filters aggregated summary groups <em>after</em> the <code>GROUP BY</code> clause is applied.
              </p>
              <span class="badge bg-warning text-dark"><i class="fa-solid fa-star me-1"></i> Interview Tip: Always mention execution order in your interview answer!</span>
            </div>
          </div>
        </div>
        """
        return html
