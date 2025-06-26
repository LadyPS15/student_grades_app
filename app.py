from flask import Flask, render_template, request, redirect, url_for
from models import mysql, create_tables
import pandas as pd
import matplotlib.pyplot as plt
import io
import base64

app = Flask(__name__)
app.config.from_object('config.Config')

# Inicializar MySQL
mysql.init_app(app)

# Crear tablas al iniciar la aplicación
with app.app_context():
    create_tables()

# Ruta para la página principal
@app.route('/')
def index():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM students")
    students = cursor.fetchall()
    print(students)  # Esto imprimirá los datos en la consola
    return render_template('index.html', students=students)

# Ruta para agregar un estudiante
@app.route('/add_student', methods=['GET', 'POST'])
def add_student():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        
        cursor = mysql.connection.cursor()
        cursor.execute("INSERT INTO students (name, email) VALUES (%s, %s)", (name, email))
        mysql.connection.commit()
        return redirect(url_for('index'))
    
    return render_template('add_student.html')

# Ruta para eliminar un estudiante
@app.route('/delete_student/<student_id>', methods=['POST'])
def delete_student(student_id):
    cursor = mysql.connection.cursor()
    cursor.execute("DELETE FROM students WHERE id = %s", (student_id,))
    mysql.connection.commit()
    return redirect(url_for('index'))

# Ruta para ver el rendimiento de un estudiante
@app.route('/view_student/<student_id>')
def view_student(student_id):
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM students WHERE id = %s", (student_id,))
    student = cursor.fetchone()
    
    cursor.execute("SELECT * FROM grades WHERE student_id = %s", (student_id,))
    grades = cursor.fetchall()

    # Generar gráfico de rendimiento
    subjects = [grade['subject'] for grade in grades]
    scores = [grade['grade'] for grade in grades]

    fig, ax = plt.subplots()
    ax.bar(subjects, scores)
    ax.set_xlabel('Subjects')
    ax.set_ylabel('Grades')
    ax.set_title(f'Performance of {student["name"]}')

    # Guardar gráfico en imagen base64
    img = io.BytesIO()
    fig.savefig(img, format='png')
    img.seek(0)
    graph_url = base64.b64encode(img.getvalue()).decode()

    return render_template('view_student.html', student=student, grades=grades, graph_url=graph_url)

# Ruta para agregar calificaciones
@app.route('/add_grade/<student_id>', methods=['GET', 'POST'])
def add_grade(student_id):
    if request.method == 'POST':
        grade = request.form['grade']
        subject = request.form['subject']
        
        cursor = mysql.connection.cursor()
        cursor.execute("INSERT INTO grades (student_id, grade, subject) VALUES (%s, %s, %s)", (student_id, grade, subject))
        mysql.connection.commit()
        return redirect(url_for('view_student', student_id=student_id))
    
    return render_template('add_grade.html', student_id=student_id)


if __name__ == '__main__':
    app.run(debug=True)
