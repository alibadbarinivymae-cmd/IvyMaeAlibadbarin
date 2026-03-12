from flask import Flask, jsonify, request
app = Flask(__name__)

@app.route('/')
def home():
return "Welcome to my Flask API!"

@app.route('/student')
def get_student():
return jsonify({
"name": "Your Name",
"grade": 10,
"section": "Zechariah"
})a Cruz",
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
