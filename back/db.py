from sqlalchemy import create_engine, text
from config import username, password, host, collation, database

connection_string = f"mysql+mysqlconnector://{username}:{password}@{host}/{database}?collation={collation}"

engine = create_engine(connection_string, echo=False)

# Usuarios
INSERT_USER = text("INSERT INTO usuarios ("
              "nombreUsuario,"
              "password,"
              "nombre, "
              "apellido,"
              "email,"
              "telefono"
              ") VALUES ("
              ":username, "
              ":password, "
              ":nombre,"
              ":apellido,"
              ":email,"
              ":telefono)")

LOGIN_USER_QUERY = text("SELECT * FROM usuarios WHERE nombreUsuario = :username and password = :password")

def engine_with_no_database():
    connection_string = f"mysql+mysqlconnector://{username}:{password}@{host}?collation={collation}"
    return create_engine(connection_string, echo=False)
