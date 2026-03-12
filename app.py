from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({
        "message": "Welcome to my Flask API!",
        "endpoints": {
            "/student": "GET - Retrieve student grade info (requires ?grade parameter)",
            "/students": "GET - List all students"
        }
    })

@app.route('/student')
def get_student():
    try:
        # Get grade from query parameter with validation
        grade_param = request.args.get('grade')
        
        if grade_param is None:
            return jsonify({
                "error": "Missing 'grade' parameter",
                "example": "/student?grade=85"
            }), 400
        
        try:
            grade = int(grade_param)
        except ValueError:
            return jsonify({
                "error": f"Invalid grade value: '{grade_param}'. Must be a number."
            }), 400
        
        # Validate grade range
        if grade < 0 or grade > 100:
            return jsonify({
                "error": "Grade must be between 0 and 100"
            }), 400
        
        # Determine pass or fail (75 is the passing mark)
        remarks = "Pass" if grade >= 75 else "Fail"
        
        # Assign grade letter
        if grade >= 90:
            letter_grade = "A"
        elif grade >= 80:
            letter_grade = "B"
        elif grade >= 75:
            letter_grade = "C"
        else:
            letter_grade = "F"
        
        return jsonify({
            "name": "Juan Dela Cruz",
            "grade": grade,
            "letter_grade": letter_grade,
            "section": "Zechariah",
            "remarks": remarks
        }), 200
        
    except Exception as e:
        return jsonify({
            "error": "An unexpected error occurred",
            "details": str(e)
        }), 500

@app.route('/students')
def get_students():
    """Get list of all students"""
    return jsonify({
        "students": [
            {
                "id": 1,
                "name": "Juan Dela Cruz",
                "section": "Zechariah",
                "grade": 85
            }
        ]
    }), 200

@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "error": "Endpoint not found"
    }), 404

if __name__ == '__main__':
    app.run(debug=True)
