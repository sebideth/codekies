from flask import Flask, redirect, render_template, url_for, request

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/blog')
def blog():
    return render_template('blog.html')

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

@app.route('/auth')
def auth():
    return render_template('auth.html')

@app.route('publicaciones')
def publicaciones():
    return render_template('publicaciones.html')

@app.route('/upload_pet', methods=["GET","POST"])
def upload_pet(logeado):
    if request.method == "POST":
        #definir logeado
        if logeado:
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

if __name__ == '__main__':
    app.run("127.0.0.1", port="5000", debug=True)