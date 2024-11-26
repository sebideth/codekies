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
    return render_template('index.html', animales=animales)

@app.route('/pets')
def pets():
    try:
        animales_response = requests.get('http://localhost:5001/api/animales')
        datos_filtro_response = requests.get('http://localhost:5001/api/animales/datos')

        animales_response.raise_for_status()
        datos_filtro_response.raise_for_status()

        animales = animales_response.json()
        datos_filtro = datos_filtro_response.json()

    except requests.exceptions.RequestException as e:

        print(f"e: {e}")
        animales = []
        datos_filtro = []

    return render_template('pets.html', animales=animales, datos_filtro=datos_filtro)

@app.route('/pets/search', methods=['GET','POST'])
def pets_search():

    try:

        datos_filtro_response = requests.get('http://localhost:5001/api/animales/datos')

        datos_filtro_response.raise_for_status()

        datos_filtro = datos_filtro_response.json()

    except requests.exceptions.RequestException as e:

        print(f"e: {e}")
        datos_filtro = []

    datosFiltro = ['animal', 'color', 'condicion', 'fecha_encontrado', 'fecha_perdido', 'raza', 'resuelto', 'ubicacion']

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
    return render_template('pets.html', animales=animales, datos_filtro = datos_filtro)


@app.route('/pets/confirm/<pet_id>', methods=['GET'])
def pet_confirm(pet_id=None):
    if not session.get('cookie'):
        redirect(url_for('login'))
    return render_template('pet_confirm.html', pet_id=pet_id)


@app.route('/pets/found/<pet_id>', methods=['GET'])
def pet_found(pet_id=None):
    if not session.get('cookie'):
        redirect(url_for('login'))
    return render_template('pet_found.html')


@app.route('/about')
def about():
    return render_template('about.html')

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
                return render_template('index.html')
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
    return render_template('auth.html')


@app.route('/pets/<int:id>')
def petinfo(id):

    try:

        response = requests.get(f'http://localhost:5001/api/animales/{id}')
        response.raise_for_status()
        mascota = response.json()

    except requests.exceptions.RequestException as e:

        print(f"error:{e}")
        mascota = []
        
    return render_template('pet_info.html', mascota=mascota)

@app.route('/upload_pet', methods=["GET","POST"])
def upload_pet():
    imagenes_mascotas = 'static/images/imagenes_mascotas'
    app.config['imagenes_mascotas'] = imagenes_mascotas
    #if not session.get('logged_in'):
        #return(redirect(url_for('auth.html')))
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
    return render_template('upload_pet.html')

@app.route('/profile', methods=["GET"])
def profile():
    #TODO: llamar al cackend para obtener el user
    return render_template('profile.html', user={
    "nombre": "Sebastian",
    "apellido": "Aznarez",
    "email": "saznarez@fi.uba.ar",
    "telefono": "1123456789"
})
@app.route('/profile', methods=["POST"])
def profile_update():
    name = request.form.get('name')
    email = request.form.get('email')
    password = request.form.get('password')
    cellphone = request.form.get('cellphone')
    print(name, email, password,cellphone)
    return render_template('profile.html', user={
    "nombre": name,
    "apellido": "Aznarez",
    "email": email,
    "telefono": cellphone
})

@app.errorhandler(500)
def internal_server_error(error):
    return render_template('critical_errors.html'), 500

@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.run("127.0.0.1", port="5000", debug=True)
