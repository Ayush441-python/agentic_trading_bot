# ⚡ Autonomous Agentic Crypto Trading Bot

An enterprise-grade, multi-agent algorithmic trading system engineered with **LangGraph**, **FastAPI**, **Streamlit**, and **LLaMA-3.3-70B**. The system synthesizes quantitative Smart Money Concepts (SMC) technical analysis with real-time NLP sentiment analysis to generate high-confidence trading decisions with dynamic risk management (Stop-Loss / Take-Profit).

---

## 🌟 Resume Bullet Points (Copy & Paste for Your Resume)

> **Tip:** Pick 2 to 4 bullet points that best align with the roles you are targeting (AI Engineer, Full-Stack Machine Learning Engineer, Backend / Python Developer, or Quantitative Developer).

### 🤖 AI / Multi-Agent & LLM Focus
- **Architected an Autonomous Multi-Agent Trading Engine** using **LangGraph** and **LangChain Core**, orchestrating asynchronous specialized agents (Market Structure, Financial NLP, and Strategy Synthesizer) with state machines and cyclic graph routing.
- **Engineered Real-Time Financial Sentiment Pipeline** leveraging **LLaMA-3.3-70B** via Groq API to ingest CoinDesk RSS feeds, featuring a zero-dependency NLP heuristic fallback ensuring 100% uptime without external API failures.
- **Implemented Smart Money Concepts (SMC) Algorithmic Engine** in Python/Pandas detecting Break of Structure (BOS), Order Blocks (OB), and Fair Value Gaps (FVG) from live Binance klines to identify institutional liquidity sweeps.

### ⚙️ Backend & Full-Stack Systems Focus
- **Built Production-Grade REST APIs with FastAPI & Pydantic**, serving endpoints for multi-agent inference (`/api/analyze`), live Binance OHLCV streaming (`/api/market-data`), and cryptocurrency news syndication (`/api/news`) with auto-generated OpenAPI / Swagger documentation.
- **Developed Interactive Quantitative Trading Terminal in Streamlit & Plotly**, delivering real-time interactive multi-pane candlestick charts, volume profile overlays, institutional structure inspections, and dual-mode execution (FastAPI REST vs. In-process embedded).
- **Designed Automated Dynamic Risk Management Engine** calculating algorithmic Stop-Loss (SL) and Take-Profit (TP) targets based on institutional swing highs/lows, enforcing strict 1:2 risk-to-reward ratios and confidence scoring thresholds.

---

## 🏛️ System Architecture

```
                                      ┌────────────────────────────────┐
                                      │   User / Streamlit Dashboard   │
                                      │            (app.py)            │
                                      └──────────────┬─────────────────┘
                                                     │ HTTP REST / Embedded
                                      ┌──────────────▼─────────────────┐
                                      │      FastAPI REST Server       │
                                      │           (main.py)            │
                                      └──────────────┬─────────────────┘
                                                     │ Invokes
                                      ┌──────────────▼─────────────────┐
                                      │   LangGraph Workflow Engine    │
                                      │      (graph/workflow.py)       │
                                      └──────────────┬─────────────────┘
                                                     │
                             ┌───────────────────────┴───────────────────────┐
                             │ Parallel Execution                            │
                             ▼                                               ▼
             ┌───────────────────────────────┐               ┌───────────────────────────────┐
             │       Market Agent            │               │          News Agent           │
             │ (Smart Money Concepts + Tech) │               │      (LLaMA-3.3-70B NLP)      │
             ├───────────────────────────────┤               ├───────────────────────────────┤
             │ • Binance API (OHLCV)         │               │ • CoinDesk RSS Feeds          │
             │ • Break of Structure (BOS)    │               │ • Groq LLaMA-3.3-70B LLM      │
             │ • Order Blocks (OB)           │               │ • Zero-downtime NLP Heuristic │
             │ • Fair Value Gaps (FVG)       │               │ • Sentiment Scoring (-1 to +1)│
             │ • RSI (14), SMA (20/50)       │               │ • Market Impact & Risk Tags   │
             └───────────────┬───────────────┘               └───────────────┬───────────────┘
                             │                                               │
                             └───────────────────────┬───────────────────────┘
                                                     ▼
                                     ┌───────────────────────────────┐
                                     │        Strategy Agent         │
                                     │     (Consensus & Risk)        │
                                     ├───────────────────────────────┤
                                     │ • Synthesizes Market & News   │
                                     │ • Generates BUY / SELL / HOLD │
                                     │ • Confidence Scoring (0-100%) │
                                     │ • Dynamic Stop-Loss & Target  │
                                     │ • Institutional Trade Logic   │
                                     └───────────────────────────────┘
```

---

## 🚀 Key Features

| Component | Technical Implementation & Capability |
| :--- | :--- |
| **Stateful Agent Orchestration** | Powered by **LangGraph** `StateGraph`, enabling parallel execution branches joined into a consensus strategy node. |
| **Smart Money Concepts (SMC)** | Algorithmic detection of **Break of Structure (BOS)**, **Bullish/Bearish Order Blocks (OB)**, and **Fair Value Gaps (FVG)**. |
| **Financial LLM Sentiment** | Ingests live news feeds, transforming raw articles into structured JSON market sentiment with **LLaMA-3.3-70B** and fallback heuristics. |
| **Dynamic Risk Parameters** | Automated Stop Loss and Take Profit computations adhering to institutional risk-to-reward ratios (1:2). |
| **FastAPI REST Microservice** | Asynchronous, typed endpoints with Pydantic validation, CORS middleware, and Swagger UI at `/docs`. |
| **Interactive Plotly Terminal** | Streamlit UI featuring dual-axis candlestick + volume charts, metric cards, and agent telemetry breakdown tabs. |
| **Dual Connectivity Mode** | Toggle between **FastAPI REST API** or **In-process Local Graph** with automatic backend health detection. |

---

## 🛠️ Tech Stack

- **Multi-Agent & LLM Framework**: LangGraph, LangChain Core, LangChain Groq (LLaMA-3.3-70B-Versatile)
- **Backend API**: FastAPI, Uvicorn, Pydantic, Requests
- **Frontend Dashboard**: Streamlit, Plotly Graph Objects, HTML/CSS
- **Quantitative & Financial Data**: Binance Public Spot API, CCXT, Pandas, NumPy, TA, Feedparser
- **Environment & Config**: Python-dotenv, PyYAML

---

## 📂 Project Structure

```
agentic_trading_bot/
│
├── main.py                     # FastAPI REST API Backend (Endpoints: /api/analyze, /market-data, /news)
├── app.py                      # Interactive Streamlit Trading Dashboard with Plotly & Multi-Agent UI
├── requirements.txt            # Project dependencies
├── .env.example                # Example environment variables (GROQ_API_KEY)
│
├── graph/
│   └── workflow.py             # LangGraph state machine orchestrating Market, News, & Strategy nodes
│
├── trading_agents/
│   ├── market_agent.py         # Market Agent (BOS, OB, FVG, RSI, SMA calculation & Binance data)
│   ├── news_agent.py           # News Agent (CoinDesk RSS + LLaMA-3.3-70B / Fallback NLP Sentiment)
│   └── strategy_agent.py       # Strategy Agent (Signal consensus, Confidence %, Stop-Loss & Take-Profit)
│
├── strategies/
│   ├── market_structure.py     # Swing Highs/Lows and Break of Structure (BOS) detection
│   ├── order_block.py          # Institutional Order Block (OB) identification
│   └── fvg.py                  # Fair Value Gap (FVG) imbalance calculation
│
└── data/
    ├── market_data.py          # Real-time Binance Kline/Candle data fetcher
    └── news_data.py            # Real-time CoinDesk RSS feed parser
```

---

## ⚡ Quickstart Guide

### 1. Clone & Set Up Environment

```bash
git clone https://github.com/<your-username>/agentic_trading_bot.git
cd agentic_trading_bot
python -m venv venv
# Windows:
.\venv\Scripts\activate
# Linux/macOS:
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Configure Environment Variables (Optional)

Create a `.env` file in the root directory:

```bash
cp .env.example .env
```

Add your Groq API key:
```env
GROQ_API_KEY=your_groq_api_key_here
```
*(Note: If you do not have a Groq key, the application will automatically switch to built-in heuristic NLP sentiment analysis without errors.)*

---

### 3. Launching the System

You can run the backend and frontend simultaneously:

#### Terminal 1: Launch FastAPI Backend
```bash
uvicorn main:app --reload --port 8000
```
- API Base: `http://localhost:8000`
- Swagger Interactive Docs: `http://localhost:8000/docs`
- Health Check: `http://localhost:8000/health`

#### Terminal 2: Launch Streamlit Dashboard
```bash
streamlit run app.py
```
- Dashboard URL: `http://localhost:8501`

---

## 📡 API Reference

### `POST /api/analyze`
Executes complete multi-agent analysis on a selected trading pair.

**Request Body:**
```json
{
  "symbol": "BTCUSDT",
  "interval": "1h",
  "groq_api_key": "optional_groq_key"
}
```

**Response Example:**
```json
{
  "success": true,
  "symbol": "BTCUSDT",
  "interval": "1h",
  "signal": "SELL",
  "strategy_decision": {
    "action": "SELL",
    "confidence": 70,
    "market_signal": "SELL",
    "news_signal": "HOLD",
    "market_price": 81207.66,
    "stop_loss": 82831.81,
    "take_profit": 77959.35,
    "risk_reward": "1:2",
    "reasoning": "Market Signal is SELL based on Smart Money Concepts (BOS/OrderBlocks/FVG)..."
  }
}
```

### `GET /api/market-data?symbol=BTCUSDT&interval=1h&limit=100`
Fetches live OHLCV candle records from Binance.

### `GET /api/news?limit=10`
Fetches latest CoinDesk articles for cryptocurrency market sentiment.

---

## 📜 License
MIT License. Created for algorithmic trading research and multi-agent systems portfolio demonstration.
