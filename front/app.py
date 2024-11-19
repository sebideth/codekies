from flask import Flask, redirect, render_template, url_for, request, session, abort
import requests

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/pets')
def pets():

    try:
        response = requests.get('http://localhost:5001/api/animales')  
        response.raise_for_status()  
        animales = response.json() 
    except Exception as e:
        animales = [] 
        print(f"Error al obtener animales: {e}")

    return render_template('pets.html', animales=animales)


@app.route('/pets/search', methods=['GET'])
def pets_search():
     
    estado = request.args.get('estado')
    raza = request.args.get('raza')
    color = request.args.get('color')
    animal = request.args.get('animal')
 
    filtro = {}
    if estado:
        filtro['condicion'] = estado
    if raza:
        filtro['raza'] = raza
    if color:
        filtro['color'] = color
    if animal:
        filtro['animal'] = animal
    
    try:
        
        response = requests.get('http://localhost:5001/api/animales/buscar', json=filtro)
        response.raise_for_status() 
        animales = response.json()  
    except Exception as e:
        animales = []  
        print(f"Error al obtener animales: {e}")

    
    return render_template('pets.html', animales=animales)

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
    
@app.route('/pets/<estado>/<id>')
def petinfo(estado, id):
    mascotas = {
        "urlFoto": url_for('static', filename='images/doge.png'),  
        "nombre": "Doge", 
        "animal": "Perro",  
        "raza": "Shiba Inu",  
        "color": "Amarillo", 
        "condicion": "Perdido", 
        "latitud": -34.6083,
        "longitud": -58.3712,
        "fecha": "2024-11-01", 
        "descripcion": "Tiene ojitos chiquitos."
    }    
    return render_template('pet_info.html', estado="perdidas", id=20, mascotas=mascotas)

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
    
@app.errorhandler(500)
def internal_server_error(error):
    return render_template('critical_errors.html'), 500

@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404
if __name__ == '__main__':
    app.run("127.0.0.1", port="5000", debug=True)