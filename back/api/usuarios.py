from db import engine, get_connection, run_query

QUERY_USUARIO_POR_ID = 'SELECT * FROM usuarios WHERE id = :id'

COLUMNAS_ACTUALIZAR = ['nombre', 'apellido', 'telefono', 'password']

connection = get_connection(engine())

def usuario_by_id(id):
    return to_dict(run_query(connection, QUERY_USUARIO_POR_ID, {'id': id}).fetchall())

def exist_user(id):
    return run_query(connection, QUERY_USUARIO_POR_ID, {'id': id}).fetchall() != []

def update_user(id, datos):
    query = 'UPDATE usuarios SET'
    for dato in datos:
        query += f' {dato} = :{dato},'
    query = query[:-1]
    query += ' WHERE id = :id'
    run_query(connection, query, {'id': id, **datos})

def validate_all_columns(data):
    for columna in COLUMNAS_ACTUALIZAR:
        if columna not in data.keys():
            return False, columna
    return True, ""

def to_dict(data):
    result = []
    for row in data:
        result.append({
            'id':               row[0],
            'username':           row[1],
            'nombre':        row[3],
            'apellido':            row[4],
            'email':        row[5],
            'telefono':          row[6],
        })
    return result
