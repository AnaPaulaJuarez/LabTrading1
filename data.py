
import pandas as pd
import numpy as np
import os

def Lectura_Datos_Naftrac(fecha: str):
    
    # Definimos la ruta de la carpeta donde están los archivos
    folder_path = "Files"
    
    # Combinamos la ruta de la carpeta con el nombre del archivo
    file_path = os.path.join(folder_path, "NAFTRAC_" + fecha + ".csv")
    
    # Leemos el archivo csv y lo guardamos en la variable `datos`
    datos = pd.read_csv(file_path, skiprows=2).dropna()
    
    # Devolvemos la variable `datos`, que contiene los datos del archivo csv limpios, al llamador de la función
    return datos
