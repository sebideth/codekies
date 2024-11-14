from db import engine, get_connection, run_query

QUERY_TODOS_LOS_ANIMALES = 'SELECT * FROM animales'

QUERY_ANIMAL_POR_ID = 'SELECT * FROM animales WHERE id = :id'

QUERY_CARGAR_ANIMAL = '''
INSERT INTO animales (animal, raza, condicion, color, ubicacion, urlFoto, descripcion, fechaPerdido, fechaEncontrado, fechaAlta, resuelto, userID)
VALUES (:animal, :raza, :condicion, :color, :ubicacion, :urlFoto, :descripcion, :fechaPerdido, :fechaEncontrado, :fechaAlta, :resuelto, :userID)
'''

QUERY_BORRAR_ANIMAL = 'DELETE FROM animales WHERE id = :id'

COLUMNAS = ['animal', 'raza', 'condicion', 'color', 'ubicacion', 'urlFoto', 'descripcion', 'fechaPerdido', 'fechaEncontrado', 'fechaAlta', 'resuelto', 'userID']

connection = get_connection(engine())

def all_animales():
    return to_dict(run_query(connection, QUERY_TODOS_LOS_ANIMALES).fetchall())

def animal_by_id(id):
    return to_dict(run_query(connection, QUERY_ANIMAL_POR_ID, {'id': id}).fetchall())

def add_animal(datos):
    run_query(connection, QUERY_CARGAR_ANIMAL, datos)

def update_animal(id, datos):
    query = 'UPDATE animales SET'
    for dato in datos:
        query += f' {dato} = :{dato},'
    query = query[:-1] #Saca la ultima coma
    query += ' WHERE id = :id'
    run_query(connection, query, {'id': id, **datos})

def delete_animal(id):
    run_query(connection, QUERY_BORRAR_ANIMAL, {'id': id})

def filter_animal(filtros):
    query = QUERY_TODOS_LOS_ANIMALES
    if len(filtros) > 0:
        query += ' WHERE '
        for filtro in filtros:
            query += f' {filtro} = :{filtro} AND '
        query = query[:-5] #Saca el ultimo AND
    return to_dict(run_query(connection, query, filtros).fetchall())

def validate_all_columns(data):
    for columna in COLUMNAS:
        if columna not in data.keys():
            return False, columna
    return True, ""

def to_dict(data):
    result = []
    for row in data:
        result.append({
            'id':               row[0],
            'animal':           row[1],
            'raza':             row[2],
            'condicion':        row[3],
            'color':            row[4],
            'ubicacion':        row[5],
            'urlFoto':          row[6],
            'descripcion':      row[7],
            'fechaPerdido':     row[8],
            'fechaEncontrado':  row[9],
            'fechaAlta':        row[10],
            'resuelto':         row[11],
            'userID':           row[12],
        })
    return result
