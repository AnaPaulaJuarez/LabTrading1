
import pandas as pd
pd.set_option('display.float_format', lambda x: '%.4f' % x)
import yfinance as yf
import numpy as np

def get_historical_prices(start: str, end: str, positions: str):
    
    # Crear un diccionario de símbolos para descargar y establecer una lista de filtros.
    symbol_weights = {}
    filter_symbols = ["KOFL", "KOFUBL", "USD", "MXN", "BSMXB", "NMKA"]
    
    # Agregar cada símbolo y su peso a los símbolos a descargar si el símbolo no está en la lista de filtros.
    for i in range(len(positions)):
        symbol = positions["Ticker"][i]
        weight = positions["Peso (%)"][i] / 100
        if symbol not in filter_symbols:
            symbol_weights[symbol.replace("*", "").replace(".", "-") + ".MX"] = weight
            
    # Descargar los precios de los símbolos y almacenarlos en un DataFrame.
    prices_df = pd.DataFrame()
    for symbol, weight in symbol_weights.items():
        prices_df[symbol] = yf.download(symbol, start=start, end=end, progress=False)["Adj Close"]
        
    # Eliminar las columnas con valores faltantes y crear un DataFrame con los precios mensuales.
    prices_df.dropna(axis=1, inplace=True)
    monthly_prices_df = pd.DataFrame(columns=prices_df.columns)
    for i in range(len(prices_df)):
        current_month = prices_df.index[i].month
        next_month = prices_df.index[i + 1].month if i < len(prices_df) - 1 else None
        if next_month is None or current_month != next_month:
            monthly_prices_df.loc[prices_df.index[i], :] = prices_df.iloc[i, :]
            
    # Devolver los precios diarios, mensuales y los símbolos utilizados.
    return prices_df, monthly_prices_df, symbol_weights


def my_investment_strategy(prices_data: pd.DataFrame, ticker_weights: dict, initial_capital: float, commission: float):
    
    """
    my_investment_strategy is a function that implements a passive investment strategy using the provided data.
    """
    
    # Create a DataFrame to store initial position information
    df_positions = pd.DataFrame(index=prices_data.columns,
    columns=["Quantity of Shares", "Gross Purchase Cost", "Commission", "Total Purchase Cost"])
    
    for ticker in prices_data.columns:
        # Calculate the quantity of shares to buy for each ticker
        share_quantity = np.floor((initial_capital * ticker_weights[ticker]) /
        (prices_data[ticker][0] * (1 + commission)))
        
        # Save the information in the DataFrame
        df_positions.loc[ticker, "Quantity of Shares"] = share_quantity
        df_positions.loc[ticker, "Gross Purchase Cost"] = share_quantity * prices_data[ticker][0]
        df_positions.loc[ticker, "Commission"] = share_quantity * prices_data[ticker][0] * commission
        df_positions.loc[ticker, "Total Purchase Cost"] = share_quantity * prices_data[ticker][0] * (1 + commission)
        df_positions.loc[ticker, "Weight"] = (share_quantity * prices_data[ticker][0]) / initial_capital

    # Create a DataFrame to store information on investment evolution
    df_evolution = pd.DataFrame(index=prices_data.index,
                                columns=["Invested Capital Evolution", "Monthly Return",                                      "Accumulated Monthly Return"])

    # Perform the backtest
    df_evolution["Invested Capital Evolution"] = np.dot(prices_data * (1 - commission), df_positions["Quantity of Shares"])
    df_evolution["Monthly Return"] = df_evolution["Invested Capital Evolution"].pct_change().dropna()
    df_evolution["Accumulated Monthly Return"] = (df_evolution["Monthly Return"] + 1).cumprod() - 1

    # Calculate investment strategy metrics
    invested_capital = df_positions["Total Purchase Cost"].sum()
    df_metrics = pd.DataFrame({"Initial Capital": initial_capital, "Invested Capital": invested_capital,
                                        "Cash": initial_capital - invested_capital,
                                        "Final Capital": initial_capital - invested_capital +
                                                        df_evolution["Invested Capital Evolution"][-1],
                                        "Effective Return %": df_evolution["Accumulated Monthly Return"][-1] * 100},
                                    index=["My Investment Strategy"])

    return df_positions, df_evolution, df_metrics

