#!/bin/bash

. ./crearEnvs.sh

cd back

pip install -r requirementsback.txt

echo "Instalando dependencias en back..."

cd ..
cd front

pip install -r requirementsfront.txt

echo "Instalando dependencias en front..."

cd ..
cd mobile

pip install -r requirementsmobile.txt

echo "Instalando dependencias en mobile..."

cd ..

echo "Se han instalado todas las dependencias."
