import os
from typing import Optional
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from graph.workflow import graph
from data.market_data import get_market_data
from data.news_data import get_coindesk_news
from trading_agents.market_agent import generate_signal

# ---------------------------------------------
# FastAPI App Initialization
# ---------------------------------------------
app = FastAPI(
    title="Autonomous Agentic Trading Bot API",
    description="FastAPI Backend for Market Structure, News Sentiment, and Multi-Agent Trading Strategy Orchestration",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Enable CORS for frontend/dashboard access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------------------------
# Pydantic Request & Response Models
# ---------------------------------------------
class AnalyzeRequest(BaseModel):
    symbol: str = Field(default="BTCUSDT", description="Crypto trading pair (e.g. BTCUSDT, ETHUSDT)")
    interval: str = Field(default="1h", description="Candle timeframe (e.g. 15m, 1h, 4h, 1d)")
    groq_api_key: Optional[str] = Field(default=None, description="Optional Groq API key for LLaMA-3.3-70B news analysis")


# ---------------------------------------------
# API Endpoints
# ---------------------------------------------
@app.get("/", tags=["Health"])
def root():
    return {
        "status": "online",
        "service": "Agentic Trading Bot API",
        "version": "1.0.0",
        "endpoints": {
            "health": "/health",
            "analyze": "POST /api/analyze",
            "market_data": "GET /api/market-data",
            "news": "GET /api/news",
            "docs": "/docs"
        }
    }


@app.get("/health", tags=["Health"])
def health_check():
    return {"status": "healthy"}


@app.post("/api/analyze", tags=["Trading Agents"])
def run_analysis(request: AnalyzeRequest):
    """
    Run full multi-agent trading analysis pipeline:
    - Market Structure Agent (SMC: BOS, OB, FVG, Indicators)
    - News & Sentiment Agent (CoinDesk RSS + LLaMA-3.3-70B or Heuristic NLP)
    - Strategy Agent (Risk assessment, Action, SL/TP calculation)
    """
    try:
        # If user provides groq_api_key in request, temporarily set in environment
        if request.groq_api_key and request.groq_api_key.strip():
            os.environ["GROQ_API_KEY"] = request.groq_api_key.strip()

        initial_state = {
            "symbol": request.symbol.upper(),
            "interval": request.interval,
            "market_data": {},
            "signal": "",
            "news": [],
            "news_analysis": {},
            "strategy_decision": {}
        }

        result = graph.invoke(initial_state)

        return {
            "success": True,
            "symbol": result.get("symbol"),
            "interval": result.get("interval"),
            "signal": result.get("signal"),
            "market_data": result.get("market_data"),
            "news_analysis": result.get("news_analysis"),
            "news": result.get("news", []),
            "strategy_decision": result.get("strategy_decision")
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")


@app.get("/api/market-data", tags=["Market Data"])
def fetch_market_data(
    symbol: str = Query("BTCUSDT", description="Crypto trading pair"),
    interval: str = Query("1h", description="Candle timeframe"),
    limit: int = Query(100, ge=10, le=1000, description="Number of candles")
):
    """
    Directly fetch live OHLCV candle data from Binance.
    """
    try:
        df = get_market_data(symbol=symbol.upper(), interval=interval, limit=limit)
        df["open_time"] = df["open_time"].astype(str)
        return {
            "symbol": symbol.upper(),
            "interval": interval,
            "count": len(df),
            "candles": df.to_dict(orient="records")
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch market data: {str(e)}")


@app.get("/api/news", tags=["News Data"])
def fetch_news(limit: int = Query(10, ge=1, le=50, description="Max news articles to fetch")):
    """
    Directly fetch latest cryptocurrency news feed.
    """
    try:
        news = get_coindesk_news(limit=limit)
        return {
            "count": len(news),
            "articles": news
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch news: {str(e)}")


# ---------------------------------------------
# Main Runner for standalone script execution
# ---------------------------------------------
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
