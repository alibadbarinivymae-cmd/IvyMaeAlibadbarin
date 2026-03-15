import os
from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
# Secret key is required for flashing messages (alerts)
app.secret_key = os.environ.get("SECRET_KEY", "dev_key_123")

# Initial Data
students_db = [
    {"id": 1, "name": "Juan Dela Cruz", "section": "Zechariah", "grade": 85, "letter": "B", "remark": "Passed"}
]

def calculate_grade_details(grade_input):
    """Safely converts input and returns letter and remark."""
    try:
        score = int(grade_input)
    except (ValueError, TypeError):
        return None, None, None
    
    if score >= 90: return score, "A", "Excellent"
    elif score >= 80: return score, "B", "Good"
    elif score >= 75: return score, "C", "Passed"
    else: return score, "F", "Failed"

@app.route('/')
def dashboard():
    total_students = len(students_db)
    
    # Using a more robust calculation method
    if total_students > 0:
        grades = [s['grade'] for s in students_db]
        avg_grade = sum(grades) / total_students
        passing_count = sum(1 for s in students_db if s['grade'] >= 75)
        passing_rate = (passing_count / total_students) * 100
    else:
        avg_grade = 0
        passing_rate = 0

    return render_template('index.html', 
                           students=students_db, 
                           total=total_students, 
                           avg=round(avg_grade, 1), 
                           rate=round(passing_rate, 1))

@app.route('/add_student', methods=['POST'])
def add_student():
    # .strip() removes accidental spaces in names
    name = request.form.get('name', '').strip()
    grade_raw = request.form.get('grade')
    section = request.form.get('section', '').strip()

    # Validation: Ensure no empty fields
    if not name or not grade_raw or not section:
        return redirect(url_for('dashboard'))

    score, letter, remark = calculate_grade_details(grade_raw)
    
    # If the grade wasn't a valid number, score will be None
    if score is not None:
        new_student = {
            "id": len(students_db) + 1,
            "name": name,
            "section": section,
            "grade": score,
            "letter": letter,
            "remark": remark
        }
        students_db.append(new_student)
    
    return redirect(url_for('dashboard'))

if __name__ == '__main__':
    # Standard Render/Cloud configuration
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
