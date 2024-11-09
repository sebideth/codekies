import logging

import http.client
from urllib import request

import click
from flask import Flask, abort, request, jsonify
from colorama import Fore, Style
from sqlalchemy import text, exc

import config
from db import engine_with_no_database, engine, INSERT_USER

logger = logging.getLogger(__name__)
app = Flask(__name__)


# Commands
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
                                "fechaAlta DATETIME NOT NULL DEFAULT NOW())"
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
                                "fechaAlta DATETIME NOT NULL DEFAULT NOW(),"
                                "resuelto BOOLEAN DEFAULT FALSE,"
                                "userID INT,"
                                "FOREIGN KEY (userID) REFERENCES usuarios(id))"
                                )
                           )
        print(f"[{Fore.GREEN}*{Style.RESET_ALL}] Created successfully!")
    except Exception as e:
        print(f"[{Fore.RED}*{Style.RESET_ALL}] Could not create database -> {e}")

# API


# Users
@app.route("/register", methods=["POST"])
def register():
    validate_fields = ['username', 'password', 'email', 'telefono', 'nombre', 'apellido']
    user_data = request.get_json()
    for key in validate_fields:
        if key not in user_data:
            return jsonify({'error': f'Keys obligatorias {validate_fields}'}), http.client.BAD_REQUEST
    with engine.connect() as connection:
        try:
            connection.execute(INSERT_USER, user_data)
            connection.commit()
        except exc.IntegrityError as error:
            logger.error(f"Could not create user {user_data.get('username')}. {error}")
            return jsonify({"error": "Usuario o email existentes"}), http.client.BAD_REQUEST
    return jsonify({"message": "Usuario creado correctamente"}), http.client.CREATED


if __name__ == "__main__":
    app.run("127.0.0.1", port=5001, debug=config.debug)

