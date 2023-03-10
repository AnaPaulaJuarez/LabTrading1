
import pandas as pd
import numpy as np

def Lectura_Datos_Naftrac(fecha: str) :
    
    # Leemos un archivo csv con el nombre "NAFTRAC_" concatenado con el argumento `fecha` y la extensión ".csv"
    # Omitimos las primeras dos filas del archivo y eliminamos todas las filas que contengan valores faltantes (NaN)
    # El resultado se asigna a una variable llamada `datos`
    datos = pd.read_csv("NAFTRAC_" + fecha + ".csv", skiprows=2).dropna()
    
    # Devolvemos la variable `datos`, que contiene los datos del archivo csv limpios, al llamador de la función
    return datos
