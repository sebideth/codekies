from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.config import Config
from kivy.core.window import Window

from kivymd.uix.list import OneLineListItem
from kivy.clock import Clock
from kivy_garden.mapview import MapMarker
import requests
from dateutil.parser import parser

#instalar kivy garden y despues hacer pip install mapview

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
                self.manager.current = "main"
            else:
                invalidLogin()

    def reset(self):
        self.user.text = ""
        self.password.text = ""

class Main(Screen):
    #La foto de la mascota tendra una ruta harcodeada para que la pagina funcione, ya que de lo contrario se guardaria una ruta perteneciente al celular del usuario y el programa no podria buscar la foto de forma local.
    animal = ObjectProperty(None)
    raza = ""
    condicion = ObjectProperty(None)
    color = ""
    descripcion = ""
    fecha = ""
    fechaPerdido = ""
    fechaEncontrado = ""
    ubicacion = ""
    current_user = ""
    current_passwd = ""

    #definirCondicion relaciona la condicion de la mascota con el tipo de fecha (perdido o encontrado) que debe añadirse al formulario, y establece el tipo de fecha no utilizado cono None. (La fecha utilizada se convierte a string primero, de otra forma al pasarlo al request no se puede convertir en json).
        
    def definirCondicion(self, condicion):
        fecha = self.fecha.text
        if condicion == "Perdido":
            self.fechaPerdido = self.normalizarFecha(str(fecha))
            self.fechaEncontrado = None
        else:
            self.fechaEncontrado = self.normalizarFecha(str(fecha))
            self.fechaPerdido = None
    
    #definirRaza toma la raza que haya ingresado el usuario, o si el usuario deja el campo vacio, cambia la raza a "Desconocida".   
    def definirRaza(self, raza):
        if raza == "":
            self.raza = "Desconocida"
        else:
            self.raza = str(raza)

    #normalizarFecha utiliza la libreria dateutil para guardar la fecha ingresada en el mismo formato que está en la base de datos (Lamentablemente no se pueden poner fechas en español).            
    def normalizarFecha(self, fecha):
        fecha_normal = parser().parse(fecha)
        return str(fecha_normal)
    
    def fechaVacia(self, fecha):
        if fecha == "" or fecha == None:
            return True
    #camposVacios recibe una lista con los campos ingresados por el usuario, y si alguno de los campos esta vacio, retorna True. Esto sirve para verificar que el usuario haya ingresado todos los campos obligatorios.
    def camposVacios(self, campos):
        for campo in campos:
            if campo == "" or campo == None:
                return True
    def añadirBtn(self):
        url = "http://localhost:5001/api/login"
        datos = {
            "username": self.current_user,
            "password": self.current_passwd
        }
        session = requests.Session()
        response_login = session.post(url, json=datos)
        campos = [self.animal.text, self.condicion.text, self.color.text, self.ubicacion.text]
        if self.fechaVacia(self.fecha.text) or self.camposVacios(campos):
            camposObligatorios()            
        elif response_login.status_code == 200:
                foto = str(importarImagen.getFoto)
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
                    "zona": ubicacion,
                    "urlFoto": "static/images/imagenes_mascotas/grumpy.jpeg"
                    }
                
                response = session.post(url, json=params)
                if response.status_code == 201:
                    successUpload()
                else:
                    print(response.text)

    def logOut(self):
        self.manager.current = "login"
        Login.reset

class importarImagen(Screen):
    foto = ObjectProperty(None)
    
    def selected(self, archivo):
        self.foto = str(archivo[0])
    
    def getFoto(self):
        return str(self.foto)
    
class WindowManager(ScreenManager):
    pass


class MostrarMapa(Screen):

    _search_timer = None
    direccion_seleccionada = None  
    marcador = None  

    def obtener_direcciones(self, query):
        api_key = "9d82b10b02a649e883471f803f7ffed5"
        url = f"https://api.geoapify.com/v1/geocode/autocomplete?text={query}&apiKey={api_key}"

        response = requests.get(url)
    
        if response.status_code == 200:
            data = response.json()
            return data.get('features', [])
        else:
            print("Error al obtener direcciones:", response.status_code)
            return []

    def actualizar_sugerencias(self, query):
        if self._search_timer:
            Clock.unschedule(self._search_timer)

        def delayed_search(query):
            direcciones = self.obtener_direcciones(query)
            self.ids.suggestions_list.clear_widgets()

            if direcciones:
                for direccion in direcciones:
                    direccion_texto = direccion['properties']['formatted']
                    item = OneLineListItem(text=direccion_texto)
                    item.direccion = direccion
                    item.bind(on_release=self.on_suggestion_click)
                    self.ids.suggestions_list.add_widget(item)

        self._search_timer = Clock.schedule_once(lambda dt: delayed_search(query), 0.7)

    def on_suggestion_click(self, instance):
        direccion = instance.direccion
        print(f"Seleccionaste: {direccion['properties']['formatted']}")

        lat = direccion['geometry']['coordinates'][1]
        lon = direccion['geometry']['coordinates'][0]

        self.ids.mapa.center_on(lat, lon) 
        self.ids.mapa.zoom = 17  

        if self.marcador:
            self.ids.mapa.remove_widget(self.marcador)

        self.marcador = MapMarker(lat=lat, lon=lon)
        self.ids.mapa.add_widget(self.marcador) 

        self.ids.suggestions_list.clear_widgets()

        self.direccion_seleccionada = direccion['properties']['formatted']     


    def guardar_direccion(self):
        if self.direccion_seleccionada:
            main_screen = self.manager.get_screen("main")
            main_screen.ids.ubicacion.text = self.direccion_seleccionada
        
        self.manager.current = "main"

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

def camposObligatorios():
    pop = Popup(title = 'Campos incompletos.',
                content = Label(text = 'Faltan datos para completar'),
                size_hint = (None, None), size = (400, 200))
    pop.open()

class MyApp(MDApp):
    def build(self):
        self.screen = Builder.load_file("templates/layout.kv")

        self.manager = WindowManager()
        paginas = [Login(name = "login"), Main(name = "main"), importarImagen(name = 'imagen'), MostrarMapa(name = 'mapa')]
        for pagina in paginas:
            self.manager.add_widget(pagina)
        
        self.manager.current = "login"

        return self.manager

#Las fuentes consultadas estarán en el readme.

if __name__ == "__main__":
    MyApp().run()


