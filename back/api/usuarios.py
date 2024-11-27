from db import engine, run_query

QUERY_USUARIO_POR_ID = 'SELECT * FROM usuarios WHERE id = :id'

QUERY_INSERT_USER = '''
INSERT INTO usuarios (nombreUsuario, password, nombre, apellido, email, telefono)
VALUES (:username, :password, :nombre, :apellido, :email, :telefono)
'''

QUERY_LOGIN_USER = 'SELECT * FROM usuarios WHERE nombreUsuario = :username and password = :password'

COLUMNAS_ACTUALIZAR_USUARIO = ['nombre', 'apellido', 'telefono']
QUERY_ACTUALIZAR_USUARIO = f"UPDATE usuarios SET {", ".join([f"{col} = :{col}" for col in COLUMNAS_ACTUALIZAR_USUARIO])}"

INSERTS_USUARIOS_DEFAULT =  [
    '''
    INSERT INTO usuarios (nombreUsuario, password, nombre, apellido, email, telefono)
    VALUES ("test", "test", "Nombre", "Apellido", "email@gmail.com", "111234565");
    ''',
    '''
    INSERT INTO usuarios (nombreUsuario, password, nombre, apellido, email, telefono)
    VALUES ("test2", "test2", "Nombre2", "Apellido2", "email2@gmail.com", "111333333");
    ''',
    '''
    INSERT INTO usuarios (nombreUsuario, password, nombre, apellido, email, telefono)
    VALUES ("test3", "test3", "Nombre3", "Apellido3", "email3@gmail.com", "111333333");'''
]

def usuario_by_id(id):
    try:
        connection = engine().connect()
        result = to_dict(run_query(connection, QUERY_USUARIO_POR_ID, {'id': id}).fetchall())
    finally:
        if connection:
            connection.close()
    return result

def exist_user(id):
    return usuario_by_id(id) != []

def register_user(datos):
    try:
        connection = engine().connect()
        run_query(connection, QUERY_INSERT_USER, datos)
    finally:
        if connection:
            connection.close()

def login_user(datos):
    try:
        connection = engine().connect()
        result = run_query(connection, QUERY_LOGIN_USER, datos).fetchone()
    finally:
        if connection:
            connection.close()
    return result

def update_user(id, datos):
    query = QUERY_ACTUALIZAR_USUARIO
    params = {col: datos.get(col) for col in COLUMNAS_ACTUALIZAR_USUARIO}
    params["id"] = id
    
    password = datos.get("password")
    if password is not None and password.strip() != "":
        query += ", password = :password"
        params["password"] = password
        
    query += ' WHERE id = :id'
    try:
        connection = engine().connect()
        run_query(connection, query, params)
    finally:
        if connection:
            connection.close()

def validate_all_columns(data):
    for columna in COLUMNAS_ACTUALIZAR_USUARIO:
        if columna not in data.keys():
            return False, columna
    return True, ""

def to_dict(data):
    result = []
    for row in data:
        result.append({
            'id':           row[0],
            'username':     row[1],
            'nombre':       row[3],
            'apellido':     row[4],
            'email':        row[5],
            'telefono':     row[6]
        })
    return result
