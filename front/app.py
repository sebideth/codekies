from flask import Flask, redirect, render_template, url_for, request, session
from werkzeug import exceptions

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

@app.route('/upload_pet', methods=["GET","POST"])
def upload_pet():
    if request.method == "POST":
        if session.get('logged_in'):
            animal = request.form.get('animal')
            raza = request.form.get('raza')
            condicion = request.form.get('condicion')
            color = request.form.get('color')
            descripcion = request.form.get('descripcion')
            fecha = request.form.get('fecha')
            foto = request.files.get('foto')
            resuelto = request.form.get('resuelto')
            return redirect(url_for('publicaciones.html'))
        else:
            return(redirect(url_for('auth.html')))
    return render_template('upload_pet.html')

@app.errorhandler(exceptions.InternalServerError)
def handle_internal_server_error(e):
    return render_template('critical_errors.html')

@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404
if __name__ == '__main__':
    app.run("127.0.0.1", port="5000", debug=True)