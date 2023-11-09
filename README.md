# medicapp-api

# PRIMERA VEZ
## Crear Python Envivorement
    python3 -m venv venv
## Seleccionar Envivorement en VSC
    abre un archivo de python del proy (Main.py por ej)
    abajo a la derecha en azulito debe decir la version de python que tienes instalado, le picas
    eliges la version que diga ('venv':venv) o 
    seleccionas "Escriba la ruta de acceso del inteprete" y selecccionas venv/Scripts/python.exe

## Activar  Envivorement
    source venv/bin/activate  (Linux)
    or
    venv/Scripts/activate.bat  (Windows)

## Instalar dependencias/librerias
    pip install -r requirements.txt (Windows)
    !! Si falla es por el uvloop, quitar la linea, instalar y volver a poner
## Correr uvicorn
    uvicorn main:app --reload

# CORRER MEDICAPP-API
## Activar  Envivorement (aveces lo hace solo)
    source venv/bin/activate  (Linux)
    or
    venv/Scripts/activate.bat  (Windows)
## Correr uvicorn
    uvicorn main:app --reload