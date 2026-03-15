from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/')
def home():
    # Indented 4 spaces
    return "Welcome to my Flask API!"

@app.route('/student')
def get_student():
    # Indented 4 spaces
    return jsonify({
        "name": "Your Name",
        "grade": 10,
        "section": "Zechariah"
    })

# This part starts the server
if __name__ == '__main__':
    app.run(debug=True)
