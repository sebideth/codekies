from sqlalchemy import create_engine, text
from config import db_username, db_password, db_host, db_collation, db_name

connection_string = f"mysql+mysqlconnector://{db_username}:{db_password}@{db_host}/{db_name}?collation={db_collation}"

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

def engine_with_no_database():
    return create_engine(f"mysql+mysqlconnector://{db_username}:{db_password}@{db_host}?collation={db_collation}",
                         echo=False)
