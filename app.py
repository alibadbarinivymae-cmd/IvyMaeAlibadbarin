from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Initial Data - Ensure 'grade' is an int
students_db = [
    {"id": 1, "name": "Juan Dela Cruz", "section": "Zechariah", "grade": 85, "letter": "B", "remark": "Passed"}
]

def get_grade_details(grade):
    # Convert to int safely
    try:
        grade = int(grade)
    except (ValueError, TypeError):
        grade = 0
        
    if grade >= 90: return "A", "Excellent"
    elif grade >= 80: return "B", "Good"
    elif grade >= 75: return "C", "Passed"
    else: return "F", "Failed"

@app.route('/')
def dashboard():
    total_students = len(students_db)
    
    # Critical Fix: Ensure grade is converted to int during calculation
    if total_students > 0:
        avg_grade = sum(int(s['grade']) for s in students_db) / total_students
        passing_count = len([s for s in students_db if int(s['grade']) >= 75])
        passing_rate = (passing_count / total_students * 100)
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
    name = request.form.get('name')
    grade = request.form.get('grade')
    section = request.form.get('section')

    if name and grade:
        letter, remark = get_grade_details(grade)
        new_student = {
            "id": len(students_db) + 1,
            "name": name,
            "section": section,
            "grade": int(grade), # Store as integer
            "letter": letter,
            "remark": remark
        }
        students_db.append(new_student)
    
    return redirect(url_for('dashboard'))

if __name__ == '__main__':
    app.run(debug=True)
