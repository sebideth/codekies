from db import engine, run_query

QUERY_TODOS_LOS_ANIMALES = 'SELECT * FROM animales'

QUERY_ANIMAL_POR_ID = 'SELECT * FROM animales WHERE id = :id'

QUERY_CARGAR_ANIMAL = '''
INSERT INTO animales (animal, raza, condicion, color, direccion, ciudad, urlFoto, descripcion, fechaPerdido, fechaEncontrado, userID)
VALUES (:animal, :raza, :condicion, :color, :direccion, :ciudad, :urlFoto, :descripcion, :fechaPerdido, :fechaEncontrado, :userID)
'''

QUERY_BORRAR_ANIMAL = 'DELETE FROM animales WHERE id = :id'

COLUMNAS_REQUERIDAS = ['animal', 'condicion', 'color', 'direccion', 'ciudad', 'urlFoto', 'descripcion', 'fechaPerdido', 'fechaEncontrado']

COLUMNAS_FILTRO = ['animal', 'raza', 'condicion', 'color', 'ciudad', 'fechaPerdido', 'fechaEncontrado', 'resuelto']

def all_animales():
    try:
        connection = engine().connect()
        result = to_dict(run_query(connection, QUERY_TODOS_LOS_ANIMALES).fetchall())
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
                datos_unicos[columna] = to_dict_filtro(run_query(connection, query).fetchall())
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
            'ciudad':           row[6],
            'urlFoto':          row[7],
            'descripcion':      row[8],
            'fechaPerdido':     row[9],
            'fechaEncontrado':  row[10],
            'fechaAlta':        row[11],
            'resuelto':         bool(row[12]),
            'userID':           row[13]
        })
    return result

def to_dict_filtro(data):
    result = []
    for row in data:
        result.append(row[0])
    return result

