# Backend

## Install

```bash
cd back
pipenv shell
pipenv install
```

## Estructura de la base de datos

### usuarios

```sql
create or replace table codekies.usuarios
(
    id            int auto_increment
        primary key,
    nombreUsuario varchar(100) not null,
    password      varchar(255) not null,
    nombre        varchar(255) null,
    apellido      varchar(255) null,
    email         varchar(255) null,
    telefono      varchar(20)  null,
    fechaAlta     datetime     not null,
    constraint email
        unique (email),
    constraint nombreUsuario
        unique (nombreUsuario)
);
```


| id | nombreUsuario | password | nombre    | apellido  | email              | telefono   |
|----|---------------|----------|-----------|-----------|--------------------|------------|
| 1  | saznarez      | 1234     | Sebastian | Aznarez   | saznarez@fi.uba.ar | 1123456789 |
| 2  | usuario2      | 1111     | Nombre1   | Apellido1 | email2@gmail.com   | 1199999999 |
| 3  | usuario3      | 2222     | Nombre2   | Apellido2 | email3@gmail.com   | 1177777777 |

Todos los campos deben ser obligatorios. Ademas de `id`, `nombreUsuario` y `email` deben ser únicos.

### mascotas

```sql
create or replace table codekies.animales
(
    id              int auto_increment
        primary key,
    animal          varchar(255)         not null,
    raza            varchar(255)         not null,
    condicion       varchar(255)         not null,
    color           varchar(50)          null,
    ubicacion       varchar(255)         null,
    urlFoto         varchar(255)         null,
    descripcion     text                 null,
    fechaPerdido    datetime             not null,
    fechaEncontrado datetime             not null,
    fechaAlta       datetime             not null,
    resuelto        tinyint(1) default 0 null,
    userID          int                  null,
    constraint animales_ibfk_1
        foreign key (userID) references codekies.usuarios (id)
);
```
| id | animal | raza     | condicion  | color  | ubicacion     | urlFoto                     | descripcion  | fecha    | resuelto | userID |
|----|--------|----------|------------|--------|---------------|-----------------------------|--------------|----------|----------|--------|
| 1  | perro  | labrador | perdido    | marron | (coordenadas) | /static/images/mascota1.jpg | descripcion1 | 20241104 | false    | 2      |
| 2  | gato   | null     | encontrado | gris   | (coordenadas) | /static/images/mascota2.jpg | descripcion2 | 20241022 | false    | 1      |
| 3  | perro  | null     | perdido    | negro  | (coordenadas) | /static/images/mascota3.jpg | descripcion3 | 20241101 | true     | 2      |

Todos los campos son obligatorios, salvo `raza` y `descripcion`.
El campo `resuelto` indica si la mascota se reencontró con su dueño/a. 
Cada mascota se relaciona con el usuario que la carga (mediante `userID`)

### Creación de la base de datos desde la consola

Primero actualizamos nuestro entorno

```bash
cd back
pipenv shell
pipenv sync
```

Creamos un archivo `.env` con el siguiente contenido que tenés que modificar en base a tu propia configuración:

```
# database
db_collation = "utf8mb4_general_ci"
db_username = "root"
db_password = "change_me" # password
db_host = "localhost:3306"
db_name = "codekies"
```

Ahora si, corremos el comando:

```
> flask init-database
```

El resultado debería ser algo como:

```bash
[*] Initializing database...
[*] Database name codekies
[*] Dropping existing database ...
[*] Creating database ...
[*] Selecting database ...
[*] Creating tables ...
[*] Created successfully!
```


-----------------------------

## Endpoints

### usuarios

#### Obtener usuario por nombre de usuario

Recibe nombre de usuario, devuelve un JSON con los datos del usuario (sin la contraseña). Si el usuario no existe devuelve un 404.

- url: http://localhost:5001/api/usuarios/<nombreUsuario>
- verbo: GET
- Ejemplos:

http://localhost:5001/api/usuarios/saznarez

```json
{
    "id": 1,
    "nombreUsuario": "saznarez",
    "nombre": "Sebastian",
    "apellido": "Aznarez",
    "email": "saznarez@fi.uba.ar",
    "telefono": "1123456789"
}
```
`200`

http://localhost:5001/api/usuarios/pepito

```json
{
    "error": "No se encontró el usuario"
}
```
`404`

#### Crear usuario

Recibe un JSON con la información del usuario y devuelve 201 y el JSON si la creación fue exitosa

- url: http://localhost:5001/api/usuarios
- verbo: POST
- Ejemplos:

Recibe:

```json
{    
    "nombreUsuario": "saznarez",
    "password": "1234",
    "nombre": "Sebastian",
    "apellido": "Aznarez",
    "email": "saznarez@fi.uba.ar",
    "telefono": "1123456789"
}
```

Devuelve:

```json
{    
    "id": 1,
    "nombreUsuario": "saznarez",
    "nombre": "Sebastian",
    "apellido": "Aznarez",
    "email": "saznarez@fi.uba.ar",
    "telefono": "1123456789"
}
```
`201`

#### Borrar ususario

Recibe nombre de usuario, devuelve un JSON con los datos del usuario (sin la contraseña) que se borró. Si el usuario no existe devuelve un 404 como el GET.

- url: http://localhost:5001/api/usuarios/<nombreUsuario>
- verbo: DELETE
- Ejemplos:

http://localhost:5001/api/usuarios/saznarez

```json
{
    "id": 1,
    "nombreUsuario": "saznarez",
    "nombre": "Sebastian",
    "apellido": "Aznarez",
    "email": "saznarez@fi.uba.ar",
    "telefono": "1123456789"
}
```
`200`

#### Actualizar datos

Recibe un JSON con los nuevos datos y devuelve todos los datos actualizados del usuario (como el endpoint de obtener ususario por nombre de ususario)

- url: http://localhost:5001/api/usuarios/<nombreUsuario>
- verbo: PUT
- Ejemplos: 

Recibe:

```json
{
    "nombre": "Sebastián",
    "apellido": "Aznárez",
    "email": "saznarez@gmail.com",
    "telefono": "11999999"
}
```

Devuelve:

```json
{
    "id": 1,
    "nombreUsuario": "saznarez",
    "nombre": "Sebastián",
    "apellido": "Aznárez",
    "email": "saznarez@gmail.com",
    "telefono": "11999999"
}
```
`200`

#### Validar login

Dados nombre de usuario y contraseña en formato JSON, devuelve 200 si el login es exitoso y 404 para el caso contrario.

- url: http://localhost:5001/api/usuarios/login
- verbo: GET
- Ejemplos:

Recibe: 

```json
{
    "nombreUsuario": "saznarez",
    "password": "1234"
}
```
Devuelve:

```json
{
    "Inicio de sesión exitoso."
}
```
`200`

Recibe: 

```json
{
    "nombreUsuario": "saznarez",
    "password": "XXXX"
}
```

Devuelve:

```json
{
    "error": "Contraseña incorrecta"
}
```
`404`

#### Consultar si un email está registrado

Devuelve 200 si el email esta registrado, 404 para el caso contrario.

- url: http://localhost:5001/api/usuarios/email/<email>
- verbo: GET
- Ejemplos:

http://localhost:5001/api/usuarios/email/saznarez@fi.uba.ar

```json
{
    "id": 1,
    "nombreUsuario": "saznarez",
    "nombre": "Sebastian",
    "apellido": "Aznarez",
    "email": "saznarez@fi.uba.ar",
    "telefono": "1123456789"
}
```
`200`

http://localhost:5001/api/usuarios/email/pepito@gmail.com

```json
{
    "error": "El email no está registrado"
}
```
`404`

---------------------------

### mascotas

#### Obtener todas las mascotas

Devuelve un JSON con una lista de todas las mascotas cargadas

- url: http://localhost:5001/api/mascotas
- verbo: GET
- Ejemplos:

```json
{
    [
        {
            "id": 2,
            "animal": "gato",
            "raza": null,
            "condicion": "encontrado",
            "color": "gris",
            "ubicacion": "(coordenadas)",
            "urlFoto": "/static/images/mascota2.jpg",
            "descripcion": "descripcion2",
            "fecha": 20241022,
            "resuelto": false,
            "userID": 1
        },
        {
            "id": 3,
            "animal": "perro",
            "raza": null,
            "condicion": "perdido",
            "color": "negro",
            "ubicacion": "(coordenadas)",
            "urlFoto": "/static/images/mascota3.jpg",
            "descripcion": "descripcion3",
            "fecha": 20241101,
            "resuelto": true,
            "userID": 2
        }
    ]   
}
```
`200`

#### Obtener mascotas por id

Devuelve un JSON con la información de la mascota, o 404 en el caso de que no exista.

- url: http://localhost:5001/api/mascotas/<id>
- verbo: GET
- Ejemplos:

http://localhost:5001/api/mascotas/2

```json
{
    "id": 2,
    "animal": "perro",
    "raza": null,
    "condicion": "perdido",
    "color": "negro",
    "ubicacion": "(coordenadas)",
    "urlFoto": "/static/images/mascota3.jpg",
    "descripcion": "descripcion3",
    "fecha": 20241101,
    "resuelto": true,
    "userID": 2
}
```
`200`

http://localhost:5001/api/mascotas/6

```json
{
    "error": "No se encontró la mascota"
}
```
`404`

#### Cargar una mascota

Recibe un JSON con la información de la mascota, devuelve 201 y el JSON cuando la creación es exitosa.

- url: http://localhost:5001/api/mascotas
- verbo: POST
- Ejemplos:

Recibe:

```json
{
    "animal": "perro",
    "raza": null,
    "condicion": "perdido",
    "color": "negro",
    "ubicacion": "(coordenadas)",
    "urlFoto": "/static/images/mascota3.jpg",
    "descripcion": "descripcion3",
    "fecha": 20241101,
    "resuelto": true,
    "userID": 2
}
```
Devuelve:

```json
{
    "id": 2,
    "animal": "perro",
    "raza": null,
    "condicion": "perdido",
    "color": "negro",
    "ubicacion": "(coordenadas)",
    "urlFoto": "/static/images/mascota3.jpg",
    "descripcion": "descripcion3",
    "fecha": 20241101,
    "resuelto": true,
    "userID": 2
}
```
`201`

#### Actualizar una mascota

Recibe un JSON con la información a actualizar de la mascota, devuelve 200 y el JSON cuando la actualización es exitosa.

- url: http://localhost:5001/api/mascotas
- verbo: PUT
- Ejemplos:

Recibe:

```json
{
    "id": 2,
    "animal": "perro",
    "raza": null,
    "condicion": "perdido",
    "color": "negro con machitas",
    "ubicacion": "(coordenadas)",
    "urlFoto": "/static/images/mascota4.jpg",
    "descripcion": "otra descripcion",
    "fecha": 20241107,
    "resuelto": false,
    "userID": 2
}
```

Devuelve:

```json
{
    "id": 2,
    "animal": "perro",
    "raza": null,
    "condicion": "perdido",
    "color": "negro con machitas",
    "ubicacion": "(coordenadas)",
    "urlFoto": "/static/images/mascota4.jpg",
    "descripcion": "otra descripcion",
    "fecha": 20241107,
    "resuelto": false,
    "userID": 2
}
```
`200`

#### Borrar una mascota

Recibe id de la mascota a borrar, devuelve 200 y el JSON cuando el borrado es exitoso.

- url: http://localhost:5001/api/mascotas/<id>
- verbo: DELETE
- Ejemplos:

http://localhost:5001/api/mascotas/2

```json
{
    "id": 2,
    "animal": "perro",
    "raza": null,
    "condicion": "perdido",
    "color": "negro",
    "ubicacion": "(coordenadas)",
    "urlFoto": "/static/images/mascota3.jpg",
    "descripcion": "descripcion3",
    "fecha": 20241101,
    "resuelto": true,
    "userID": 2
}
```
`200`

#### Obtener todas las mascotas cargadas por un ususario

Devuelve un JSON con todas las mascotas cargadas por el usuario con el id dado, o 404 en el caso de que no exista.

- url: http://localhost:5001/api/mascotas/usuario/<id>
- verbo: GET
- Ejemplos:

http://localhost:5001/api/mascotas/usuario/2

```json
{
    [
        {
            "id": 1,
            "animal": "perro",
            "raza": "labrador",
            "condicion": "perdido",
            "color": "marron",
            "ubicacion": "(coordenadas)",
            "urlFoto": "/static/images/mascota1.jpg",
            "descripcion": "descripcion1",
            "fecha": 20241104,
            "resuelto": false,
            "userID": 2
        },
        {
            "id": 2,
            "animal": "perro",
            "raza": null,
            "condicion": "perdido",
            "color": "negro",
            "ubicacion": "(coordenadas)",
            "urlFoto": "/static/images/mascota3.jpg",
            "descripcion": "descripcion3",
            "fecha": 20241101,
            "resuelto": true,
            "userID": 2
        }
    ]
}
```
`200`

http://localhost:5001/api/mascotas/usuario/6

```json
{
    "error": "No se encontró el usuario"
}
```
`404`

#### Filtrar

Dado un JSON con una serie de caracteristicas, devuelve un JSON con la lista de mascotas que cumplan con el filtro.

- url: http://localhost:5001/api/mascotas/filtrar
- verbo: GET
- Ejemplos:

Recibe:

```json
{
    "animal": "perro",
    "condicion": "perdido"
}
```

Devuelve:

```json
{
    [
        {
            "id": 1,
            "animal": "perro",
            "raza": "labrador",
            "condicion": "perdido",
            "color": "marron",
            "ubicacion": "(coordenadas)",
            "urlFoto": "/static/images/mascota1.jpg",
            "descripcion": "descripcion1",
            "fecha": 20241104,
            "resuelto": false,
            "userID": 2
        },
        {
            "id": 2,
            "animal": "perro",
            "raza": null,
            "condicion": "perdido",
            "color": "negro",
            "ubicacion": "(coordenadas)",
            "urlFoto": "/static/images/mascota3.jpg",
            "descripcion": "descripcion3",
            "fecha": 20241101,
            "resuelto": true,
            "userID": 2
        }
    ]
}
```
`200`
