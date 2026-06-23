import requests
import pandas as pd

def get_market_data(symbol="BTCUSDT", interval="1h", limit=1000):

    url = "https://api.binance.com/api/v3/klines"

    params = {
        "symbol": symbol,
        "interval": interval,
        "limit": limit
    }

    response = requests.get(url, params=params)
    response.raise_for_status()

    data = response.json()

    df = pd.DataFrame(
        data,
        columns=[
            "open_time",
            "open",
            "high",
            "low",
            "close",
            "volume",
            "close_time",
            "quote_asset_volume",
            "num_trades",
            "taker_buy_base_volume",
            "taker_buy_quote_volume",
            "ignore"
        ]
    )

    df = df[["open_time", "open", "high", "low", "close", "volume"]]

    df["open_time"] = pd.to_datetime(
        df["open_time"],
        unit="ms"
    )

    numeric_cols = ["open", "high", "low", "close", "volume"]

    df[numeric_cols] = df[numeric_cols].astype(float)

    return df