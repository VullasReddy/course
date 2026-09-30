# ?? Arshith LMS — Learning Management System

A full-featured Learning Management System built with **Django** — featuring PDF-based course modules, protected PDF viewing, certificates, and an admin dashboard.

---

## ?? Setup Instructions (After Cloning)

> ?? **Important:** The database is NOT included in the repo. You must run these steps after cloning to get courses working.

### 1. Clone the Repository

```bash
git clone https://github.com/VullasReddy/course.git
cd course
```

### 2. Create and Activate Virtual Environment

```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Mac/Linux
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Apply Migrations

```bash
python manage.py migrate
```

### 5. Seed the Database (Creates Courses + Users)

```bash
python manage.py seed_data
```

This creates:
- 4 courses: Python Full Stack, Web Development, DBMS with SQL, AI with Data Science
- Demo student account
- Admin account

### 6. Import PDF Modules into Courses

```bash
python manage.py import_modules "Python"
python manage.py import_modules "Web"
```

### 7. Run the Development Server

```bash
python manage.py runserver
```

Visit: http://127.0.0.1:8000

---

## ?? Demo Login Credentials

| Role    | Email               | Password   |
|---------|---------------------|------------|
| Student | student@arshith.com | student123 |
| Admin   | admin@arshith.com   | admin123   |

*(Created by seed_data command)*

---

## ? Why Are Courses Empty After Download?

The db.sqlite3 database is NOT included in the repository (it is in .gitignore).
You MUST run seed_data + import_modules commands (steps 5 and 6 above) to populate the database.
The PDF files in media/courses/ ARE included. The import command links them to the DB.

---

## ??? Tech Stack

- Backend: Django 4.x, Django REST Framework
- Database: SQLite (development)
- Frontend: HTML5, CSS3, JavaScript
- PDF Viewing: Protected PDF module viewer
