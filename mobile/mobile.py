from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.config import Config
from kivy.core.window import Window
from kivy.network.urlrequest import UrlRequest

Config.set('graphics', 'width', '200')
Config.set('graphics', 'height', '200')
Window.size = (414, 736)

class Login(Screen):
    user = ObjectProperty(None)
    password = ObjectProperty(None)

    #Usuario y contraseña provisorios para realizar pruebas, luego se hará la integración con la base de datos.

    def loginBtn(self):
        if self.user.text == "admin" and self.password.text == "1234":
            Main.current = self.user.text
            self.reset()
            screen.current = "main"
        else:
            invalidLogin()

    def reset(self):
        self.user.text = ""
        self.password.text = ""
    #El metodo reset() "limpia" los labels en los que el usuario ingresa contraseña y nombre de usuario.

class Main(Screen):
    animal = ObjectProperty(None)
    raza = ObjectProperty(None)
    condicion = ObjectProperty(None)
    color = ObjectProperty(None)
    datos = ObjectProperty(None)
    fecha = ObjectProperty(None)
    foto = ObjectProperty(None)

    current = ""

    def obtenerAnimal(self,value):
        self.animal.text = value

    def obtenerCondicion(self,value):
        self.condicion.text = value

    def añadirBtn(self):
        #Test
        print(self.foto.text)

    def logOut(self):
        screen.current = "login"
        
    
class WindowManager(ScreenManager):
    pass

def invalidLogin():
    pop = Popup(title = 'Error de inicio de sesión.',
                content = Label(text = 'Nombre de usuario o contraseña inválidos.'),
                size_hint = (None, None), size = (400, 400))
    pop.open()

kv = Builder.load_file("templates/layout.kv")

screen = WindowManager()

paginas = [Login(name = "login"), Main(name = "main")]
for pagina in paginas:
    screen.add_widget(pagina)
screen.current = "login"

class App(App):
    def build(self):
        return screen
    
if __name__ == "__main__":
    App().run()

# Implementar FileChooser en un pop-up o boton