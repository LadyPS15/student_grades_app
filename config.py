import os

class Config:
    SECRET_KEY = os.urandom(24)  # Clave secreta para sesiones de usuario
    MYSQL_HOST = 'localhost'     # Host de la base de datos
    MYSQL_USER = 'root'          # Usuario de la base de datos
    MYSQL_PASSWORD = 'Senati2025!'  # Contraseña de la base de datos
    MYSQL_DB = 'student_grades'  # Nombre de la base de datos
    MYSQL_PORT = 3306  # Puerto de la base de datos (opcional, por defecto es 3306)
    MYSQL_CURSORCLASS = 'DictCursor'  # Clase de cursor para obtener resultados como diccionarios
