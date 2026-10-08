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

    market_price = 0.0
    if isinstance(state.get("market_data"), dict):
        market_price = state["market_data"].get("latest_price", 0.0)

    # Dynamic risk calculations based on action
    stop_loss = 0.0
    take_profit = 0.0
    risk_reward = "1:2"

    if market_price > 0:
        if action == "BUY":
            stop_loss = round(market_price * 0.98, 2)
            take_profit = round(market_price * 1.04, 2)
        elif action == "SELL":
            stop_loss = round(market_price * 1.02, 2)
            take_profit = round(market_price * 0.96, 2)
        else:
            stop_loss = round(market_price * 0.99, 2)
            take_profit = round(market_price * 1.01, 2)

    reasoning = (
        f"Market Signal is {market_signal} based on Smart Money Concepts (BOS/OrderBlocks/FVG). "
        f"News sentiment analysis returned {news_signal}. "
        f"Synthesized strategic action: {action} with {confidence}% confidence."
    )

    return {
        "strategy_decision": {
            "action": action,
            "confidence": confidence,
            "market_signal": market_signal,
            "news_signal": news_signal,
            "market_price": market_price,
            "stop_loss": stop_loss,
            "take_profit": take_profit,
            "risk_reward": risk_reward,
            "reasoning": reasoning
        }
    }


