import click
from flask import Flask
from colorama import init
from colorama import Fore, Style
from sqlalchemy import text
from db import engine


app = Flask(__name__)


@app.cli.command("init-database", help="Initialize the database.")
@click.argument("host", default="localhost")
@click.argument("username", default="root")
@click.argument("password", default="change_me")
@click.argument("database", default="codekis")
def init_database(host, username, password, database):
    print(f"[{Fore.GREEN}*{Style.RESET_ALL}] Initializing database...")
    print(f"[{Fore.GREEN}*{Style.RESET_ALL}] Username -> {username}")
    print(f"[{Fore.GREEN}*{Style.RESET_ALL}] Password -> {password}")
    print(f"[{Fore.GREEN}*{Style.RESET_ALL}] Host -> {host}")
    try:
        connection = engine.connect()
        connection.execute(text(f"DROP DATABASE {database}"))
        connection.execute(text(f"CREATE DATABASE {database}"))
        connection.execute(text(f"USE {database}"))
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
        # TODO: Se puede mejorar agregando tablas de Raza, Animal
    except Exception as e:
        print(e)


if __name__ == "__main__":
    app.run("127.0.0.1", port="5001", debug=True)

