from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Initial Data
students_db = [
    {"id": 1, "name": "Juan Dela Cruz", "section": "Zechariah", "grade": 85, "letter": "B", "remark": "Passed"}
]

def get_grade_details(grade):
    grade = int(grade)
    if grade >= 90: return "A", "Excellent"
    elif grade >= 80: return "B", "Good"
    elif grade >= 75: return "C", "Passed"
    else: return "F", "Failed"

@app.route('/')
def dashboard():
    # Calculate Dashboard Stats
    total_students = len(students_db)
    avg_grade = sum(int(s['grade']) for s in students_db) / total_students if total_students > 0 else 0
    passing_count = len([s for s in students_db if s['remark'] != "Failed"])
    passing_rate = (passing_count / total_students * 100) if total_students > 0 else 0

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
            "grade": grade,
            "letter": letter,
            "remark": remark
        }
        students_db.append(new_student)
    
    return redirect(url_for('dashboard'))

if __name__ == '__main__':
    app.run(debug=True)
