import pyotp
import sqlite3
import hashlib
from flask import Flask, request

app = Flask(__name__)
db_name = 'usuarios.db'

@app.route('/')
def index():
    return 'Bienvenido al sistema de control de contraseñas seguras (versión Rafael)'

@app.route('/signup', methods=['POST'])
def signup():
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS USUARIOS (
                    USERNAME TEXT PRIMARY KEY NOT NULL,
                    HASH TEXT NOT NULL);''')
    conn.commit()
    try:
        hash_value = hashlib.sha256(request.form['password'].encode()).hexdigest()
        c.execute("INSERT INTO USUARIOS (USERNAME, HASH) VALUES (?, ?)", 
                  (request.form['username'], hash_value))
        conn.commit()
    except sqlite3.IntegrityError:
        return "El usuario ya está registrado."
    return "Registro exitoso"

def verificar_usuario(username, password):
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    c.execute("SELECT HASH FROM USUARIOS WHERE USERNAME = ?", (username,))
    record = c.fetchone()
    conn.close()
    if not record:
        return False
    return record[0] == hashlib.sha256(password.encode()).hexdigest()

@app.route('/login', methods=['POST'])
def login():
    if verificar_usuario(request.form['username'], request.form['password']):
        return 'Inicio de sesión exitoso'
    else:
        return 'Usuario o contraseña incorrectos'

@app.route('/signup_plain', methods=['POST'])
def signup_plain():
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS USUARIOS_PLAIN (
                    USERNAME TEXT PRIMARY KEY NOT NULL,
                    PASSWORD TEXT NOT NULL);''')
    conn.commit()
    try:
        c.execute("INSERT INTO USUARIOS_PLAIN (USERNAME, PASSWORD) VALUES (?, ?)", 
                  (request.form['username'], request.form['password']))
        conn.commit()
    except sqlite3.IntegrityError:
        return "El usuario ya está registrado en texto plano."
    return "Registro en texto plano exitoso"

def insertar_usuarios_prueba():
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS USUARIOS_PLAIN (
                    USERNAME TEXT PRIMARY KEY NOT NULL,
                    PASSWORD TEXT NOT NULL);''')
    conn.commit()
    usuarios = [
        ('rafael', 'contraseña123'),
        ('compañero', 'clave456')
    ]
    for user, pwd in usuarios:
        try:
            c.execute("INSERT INTO USUARIOS_PLAIN (USERNAME, PASSWORD) VALUES (?, ?)", (user, pwd))
        except sqlite3.IntegrityError:
            pass
    conn.commit()
    conn.close()

if __name__ == '__main__':
    insertar_usuarios_prueba()
    app.run(host='0.0.0.0', port=5566)
