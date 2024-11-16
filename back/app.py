import logging

import http.client
from urllib import request

from flask import (
    Flask,
    abort,
    request,
    jsonify,
    session,
)
from sqlalchemy import exc

import config
from commands.database import database_cli
from db import (
    INSERT_USER,
    engine,
    LOGIN_USER_QUERY
)

logger = logging.getLogger(__name__)
app = Flask(__name__)
app.secret_key = 'super secret key'

app.cli.add_command(database_cli)


# Users
@app.route("/register", methods=["POST"])
def register():
    validate_fields = ['username', 'password', 'email', 'telefono', 'nombre', 'apellido']
    user_data = request.get_json()
    for key in validate_fields:
        if key not in user_data:
            return jsonify({'error': f'Keys obligatorias {validate_fields}'}), http.client.BAD_REQUEST

    try:
        connection = engine.connect()
    except exc.DatabaseError as error:
        logger.error(f"No pudimos conectarnos a la base de datos. {error}")
        return jsonify({'error': 'Hubo un error al obtener tus datos :('}), http.client.INTERNAL_SERVER_ERROR

    try:
        connection.execute(INSERT_USER, user_data)
        connection.commit()
    except exc.IntegrityError as error:
        logger.error(f"Could not create user {user_data.get('username')}. {error}")
        return jsonify({"error": "Usuario o email existentes"}), http.client.BAD_REQUEST
    finally:
        connection.close()

    return jsonify({"message": "Usuario creado correctamente"}), http.client.CREATED


@app.route("/login", methods=["POST"])
def login():

    if session.get('logged_in'):
        return jsonify({'error': 'Ya estabas loggeado ...'}), http.client.BAD_REQUEST

    validate_fields = ['username', 'password']
    user_data = request.get_json()
    for key in validate_fields:
        if key not in user_data:
            return jsonify({'error': f'Keys obligatorias {validate_fields}'}), http.client.BAD_REQUEST

    try:
        connection = engine.connect()
    except exc.DatabaseError as error:
        logger.error(f"No pudimos conectarnos a la base de datos. {error}")
        return jsonify({'error': 'Hubo un error al obtener tus datos :('}), http.client.INTERNAL_SERVER_ERROR

    try:
        user = connection.execute(LOGIN_USER_QUERY, user_data).fetchone()
        if not user:
            return jsonify({'error': 'Usuario o Password invalidos'}), http.client.FORBIDDEN
        session["logged_in"] = True
        session["user_id"] = user.id
    except Exception as error:
        logger.error(f"Could not fetch user {user_data.get('username')}. {error}")
        return jsonify({"error": "Usuario o email existentes"}), http.client.INTERNAL_SERVER_ERROR
    finally:
        connection.close()
    return jsonify({"message": "Login exitoso"}), http.client.OK


@app.route("/logout", methods=["GET"])
def logout():
    session.clear()
    return jsonify({"message": "Bye"}), http.client.OK


if __name__ == "__main__":
    app.run("127.0.0.1", port=5001, debug=config.debug)

