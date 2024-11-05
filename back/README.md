# Backend

## Estructura de la base de datos

### usuarios

| id | nombreUsuario | password | nombre    | apellido  | email              | telefono   |
|----|---------------|----------|-----------|-----------|--------------------|------------|
| 1  | saznarez      | 1234     | Sebastian | Aznarez   | saznarez@fi.uba.ar | 1123456789 |
| 2  | usuario2      | 1111     | Nombre1   | Apellido1 | email2@gmail.com   | 1199999999 |
| 3  | usuario3      | 2222     | Nombre2   | Apellido2 | email3@gmail.com   | 1177777777 |

Todos los campos deberian ser obligatorios

### mascotas

| id | animal | raza     | condicion  | color  | ubicacion     | urlFoto                     | descripcion  | fecha    | resuelto | userID |
|----|--------|----------|------------|--------|---------------|-----------------------------|--------------|----------|----------|--------|
| 1  | perro  | labrador | perdido    | marron | (coordenadas) | /static/images/mascota1.jpg | descripcion1 | 20241104 | false    | 2      |
| 2  | gato   | null     | encontrado | gris   | (coordenadas) | /static/images/mascota2.jpg | descripcion2 | 20241022 | false    | 1      |
| 3  | perro  | null     | perdido    | negro  | (coordenadas) | /static/images/mascota3.jpg | descripcion3 | 20241101 | true     | 2      |

Todos los campos son obligatorios, salvo `raza` y `descripcion`.
El campo `resuelto` indica si la mascota se reencontró con su dueño/a. 
Cada mascota se relaciona con el usuario que la carga (mediante `userID`)

