import csv
import pathlib, json

def leer_csv_login(ruta_archivo):
    """
    Lee un archivo CSV y devuelve una lista de tuplas
    para usar en parametrización de pytest
    """
    datos = []
    ruta = pathlib.Path(ruta_archivo)

    if not ruta.exists():
        raise FileNotFoundError(f"No se encontró el archivo: {ruta}")
    
    with open(ruta, newline='', encoding='utf-8') as archivo:
        lector = csv.DictReader(archivo)
        for fila in lector:
            # Convertir string 'True'/'False' a booleano
            debe_funcionar = fila['debe_funcionar'].lower() == 'true'
            datos.append((
                fila['usuario'], 
                fila['clave'], 
                debe_funcionar,
                fila['descripcion']
            ))
    
    return datos

import json

def leer_json_productos(ruta_archivo):
    """
    Lee un archivo JSON con información de productos
    """

    ruta = pathlib.Path(ruta_archivo)
    
    if not ruta.exists():
        raise FileNotFoundError(f"No se encontró el archivo: {ruta}")
    
    with open(ruta, 'r', encoding='utf-8') as archivo:
        productos = json.load(archivo)
    
    # Extraer solo los nombres para parametrización
    return productos

