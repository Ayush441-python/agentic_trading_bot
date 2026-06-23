from typing import TypedDict
import json

from dotenv import load_dotenv
from langchain_core.tools import tool
from langchain_groq import ChatGroq

from data.news_data import get_coindesk_news

load_dotenv()


llm = ChatGroq(
    model="llama-3.3-70b-versatile"
)


@tool
def stock_news():
    """
    Fetch latest Bitcoin and cryptocurrency news.
    """
    return get_coindesk_news()


class MARKETState(TypedDict):
    news: list
    news_analysis: dict


def news_node(state: MARKETState):

    news = stock_news.invoke({})

    prompt = f"""
    You are a professional Bitcoin News Analyst.

    Analyze the following crypto news and determine
    the likely market impact.

    Return ONLY valid JSON.

    Do NOT include:
    - Markdown
    - Explanations
    - ```json blocks
    - Any text outside the JSON

    News:
    {news}

    Output format:

    {{
        "summary": "short summary",
        "sentiment": "bullish|bearish|neutral",
        "importance": 1,
        "market_impact": "market impact description",
        "risks": ["risk1", "risk2"],
        "signal": "BUY|SELL|HOLD"
    }}
    """

    response = llm.invoke(prompt)

    print("\n=== RAW LLM RESPONSE ===")
    print(response.content)
    print("========================\n")

    try:

        content = response.content.strip()

        if content.startswith("```json"):
            content = content.replace("```json", "").replace("```", "").strip()

        elif content.startswith("```"):
            content = content.replace("```", "").strip()

        analysis = json.loads(content)

    except Exception as e:

        print(f"JSON Parse Error: {e}")

        analysis = {
            "summary": "Failed to parse LLM response",
            "sentiment": "neutral",
            "importance": 0,
            "market_impact": "unknown",
            "risks": [],
            "signal": "HOLD"
        }

    return {
        "news": news,
        "news_analysis": analysis
    }

