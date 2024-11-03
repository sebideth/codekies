#!/bin/bash
# Correr con . ./crearEnvs.sh (para que el cd funcione fuera del script)

DIRECTORIO=$1

mkdir front/.venv back/.venv

cd front
echo "Instalando Flask en front..."
pipenv install flask

cd ..
cd back
echo "Instalando Flask en back..."
pipenv install flask

cd ..

echo "Abriendo Visual Code Studio..."
code .

echo "Activar proyecto con:"
echo "pipenv shell"
echo "Correr Flask con:"
echo "flask run --debug"
echo "Salir del venv:"
echo "deactivate"
