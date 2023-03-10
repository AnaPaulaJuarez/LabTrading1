import pandas as pd
from functions import get_historical_prices, my_investment_strategy
from data import Lectura_Datos_Naftrac


# Definir la fecha deseada para leer las posiciones del NAFTRAC
fecha = "2023-01-25"

# Leer las posiciones del NAFTRAC para la fecha deseada
posiciones = Lectura_Datos_Naftrac("20230125")

# Obtener los precios históricos de los tickers y los pesos correspondientes
start_date = "2021-01-29"
end_date = fecha
prices_df, monthly_prices_df, symbol_weights = get_historical_prices(start_date, end_date, posiciones)

# Realizar la estrategia de inversión pasiva
initial_capital = 10000
commission = 0.001
df_positions, df_evolution, df_metrics = my_investment_strategy(prices_df, symbol_weights, initial_capital, commission)

# Mostrar los resultados

print("\nInformación sobre la estrategia de inversión pasiva:")
print(df_positions)
print("\nResultados de la estrategia de inversión pasiva:")
print(df_evolution)
print("\nMétricas de la estrategia de inversión pasiva:")
print(df_metrics)
