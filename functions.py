
import pandas as pd
pd.set_option('display.float_format', lambda x: '%.4f' % x)
import yfinance as yf
import numpy as np

def get_historical_prices(start_date: str, end_date: str, positions_data: str):


    # Crear un diccionario de tickers para descargar y establecer una lista de filtros.
    ticker_weights = {}
    filter_tickers = ["KOFL", "KOFUBL", "USD", "MXN", "BSMXB", "NMKA"]

    # Agregar cada ticker y su peso a los tickers a descargar si el ticker no está en la lista de filtros.
    for i in range(len(positions_data)):
        ticker = positions_data["Ticker"][i]
        weight = positions_data["Peso (%)"][i] / 100

        if ticker not in filter_tickers:
            ticker_weights[ticker.replace("*", "").replace(".", "-") + ".MX"] = weight

    # Descargar los precios de los tickers y almacenarlos en un DataFrame.
    prices_df = pd.DataFrame()
    for ticker, weight in ticker_weights.items():
        prices_df[ticker] = yf.download(ticker, start=start_date, end=end_date, progress=False)["Adj Close"]

    # Eliminar las columnas con valores faltantes y crear un DataFrame con los precios mensuales.
    prices_df.dropna(axis=1, inplace=True)
    monthly_prices_df = pd.DataFrame(columns=prices_df.columns)

    for i in range(len(prices_df)):
        current_month = prices_df.index[i].month
        next_month = prices_df.index[i + 1].month if i < len(prices_df) - 1 else None

        if next_month is None or current_month != next_month:
            monthly_prices_df.loc[prices_df.index[i], :] = prices_df.iloc[i, :]

    # Devolver los precios diarios, mensuales y los tickers utilizados.
    return prices_df, monthly_prices_df, ticker_weights

def inversion_pasiva(prices_monthly: pd.DataFrame, ticker_weights: dict, initial_capital: float, commission: float):
    """
    inversion_pasiva es una función que elabora la estrategia de inversión pasiva.
    """
    # Posiciones iniciales
    df_pasiva_info = pd.DataFrame(index=prices_monthly.columns,
                                   columns=["Títulos", "Costo de Compra Bruto", "Comisión", "Costo de Compra Total"])
    for ticker in prices_monthly.columns:
        df_pasiva_info.loc[ticker, "Títulos"] = np.floor((initial_capital * ticker_weights[ticker]) /
                                                          (prices_monthly[ticker][0] * (1 + commission)))
        df_pasiva_info.loc[ticker, "Costo de Compra Bruto"] = df_pasiva_info.loc[ticker, "Títulos"] * \
                                                               prices_monthly[ticker][0]
        df_pasiva_info.loc[ticker, "Comisión"] = df_pasiva_info.loc[ticker, "Títulos"] * \
                                                   prices_monthly[ticker][0] * commission
        df_pasiva_info.loc[ticker, "Costo de Compra Total"] = df_pasiva_info.loc[ticker, "Títulos"] * \
                                                                prices_monthly[ticker][0] * (1 + commission)
        df_pasiva_info.loc[ticker, "Ponderación"] = (df_pasiva_info.loc[ticker, "Títulos"] *
                                                      prices_monthly[ticker][0]) / initial_capital

    df_pasiva = pd.DataFrame(index=prices_monthly.index,
                              columns=["Evolución Capital Invertido", "Rendimiento Mensual",
                                       "Rendimiento Mensual Acumulado"])

    # Backtest
    df_pasiva["Evolución Capital Invertido"] = np.dot(prices_monthly * (1 - commission), df_pasiva_info["Títulos"])
    df_pasiva["Rendimiento Mensual"] = df_pasiva["Evolución Capital Invertido"].pct_change().dropna()
    df_pasiva["Rendimiento Mensual Acumulado"] = (df_pasiva["Rendimiento Mensual"] + 1).cumprod() - 1

    capital_invertido = df_pasiva_info["Costo de Compra Total"].sum()
    df_pasiva_metricas = pd.DataFrame({"Capital Inicial": initial_capital, "Capital Invertido": capital_invertido,
                                        "Efectivo": initial_capital - capital_invertido,
                                        "Capital Final": initial_capital - capital_invertido +
                                                         df_pasiva["Evolución Capital Invertido"][-1],
                                        "Rendimiento Efectivo %": df_pasiva["Rendimiento Mensual Acumulado"][-1] * 100},
                                       index=["Estrategia Pasiva"])

    return df_pasiva_info, df_pasiva, df_pasiva_metricas
