from flask import Flask, jsonify, request

app = Flask(__name__)

# This acts as our temporary database
students_db = [
    {"id": 1, "name": "Juan Dela Cruz", "section": "Zechariah", "grade": 85, "letter_grade": "B", "remarks": "Passed"}
]

def calculate_grade_details(grade):
    """Helper function to automate grading logic"""
    if grade >= 90:
        return "A", "Excellent"
    elif grade >= 80:
        return "B", "Good"
    elif grade >= 75:
        return "C", "Passed"
    else:
        return "F", "Failed"

@app.route('/')
def home():
    return "Welcome to the Student Management API!"

# 1. GET all students
@app.route('/students', methods=['GET'])
def get_students():
    return jsonify({"students": students_db}), 200

# 2. POST to add a new student
@app.route('/students', methods=['POST'])
def add_student():
    data = request.get_json()
    
    # Validation: Ensure required fields are present
    if not data or 'name' not in data or 'grade' not in data:
        return jsonify({"error": "Missing name or grade"}), 400
    
    # Calculate grade details automatically
    letter, remark = calculate_grade_details(data['grade'])
    
    new_student = {
        "id": len(students_db) + 1,
        "name": data['name'],
        "section": data.get('section', 'General'),
        "grade": data['grade'],
        "letter_grade": letter,
        "remarks": remark
    }
    
    students_db.append(new_student)
    return jsonify({"message": "Student added successfully!", "student": new_student}), 201

# 3. GET a specific student by ID
@app.route('/student/<int:student_id>', methods=['GET'])
def get_student(student_id):
    student = next((s for s in students_db if s['id'] == student_id), None)
    if student:
        return jsonify(student), 200
    return jsonify({"error": "Student not found"}), 404

@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Endpoint not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)
    app.run(debug=True)
if __name__ == '__main__':
    app.run(debug=True)
