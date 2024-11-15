from flask import Flask, jsonify, request

from commands.database import database_cli
from api import animales

app = Flask(__name__)

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

if __name__ == "__main__":
    app.run("127.0.0.1", port=5001, debug=True)

