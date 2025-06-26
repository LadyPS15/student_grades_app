from flask import current_app
from flask_mysqldb import MySQL

mysql = MySQL()

def create_tables():
    # Usar app.app_context() para trabajar dentro del contexto de la aplicación
    with current_app.app_context():
        cursor = mysql.connection.cursor()

        # Crear tabla para estudiantes
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100),
            email VARCHAR(100) UNIQUE
        );
        """)

        # Crear tabla para calificaciones
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS grades (
            id INT AUTO_INCREMENT PRIMARY KEY,
            student_id INT,
            grade FLOAT,
            subject VARCHAR(50),
            FOREIGN KEY (student_id) REFERENCES students(id)
        );
        """)
        
        mysql.connection.commit()
