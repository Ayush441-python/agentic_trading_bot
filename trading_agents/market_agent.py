from typing import TypedDict, Dict, Any

from langchain_core.tools import tool

from strategies.market_structure import MarketStructure
from strategies.order_block import OrderBlock
from strategies.fvg import FVG

from data.market_data import get_market_data


@tool
def generate_signal(
    symbol: str = "BTCUSDT",
    interval: str = "1h"
):
    """
    Generate trading signal using:
    - Market Structure (BOS)
    - Order Blocks
    - Fair Value Gaps
    """

    df = get_market_data(
        symbol=symbol,
        interval=interval
    )

    # Market Structure
    swing_highs, swing_lows = MarketStructure.find_swings(df)

    bos = MarketStructure.detect_bos(
        df,
        swing_highs,
        swing_lows
    )

    # Smart Money Concepts
    order_blocks = OrderBlock.detect(df)
    fvgs = FVG.detect(df)

    signal = "NEUTRAL"

    if bos:
        latest_bos = bos[-1]
        print("Latest BOS:", latest_bos)
        bos_type = latest_bos.get("type", "").lower()
        direction = latest_bos.get("direction", "").lower()

        if "bullish" in bos_type or direction == "bullish":
            signal = "BUY"
        elif "bearish" in bos_type or direction == "bearish":
            signal = "SELL"
        else:
            print(
                f"Warning: direction/type key not resolved. "
                f"Received: {latest_bos}"
            )

    # Compute key technical indicators
    close_s = df["close"]
    high_s = df["high"]
    low_s = df["low"]

    # Simple & Exponential Moving Averages
    df["sma_20"] = close_s.rolling(window=20).mean()
    df["sma_50"] = close_s.rolling(window=50).mean()
    df["ema_20"] = close_s.ewm(span=20, adjust=False).mean()

    # RSI (14)
    delta = close_s.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    rs = gain / loss.replace(0, 0.00001)
    df["rsi_14"] = 100 - (100 / (1 + rs))

    latest_rsi = round(float(df["rsi_14"].iloc[-1]), 2) if not df["rsi_14"].isna().iloc[-1] else 50.0
    latest_sma_20 = round(float(df["sma_20"].iloc[-1]), 2) if not df["sma_20"].isna().iloc[-1] else float(df["close"].iloc[-1])
    latest_sma_50 = round(float(df["sma_50"].iloc[-1]), 2) if not df["sma_50"].isna().iloc[-1] else float(df["close"].iloc[-1])

    # Convert recent candles to lightweight dict for charting
    recent_candles = df.tail(120)[["open_time", "open", "high", "low", "close", "volume"]].copy()
    recent_candles["open_time"] = recent_candles["open_time"].astype(str)
    candles_records = recent_candles.to_dict(orient="records")

    return {
        "symbol": symbol,
        "interval": interval,
        "signal": signal,
        "latest_price": float(df["close"].iloc[-1]),
        "change_24h_pct": round(float((df["close"].iloc[-1] - df["close"].iloc[0]) / df["close"].iloc[0] * 100), 2),
        "high_24h": float(df["high"].max()),
        "low_24h": float(df["low"].min()),
        "indicators": {
            "rsi_14": latest_rsi,
            "sma_20": latest_sma_20,
            "sma_50": latest_sma_50,
            "trend": "Bullish" if latest_sma_20 > latest_sma_50 else "Bearish"
        },
        "bos": bos[-5:] if bos else [],
        "order_blocks": order_blocks[-5:] if order_blocks else [],
        "fvgs": fvgs[-5:] if fvgs else [],
        "recent_candles": candles_records
    }


class MARKETState(TypedDict):
    symbol: str
    interval: str
    market_data: Dict[str, Any]
    signal: str


def market_node(state: MARKETState):

    try:

        result = generate_signal.invoke({
            "symbol": state["symbol"],
            "interval": state["interval"]
        })

        return {
            **state,
            "market_data": result,
            "signal": result["signal"]
        }

    except Exception as e:

        print(f"Market Agent Error: {e}")

        return {
            **state,
            "market_data": {},
            "signal": "ERROR"
        }

