import os
from flask import Flask, redirect, render_template, url_for, request, session, abort, jsonify
from werkzeug import exceptions
import requests

app = Flask(__name__)
app.secret_key = 'sarasa'

@app.route('/')
def home():
    try:
        animales_response = requests.get('http://localhost:5001/api/animales/ultimos/3')
        animales_response.raise_for_status()
        animales = animales_response.json()
    except requests.exceptions.RequestException as e:
        print(f"e: {e}")
        animales = []
    return render_template('index.html', animales=animales, is_logged_in = is_logged_in())

@app.route('/pets')
def pets():
    try:
        datos_filtro_response = requests.get('http://localhost:5001/api/animales/datos')
        datos_filtro_response.raise_for_status()
        datos_filtro = datos_filtro_response.json()
    except requests.exceptions.RequestException as e:
        print(f"error al obtener los datos de animales: {e}")
        datos_filtro = []

    try:
        animales_response = requests.get('http://localhost:5001/api/animales')
        animales_response.raise_for_status()
        animales = animales_response.json()
    except requests.exceptions.RequestException as e:
        print(f"error al obtener animales: {e}")
        animales = []

    return render_template('pets.html', animales=animales, datos_filtro=datos_filtro, is_logged_in = is_logged_in())

@app.route('/pets/search', methods=['GET','POST'])
def pets_search():
    try:
        datos_filtro_response = requests.get('http://localhost:5001/api/animales/datos')
        datos_filtro_response.raise_for_status()
        datos_filtro = datos_filtro_response.json()
    except requests.exceptions.RequestException as e:
        print(f"e: {e}")
        datos_filtro = []
    datosFiltro = ['animal', 'color', 'condicion', 'fechaEncontrado', 'fechaPerdido', 'raza', 'resuelto', 'ubicacion']
    filtro = {}
    for dato in datosFiltro:
        valor = request.args.get(dato)
        if valor:
            filtro[dato] = valor
    try:
        response = requests.get('http://localhost:5001/api/animales/buscar', json=filtro)
        response.raise_for_status()
        animales = response.json()
    except requests.exceptions.RequestException as e:
        animales = []
        print(f"Error al obtener animales: {e}")
    return render_template('pets.html', animales=animales, datos_filtro = datos_filtro, is_logged_in = is_logged_in())


@app.route('/pets/confirm/<pet_id>', methods=['GET'])
def pet_confirm(pet_id=None):
    if not is_logged_in():
        return redirect(url_for('auth'))
    return render_template('pet_confirm.html', pet_id=pet_id, is_logged_in = is_logged_in())


@app.route('/pets/found/<pet_id>', methods=['GET'])
def pet_found(pet_id=None):
    if not session.get('cookie'):
        redirect(url_for('login'))
    if not pet_id:
        return redirect(url_for('pets'))
    response = requests.post("http://127.0.0.1:5001/api/animales/found", json={"animal_id": pet_id}, cookies=session.get('cookie'))
    if response.status_code != 201:
        return render_template('pet_found.html')
    return render_template('pet_found.html')


@app.route('/about')
def about():
    return render_template('about.html', is_logged_in = is_logged_in())

@app.route('/auth', methods=["POST", "GET"])
def auth():
    if request.method == 'POST':
        username = request.form.get("username")
        passwd = request.form.get('passwd')
        newemail = request.form.get("newemail")
        newphone = request.form.get("newphone")
        newpasswd = request.form.get("newpasswd")
        newname = request.form.get("newname")
        newlastname = request.form.get("newlastname")
        newusername = request.form.get("newusername")
        if username and passwd:
            datos = {
                    "username": username,
                    "password": passwd
                }
            request_session = requests.Session()
            response = request_session.post('http://127.0.0.1:5001/api/login', json = datos)
            if response.status_code == 200:
                session['cookie'] = request_session.cookies.get_dict()
                session['user_id'] = response.json()['user_id']
                return redirect(url_for('home'))
            #else:
                #return redirect(url_for('index.html'))
        else:
            datos = {
                    "email": newemail,
                    "password" : newpasswd,
                    "username" : newusername,
                    "telefono" : newphone,
                    "nombre" : newname,
                    "apellido" : newlastname
                }
            response = requests.post('http://127.0.0.1:5001/api/register', json = datos)
            #if response.status_code != 201:
    return render_template('auth.html', is_logged_in = is_logged_in())

@app.route('/logout')
def logout():
    response = requests.get('http://127.0.0.1:5001/api/logout')
    if response.status_code == 200:
        session.clear()
        return redirect(url_for('home'))

@app.route('/pets/<int:id>')
def petinfo(id):
    try:
        response = requests.get(f'http://localhost:5001/api/animales/{id}')
        response.raise_for_status()
        mascota = response.json()
    except requests.exceptions.RequestException as e:
        print(f"error:{e}")
        mascota = []
    return render_template('pet_info.html', mascota=mascota, is_logged_in = is_logged_in())

@app.route('/upload_pet', methods=["GET","POST"])
def upload_pet():
    imagenes_mascotas = 'static/images/imagenes_mascotas'
    app.config['imagenes_mascotas'] = imagenes_mascotas
    if not is_logged_in():
        return redirect(url_for('auth'))
    if request.method == "POST":
        animal = request.form.get('animal')
        color = request.form.get('color')
        condicion = request.form.get('condicion')
        raza = request.form.get('raza')
        raza = raza if raza else "Desconocida"
        descripcion = request.form.get('descripcion')
        descripcion = descripcion if descripcion else "Sin descripción"
        fecha = request.form.get('fecha')
        if condicion == "Perdido":
            fechaPerdido = fecha
            fechaEncontrado = None
        elif condicion == "Encontrado sin dueño":
            fechaEncontrado = fecha
            fechaPerdido = None
        foto = request.files['foto']
        ruta = os.path.join(app.config['imagenes_mascotas'], foto.filename)
        foto.save(ruta)
        urlfoto = f"/{app.config['imagenes_mascotas']}/{foto.filename}"
        ubicacion = request.form.get('ubicacion')
        datos = {
                "animal": animal,
                "color" : color,
                "condicion" : condicion,
                "descripcion" : descripcion,
                "fechaEncontrado" : fechaEncontrado,
                "fechaPerdido" : fechaPerdido,
                "raza" : raza,
                "direccion" : ubicacion,
                "urlFoto" : urlfoto
            }
        if animal and color and condicion and fecha and foto and urlfoto and ubicacion:
            requests.post('http://127.0.0.1:5001/api/animales', json=datos, cookies=session['cookie'])
            return redirect(url_for('pets'))
    return render_template('upload_pet.html', is_logged_in = is_logged_in())

@app.route('/profile', methods=["GET"])
def profile():
    if not is_logged_in():
        return render_template('auth.html', is_logged_in = is_logged_in())
    try:
        response = requests.get(f"http://localhost:5001/api/usuarios/{session.get('user_id')}")
        response.raise_for_status()
        user = response.json()
    except requests.exceptions.RequestException as e:
        print(f"error:{e}")
    return render_template('profile.html', user=user, is_logged_in = is_logged_in())


@app.route('/profile/update', methods=["GET"])
def profile_edit():
    try:
        response = requests.get(f"http://localhost:5001/api/usuarios/{session['user_id']}")
        response.raise_for_status()
        user = response.json()
    except requests.exceptions.RequestException as e:
        print(f"error:{e}")
    return render_template('update_profile.html', user=user, is_logged_in = is_logged_in())


@app.route('/profile', methods=["POST"])
def profile_update():
    try:
        response = requests.put(f"http://localhost:5001/api/usuarios/{session['user_id']}", json={
            "nombre" :request.form.get('name'),
            "apellido" : request.form.get('lastname'),
            "password": request.form.get('password'),
            "telefono" : request.form.get('cellphone')
        })
        response.raise_for_status()
        user = response.json()
    except requests.exceptions.RequestException as e:
        print(f"error:{e}")
    return render_template('profile.html', user=user, is_logged_in = is_logged_in())

@app.errorhandler(500)
def internal_server_error(error):
    return render_template('critical_errors.html', is_logged_in = is_logged_in()), 500

@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html', is_logged_in = is_logged_in()), 404

def is_logged_in():
    return session.get('cookie') != None

if __name__ == '__main__':
    app.run("127.0.0.1", port="5000", debug=True)
