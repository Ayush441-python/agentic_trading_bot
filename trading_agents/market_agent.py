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

        direction = latest_bos.get("direction")

        if direction == "bullish":
            signal = "BUY"

        elif direction == "bearish":
            signal = "SELL"

        else:
            print(
                f"Warning: direction key not found. "
                f"Received: {latest_bos}"
            )

    return {
        "symbol": symbol,
        "interval": interval,
        "signal": signal,
        "latest_price": float(df["close"].iloc[-1]),
        "bos": bos[-5:] if bos else [],
        "order_blocks": order_blocks[-5:] if order_blocks else [],
        "fvgs": fvgs[-5:] if fvgs else []
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

