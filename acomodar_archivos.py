"""
Modulo que escanea una ubicación y clasifica los archivos por carpetas y por tipo de archivo

Función principal:
    acomodar_archivos

Autor: Carlos Emilio Mejía Vázquez
Fecha de creación: 26/12/2024
Versión: 0.2

Ultima modificación: 27/12/2024
Cambio de versiones: 0.1 -> 0.2
"""

import os
import PySimpleGUI as sg
from tkinter.filedialog import askdirectory, askopenfile
from icecream import ic

def obtener_ruta(no_gui:bool=False)->str:
    '''
    Obtiene la ubicación de un directorio.

    Args :
        no_gui (bool) :    Booleano que define si se ocupa el selector de
        carpeta de PySimpleGUI o TKinter.
            [DEFECTO] False :    Ocupa el selector de carpeta de PysimpleGUI
            True :    Ocupa el selector de carpeta de TKinter

    Returns :
        str :    Ruta normalizada de la carpeta seleccionada
    '''
    if no_gui:
        path = askdirectory()
    else:
        path = sg.popup_get_folder("Selecciona la ubicación a escanear:")
    if path in (None, ""):
        return None
    else:
        return os.path.normpath(path)

def obtener_archivo(no_gui:bool=False)->str:
    '''
    Obtiene la ubicación de un archivo.

    Args :
        no_gui (bool) :    Booleano que define si se ocupa el selector de archivos de PySimpleGUI o TKinter.
            [DEFECTO] False :    Ocupa el selector de archivos de PysimpleGUI
            True :    Ocupa el selector de archivos de TKinter

    Returns :
        str :    Ruta normalizada del archivo seleccionado
    '''
    if no_gui:
        path = askopenfile()
    else:
        path = sg.popup_get_file("Selecciona un archivo:")
    if path in (None, ""):
        return None
    else:
        return os.path.normpath(path)

def escanear_archivos(path:str)->dict[str,list[str]]:
    '''
    Escanea una ubicación y clasifica solo los archivos encontrados

    Args :
        path (str) :    Es la ubicacion donde se va a realizar el escaneo

    Returns :
        dict[str, list[str]] :    Un diccionario donde:
            - Claves :    Extensiones de archvos
            - Valores :    Lista con las rutas de los archivos con extencion igual a la Clave
    '''
    archivos = [file for file in os.listdir(path) if os.path.isfile(os.path.join(path, file))]
    extensiones = {}
    for archivo in archivos:
        name, extension = os.path.splitext(archivo)
        # extension = extension.replace(".", "")
        try:
            extensiones[extension].append(os.path.normpath(os.path.join(path, archivo)))
        except KeyError:
            extensiones[extension]= [os.path.normpath(os.path.join(path, archivo))]
    return extensiones

def crear_carpeta(ubicacion:str, nombre:str)->int:
    '''
    Crea carpetas ocupando CMD en Windows

    Args:
        nombre (str) :    El nombre de la carpeta que se va a crear
        ubicacion (str):    La ubicación donde se va a crear la carpeta

    Returns :
        int: donde:
            - 0 :    No se creó la carpeta
            - 1 :    Se creó la carpeta
    '''
    folder_name = os.path.join(ubicacion, nombre)
    if os.path.isdir(folder_name):
        return 0
    else:
        output = os.system(f"mkdir \"{folder_name}\"")
        if output == 0:
            return 1
        else:
            return 0

def mover_archivos(ubi_archivo:str, ubi_nueva:str)->int:
    '''
    Mueve archivos de una ubicación a otra ocupando CMD en Windows

    Args:
        ubi_archivo (str) :    La ubicación del archivo que se desea mover.
        ubi_nueva (str) :    La ubicación a donde se va a mover el archivo.

    Returns :
        int: donde:
            - 0 :    No se movió el archivo.
            - 1 :    Se movió el archivo.
    '''
    output = os.system(f'move \"{ubi_archivo}\" \"{ubi_nueva}\"')
    if output == 0:
        return 1
    else:
        return 0

def acomodar_archivos(archivos:list[list[str]], extensiones:list[str], main_path:str):
    '''
    Función principal del programa. Acomoda y clasifica los archivos de una ubicación en carpetas

    Args:
        archivos (list[list[str]]):    Es una lista de archivos almacenados por listas por tipo de archivos
        extenciones (list[str]):    Es una lista de archivos que sirven para crear las carpetas
        main_path (str):    es la ubicación seleccionada para escanear y clasificar los archivos
    '''
    for i, ext in enumerate(extensiones):
        crear_carpeta(main_path, ext)
        for arch in archivos[i]:
            mover_archivos(arch, os.path.join(main_path, ext))

main_path = obtener_ruta(no_gui=True)
files = escanear_archivos(path=main_path)

paths = [name for name in files.values()]
exten = [ext for ext in files.keys()]

acomodar_archivos(paths, exten, main_path)