from db import engine, run_query
from datetime import datetime

QUERY_TODOS_LOS_ANIMALES = 'SELECT * FROM animales'

QUERY_ANIMAL_POR_ID = 'SELECT * FROM animales WHERE id = :id'

QUERY_CARGAR_ANIMAL = '''
INSERT INTO animales (animal, raza, condicion, color, direccion, urlFoto, descripcion, fechaPerdido, fechaEncontrado, userID)
VALUES (:animal, :raza, :condicion, :color, :direccion, :urlFoto, :descripcion, :fechaPerdido, :fechaEncontrado, :userID)
'''

QUERY_CARGAR_ANIMAL_ENCONTRADO = '''
INSERT INTO usuarios_animales (animal_id, usuario_id) VALUES (:animal_id, :usuario_id)
'''


QUERY_BORRAR_ANIMAL = 'DELETE FROM animales WHERE id = :id'

QUERY_ULTIMOS_N_ANIMALES = 'SELECT * FROM animales ORDER BY id DESC LIMIT :n'

COLUMNAS_REQUERIDAS = ['animal', 'condicion', 'color', 'direccion', 'urlFoto', 'descripcion', 'fechaPerdido', 'fechaEncontrado']

COLUMNAS_FILTRO = ['animal', 'raza', 'condicion', 'color', 'fechaPerdido', 'fechaEncontrado', 'resuelto']

INSERTS_ANIMALES_DEFAULT = [
    '''
    INSERT INTO animales (animal, raza, condicion, color, direccion, urlFoto, descripcion, fechaPerdido, fechaEncontrado, userID)
    VALUES ("Perro", "Chihuahua", "Perdido", "Blanco", "Avenida Paseo Colón 805, San Telmo, C1100 AAC Buenos Aires, Argentina", "/static/images/imagenes_mascotas/chihuahua.jpg", "Es muy simpaticón, responde al nombre Pepito", "2024-11-23", null, 1);
    ''',
    '''
    INSERT INTO animales (animal, raza, condicion, color, direccion, urlFoto, descripcion, fechaPerdido, fechaEncontrado, userID)
    VALUES ("Perro", "Desconocida", "Encontrado sin dueño", "Marron claro", "Villa Devoto, Buenos Aires, Argentina", "/static/images/imagenes_mascotas/doge.png", "Cara de meme", null, "2024-06-11", 1);
    ''',
    '''
    INSERT INTO animales (animal, raza, condicion, color, direccion, urlFoto, descripcion, fechaPerdido, fechaEncontrado, userID)
    VALUES ("Gato", "Desconocida", "Encontrado sin dueño", "Negro", "UBA Facultad de Ingeniería, Avenida Paseo Colón 850, San Telmo, C1100 AAC Buenos Aires, Argentina", "/static/images/imagenes_mascotas/gato.jpg", "Gato negro", null, "2024-06-11", 2);
    ''',
    '''
    INSERT INTO animales (animal, raza, condicion, color, direccion, urlFoto, descripcion, fechaPerdido, fechaEncontrado, userID)
    VALUES ("Gato", "Siames", "Perdido", "Marron claro", "General San Martín, B, Argentina", "/static/images/imagenes_mascotas/grumpy.jpeg", "No se lo ve muy contento", "2024-01-22", null, 3);
    '''
]

def all_animales():
    try:
        connection = engine().connect()
        result = to_dict(run_query(connection, QUERY_TODOS_LOS_ANIMALES).fetchall())
    finally:
        if connection:
            connection.close()
    return result

def last_n_animales(n):
    try:
        connection = engine().connect()
        result = to_dict(run_query(connection, QUERY_ULTIMOS_N_ANIMALES, {'n': n}).fetchall())
    finally:
        if connection:
            connection.close()
    return result

def animal_by_id(id):
    try:
        connection = engine().connect()
        result = to_dict(run_query(connection, QUERY_ANIMAL_POR_ID, {'id': id}).fetchall())
    finally:
        if connection:
            connection.close()
    return result

def add_animal(datos, user_id):
    try:
        connection = engine().connect()
        datos["userID"] = user_id
        run_query(connection, QUERY_CARGAR_ANIMAL, datos)
    finally:
        if connection:
            connection.close()


def add_animal_encontrado(datos, user_id):
    with engine().connect() as connection:
        datos["usuario_id"] = user_id
        run_query(connection, QUERY_CARGAR_ANIMAL_ENCONTRADO, datos)


def update_animal(id, datos):
    try:
        connection = engine().connect()
        query = 'UPDATE animales SET'
        for dato in datos:
            query += f' {dato} = :{dato},'
        query = query[:-1] #Saca la ultima coma
        query += ' WHERE id = :id'
        run_query(connection, query, {'id': id, **datos})
    finally:
        if connection:
            connection.close()

def delete_animal(id):
    try:
        connection = engine().connect()
        run_query(connection, QUERY_BORRAR_ANIMAL, {'id': id})
    finally:
        if connection:
            connection.close()

def filter_animal(filtros):
    try:
        connection = engine().connect()
        query = QUERY_TODOS_LOS_ANIMALES
        print(filtros)
        if len(filtros) > 0:
            query += ' WHERE '
            for filtro in filtros:
                query += f' {filtro} = :{filtro} AND '
            query = query[:-5] #Saca el ultimo AND
        result = to_dict(run_query(connection, query, filtros).fetchall())
    finally:
        if connection:
            connection.close()
    return result

def datos_animales():
    try:
        connection = engine().connect()
        datos_unicos = {}
        for columna in COLUMNAS_FILTRO:
            query = f"SELECT DISTINCT {columna} FROM animales"
            try:
                datos_unicos[columna] = to_dict_filtro(run_query(connection, query).fetchall(), columna)
            except Exception as e:
                print(f"Error al obtener datos unicos para '{columna}': {e}")
                datos_unicos[columna] = []
    finally:
        if connection:
            connection.close()
    return datos_unicos

def exist_animal(id):
    return animal_by_id(id) != []

def validate_all_columns(data):
    for columna in COLUMNAS_REQUERIDAS:
        if columna not in data.keys():
            return False, columna
    return True, ""

def validate_user_owner(animal_id, user_id):
    return animal_by_id(animal_id)[0]['userID'] == user_id

def to_dict(data):
    result = []
    for row in data:
        result.append({
            'id':               row[0],
            'animal':           row[1],
            'raza':             row[2],
            'condicion':        row[3],
            'color':            row[4],
            'direccion':        row[5],
            'urlFoto':          row[6],
            'descripcion':      row[7],
            'fechaPerdido':     row[8].strftime('%Y-%m-%d') if row[8] else row[8],
            'fechaEncontrado':  row[9].strftime('%Y-%m-%d') if row[9] else row[9],
            'fechaAlta':        row[10],
            'resuelto':         bool(row[11]),
            'userID':           row[12]
        })
    return result

def to_dict_filtro(data, columna):
    result = []
    for row in data:
        value = row[0]
        if not value:
            continue
        if columna == 'fechaPerdido' or columna == 'fechaEncontrado':
            value = value.strftime('%Y-%m-%d')
        result.append(value)
    return result
