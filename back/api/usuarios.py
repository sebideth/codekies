from db import engine, run_query

QUERY_USUARIO_POR_ID = 'SELECT * FROM usuarios WHERE id = :id'

QUERY_INSERT_USER = '''
INSERT INTO usuarios (nombreUsuario, password, nombre, apellido, email, telefono)
VALUES (:username, :password, :nombre, :apellido, :email, :telefono)
'''

QUERY_LOGIN_USER = 'SELECT * FROM usuarios WHERE nombreUsuario = :username and password = :password'

COLUMNAS_ACTUALIZAR_USUARIO = ['nombre', 'apellido', 'telefono']
QUERY_ACTUALIZAR_USUARIO = f'UPDATE usuarios SET {", ".join([f"{col} = :{col}" for col in COLUMNAS_ACTUALIZAR_USUARIO])}'

INSERTS_USUARIOS_DEFAULT =  [
    '''
    INSERT INTO usuarios (nombreUsuario, password, nombre, apellido, email, telefono)
    VALUES ("test", "test", "Pedro", "Perez", "fdarias@fi.uba.ar", "111234565");
    ''',
    '''
    INSERT INTO usuarios (nombreUsuario, password, nombre, apellido, email, telefono)
    VALUES ("test2", "test2", "Maria", "Lopez", "dnadares@fi.uba.ar", "111333333");
    ''',
    '''
    INSERT INTO usuarios (nombreUsuario, password, nombre, apellido, email, telefono)
    VALUES ("test3", "test3", "Juan", "Gomez", "mcmena@fi.uba.ar", "111333333");'''
]

QUERY_CARGAR_DATOS_USUARIO_MASCOTA_ENCONTRADA = '''
select animales.animal, animales.raza, animales.urlFoto, animales.descripcion, animales.id, usuarios.nombre, usuarios.apellido, usuarios.email 
From usuarios_animales, usuarios, animales 
where animal_id in (
select id from animales where userID=:usuario_id
) and usuario_id = usuarios.id and animal_id = animales.id  
'''

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


def get_my_founded_pets(user_id):
    with engine().connect() as connection:
        result = pet_found_to_dict(run_query(connection, QUERY_CARGAR_DATOS_USUARIO_MASCOTA_ENCONTRADA, {'usuario_id': user_id}))
        return result


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


def pet_found_to_dict(data):
    result = []
    for row in data:
        result.append({
            'animal': row[0],
            'raza': row[1],
            'fotoUrl': row[2],
            'descripcion': row[3],
            'animal_id': row[4],
            'nombre_usuario': row[5],
            'apellido_usuario': row[6],
            'email_usuario': row[7]
        })
    return result
