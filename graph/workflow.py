from typing import TypedDict, Dict, Any

from langgraph.graph import StateGraph, START, END

from trading_agents.market_agent import market_node
from trading_agents.news_agent import news_node
from trading_agents.strategy_agent import strategy_node


class TradingState(TypedDict):
    symbol: str
    interval: str

    # Market Agent
    market_data: Dict[str, Any]
    signal: str

    # News Agent
    news: list
    news_analysis: Dict[str, Any]

    # Strategy Agent
    strategy_decision: Dict[str, Any]


graph_builder = StateGraph(TradingState)

# Nodes
graph_builder.add_node("market_agent", market_node)
graph_builder.add_node("news_agent", news_node)
graph_builder.add_node("strategy_agent", strategy_node)

# Parallel execution
graph_builder.add_edge(START, "market_agent")
graph_builder.add_edge(START, "news_agent")

# Join branches
graph_builder.add_edge("market_agent", "strategy_agent")
graph_builder.add_edge("news_agent", "strategy_agent")

# End
graph_builder.add_edge("strategy_agent", END)

graph = graph_builder.compile()