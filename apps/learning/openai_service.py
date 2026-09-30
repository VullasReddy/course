import os
import json
import urllib.request
import urllib.error

def generate_lesson_content_openai(course_name, module_name, lesson_title, difficulty="beginner", db_type="PostgreSQL"):
    """
    Secure backend service to generate educational lesson content using OpenAI API.
    If OPENAI_API_KEY is not configured or request fails, returns None so callers fall back seamlessly.
    """
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        return None

    prompt = f"""
    Create a comprehensive, professional, textbook-quality educational lesson for a student on ARSHITH BOOTCAMP.
    Course: {course_name}
    Module: {module_name}
    Lesson Title: {lesson_title}
    Difficulty: {difficulty}
    Primary Database Focus: {db_type}

    Provide output in clean HTML following this exact 12-section layout:
    1. Lesson Header (Title, Estimated time, Difficulty)
    2. Learning Objectives (4 bullet checkmarks)
    3. 1. Introduction (Simple student-friendly explanation)
    4. 2. Detailed Explanation (What is it, why it exists, where used)
    5. 3. Database Explanation & Visual Diagram (ASCII/CSS schema tree)
    6. 4. Real-World Enterprise Example (E-commerce / Banking)
    7. 5. SQL Syntax & Code Example (Syntax highlighted code block with line-by-line breakdown)
    8. 6. Expected Output (HTML table with realistic sample rows)
    9. 7. Why SQL is Important (Industry use cases)
    10. 8. Common Mistakes (Beginner errors vs correct query)
    11. 9. Interview Question (Question, Short Answer, Detailed Answer, Tip)
    12. 10. Practice Questions (3-5 practice questions with expandable solution)
    13. 11. Lesson Summary (5-8 bullet summary)
    """

    try:
        url = "https://api.openai.com/v1/chat/completions"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        }
        data = {
            "model": "gpt-3.5-turbo",
            "messages": [
                {"role": "system", "content": "You are an expert database lead instructor generating original, educational HTML lesson content for students."},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.7,
            "max_tokens": 2500
        }

        req = urllib.request.Request(url, data=json.dumps(data).encode('utf-8'), headers=headers)
        with urllib.request.urlopen(req, timeout=15) as response:
            res_body = json.loads(response.read().decode('utf-8'))
            content = res_body['choices'][0]['message']['content']
            return content
    except Exception as e:
        print(f"OpenAI Generation Fallback triggered: {e}")
        return None
