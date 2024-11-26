import logging

import http.client
from urllib import request

from flask import (
    Flask,
    request,
    jsonify,
    session,
)
from sqlalchemy import exc
from utils.decorators import login_required
import config
from commands.database import database_cli
from api import animales, usuarios

logger = logging.getLogger(__name__)
app = Flask(__name__)
app.secret_key = 'super secret key'
app.cli.add_command(database_cli)

LOG_ERROR_QUERY = "Error al correr la query: "
ERROR_INESPERADO = "Error inesperado."
ERROR_USUARIO_NO_ENCONTRADRO = "Usuario no encontrado"

# Animales
@app.route('/api/animales', methods=['GET'])
def get_all_animales():
    try:
        result = animales.all_animales()
    except Exception as error:
        logger.error(LOG_ERROR_QUERY + 'animales.all_animales' + str(error))
        return jsonify({"error": ERROR_INESPERADO}), http.client.INTERNAL_SERVER_ERROR
    return jsonify(result), http.client.OK

@app.route('/api/animales/ultimos/<int:n>', methods=['GET'])
def get_last_n_animales(n):
    try:
        result = animales.last_n_animales(n)
    except Exception as error:
        logger.error(LOG_ERROR_QUERY + 'animales.last_n_animales' + str(error))
        return jsonify({"error": ERROR_INESPERADO}), http.client.INTERNAL_SERVER_ERROR
    return jsonify(result), http.client.OK

@app.route('/api/animales/<int:id>', methods=['GET'])
def get_animal_by_id(id):
    try:
        if not animales.exist_animal(id):
            return jsonify({'error': 'No se encontró al animal.'}), http.client.NOT_FOUND
        result = animales.animal_by_id(id)
    except Exception as error:
        logger.error(LOG_ERROR_QUERY + 'animales.animal_by_id' + str(error))
        return jsonify({"error": ERROR_INESPERADO}), http.client.INTERNAL_SERVER_ERROR
    return jsonify(result[0]), http.client.OK

@app.route('/api/animales', methods=['POST'])
@login_required
def add_animal():
    datos = request.get_json()
    is_valid, column = animales.validate_all_columns(datos)
    if not is_valid:
        return jsonify({'error': f'Falta el dato {column}'}), http.client.BAD_REQUEST
    try:
        animales.add_animal(datos, session["user_id"])
    except Exception as error:
        logger.error(LOG_ERROR_QUERY + 'animales.add_animal' + str(error))
        return jsonify({"error": ERROR_INESPERADO}), http.client.INTERNAL_SERVER_ERROR
    return jsonify(datos), http.client.CREATED

@app.route('/api/animales/<int:id>', methods=['PUT'])
@login_required
def update_animal(id):
    datos = request.get_json()
    try:
        animales.update_animal(id,datos)
        if not animales.validate_user_owner(id, session['user_id']):
            return jsonify({'error': 'Esta publicación no pertenece al usuario'}), http.client.FORBIDDEN
    except Exception as error:
        logger.error(LOG_ERROR_QUERY + 'animales.update_animal' + str(error))
        return jsonify({"error": ERROR_INESPERADO}), http.client.INTERNAL_SERVER_ERROR
    return jsonify(animales.animal_by_id(id)), http.client.OK

@app.route('/api/animales/<int:id>', methods=['DELETE'])
@login_required
def delete_animal(id):
    try:
        if not animales.exist_animal(id):
            return jsonify({'error': 'No se encontró al animal.'}), http.client.NOT_FOUND
        if not animales.validate_user_owner(id, session['user_id']):
            return jsonify({'error': 'Esta publicación no pertenece al usuario'}), http.client.FORBIDDEN
        animales.delete_animal(id)
    except Exception as error:
        logger.error(LOG_ERROR_QUERY + 'animales.delete_animal' + str(error))
        return jsonify({"error": ERROR_INESPERADO}), http.client.INTERNAL_SERVER_ERROR
    return jsonify({"message": "Publicación eliminada con éxito"}), http.client.OK

@app.route('/api/animales/buscar', methods=['GET'])
def search_animales():
    datos = request.get_json()
    try:
        result = animales.filter_animal(datos)
    except Exception as error:
        logger.error(LOG_ERROR_QUERY + 'animales.filter_animal' + str(error))
        return jsonify({"error": ERROR_INESPERADO}), http.client.INTERNAL_SERVER_ERROR
    return jsonify(result), http.client.OK

@app.route('/api/animales/usuario', methods=['GET'])
@login_required
def get_all_animales_from_usuario():
    try:
        result = animales.filter_animal({'userID': session["user_id"]})
    except Exception as error:
        logger.error(LOG_ERROR_QUERY + 'animales.filter_animal' + str(error))
        return jsonify({"error": ERROR_INESPERADO}), http.client.INTERNAL_SERVER_ERROR
    return jsonify(result), http.client.OK

@app.route('/api/animales/datos', methods=['GET'])
def datos_animales_():
    try:
        result = animales.datos_animales()
    except Exception as error:
        logger.error(LOG_ERROR_QUERY + 'animales.datos_animales' + str(error))
        return jsonify({"error": ERROR_INESPERADO}), http.client.INTERNAL_SERVER_ERROR
    return jsonify(result),http.client.OK

# Users
@app.route("/api/register", methods=["POST"])
def register():
    validate_fields = ['username', 'password', 'email', 'telefono', 'nombre', 'apellido']
    user_data = request.get_json()
    for key in validate_fields:
        if key not in user_data:
            logger.error(f"Keys obligatorias {validate_fields}")
            return jsonify({"error": "Error al registrar usuario."}), http.client.BAD_REQUEST
    try:
        usuarios.register_user(user_data)
    except exc.IntegrityError as error:
        logger.error(f"No se pudo crear el usuario {user_data.get('username')}. {error}")
        return jsonify({"error": "Usuario o email existentes"}), http.client.BAD_REQUEST
    except Exception as error:
        logger.error(LOG_ERROR_QUERY + 'animales.datos_animales' + str(error))
        return jsonify({"error": ERROR_INESPERADO}), http.client.INTERNAL_SERVER_ERROR
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
            logger.error(f"Keys obligatorias {validate_fields}")
            return jsonify({"error": "Error al iniciar sesión."}), http.client.BAD_REQUEST
    try:
        user = usuarios.login_user(user_data)
        if not user:
            return jsonify({'error': 'Usuario o Password invalidos'}), http.client.FORBIDDEN
        session["logged_in"] = True
        session["user_id"] = user.id
    except Exception as error:
        logger.error(f"Could not fetch user {user_data.get('username')}. {error}")
        return jsonify({"error": "Error al iniciar sesión."}), http.client.INTERNAL_SERVER_ERROR
    return jsonify({"message": "Bienvenido!"}), http.client.OK

@app.route('/api/usuarios/login')
def is_logged_in():
    if session.get('logged_in'):
        return jsonify({"message": "Usuario loggeado"}), http.client.OK
    return jsonify({"message": "No hay usuario loggeado"}), http.client.BAD_REQUEST

@app.route("/api/logout", methods=["GET"])
def logout():
    session.clear()
    return jsonify({"message": "Bye"}), http.client.OK

@app.route('/api/usuarios/<int:id>', methods=['PUT'])
@login_required
def update_user(id):
    if not usuarios.exist_user(id):
        return jsonify({'error': ERROR_USUARIO_NO_ENCONTRADRO}), http.client.NOT_FOUND
    datos = request.get_json()
    is_valid, column = usuarios.validate_all_columns(datos)
    if not is_valid:
        logger.error(f"{column} no puede ser null")
        return jsonify({'error': "Error al actualizar tus datos."}), http.client.BAD_REQUEST
    try:
        usuarios.update_user(id,datos)
    except Exception as e:
        return jsonify({'error': ERROR_INESPERADO}), http.client.INTERNAL_SERVER_ERROR
    return jsonify(usuarios.usuario_by_id(id)), http.client.OK

@app.route('/api/usuarios/<int:id>', methods=['GET'])
@login_required
def get_user(id):
    if not usuarios.exist_user(id):
        return jsonify({'error': ERROR_USUARIO_NO_ENCONTRADRO}), http.client.NOT_FOUND
    return jsonify(usuarios.usuario_by_id(id)[0]), http.client.OK


if __name__ == "__main__":
    app.run("127.0.0.1", port=5001, debug=config.debug)
