from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.config import Config
from kivy.core.window import Window
import requests

Config.set('graphics', 'width', '200')
Config.set('graphics', 'height', '200')
Window.size = (414, 736)

class Login(Screen):
    user = ObjectProperty(None)
    password = ObjectProperty(None)

    def loginBtn(self):
            url = "http://localhost:5001/api/login"
            datos = {
                "username": str(self.user.text),
                "password": str(self.password.text)
                }
            req = requests.Session()

            response = req.post(url, json=datos)

            if response.status_code == 200:
                Main.current_user = self.user.text
                Main.current_passwd = self.password.text
                screen.current = "main"
            else:
                invalidLogin()


    def reset(self):
        self.user.text = ""
        self.password.text = ""


class Main(Screen):
    animal = ObjectProperty(None)
    raza = ""
    condicion = ObjectProperty(None)
    color = ""
    descripcion = ""
    fecha = ""
    fechaPerdido = ""
    fechaEncontrado = ""
    foto = ""
    ubicacion = ""
    current_user = ""
    current_passwd = ""
    
    #definirCondicion relaciona la condicion de la mascota con el tipo de fecha (perdido o encontrado) que debe añadirse al formulario, y establece el tipo de fecha no utilizado cono None. (La fecha utilizada se convierte a string primero, de otra forma al pasarlo al request no se puede convertir en json).
    def definirCondicion(self, condicion):
        fecha = self.fecha.text
        if condicion == "Perdido":
            self.fechaPerdido = str(fecha)
            self.fechaEncontrado = None
        else:
            self.fechaEncontrado = str(fecha)
            self.fechaPerdido = None
    
    #definirRaza toma la raza que haya ingresado el usuario, o si el usuario deja el campo vacio, cambia la raza a "Desconocida".
    def definirRaza(self, raza):
        if raza == "":
            self.raza = "Desconocida"
        else:
            self.raza = str(raza)

    def añadirBtn(self):
        url = "http://localhost:5001/api/login"
        datos = {
            "username": self.current_user,
            "password": self.current_passwd
        }
        session = requests.Session()
        response_login = session.post(url, json=datos)
        if response_login.status_code == 200:
            animal = self.animal.text
            condicion = self.condicion.text
            raza = self.raza.text
            color = self.color.text
            descripcion = self.descripcion.text
            ubicacion = self.ubicacion.text
            self.definirCondicion(condicion)
            self.definirRaza(raza)
            url = 'http://localhost:5001/api/animales'
            params = {
                "animal": animal,
                "color": color,
                "condicion": condicion,
                "descripcion": descripcion,
                "fechaEncontrado": self.fechaEncontrado,
                "fechaPerdido": self.fechaPerdido,
                "raza": self.raza,
                "direccion": ubicacion,
                "urlFoto": 'IMGURL',
                }
            response = session.post(url, json=params)
            if response.status_code == 201:
                successUpload()
            else:
                  print(response.text)


    def logOut(self):
        screen.current = "login"
        Login.reset

class importarImagen(Screen):
    #esta vista va a ser para agregar la foto
    pass

class WindowManager(ScreenManager):
    pass

def invalidLogin():
    pop = Popup(title = 'Error de inicio de sesión.',
                content = Label(text = 'Nombre de usuario o contraseña inválidos.'),
                size_hint = (None, None), size = (400, 200))
    pop.open()

def successUpload():
    pop = Popup(title = '',
                content = Label(text = 'Mascota añadida con éxito!'),
                size_hint = (None, None), size = (400, 200))
    pop.open()


kv = Builder.load_file("templates/layout.kv")

screen = WindowManager()

logged_user = ""
logged_passwd = ""

paginas = [Login(name = "login"), Main(name = "main")]
for pagina in paginas:
    screen.add_widget(pagina)
screen.current = "login"

class App(App):
    def build(self):
        return screen
    
if __name__ == "__main__":
    App().run()


