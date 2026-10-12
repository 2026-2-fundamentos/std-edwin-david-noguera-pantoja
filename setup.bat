REM Este archivo es para instalar las dependencias del proyecto en Windows, se ejecita con el comando setup.bat dentro del en
REM vironment virtual creado con el comando venv
REM Para instalar las dependencias en Linux o MacOS se debe ejecutar el archivo setup.sh con el comando source setup.sh
REM Se realiza una una unica vez para un proyecto nuevo en la maquina, o cuando se agregan nuevas dependencias al proyecto, para que estas sean instaladas en el environment virtual

@echo off

python -m pip install --upgrade pip 
python -m pip install -r requirements.txt REM Instala las dependências do projeto en windows
