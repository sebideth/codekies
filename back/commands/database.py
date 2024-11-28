import click
from colorama import Fore, Style
from sqlalchemy import text
from flask.cli import AppGroup
import config
from db import engine_with_no_database, engine, run_query
from api.usuarios import INSERTS_USUARIOS_DEFAULT
from api.animales import INSERTS_ANIMALES_DEFAULT

database_cli = AppGroup('database', help='Database related commands')

@database_cli.command("init", help="Initialize the database.")
@click.argument("database", default=config.db_name)
def init_database(database):
    print(f"[{Fore.GREEN}*{Style.RESET_ALL}] Initializing database...")
    print(f"[{Fore.GREEN}*{Style.RESET_ALL}] Database name {database}")
    connection = None
    try:
        connection = engine_with_no_database().connect()
        print(f"[{Fore.YELLOW}*{Style.RESET_ALL}] Dropping existing database ...")
        connection.execute(text(f"DROP DATABASE IF EXISTS {database}"))
        print(f"[{Fore.YELLOW}*{Style.RESET_ALL}] Creating database ...")
        connection.execute(text(f"CREATE DATABASE {database}"))
        print(f"[{Fore.YELLOW}*{Style.RESET_ALL}] Selecting database ...")
        connection.execute(text(f"USE {database}"))
        print(f"[{Fore.YELLOW}*{Style.RESET_ALL}] Creating tables ...")
        connection.execute(text("CREATE TABLE usuarios ("
                                "id INT AUTO_INCREMENT PRIMARY KEY,"
                                "nombreUsuario VARCHAR(100) NOT NULL UNIQUE,"
                                "password VARCHAR(255) NOT NULL,"
                                "nombre VARCHAR(255),"
                                "apellido VARCHAR(255),"
                                "email VARCHAR(255) UNIQUE,"
                                "telefono VARCHAR(20),"
                                "fechaAlta DATETIME NOT NULL DEFAULT NOW())"
                                )
                           )
        connection.execute(text("CREATE TABLE animales ("
                                "id INT AUTO_INCREMENT PRIMARY KEY,"
                                "animal VARCHAR(255) NOT NULL,"
                                "raza VARCHAR(255) DEFAULT NULL,"
                                "condicion VARCHAR(255) NOT NULL,"
                                "color VARCHAR(50),"
                                "zona VARCHAR(255),"
                                "lat VARCHAR(255),"
                                "lng VARCHAR(255),"
                                "urlFoto VARCHAR(255),"
                                "descripcion TEXT,"
                                "fechaPerdido DATE,"
                                "fechaEncontrado DATE,"
                                "fechaAlta DATETIME NOT NULL DEFAULT NOW(),"
                                "resuelto BOOLEAN DEFAULT FALSE,"
                                "userID INT NOT NULL,"
                                "FOREIGN KEY (userID) REFERENCES usuarios(id))"
                                )
                           )
        connection.execute(text("CREATE TABLE usuarios_animales ("
                                "usuario_id INT NOT NULL,"
                                "animal_id INT NOT NULL,"
                                "PRIMARY KEY (usuario_id, animal_id),"
                                "FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE,"
                                "FOREIGN KEY (animal_id) REFERENCES animales(id) ON DELETE CASCADE)"
                                )
                           )
        print(f"[{Fore.GREEN}*{Style.RESET_ALL}] Created successfully!")
    except Exception as e:
        print(f"[{Fore.RED}*{Style.RESET_ALL}] Could not create database -> {e}")
    finally:
        if connection:
            connection.close()

@database_cli.command("build", help="Building the database.")
@click.argument("database", default=config.db_name)
def build_database(database):
    connection = None
    print(f"[{Fore.GREEN}*{Style.RESET_ALL}] Building database...")
    print(f"[{Fore.GREEN}*{Style.RESET_ALL}] Database name {database}")
    try:
        connection = engine.connect()
        print(f"[{Fore.YELLOW}*{Style.RESET_ALL}] Populating tables ...")
        queries = [*INSERTS_USUARIOS_DEFAULT, *INSERTS_ANIMALES_DEFAULT]
        for query in queries:
            run_query(connection, query)
        print(f"[{Fore.GREEN}*{Style.RESET_ALL}] Builded successfully!")
    except Exception as e:
        print(f"[{Fore.RED}*{Style.RESET_ALL}] Could not build database -> {e}")
        return
    finally:
        if connection is not None:
            connection.close()
