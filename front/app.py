import os
from flask import Flask, redirect, render_template, url_for, request, session, abort, jsonify
from werkzeug import exceptions
import requests
from config import api_url, app_path, statics_files_path

app = Flask(__name__)
app.secret_key = 'sarasa'


@app.route('/')
def home():
    try:
        animales_response = requests.get(f'{api_url}/api/animales/ultimos/3')
        animales_response.raise_for_status()
        animales = animales_response.json()
    except requests.exceptions.RequestException as e:
        print(f"e: {e}")
        animales = []
    return render_template('index.html', animales=animales, is_logged_in=is_logged_in())


@app.route('/pets')
def pets():
    try:
        datos_filtro_response = requests.get(f'{api_url}/api/animales/datos')
        datos_filtro_response.raise_for_status()
        datos_filtro = datos_filtro_response.json()
    except requests.exceptions.RequestException as e:
        print(f"error al obtener los datos de animales: {e}")
        datos_filtro = []

    try:
        animales_response = requests.get(f'{api_url}/api/animales')
        animales_response.raise_for_status()
        animales = animales_response.json()
    except requests.exceptions.RequestException as e:
        print(f"error al obtener animales: {e}")
        animales = []

    return render_template('pets.html', animales=animales, datos_filtro=datos_filtro, is_logged_in=is_logged_in())


@app.route('/pets/search', methods=['GET', 'POST'])
def pets_search():
    try:
        datos_filtro_response = requests.get(f'{api_url}/api/animales/datos')
        datos_filtro_response.raise_for_status()
        datos_filtro = datos_filtro_response.json()
    except requests.exceptions.RequestException as e:
        print(f"e: {e}")
        datos_filtro = []
    datosFiltro = ['animal', 'color', 'condicion', 'fechaEncontrado', 'fechaPerdido', 'raza', 'zona']
    filtro = {}
    for dato in datosFiltro:
        valor = request.args.get(dato)
        if valor:
            filtro[dato] = valor
    try:
        response = requests.get(f'{api_url}/api/animales/buscar', json=filtro)
        response.raise_for_status()
        animales = response.json()
    except requests.exceptions.RequestException as e:
        animales = []
        print(f"Error al obtener animales: {e}")
    return render_template('pets.html', animales=animales, datos_filtro=datos_filtro, is_logged_in=is_logged_in())


@app.route('/pets/confirm/<pet_id>', methods=['GET'])
def pet_confirm(pet_id=None):
    if not is_logged_in():
        return redirect(url_for('auth'))
    return render_template('pet_confirm.html', pet_id=pet_id, is_logged_in=is_logged_in())


@app.route('/pets/found/<pet_id>', methods=['GET'])
def pet_found(pet_id=None):
    if not session.get('cookie'):
        redirect(url_for('login'))
    if not pet_id:
        return redirect(url_for('pets'))
    response = requests.post(f"{api_url}/api/animales/found", json={"animal_id": pet_id},
                             cookies=session.get('cookie'))
    if response.status_code != 201:
        return render_template('pet_found.html')
    return render_template('pet_found.html')


@app.route('/pets/edit/<int:id>', methods=["GET"])
def pet_edit(id):
    try:
        response = requests.get(f"{api_url}/api/animales/{id}")
        response.raise_for_status()
        animal = response.json()
    except requests.exceptions.RequestException as e:
        print(f"error:{e}")
    return render_template('pet_edit.html', animal=animal, is_logged_in=is_logged_in())


@app.route('/pets/edit/<int:id>', methods=["POST"])
def pet_update(id):
    try:
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
        if foto:
            ruta = statics_files_path + "/" + foto.filename
            foto.save(ruta)
            urlfoto = foto.filename
        lat = request.form.get('lat')
        lng = request.form.get('lng')
        zona = request.form.get('zona')
        datos = {
            "animal": animal,
            "color": color,
            "condicion": condicion,
            "descripcion": descripcion,
            "fechaEncontrado": fechaEncontrado,
            "fechaPerdido": fechaPerdido,
            "raza": raza,
        }
        if foto:
            datos['urlFoto'] = urlfoto
        if zona:
            datos['zona'] = zona
            datos['lat'] = lat
            datos['lng'] = lng
        response = requests.put(f"{api_url}/api/animales/{id}", json=datos, cookies=session.get('cookie'))
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"error:{e}")
    if response.status_code == 403:
        abort(403)
    return redirect(url_for('profile'))


@app.route('/pets/delete/<int:id>', methods=["GET"])
def pet_delete(id):
    try:
        response = requests.delete(f"{api_url}/api/animales/{id}", cookies=session.get('cookie'))
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"error:{e}")
    response_code = response.status_code
    if response_code in [403, 404]:
        abort(response_code)
    return redirect(url_for('profile'))


@app.route('/about')
def about():
    return render_template('about.html', is_logged_in=is_logged_in())


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
            response = request_session.post(f'{api_url}/api/login', json=datos)
            if response.status_code == 200:
                session['cookie'] = request_session.cookies.get_dict()
                session['user_id'] = response.json()['user_id']
                return redirect(url_for('home'))
            else:
                return render_template('auth_error.html', error=response.json()['error'])
        else:
            datos = {
                "email": newemail,
                "password": newpasswd,
                "username": newusername,
                "telefono": newphone,
                "nombre": newname,
                "apellido": newlastname
            }
            response = requests.post(f'{api_url}/api/register', json=datos)
            if response.status_code != 201:
                return render_template('auth_error.html', error=response.json()['error'])
    return render_template('auth.html', is_logged_in=is_logged_in())


@app.route('/logout')
def logout():
    response = requests.get(f'{api_url}/api/logout')
    if response.status_code == 200:
        session.clear()
        return redirect(url_for('home'))


@app.route('/pets/<int:id>')
def petinfo(id):
    try:
        response = requests.get(f"{api_url}/api/animales/{id}")
        response.raise_for_status()
        mascota = response.json()
    except requests.exceptions.RequestException as e:
        print(f"error:{e}")
        mascota = []
    if response.status_code == 404:
        abort(404)
    return render_template('pet_info.html', mascota=mascota, is_logged_in=is_logged_in())


@app.route('/upload_pet', methods=["GET", "POST"])
def upload_pet():
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
        ruta = statics_files_path + "/" + foto.filename  # os.path.join(app_path, statics, foto.filename)
        foto.save(ruta)
        urlfoto = foto.filename
        ubicacion = request.form.get('ubicacion')
        lat = request.form.get('lat')
        lng = request.form.get('lng')
        print(f"lat {lat} lng {lng}")
        # apiKey = "9d82b10b02a649e883471f803f7ffed5"
        # ubicacion_request = requests.get(f"https://api.geoapify.com/v1/geocode/search?text={ubicacion}&limit=1&filter=countrycode:ar&format=json&apiKey={apiKey}")
        # zona = ubicacion_request.json()['results'][0]['suburb']
        zona = request.form.get('zona')
        datos = {
            "animal": animal,
            "color": color,
            "condicion": condicion,
            "descripcion": descripcion,
            "fechaEncontrado": fechaEncontrado,
            "fechaPerdido": fechaPerdido,
            "raza": raza,
            "zona": zona,
            "lat": lat,
            "lng": lng,
            "urlFoto": urlfoto
        }
        if animal and color and condicion and fecha and foto and urlfoto and ubicacion:
            requests.post(f'{api_url}/api/animales', json=datos, cookies=session.get('cookie'))
            return redirect(url_for('pets'))
    return render_template('upload_pet.html', is_logged_in=is_logged_in())


@app.route('/profile', methods=["GET"])
def profile():
    if not is_logged_in():
        return render_template('auth.html', is_logged_in=is_logged_in())
    try:
        response = requests.get(f"{api_url}/api/usuarios/{session.get('user_id')}")
        response.raise_for_status()
        user = response.json()
        animales_response = requests.get(f"{api_url}/api/animales/usuario/{session.get('user_id')}",
                                         cookies=session.get('cookie'))
        my_animals = animales_response.json()
    except requests.exceptions.RequestException as e:
        print(f"error:{e}")
    return render_template('profile.html', user=user, animales=my_animals, is_logged_in=is_logged_in())


@app.route('/profile/update', methods=["GET"])
def profile_edit():
    try:
        response = requests.get(f"{api_url}/api/usuarios/{session['user_id']}")
        response.raise_for_status()
        user = response.json()
    except requests.exceptions.RequestException as e:
        print(f"error:{e}")
    return render_template('update_profile.html', user=user, is_logged_in=is_logged_in())


@app.route('/profile', methods=["POST"])
def profile_update():
    try:
        response = requests.put(f"{api_url}/api/usuarios/{session['user_id']}", json={
            "nombre": request.form.get('name'),
            "apellido": request.form.get('lastname'),
            "password": request.form.get('password'),
            "telefono": request.form.get('cellphone')
        })
        response.raise_for_status()
        user = response.json()
    except requests.exceptions.RequestException as e:
        print(f"error:{e}")
    return render_template('profile.html', user=user, is_logged_in=is_logged_in())


@app.errorhandler(500)
def internal_server_error(error):
    return render_template('critical_errors.html', is_logged_in=is_logged_in()), 500


@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html', is_logged_in=is_logged_in()), 404


@app.errorhandler(403)
def forbidden(error):
    return render_template('403.html', is_logged_in=is_logged_in()), 403


def is_logged_in():
    return session.get('cookie') != None


if __name__ == '__main__':
    app.run("127.0.0.1", port="5000", debug=True)
