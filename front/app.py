from flask import Flask, redirect, render_template, url_for, request, session, jsonify
from werkzeug import exceptions
import requests


app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/pets')
def pets():
    estado = request.args.get('estado')
    raza = request.args.get('raza')
    color = request.args.get('color')
    
    filtro = [estado, raza, color]

    return render_template('pets.html', filtro = filtro)

@app.route('/pets/<condicion>')
def petsFiltro(condicion):
    
    return render_template('pets.html', condicion=condicion)

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/work-single')
def workSingle():
    return render_template('work-single.html')

@app.route('/work')
def work():
    return render_template('work.html')

@app.route('/auth', methods=["POST", "GET"])
def auth():
    if request.method == 'POST':
        mail = request.form.get("mail")
        passwd = request.form.get('passwd')
        newemail = request.form.get("newemail")
        newphone = request.form.get("newphone")
        newpasswd = request.form.get("newpasswd")
    return render_template('auth.html')

@app.route('/publicaciones')
def publicaciones():
    return render_template('publicaciones.html')
    
@app.route('/mascotas/<estado>/<id>')
def petinfo(estado, id):
    return render_template('pet_info.html', estado="perdidas", id=20)

@app.route('/upload_pet', methods=["GET","POST"])
def upload_pet():
    imagenes_mascotas = 'imagenes_mascotas'
    app.config['imagenes_mascotas'] = imagenes_mascotas
    if request.method == "POST":
        #if session.get('logged_in'):
        animal = request.form.get('animal')
        color = request.form.get('color')
        condicion = request.form.get('condicion')
        raza = request.form.get('raza')
        descripcion = request.form.get('descripcion')
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
        resuelto = request.form.get('resuelto')
        ubicacion = request.form.get('ubicacion')
        datos = jsonify(
            {
                "animal": animal,
                "color" : color,
                "condicion" : condicion,
                "descripcion" : descripcion,
                "fechaEncontrado" : fechaEncontrado,
                "fechaPerdido" : fechaPerdido,
                "raza" : raza,
                "resuelto" : resuelto,
                "ubicacion" : ubicacion,
                "urlFoto" : urlfoto
            }
        )
        requests.post('http://127.0.0.1:5001/api/animales', json = datos)
        return redirect(url_for('publicaciones.html'))
        #else:
            #return(redirect(url_for('auth.html')))
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
    

@app.errorhandler(exceptions.InternalServerError)
def handle_internal_server_error(e):
    return render_template('critical_errors.html')

@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404
if __name__ == '__main__':
    app.run("127.0.0.1", port="5000", debug=True)