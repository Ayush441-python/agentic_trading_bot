from typing import TypedDict, Dict, Any


class TradingState(TypedDict):
    symbol: str
    interval: str

    market_data: Dict[str, Any]
    signal: str

    news: list
    news_analysis: Dict[str, Any]

    strategy_decision: Dict[str, Any]


def strategy_node(state: TradingState):

    market_signal = state["signal"]

    news_signal = state["news_analysis"]["signal"]

    if market_signal == "BUY" and news_signal == "BUY":

        action = "BUY"
        confidence = 90

    elif market_signal == "SELL" and news_signal == "SELL":

        action = "SELL"
        confidence = 90

    elif market_signal == "BUY" and news_signal == "HOLD":

        action = "BUY"
        confidence = 70

    elif market_signal == "SELL" and news_signal == "HOLD":

        action = "SELL"
        confidence = 70

    elif market_signal == "NEUTRAL":

        action = "HOLD"
        confidence = 50

    else:

        action = "HOLD"
        confidence = 40

    return {
        "strategy_decision": {
            "action": action,
            "confidence": confidence,
            "market_signal": market_signal,
            "news_signal": news_signal,
            "market_price": state["market_data"]["latest_price"]
        }
    }


