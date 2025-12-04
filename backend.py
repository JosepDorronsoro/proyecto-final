import os
import psycopg2
import psycopg2.errors
from flask import Flask, request, jsonify, session
from werkzeug.security import generate_password_hash, check_password_hash
from flask_cors import CORS
from functools import wraps

app = Flask(__name__)

frontend_url = os.environ.get('FRONTEND_URL')
if frontend_url:
    allowed_origins = [frontend_url.rstrip('/')] 
else:
    allowed_origins = ["http://localhost:5173", "http://127.0.0.1:5173"]

CORS(app, supports_credentials=True, origins=allowed_origins)

app.config['SECRET_KEY'] = 'practicas-computacion-distribuida-2025'

def get_db_connection():
    try:
        database_url = os.environ.get('DATABASE_URL')
        if database_url:
            return psycopg2.connect(database_url)
        else:
            return psycopg2.connect(
                host=os.environ.get('DB_HOST', 'localhost'),
                port="5432",
                database="semana2",
                user="postgres",
                password=""
            )
    except Exception as e:
        print(f"Error conectando a BBDD: {e}")
        return None

def init_db():
    print("--- Verificando estado de la Base de Datos ---")
    conexion = get_db_connection()
    if not conexion:
        print("ERROR: No se pudo conectar para inicializar.")
        return

    try:
        with conexion.cursor() as cursor:

            cursor.execute('''
                CREATE TABLE IF NOT EXISTS JUEGOS (
                    id SERIAL PRIMARY KEY, 
                    name VARCHAR(255) NOT NULL,
                    description TEXT,
                    year INTEGER,
                    image TEXT,
                    url TEXT,
                    isLocal BOOLEAN DEFAULT false
                );
            ''')
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS USUARIOS (
                    NOMBRE TEXT PRIMARY KEY,
                    PASSWORD_HASH TEXT NOT NULL
                )
            ''')
            
            cursor.execute("SELECT COUNT(*) FROM JUEGOS")
            if cursor.fetchone()[0] == 0:
                print("Tabla JUEGOS vacía. Insertando datos iniciales...")
                cursor.execute('''    
                INSERT INTO JUEGOS (name, description, year, image, url, isLocal) VALUES
                ('La Serpiente', 'Consigue comer todas las manzanas...', 1970, 'https://www5.minijuegosgratis.com/v3/games/thumbnails/246309_1.jpg', 'https://es.wikipedia.org/wiki/La_serpiente_(videojuego)', false),
                ('PacMan', 'Clásico arcade...', 1980, 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTcwYQ8aUGsRRyHOV47MD50N700tSYO_PGTRQ&s', 'https://es.wikipedia.org/wiki/Pac-Man', false),
                ('Batalla Naval', 'Juego estratégico...', 1931, 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQHPifWn7MH0c9f38wA1KwpTZR0LBwca5ItjQ&s', 'https://es.wikipedia.org/wiki/Videojuego_de_estrategia', false),
                ('Busca Minas', 'Juego de lógica...', 1990, 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQyt9aXYvIMfazAG4s8MrF9l7TcHEuvm60WQA&s', 'https://es.wikipedia.org/wiki/Buscaminas', false),
                ('Tetris', 'Juego clásico de ingenio...', 1984, 'https://cdn-icons-png.flaticon.com/512/1138/1138876.png', 'https://es.wikipedia.org/wiki/Tetris', false),
                ('Tres en Raya', 'Clásico juego de tres en raya...', 2025, 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTki6sw_Oh_xQiXXDrVSUJcHrvMIXvgemlW7Q&s', NULL, true)
                ''')
            
            cursor.execute("SELECT * FROM USUARIOS WHERE NOMBRE = 'admin'")
            if not cursor.fetchone():
                print("Creando usuario admin...")
                contraseña_admin = generate_password_hash('admin_2025')
                cursor.execute(
                    "INSERT INTO USUARIOS (NOMBRE, PASSWORD_HASH) VALUES (%s, %s)",
                    ('admin', contraseña_admin)
                )
            
            conexion.commit()
            print("--- Base de Datos lista y actualizada ---")

    except Exception as e:
        print(f"Error en la inicialización de DB: {e}")
        conexion.rollback()
    finally:
        conexion.close()

init_db()

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' not in session:
            return jsonify({'error': 'No autorizado'}), 401
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' not in session:
            return jsonify({'error': 'No autorizado'}), 401
        if session['user'] != 'admin':
            return jsonify({'error': 'Acción no permitida'}), 403
        return f(*args, **kwargs)
    return decorated_function


@app.route('/api/register', methods=['POST'])
def register():
    data = request.get_json()
    if not data or 'username' not in data or 'password' not in data:
        return jsonify({'error': 'Faltan datos'}), 400
    
    username = data['username']
    password = data['password']
    hashed_password = generate_password_hash(password)
    
    conexion = get_db_connection()
    if not conexion: return jsonify({'error': 'Error DB'}), 500

    try:
        with conexion.cursor() as cursor:
            cursor.execute("INSERT INTO USUARIOS (NOMBRE, PASSWORD_HASH) VALUES (%s, %s)", (username, hashed_password))
            conexion.commit()
        return jsonify({'message': f'Usuario {username} creado'}), 201
    except psycopg2.errors.UniqueViolation:
        conexion.rollback()
        return jsonify({'error': 'El usuario ya existe'}), 409
    except Exception as e:
        conexion.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        conexion.close()

@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data or 'username' not in data or 'password' not in data:
        return jsonify({'error': 'Faltan datos'}), 400
    
    username = data['username']
    password = data['password']
    
    conexion = get_db_connection()
    if not conexion: return jsonify({'error': 'Error DB'}), 500

    try:
        with conexion.cursor() as cursor:
            cursor.execute("SELECT PASSWORD_HASH FROM USUARIOS WHERE NOMBRE = %s", (username,))
            user_row = cursor.fetchone()
        
        if user_row is None or not check_password_hash(user_row[0], password):
            return jsonify({'error': 'Credenciales incorrectas'}), 401
        
        session['user'] = username
        return jsonify({
            'message': 'Login exitoso',
            'user': {'username': username, 'isAdmin': username == 'admin'}
        })
    finally:
        conexion.close()

@app.route('/api/profile')
@login_required
def profile():
    return jsonify({'message': f'Logueado como: {session["user"]}', 'username': session['user']})

@app.route('/api/logout')
@login_required
def logout():
    session.pop('user', None)
    return jsonify({'message': 'Logout exitoso'})

@app.route('/api/listar_juegos', methods=['GET'])
@login_required
def listar_juegos():
    conexion = get_db_connection()
    if not conexion: return jsonify({'error': 'Error DB'}), 500
    try:
        with conexion.cursor() as cursor:
            cursor.execute("SELECT id, name, description, year, image, url, isLocal FROM JUEGOS ORDER BY id")
            columns = [desc[0] for desc in cursor.description]
            games = [dict(zip(columns, row)) for row in cursor.fetchall()]
        return jsonify(games), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        conexion.close()

@app.route('/api/juego/<int:id>', methods=['GET'])
@login_required
def get_juego(id):
    conexion = get_db_connection()
    if not conexion: return jsonify({'error': 'Error DB'}), 500
    try:
        with conexion.cursor() as cursor:
            cursor.execute("SELECT id, name, description, year, image, url, isLocal FROM JUEGOS WHERE id = %s", (id,))
            row = cursor.fetchone()
            if not row: return jsonify({'error': 'Juego no encontrado'}), 404
            columns = [desc[0] for desc in cursor.description]
            return jsonify(dict(zip(columns, row))), 200
    finally:
        conexion.close()

@app.route('/api/anadir_juego', methods=['POST'])
@admin_required
def anadir_juego():
    data = request.get_json()
    if not data or 'name' not in data or 'description' not in data:
        return jsonify({'error': 'Faltan datos'}), 400
    
    conexion = get_db_connection()
    if not conexion: return jsonify({'error': 'Error DB'}), 500
    try:
        with conexion.cursor() as cursor:
            cursor.execute(
                "INSERT INTO JUEGOS (name, description, year, image, url, isLocal) VALUES (%s, %s, %s, %s, %s, %s)",
                (data['name'], data['description'], data.get('year'), data.get('image'), data.get('url'), data.get('islocal', False))
            )
            conexion.commit()
        return jsonify({'message': 'Juego añadido'}), 201
    except Exception as e:
        conexion.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        conexion.close()

@app.route('/api/editar_juego/<int:id>', methods=['PUT'])
@admin_required
def editar_juego(id):
    data = request.get_json()
    if not data or 'name' not in data or 'description' not in data:
        return jsonify({'error': 'Faltan datos'}), 400
    
    conexion = get_db_connection()
    if not conexion: return jsonify({'error': 'Error DB'}), 500
    try:
        with conexion.cursor() as cursor:
            cursor.execute(
                "UPDATE JUEGOS SET name=%s, description=%s, year=%s, image=%s, url=%s, isLocal=%s WHERE id=%s",
                (data['name'], data['description'], data.get('year'), data.get('image'), data.get('url'), data.get('islocal', False), id)
            )
            conexion.commit()
            if cursor.rowcount == 0: return jsonify({'error': 'Juego no encontrado'}), 404
        return jsonify({'message': 'Juego actualizado'})
    except Exception as e:
        conexion.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        conexion.close()

@app.route('/api/eliminar_juego/<int:id>', methods=['DELETE'])
@admin_required
def eliminar_juego(id):
    conexion = get_db_connection()
    if not conexion: return jsonify({'error': 'Error DB'}), 500
    try:
        with conexion.cursor() as cursor:
            cursor.execute("DELETE FROM JUEGOS WHERE id = %s", (id,))
            conexion.commit()
            if cursor.rowcount == 0: return jsonify({'error': 'Juego no encontrado'}), 404
        return jsonify({'message': 'Juego eliminado'})
    except Exception as e:
        conexion.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        conexion.close()

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)