from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/')
def home():
    return "Welcome to my Flask API!"

@app.route('/student')
def get_student():
    # Get grade from query parameter (default = 0)
    grade_param = request.args.get('grade', 0)
    grade = int(grade_param)
    
    # Determine pass or fail (75 is the passing mark)
    remarks = "Pass" if grade >= 75 else "Fail"
    
    return jsonify({
        "name": "Juan Dela Cruz",
        "grade": grade,
        "section": "Zechariah",
        "remarks": remarks
    })

if __name__ == '__main__':
    app.run(debug=True)
