from typing import TypedDict
import json

from dotenv import load_dotenv
from langchain_core.tools import tool
from langchain_groq import ChatGroq

from data.news_data import get_coindesk_news

import os
import re

load_dotenv()


def analyze_news_fallback(news_items: list) -> dict:
    bullish_keywords = ["bull", "surge", "gain", "high", "rally", "outrun", "jump", "record", "inflow", "boost", "support", "growth", "positive"]
    bearish_keywords = ["bear", "crash", "fall", "drop", "hack", "ban", "loss", "low", "outflow", "regulatory", "crackdown", "slump", "negative", "remove"]
    
    score = 0
    total_words = 0
    titles = [item.get("title", "") for item in news_items[:10]]
    combined_text = " ".join(titles).lower()
    
    for word in bullish_keywords:
        score += combined_text.count(word)
    for word in bearish_keywords:
        score -= combined_text.count(word)
        
    if score > 1:
        sentiment = "bullish"
        signal = "BUY"
    elif score < -1:
        sentiment = "bearish"
        signal = "SELL"
    else:
        sentiment = "neutral"
        signal = "HOLD"
        
    summary = f"Aggregated {len(news_items)} market news items. Net market tone is {sentiment}."
    return {
        "summary": summary,
        "sentiment": sentiment,
        "importance": 7 if abs(score) > 2 else 4,
        "market_impact": f"Heuristic sentiment analysis score: {score:+d}",
        "risks": ["Crypto market volatility", "Regulatory developments"],
        "signal": signal,
        "mode": "Heuristic (Provide GROQ_API_KEY for deep LLM analysis)"
    }


def get_llm():
    api_key = os.getenv("GROQ_API_KEY")
    if api_key and api_key.strip():
        return ChatGroq(
            model="llama-3.3-70b-versatile",
            api_key=api_key.strip()
        )
    return None


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
    llm = get_llm()

    if not llm:
        print("GROQ_API_KEY not configured or empty. Using news analysis fallback.")
        analysis = analyze_news_fallback(news)
        return {
            "news": news,
            "news_analysis": analysis
        }

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

    try:
        response = llm.invoke(prompt)
        print("\n=== RAW LLM RESPONSE ===")
        print(response.content)
        print("========================\n")

        content = response.content.strip()
        if content.startswith("```json"):
            content = content.replace("```json", "").replace("```", "").strip()
        elif content.startswith("```"):
            content = content.replace("```", "").strip()

        analysis = json.loads(content)
    except Exception as e:
        print(f"LLM or JSON Parse Error: {e}. Falling back to heuristic analysis.")
        analysis = analyze_news_fallback(news)

    return {
        "news": news,
        "news_analysis": analysis
    }

