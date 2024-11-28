#!/bin/bash

. ./crearEnvs.sh

cd back

pip install -r requirementsback.txt
pip install sendgrid
pip install requests

echo "Instalando dependencias en back..."

cd ..
cd front

pip install -r requirementsfront.txt
pip install requests

echo "Instalando dependencias en front..."

cd ..
cd mobile

pip install -r requirementsmobile.txt
pip install requests

echo "Instalando dependencias en mobile..."

cd ..

echo "Se han instalado todas las dependencias."
