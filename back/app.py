import logging

import http.client
from functools import wraps
from urllib import request

from flask import (
    Flask,
    request,
    jsonify,
    session,
)
from sqlalchemy import exc

import config
from commands.database import database_cli
from api import animales
from db import (
    INSERT_USER,
    engine,
    LOGIN_USER_QUERY
)

logger = logging.getLogger(__name__)
app = Flask(__name__)
app.secret_key = 'super secret key'

app.cli.add_command(database_cli)

# Animales

@app.route('/api/animales', methods=['GET'])
def get_all_animales():
    try:
        result = animales.all_animales()
    except Exception as e:
        #Cambiar mensaje de error para no mostrar errores de la DB
        return jsonify({'error': str(e)}), 500
    return jsonify(result), 200

@app.route('/api/animales/<int:id>', methods=['GET'])
def get_animal_by_id(id):
    try:
        result = animales.animal_by_id(id)
    except Exception as e:
        #Cambiar mensaje de error para no mostrar errores de la DB
        return jsonify({'error': str(e)}), 500
    if len(result) == 0:
        return jsonify({'error': 'No se encontró al animal.'}), 404
    return jsonify(result), 200

@app.route('/api/animales', methods=['POST'])
def add_animal():
    datos = request.get_json()
    is_valid, column = animales.validate_all_columns(datos)
    if not is_valid:
        return jsonify({'error': f'Falta el dato {column}'}), 400
    try:
        animales.add_animal(datos)
    except Exception as e:
        #Cambiar mensaje de error para no mostrar errores de la DB
        return jsonify({'error': str(e)}), 500
    return jsonify(datos), 201

@app.route('/api/animales/<int:id>', methods=['PUT'])
def update_animal(id):
    datos = request.get_json()
    is_valid, column = animales.validate_all_columns(datos)
    try:
        animales.update_animal(id,datos)
    except Exception as e:
        #Cambiar mensaje de error para no mostrar errores de la DB
        return jsonify({'error': str(e)}), 500
    return jsonify(animales.animal_by_id(id)), 200

@app.route('/api/animales/<int:id>', methods=['DELETE'])
def delete_animal(id):
    try:
        result = animales.animal_by_id(id)   
        animales.delete_animal(id)
        if len(result) == 0:
            return jsonify({'error': 'No se encontró al animal.'}), 404
    except Exception as e:
        #Cambiar mensaje de error para no mostrar errores de la DB
        return jsonify({'error': str(e)}), 500
    return jsonify(result), 200

@app.route('/api/animales/buscar', methods=['GET'])
def search_animales():
    datos = request.get_json()
    try:
        result = animales.filter_animal(datos)
    except Exception as e:
        #Cambiar mensaje de error para no mostrar errores de la DB
        return jsonify({'error': str(e)}), 500
    return jsonify(result), 200

@app.route('/api/animales/usuario/<int:id>', methods=['GET'])
def get_all_animales_from_usuario(id):
    try:
        #Verificar si el usuario existe
        result = animales.filter_animal({'userID': id})
    except Exception as e:
        #Cambiar mensaje de error para no mostrar errores de la DB
        return jsonify({'error': str(e)}), 500
    return jsonify(result), 200


def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if session.get('logged_in') is None:
            return jsonify({'message': 'Para usar este recurso es necesario estar loggeado.'}), 401
        return func(*args, **kwargs)
    return wrapper


# Users
@app.route("/api/register", methods=["POST"])
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
    user_data.pop("password")
    return jsonify(user_data), http.client.CREATED


@app.route("/api/login", methods=["POST"])
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
    return jsonify({"message": "Bienvenido!"}), http.client.OK


@app.route("/api/logout", methods=["GET"])
def logout():
    session.clear()
    return jsonify({"message": "Bye"}), http.client.OK


if __name__ == "__main__":
    app.run("127.0.0.1", port=5001, debug=config.debug)

