import psycopg2
import os
from werkzeug.security import generate_password_hash, check_password_hash

############ DEFINIMOS LA BASE DE DATOS ############

def get_db_connection():

    database_url = os.environ.get('DATABASE_URL')
    
    try:
        if database_url:

            print("Conectando a la BBDD de la Nube...")
            return psycopg2.connect(database_url)
        else:

            print("Conectando a la BBDD Local...")
            return psycopg2.connect(
                host="localhost",
                port="5432",
                database="semana2",
                user="postgres",
                password=""
            )
    except Exception as e:
        print(f"Error crítico de conexión: {e}")
        exit(1)


conexion = get_db_connection()

try:
    with conexion.cursor() as cursor:
        print("Borrando tablas antiguas...")
        cursor.execute('DROP TABLE IF EXISTS JUEGOS')
        cursor.execute('DROP TABLE IF EXISTS USUARIOS')

        print("Creando tabla JUEGOS...")
        cursor.execute('''
            CREATE TABLE JUEGOS (
                id SERIAL PRIMARY KEY, 
                name VARCHAR(255) NOT NULL,
                description TEXT,
                year INTEGER,
                image TEXT,
                url TEXT,
                isLocal BOOLEAN DEFAULT false
                );
            ''')
        
        print("Insertando datos de juegos...")
        cursor.execute(
            '''    
            INSERT INTO JUEGOS (name, description, year, image, url, isLocal)
            VALUES
            (
            'La Serpiente',
            'Consigue comer tosas las manzanas que puedas sin chocarte con las paredes ni contigo mismo.',
            1970,
            'https://www5.minijuegosgratis.com/v3/games/thumbnails/246309_1.jpg',
            'https://es.wikipedia.org/wiki/La_serpiente_(videojuego)',
            false
            ),
            (
            'PacMan',
            'Clásico arcade donde guías a una bola amarilla para comer puntos y esquivar fantasmas en un laberinto.',
            1980,
            'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTcwYQ8aUGsRRyHOV47MD50N700tSYO_PGTRQ&s',
            'https://es.wikipedia.org/wiki/Pac-Man',
            false
            ),
            (
            'Batalla Naval',
            'Juego estratégico donde colocas barcos y tratas de adivinar las posiciones del enemigo para hundir su flota antes que la tuya.',
            1931,
            'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQHPifWn7MH0c9f38wA1KwpTZR0LBwca5ItjQ&s',
            'https://es.wikipedia.org/wiki/Videojuego_de_estrategia',
            false
            ),
            (
            'Busca Minas',
            'Juego de lógica donde debes descubrir celdas vacías evitando detonar las minas ocultas en el tablero.',
            1990,
            'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQyt9aXYvIMfazAG4s8MrF9l7TcHEuvm60WQA&s',
            'https://es.wikipedia.org/wiki/Buscaminas',
            false
            ),
            (
            'Tetris',
            'Juego clásico de ingenio donde encajas piezas de distintas formas para completar y eliminar líneas sin llenar la pantalla.',
            1984,
            'https://cdn-icons-png.flaticon.com/512/1138/1138876.png',
            'https://es.wikipedia.org/wiki/Tetris',
            false
            ),
            (
            'Tres en Raya',
            'Clásico juego de tres en raya contra otro jugador. Haz tu jugada y gana la partida.',
            2025,
            'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTki6sw_Oh_xQiXXDrVSUJcHrvMIXvgemlW7Q&s',
            NULL,
            true
            )''')
        
        print("Creando tabla USUARIOS...")
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS USUARIOS (
                NOMBRE TEXT PRIMARY KEY,
                PASSWORD_HASH TEXT NOT NULL
            )
        ''')
        
        print("Creando usuario admin...")
        contraseña_admin = generate_password_hash('admin_2025')
        cursor.execute(
            "INSERT INTO USUARIOS (NOMBRE, PASSWORD_HASH) VALUES (%s, %s)",
            ('admin', contraseña_admin)
        )
        conexion.commit()
        print("¡Base de datos inicializada con éxito!")

except Exception as e:
    print("Ocurrió un error:", e)
finally:
    if conexion:
        conexion.close()