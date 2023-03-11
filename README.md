# LabTrading1

Este código permite realizar una estrategia de inversión pasiva con el NAFTRAC, un fondo cotizado (ETF) que replica el comportamiento del índice de la Bolsa Mexicana de Valores (BMV) compuesto por las 35 empresas más grandes de México.

Para utilizar este código, es necesario tener instalado Python 3 y las siguientes librerías: pandas, numpy, y matplotlib. Además, se deben tener los datos del NAFTRAC en formato csv en una carpeta llamada "data" en la misma ubicación que el archivo functions.py.

El archivo functions.py contiene las funciones necesarias para obtener los precios históricos de los tickers y los pesos correspondientes, y realizar la estrategia de inversión pasiva. También se incluye el archivo Lectura_Datos_Naftrac.py, que contiene la función para leer las posiciones del NAFTRAC para una fecha específica.

El archivo main.py es el archivo principal que debe ser ejecutado. En este archivo, se define la fecha deseada para leer las posiciones del NAFTRAC, se leen las posiciones correspondientes, se obtienen los precios históricos, se realiza la estrategia de inversión pasiva y se muestran los resultados en tres dataframes.

El primer dataframe, df_positions, muestra las posiciones de cada ticker en el portafolio a lo largo del tiempo. El segundo dataframe, df_evolution, muestra la evolución del capital inicial y el capital acumulado a lo largo del tiempo. El tercer dataframe, df_metrics, muestra algunas métricas relevantes de la estrategia de inversión pasiva, como el rendimiento anualizado, la desviación estándar anualizada y el índice de Sharpe.

Este código permite a los usuarios realizar una estrategia de inversión pasiva con el NAFTRAC y evaluar su desempeño a lo largo del tiempo. Sin embargo, es importante tener en cuenta que los resultados obtenidos pueden variar en función de los precios de mercado y las condiciones económicas y políticas del país.