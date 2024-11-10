import logging

import http.client
from urllib import request

from flask import Flask, abort, request, jsonify
from sqlalchemy import exc

import config
from commands.database import database_cli
from db import INSERT_USER

logger = logging.getLogger(__name__)
app = Flask(__name__)

app.cli.add_command(database_cli)


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

