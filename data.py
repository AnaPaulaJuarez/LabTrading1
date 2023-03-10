import pandas as pd
import numpy as np

def Lectura_Datos_Naftrac(fecha: str) :
    
    
    datos = pd.read_csv("NAFTRAC_" + fecha + ".csv", skiprows=2).dropna()
    
    return datos
