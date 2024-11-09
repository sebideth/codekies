import click
from flask import Flask
from colorama import Fore, Style
from sqlalchemy import text

import config
from db import engine_with_no_database


app = Flask(__name__)


@app.cli.command("init-database", help="Initialize the database.")
@click.argument("database", default=config.database)
def init_database(database):
    print(f"[{Fore.GREEN}*{Style.RESET_ALL}] Initializing database...")
    print(f"[{Fore.GREEN}*{Style.RESET_ALL}] Database name {database}")
    try:
        connection = engine_with_no_database().connect()
        print(f"[{Fore.YELLOW}*{Style.RESET_ALL}] Dropping existing database ...")
        connection.execute(text(f"DROP DATABASE IF EXISTS {database}"))
        print(f"[{Fore.YELLOW}*{Style.RESET_ALL}] Creating database ...")
        connection.execute(text(f"CREATE DATABASE {database}"))
        print(f"[{Fore.YELLOW}*{Style.RESET_ALL}] Selecting database ...")
        connection.execute(text(f"USE {database}"))
        # TODO: Se puede mejorar agregando tablas de Raza, Animal
        print(f"[{Fore.YELLOW}*{Style.RESET_ALL}] Creating tables ...")
        connection.execute(text("CREATE TABLE usuarios ("
                                "id INT AUTO_INCREMENT PRIMARY KEY,"
                                "nombreUsuario VARCHAR(100) NOT NULL UNIQUE,"
                                "password VARCHAR(255) NOT NULL,"
                                "nombre VARCHAR(255),"
                                "apellido VARCHAR(255),"
                                "email VARCHAR(255) UNIQUE,"
                                "telefono VARCHAR(20),"
                                "fechaAlta DATETIME NOT NULL)"
                                )
                           )
        connection.execute(text("CREATE TABLE animales ("
                                "id INT AUTO_INCREMENT PRIMARY KEY,"
                                "animal VARCHAR(255) NOT NULL,"
                                "raza VARCHAR(255) NOT NULL,"
                                "condicion VARCHAR(255) NOT NULL,"
                                "color VARCHAR(50),"
                                "ubicacion VARCHAR(255),"
                                "urlFoto VARCHAR(255),"
                                "descripcion TEXT,"
                                "fechaPerdido DATETIME NOT NULL,"
                                "fechaEncontrado DATETIME NOT NULL,"
                                "fechaAlta DATETIME NOT NULL,"
                                "resuelto BOOLEAN DEFAULT FALSE,"
                                "userID INT,"
                                "FOREIGN KEY (userID) REFERENCES usuarios(id))"
                                )
                           )
        print(f"[{Fore.GREEN}*{Style.RESET_ALL}] Created successfully!")
    except Exception as e:
        print(f"[{Fore.RED}*{Style.RESET_ALL}] Could not create database -> {e}")


if __name__ == "__main__":
    app.run("127.0.0.1", port="5001", debug=True)

