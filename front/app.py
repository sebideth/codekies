from flask import Flask, redirect, render_template, url_for, request, session
from werkzeug import exceptions
import requests
app = Flask(__name__)

API_URL = 'http://localhost:5001'

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
    
@app.route('/pets/<int:id>', methods=["GET"])
def petInfo(id):

    response = requests.get(f"{API_URL}/api/animales/{id}")

    if response.status_code == 200:
        mascotas = response.json()
        mascotas = mascotas[0] 
        return render_template('pet_info.html', id=id, mascotas=mascotas)
    else:
        return render_template('404.html')
    
@app.route('/upload_pet', methods=["GET","POST"])
def upload_pet():
    #if request.method == "POST":
        #if session.get('logged_in'):
            #animal = request.form.get('animal')
            #raza = request.form.get('raza')
            #condicion = request.form.get('condicion')
            #color = request.form.get('color')
            #descripcion = request.form.get('descripcion')
            #fecha = request.form.get('fecha')
            #foto = request.files.get('foto')
            #resuelto = request.form.get('resuelto')
            #return redirect(url_for('publicaciones.html'))
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