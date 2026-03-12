from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/')
def home():
    return "Welcome to my Flask API!"

@app.route('/student')
def get_student():
    try:
        # Assuming these variables (grade, letter_grade, remarks) 
        # are defined or fetched from somewhere. 
        # For now, I'll set placeholders so the code runs.
        grade = 85
        letter_grade = "B"
        remarks = "Passed"

        return jsonify({
            "name": "Juan Dela Cruz", # Fixed the stray "a 'Cruz" here
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
if __name__ == '__main__':
    app.run(debug=True)
