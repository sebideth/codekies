from kivy.app import App
from kivy.lang import Builder
from kivy.uix.scrollview import ScrollView
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.config import Config
from kivy.core.window import Window

Config.set('graphics', 'width', '200')
Config.set('graphics', 'height', '200')
Window.size = (414, 896)

class Login(Screen):
    email = ObjectProperty(None)
    password = ObjectProperty(None)

    #Email y contraseña provisorios para realizar pruebas, luego se hará la integración con la base de datos.

    def loginBtn(self):
        if self.email.text == "admin" and self.password.text == "1234":
            Main.current = self.email.text
            self.reset()
            screen.current = "main"
        else:
            invalidLogin()
    
    def createBtn(self):
        self.reset()
        screen.current = "create"

    def reset(self):
        self.email.text = ""
        self.password.text = ""
    #El metodo reset() "limpia" los labels en los que el usuario ingresa contraseña y email.

class Main(Screen):
    animal = ObjectProperty(None)
    raza = ObjectProperty(None)
    condicion = ObjectProperty(None)
    color = ObjectProperty(None)
    datos = ObjectProperty(None)
    fecha = ObjectProperty(None)
    foto = ObjectProperty(None)

    current = ""
    
    def logOut(self):
        screen.current = "login"
        
    
class WindowManager(ScreenManager):
    pass

def invalidLogin():
    pop = Popup(title = 'Error de inicio de sesión.',
                content = Label(text = 'Nombre de usuario o contraseña inválidos.'),
                size_hint = (None, None), size = (400, 400))
    pop.open()

kv = Builder.load_file("layout.kv")

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

#Emprolijar estéticamente y obtener el input de los usuarios. Agregar mapa y poder cargar foto.