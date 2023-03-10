import pandas as pd
from functions import get_historical_prices, inversion_pasiva
from data import Lectura_Datos_Naftrac


# Definir la fecha deseada para leer las posiciones del NAFTRAC
fecha = "2023-01-25"

# Leer las posiciones del NAFTRAC para la fecha deseada
posiciones = Lectura_Datos_Naftrac("20230125")

# Obtener los precios históricos de los tickers y los pesos correspondientes
start_date = "2021-01-29"
end_date = fecha
prices_daily, prices_monthly, ticker_weights = get_historical_prices(start_date, end_date, posiciones)

# Realizar la estrategia de inversión pasiva
initial_capital = 10000
commission = 0.001
df_pasiva_info, df_pasiva, df_pasiva_metricas = inversion_pasiva(prices_monthly, ticker_weights, initial_capital, commission)

# Mostrar los resultados

print("\nPrecios históricos de los tickers y pesos correspondientes:")
print(prices_monthly)
print("\nInformación sobre la estrategia de inversión pasiva:")
print(df_pasiva_info)
print("\nResultados de la estrategia de inversión pasiva:")
print(df_pasiva)
print("\nMétricas de la estrategia de inversión pasiva:")
print(df_pasiva_metricas)
