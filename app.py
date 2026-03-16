from flask import Flask, request, redirect, render_template_string
import sqlite3

app = Flask(__name__)

# DATABASE CONNECTION
def get_db():
    conn = sqlite3.connect("students.db")
    conn.row_factory = sqlite3.Row
    return conn

# CREATE TABLE IF NOT EXISTS
def create_table():
    conn = get_db()
    conn.execute('''
    CREATE TABLE IF NOT EXISTS students(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id TEXT,
        name TEXT,
        course TEXT,
        year_level INTEGER,
        first_sem REAL,
        second_sem REAL,
        gpa REAL,
        status TEXT
    )
    ''')
    conn.commit()
    conn.close()

create_table()

# BRAND NEW CSS THEME: Midnight Emerald
COMMON_HEAD = '''
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap" rel="stylesheet">
    <style>
        :root {
            --bg-dark: #0f172a;
            --card-dark: #1e293b;
            --emerald: #10b981;
            --accent: #38bdf8;
            --text-main: #f1f5f9;
            --text-dim: #94a3b8;
        }
        body { 
            background-color: var(--bg-dark); 
            font-family: 'Inter', sans-serif; 
            color: var(--text-main);
            min-height: 100vh;
        }
        .container { max-width: 1100px; }
        
        /* Modern Card Styling */
        .main-card {
            background: var(--card-dark);
            border: 1px solid rgba(255,255,255,0.05);
            border-radius: 16px;
            box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.3);
        }

        /* Table Aesthetics */
        .table { color: var(--text-main); margin-bottom: 0; }
        .table thead { background: rgba(0,0,0,0.2); }
        .table th { border: none; font-weight: 600; color: var(--accent); text-transform: uppercase; font-size: 0.75rem; letter-spacing: 1px; }
        .table td { border-color: rgba(255,255,255,0.05); padding: 1rem; vertical-align: middle; }
        
        /* Status Badges */
        .badge-passed { background: rgba(16, 185, 129, 0.1); color: #34d399; border: 1px solid rgba(16, 185, 129, 0.2); }
        .badge-failed { background: rgba(239, 68, 68, 0.1); color: #f87171; border: 1px solid rgba(239, 68, 68, 0.2); }
        
        /* Buttons */
        .btn-emerald { background-color: var(--emerald); color: white; border-radius: 8px; font-weight: 600; transition: 0.3s; border: none; }
        .btn-emerald:hover { background-color: #059669; transform: translateY(-1px); color: white; }
        .btn-outline-custom { border: 1px solid var(--text-dim); color: var(--text-dim); border-radius: 8px; }
        .btn-outline-custom:hover { border-color: var(--accent); color: var(--accent); }

        /* Form Inputs */
        .form-label { color: var(--text-dim); font-weight: 500; font-size: 0.85rem; }
        .form-control { 
            background: #0f172a; 
            border: 1px solid #334155; 
            color: white; 
            border-radius: 10px;
            padding: 0.75rem;
        }
        .form-control:focus { 
            background: #0f172a; 
            color: white; 
            border-color: var(--accent); 
            box-shadow: 0 0 0 4px rgba(56, 189, 248, 0.1); 
        }
        
        .header-section { padding: 40px 0; }
        .page-title { font-weight: 700; letter-spacing: -1px; }
        .student-id-pill { background: #334155; padding: 4px 10px; border-radius: 6px; font-family: monospace; font-size: 0.9rem; }
    </style>
'''

# HOME PAGE
@app.route('/')
def index():
    conn = get_db()
    students = conn.execute("SELECT * FROM students").fetchall()
    conn.close()

    return render_template_string(f'''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <title>IMS | Student Registry</title>
        {COMMON_HEAD}
    </head>
    <body>
        <div class="container">
            <div class="header-section d-flex justify-content-between align-items-center">
                <div>
                    <h2 class="page-title mb-0">Student <span style="color:var(--emerald)">Registry</span></h2>
                    <p class="text-muted mb-0">Academic Information Management System</p>
                </div>
                <a href="/add" class="btn btn-emerald px-4 py-2">
                    <i class="fas fa-plus-circle me-2"></i>New Enrollment
                </a>
            </div>
            
            <div class="main-card overflow-hidden">
                <div class="table-responsive">
                    <table class="table">
                        <thead>
                            <tr>
                                <th>Student ID</th>
                                <th>Full Name</th>
                                <th>Course & Year</th>
                                <th>GPA</th>
                                <th>Status</th>
                                <th class="text-end">Actions</th>
                            </tr>
                        </thead>
                        <tbody>
                            {{% for s in students %}}
                            <tr>
                                <td><span class="student-id-pill text-accent">{{{{s.student_id}}}}</span></td>
                                <td class="fw-bold">{{{{s.name}}}}</td>
                                <td>
                                    <div class="small">{{{{s.course}}}}</div>
                                    <div class="text-muted small">Year {{{{s.year_level}}}}</div>
                                </td>
                                <td><span class="fw-bold" style="color:var(--accent)">{{{{s.gpa}}}}</span></td>
                                <td>
                                    {{% if s.status == 'Passed' %}}
                                        <span class="badge badge-passed"><i class="fas fa-check me-1"></i>Passed</span>
                                    {{% else %}}
                                        <span class="badge badge-failed"><i class="fas fa-exclamation-triangle me-1"></i>Failed</span>
                                    {{% endif %}}
                                </td>
                                <td class="text-end">
                                    <a href="/edit/{{{{s.id}}}}" class="btn btn-sm btn-outline-custom me-2"><i class="fas fa-edit"></i></a>
                                    <a href="/delete/{{{{s.id}}}}" class="btn btn-sm btn-outline-danger" onclick="return confirm('Delete record?');"><i class="fas fa-trash"></i></a>
                                </td>
                            </tr>
                            {{% else %}}
                            <tr>
                                <td colspan="6" class="text-center py-5 text-muted">
                                    No records found in the database.
                                </td>
                            </tr>
                            {{% endfor %}}
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    </body>
    </html>
    ''', students=students)

# ADD STUDENT
@app.route('/add', methods=['GET','POST'])
def add():
    if request.method == 'POST':
        # (Your existing logic remains untouched)
        student_id = request.form['student_id']
        name = request.form['name']
        course = request.form['course']
        year_level = request.form['year_level']
        first_sem = float(request.form['first_sem'])
        second_sem = float(request.form['second_sem'])
        gpa = (first_sem + second_sem) / 2
        status = "Passed" if gpa <= 3 else "Failed"
        conn = get_db()
        conn.execute("INSERT INTO students (student_id,name,course,year_level,first_sem,second_sem,gpa,status) VALUES (?,?,?,?,?,?,?,?)",
            (student_id,name,course,year_level,first_sem,second_sem,gpa,status))
        conn.commit()
        conn.close()
        return redirect('/')

    return render_template_string(f'''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <title>New Enrollment</title>
        {COMMON_HEAD}
    </head>
    <body>
        <div class="container mt-5">
            <div class="row justify-content-center">
                <div class="col-md-6">
                    <div class="main-card p-4">
                        <h4 class="mb-4 fw-bold"><i class="fas fa-user-plus text-emerald me-2"></i>Add Student</h4>
                        <form method="post">
                            <div class="mb-3">
                                <label class="form-label">Student ID</label>
                                <input type="text" class="form-control" name="student_id" required>
                            </div>
                            <div class="mb-3">
                                <label class="form-label">Full Name</label>
                                <input type="text" class="form-control" name="name" required>
                            </div>
                            <div class="row mb-3">
                                <div class="col-8">
                                    <label class="form-label">Course</label>
                                    <input type="text" class="form-control" name="course" required>
                                </div>
                                <div class="col-4">
                                    <label class="form-label">Year Level</label>
                                    <input type="number" class="form-control" name="year_level" min="1" max="5" required>
                                </div>
                            </div>
                            <div class="row mb-4">
                                <div class="col-6">
                                    <label class="form-label">1st Sem Grade</label>
                                    <input type="number" step="0.01" class="form-control" name="first_sem" required>
                                </div>
                                <div class="col-6">
                                    <label class="form-label">2nd Sem Grade</label>
                                    <input type="number" step="0.01" class="form-control" name="second_sem" required>
                                </div>
                            </div>
                            <div class="d-flex gap-2">
                                <button type="submit" class="btn btn-emerald w-100 py-2">Create Record</button>
                                <a href="/" class="btn btn-outline-custom w-50 py-2">Back</a>
                            </div>
                        </form>
                    </div>
                </div>
            </div>
        </div>
    </body>
    </html>
    ''')

# (Edit/Delete routes would follow the same pattern of using the main-card class and emerald buttons)
# ... [Rest of your Edit/Delete logic] ...

@app.route('/edit/<int:id>', methods=['GET','POST'])
def edit(id):
    conn = get_db()
    student = conn.execute("SELECT * FROM students WHERE id=?", (id,)).fetchone()
    if request.method == 'POST':
        # ... logic ...
        student_id = request.form['student_id']
        name = request.form['name']
        course = request.form['course']
        year_level = request.form['year_level']
        first_sem = float(request.form['first_sem'])
        second_sem = float(request.form['second_sem'])
        gpa = (first_sem + second_sem) / 2
        status = "Passed" if gpa <= 3 else "Failed"
        conn.execute("UPDATE students SET student_id=?,name=?,course=?,year_level=?,first_sem=?,second_sem=?,gpa=?,status=? WHERE id=?",
            (student_id,name,course,year_level,first_sem,second_sem,gpa,status,id))
        conn.commit()
        conn.close()
        return redirect('/')
    conn.close()
    return render_template_string(f'''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <title>Edit Record</title>
        {COMMON_HEAD}
    </head>
    <body>
        <div class="container mt-5">
            <div class="row justify-content-center">
                <div class="col-md-6">
                    <div class="main-card p-4">
                        <h4 class="mb-4 fw-bold"><i class="fas fa-edit text-accent me-2"></i>Edit Student</h4>
                        <form method="post">
                            <div class="mb-3">
                                <label class="form-label">Student ID</label>
                                <input type="text" class="form-control" name="student_id" value="{{{{s.student_id}}}}" required>
                            </div>
                            <div class="mb-3">
                                <label class="form-label">Full Name</label>
                                <input type="text" class="form-control" name="name" value="{{{{s.name}}}}" required>
                            </div>
                            <div class="row mb-3">
                                <div class="col-8">
                                    <label class="form-label">Course</label>
                                    <input type="text" class="form-control" name="course" value="{{{{s.course}}}}" required>
                                </div>
                                <div class="col-4">
                                    <label class="form-label">Year Level</label>
                                    <input type="number" class="form-control" name="year_level" value="{{{{s.year_level}}}}" min="1" max="5" required>
                                </div>
                            </div>
                            <div class="row mb-4">
                                <div class="col-6">
                                    <label class="form-label">1st Sem Grade</label>
                                    <input type="number" step="0.01" class="form-control" name="first_sem" value="{{{{s.first_sem}}}}" required>
                                </div>
                                <div class="col-6">
                                    <label class="form-label">2nd Sem Grade</label>
                                    <input type="number" step="0.01" class="form-control" name="second_sem" value="{{{{s.second_sem}}}}" required>
                                </div>
                            </div>
                            <div class="d-flex gap-2">
                                <button type="submit" class="btn btn-emerald w-100 py-2">Update Record</button>
                                <a href="/" class="btn btn-outline-custom w-50 py-2">Cancel</a>
                            </div>
                        </form>
                    </div>
                </div>
            </div>
        </div>
    </body>
    </html>
    ''', s=student)

@app.route('/delete/<int:id>')
def delete(id):
    conn = get_db()
    conn.execute("DELETE FROM students WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return redirect('/')

if __name__ == "__main__":
    app.run(debug=True)
