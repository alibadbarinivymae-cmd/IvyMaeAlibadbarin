from flask import Flask, jsonify, request

app = Flask(__name__)

# This is our temporary database (it resets when Render restarts)
students_db = [
    {
        "id": 1, 
        "name": "Juan Dela Cruz", 
        "section": "Zechariah", 
        "grade": 85, 
        "letter_grade": "B", 
        "remarks": "Passed"
    }
]

def calculate_grade_details(grade):
    """Automatically determines letter grade and remarks"""
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

# 1. GET ALL STUDENTS
@app.route('/students', methods=['GET'])
def get_students():
    return jsonify({"students": students_db}), 200

# 2. GET SINGLE STUDENT (Your original /student link)
@app.route('/student', methods=['GET'])
def get_default_student():
    # Returns the first student in the list
    return jsonify(students_db[0]), 200

# 3. GET STUDENT BY ID (e.g., /student/1)
@app.route('/student/<int:student_id>', methods=['GET'])
def get_student_by_id(student_id):
    student = next((s for s in students_db if s['id'] == student_id), None)
    if student:
        return jsonify(student), 200
    return jsonify({"error": "Student not found"}), 404

# 4. POST TO ADD A NEW STUDENT
@app.route('/students', methods=['POST'])
def add_student():
    data = request.get_json()
    
    # Validation
    if not data or 'name' not in data or 'grade' not in data:
        return jsonify({"error": "Missing name or grade in JSON body"}), 400
    
    # Use our logic function
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

@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Endpoint not found"}), 404

if __name__ == '__main__':
    # Render uses environment variables for Port, but this is fine for local testing
    app.run(debug=True)
