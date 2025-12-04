import psycopg2
import psycopg2.errors
from flask import Flask, request, jsonify, session
from werkzeug.security import generate_password_hash, check_password_hash
from flask_cors import CORS
from functools import wraps
import os

app = Flask(__name__)

CORS(app, 
     supports_credentials=True, 
     origins=["http://172.16.13.133", "http://localhost:5173", "http://127.0.0.1:5173"]
)

app.config['SECRET_KEY'] = 'practicas-computacion-distribuida-2025' # para crear las cookies

############ DEFINIMOS LA BASE DE DATOS ############

def get_db_connection():
    try:
        # Si Render nos da la URL completa, usamos esa
        if os.environ.get('DATABASE_URL'):
            return psycopg2.connect(os.environ.get('DATABASE_URL'))
        
        # Si no, usamos la configuración local de siempre
        return psycopg2.connect(
            host=os.environ.get('DB_HOST', 'localhost'),
            port="5432",
            database="semana2",
            user="postgres",
            password=""
        )
    except Exception as e:
        print("Error conectando a la BBDD:", e)
        return None
    
############ DECORADORES DE SEGURIDAD ############

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' not in session:
            return jsonify({'error': 'No autorizado. Debes iniciar sesión.'}), 401
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' not in session:
            return jsonify({'error': 'No autorizado. Debes iniciar sesión.'}), 401
        if session['user'] != 'admin':
            return jsonify({'error': 'Acción no permitida. Solo el admin puede realizar esta operación.'}), 403
        return f(*args, **kwargs)
    return decorated_function

############ ENDPOINTS DE AUTENTICACIÓN ############

# REGISTRO
@app.route('/api/register', methods=['POST'])
def register():
    conexion = get_db_connection()
    data = request.get_json()
    if not data or 'username' not in data or 'password' not in data:
        return jsonify({'error': 'Faltan usuario y contraseña'}), 400
    username = data['username']
    password = data['password']
    hashed_password = generate_password_hash(password)
    try:
        with conexion.cursor() as cursor:
            cursor.execute(
                "INSERT INTO USUARIOS (NOMBRE, PASSWORD_HASH) VALUES (%s, %s)",
                (username, hashed_password)
            )
            conexion.commit()
        return jsonify({'message': f'Usuario {username} creado exitosamente'}), 201
    except psycopg2.errors.UniqueViolation:
        conexion.rollback()
        return jsonify({'error': 'El nombre de usuario ya existe'}), 409
    except Exception as e:
        conexion.rollback()
        return jsonify({'error': f'Error de servidor: {str(e)}'}), 500

# LOGIN
@app.route('/api/login', methods=['POST'])
def login():
    conexion = get_db_connection()
    data = request.get_json()
    if not data or 'username' not in data or 'password' not in data:
        return jsonify({'error': 'Faltan usuario y contraseña'}), 400
    username = data['username']
    password = data['password']
    with conexion.cursor() as cursor:
        cursor.execute(
            "SELECT PASSWORD_HASH FROM USUARIOS WHERE NOMBRE = %s",
            (username,)
        )
        user_row = cursor.fetchone()
    if user_row is None:
        return jsonify({'error': 'Usuario o contraseña incorrectos'}), 401
    stored_hash = user_row[0]
    if not check_password_hash(stored_hash, password):
        return jsonify({'error': 'Usuario o contraseña incorrectos'}), 401
    session['user'] = username
    return jsonify({
        'message': f'Login exitoso. ¡Bienvenido, {username}!',
        'user': {
            'username': username,
            'isAdmin': username == 'admin'
        }
    })

@app.route('/api/profile')
@login_required
def profile():

    username = session['user']
    return jsonify({
        'message': f'Estás logueado como: {username}',
        'username': username
    })

@app.route('/api/logout')
@login_required
def logout():
    session.pop('user', None)
    return jsonify({'message': 'Has cerrado sesión exitosamente.'})

##### ##### - - - - - - - - - - - ##### #####

##### ##### ENDPOINTS DE FUNCIONES ##### #####

@app.route('/api/listar_juegos', methods=['GET'])
@login_required
def listar_juegos():
    conexion = get_db_connection()
    juegos_lista = []
    try:
        with conexion.cursor() as cursor:
            cursor.execute(
                "SELECT id, name, description, year, image, url, isLocal FROM JUEGOS ORDER BY id"
            )
            juegos_raw = cursor.fetchall()
            columnas = [desc[0] for desc in cursor.description]
            for juego_raw in juegos_raw:
                juegos_lista.append(dict(zip(columnas, juego_raw)))
        return jsonify(juegos_lista), 200
    except Exception as e:
        return jsonify({'error': f'Error al obtener la lista de juegos: {str(e)}'}), 500

@app.route('/api/juego/<int:id>', methods=['GET'])
@login_required
def get_juego(id):
    conexion = get_db_connection()
    try:
        with conexion.cursor() as cursor:
            cursor.execute(
                "SELECT id, name, description, year, image, url, isLocal FROM JUEGOS WHERE id = %s",
                (id,)
            )
            juego_raw = cursor.fetchone()
            
            if not juego_raw:
                return jsonify({'error': 'Juego no encontrado'}), 404
                
            columnas = [desc[0] for desc in cursor.description]
            juego_dict = dict(zip(columnas, juego_raw))
            return jsonify(juego_dict), 200

    except Exception as e:
        return jsonify({'error': f'Error al obtener el juego: {str(e)}'}), 500

@app.route('/api/anadir_juego', methods=['POST'])
@admin_required
def anadir_juego():
    
    conexion = get_db_connection()
    data = request.get_json()
    
    if not data or 'name' not in data or 'description' not in data:
        return jsonify({'error': 'Faltan datos (name, description son obligatorios)'}), 400
    
    try:

        name = data['name']
        description = data['description']
        year = data.get('year', None)
        image = data.get('image', None)
        url = data.get('url', None)
        isLocal = data.get('islocal', False)
        
        with conexion.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO JUEGOS (name, description, year, image, url, isLocal)
                VALUES (%s, %s, %s, %s, %s, %s)
                """,
                (name, description, year, image, url, isLocal)
            )
            conexion.commit()
        
        return jsonify({'message': f'Juego "{name}" añadido exitosamente'}), 201

    except Exception as e:
        conexion.rollback()
        return jsonify({'error': f'Error de servidor al añadir juego: {str(e)}'}), 500

@app.route('/api/editar_juego/<int:id>', methods=['PUT'])
@admin_required
def editar_juego(id):
    conexion = get_db_connection()
    data = request.get_json()
    
    if not data or 'name' not in data or 'description' not in data:
        return jsonify({'error': 'Faltan datos (name, description son obligatorios)'}), 400
    
    try:
        name = data['name']
        description = data['description']
        year = data.get('year', None)
        image = data.get('image', None)
        url = data.get('url', None)
        isLocal = data.get('islocal', False)
        
        with conexion.cursor() as cursor:
            cursor.execute(
                """
                UPDATE JUEGOS
                SET name = %s, description = %s, year = %s, image = %s, url = %s, isLocal = %s
                WHERE id = %s
                """,
                (name, description, year, image, url, isLocal, id)
            )
            conexion.commit()
        
        if cursor.rowcount == 0:
            return jsonify({'error': 'Juego no encontrado o sin cambios'}), 404
            
        return jsonify({'message': f'Juego ID {id} actualizado exitosamente'})

    except Exception as e:
        conexion.rollback()
        return jsonify({'error': f'Error de servidor al editar juego: {str(e)}'}), 500

@app.route('/api/eliminar_juego/<int:id>', methods=['DELETE'])
@admin_required
def eliminar_juego(id):
    conexion = get_db_connection()
    try:
        with conexion.cursor() as cursor:
            cursor.execute(
                "DELETE FROM JUEGOS WHERE id = %s",
                (id,)
            )
            conexion.commit()
        
        if cursor.rowcount == 0:
            return jsonify({'error': 'Juego no encontrado'}), 404
            
        return jsonify({'message': f'Juego ID {id} eliminado exitosamente'})

    except Exception as e:
        conexion.rollback()
        return jsonify({'error': f'Error de servidor al eliminar juego: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)