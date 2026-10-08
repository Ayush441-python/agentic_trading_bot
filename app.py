import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import requests
import os

from graph.workflow import graph

# -------------------------------
# Page Config & Custom Styling
# -------------------------------
st.set_page_config(
    page_title="AI Agentic Trading Bot",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for modern clean aesthetic
st.markdown("""
<style>
    .metric-card {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 10px;
        padding: 16px;
        margin-bottom: 12px;
    }
    .badge-buy {
        background-color: #00c853;
        color: white;
        padding: 4px 12px;
        border-radius: 16px;
        font-weight: 600;
        display: inline-block;
    }
    .badge-sell {
        background-color: #ff3d00;
        color: white;
        padding: 4px 12px;
        border-radius: 16px;
        font-weight: 600;
        display: inline-block;
    }
    .badge-hold {
        background-color: #ffa000;
        color: white;
        padding: 4px 12px;
        border-radius: 16px;
        font-weight: 600;
        display: inline-block;
    }
</style>
""", unsafe_allow_html=True)

# -------------------------------
# Header
# -------------------------------
st.title("⚡ Autonomous Agentic Crypto Trading Bot")
st.caption("Multi-Agent Architecture: Smart Money Market Structure Agent + News Sentiment Agent + Strategic Risk Agent")

# -------------------------------
# Sidebar Configuration
# -------------------------------
with st.sidebar:
    st.header("⚙️ Execution Mode")
    
    execution_mode = st.radio(
        "Backend Connection",
        ["FastAPI Server (REST API)", "Direct Embedded Agents (Local)"],
        index=0,
        help="Choose whether Streamlit communicates with the FastAPI backend over HTTP or runs agents in-process."
    )

    default_backend = os.environ.get("BACKEND_URL", "http://localhost:8000")
    api_url = default_backend
    if execution_mode.startswith("FastAPI"):
        api_url = st.text_input("FastAPI Base URL", value=default_backend)
        try:
            health_res = requests.get(f"{api_url}/health", timeout=2.5)
            if health_res.status_code == 200:
                st.success("🟢 FastAPI Backend Online")
            else:
                st.warning("🟡 FastAPI reached but status unexpected")
        except Exception:
            st.warning("⚠️ FastAPI server not detected. (Start it via `python main.py` or switch to Direct Embedded mode)")

    st.markdown("---")
    st.header("📊 Market Pair & Timeframe")
    
    symbol = st.selectbox(
        "Trading Pair",
        ["BTCUSDT", "ETHUSDT", "SOLUSDT", "BNBUSDT", "XRPUSDT", "ADAUSDT"],
        index=0
    )
    
    interval = st.selectbox(
        "Timeframe",
        ["15m", "1h", "4h", "1d"],
        index=1
    )

    st.markdown("---")
    st.subheader("🔑 AI Provider (Groq)")
    groq_input = st.text_input(
        "GROQ_API_KEY (Optional)",
        type="password",
        value=os.getenv("GROQ_API_KEY", ""),
        help="Optional: Deep analysis via LLaMA-3.3-70B. If empty, built-in heuristic NLP sentiment is automatically utilized."
    )
    if groq_input:
        os.environ["GROQ_API_KEY"] = groq_input.strip()

    st.markdown("---")
    analyze_btn = st.button("🚀 Run Multi-Agent Analysis", use_container_width=True, type="primary")

    st.markdown("### 🤖 Agents in Workflow")
    st.markdown("""
    1. **Market Agent**: Live Binance OHLCV, Swing High/Low, Break of Structure (BOS), Order Blocks (OB), Fair Value Gaps (FVG), RSI & SMAs.
    2. **News Agent**: CoinDesk crypto news feed analyzed with LLaMA-3.3-70B or NLP heuristic sentiment score.
    3. **Strategy Agent**: Synthesizes market momentum + fundamental sentiment, computing action, stop loss, and take profit.
    """)

# -------------------------------
# Helper function for charts
# -------------------------------
def render_market_chart(candles, bos_list, ob_list, fvg_list):
    if not candles:
        return None
    
    df = pd.DataFrame(candles)
    df["open_time"] = pd.to_datetime(df["open_time"])
    
    fig = make_subplots(
        rows=2, cols=1,
        shared_xaxes=True,
        vertical_spacing=0.04,
        row_heights=[0.75, 0.25],
        subplot_titles=("Price Action & SMC Annotations", "Volume")
    )
    
    # Candlestick chart
    fig.add_trace(
        go.Candlestick(
            x=df["open_time"],
            open=df["open"],
            high=df["high"],
            low=df["low"],
            close=df["close"],
            name="OHLC",
            increasing_line_color="#26a69a",
            decreasing_line_color="#ef5350"
        ),
        row=1, col=1
    )
    
    # Volume chart
    colors = ['#26a69a' if row['close'] >= row['open'] else '#ef5350' for _, row in df.iterrows()]
    fig.add_trace(
        go.Bar(
            x=df["open_time"],
            y=df["volume"],
            name="Volume",
            marker_color=colors,
            opacity=0.7
        ),
        row=2, col=1
    )
    
    fig.update_layout(
        height=520,
        margin=dict(l=20, r=20, t=30, b=20),
        xaxis_rangeslider_visible=False,
        template="plotly_dark",
        showlegend=False
    )
    return fig

# -------------------------------
# Helper function for Agent Execution
# -------------------------------
def execute_agents(symbol: str, interval: str, groq_key: str, use_api: bool, base_url: str):
    """Executes trading agents either via FastAPI REST endpoints or directly via LangGraph."""
    if use_api:
        endpoint = f"{base_url.rstrip('/')}/api/analyze"
        payload = {
            "symbol": symbol,
            "interval": interval,
            "groq_api_key": groq_key or None
        }
        resp = requests.post(endpoint, json=payload, timeout=45)
        resp.raise_for_status()
        data = resp.json()
        return data
    else:
        state = {
            "symbol": symbol,
            "interval": interval,
            "market_data": {},
            "signal": "",
            "news": [],
            "news_analysis": {},
            "strategy_decision": {}
        }
        return graph.invoke(state)

# -------------------------------
# Main Analysis Execution
# -------------------------------
if analyze_btn:
    use_api = execution_mode.startswith("FastAPI")
    with st.spinner(f"Coordinating agents for {symbol} ({interval}) via {'FastAPI' if use_api else 'Local Engine'}..."):
        try:
            result = execute_agents(symbol, interval, groq_input, use_api, api_url)
            st.session_state["last_result"] = result
            st.session_state["analyzed_symbol"] = symbol
            st.session_state["analyzed_interval"] = interval
            st.session_state["executed_via"] = "FastAPI Backend" if use_api else "Direct Embedded"
        except Exception as e:
            st.error(f"Execution Error: {e}")
            if use_api:
                st.info("💡 You can run the FastAPI backend with: `python main.py`, or switch 'Backend Connection' in the sidebar to 'Direct Embedded Agents'.")

# Display results if present in session
if "last_result" in st.session_state:
    result = st.session_state["last_result"]
    symbol = st.session_state.get("analyzed_symbol", symbol)
    interval = st.session_state.get("analyzed_interval", interval)
    executed_via = st.session_state.get("executed_via", "Direct Embedded")
    
    market_data = result.get("market_data", {})
    signal = result.get("signal", "N/A")
    strategy = result.get("strategy_decision", {})
    news_analysis = result.get("news_analysis", {})
    news = result.get("news", [])
    
    action = strategy.get("action", "HOLD")
    confidence = strategy.get("confidence", 50)
    market_price = strategy.get("market_price", market_data.get("latest_price", 0.0))
    stop_loss = strategy.get("stop_loss", 0.0)
    take_profit = strategy.get("take_profit", 0.0)
    risk_reward = strategy.get("risk_reward", "1:2")
    indicators = market_data.get("indicators", {})

    st.success(f"Analysis successfully completed for {symbol} on {interval} timeframe via {executed_via}!")

    # Top Key Metrics Bar
    m1, m2, m3, m4, m5 = st.columns(5)
    m1.metric("Asset Pair", symbol)
    m2.metric("Latest Price", f"${market_price:,.2f}" if isinstance(market_price, (int, float)) else str(market_price))
    m3.metric("Market Structure Signal", signal)
    m4.metric("Consensus Action", action)
    m5.metric("Decision Confidence", f"{confidence}%")

    st.markdown("---")

    # Decision Banner
    col_banner, col_risk = st.columns([1.5, 1])
    with col_banner:
        st.subheader("🎯 Executive Strategy Order")
        if action == "BUY":
            st.markdown(f"### <span class='badge-buy'>STRONG BUY</span>", unsafe_allow_html=True)
        elif action == "SELL":
            st.markdown(f"### <span class='badge-sell'>STRONG SELL</span>", unsafe_allow_html=True)
        else:
            st.markdown(f"### <span class='badge-hold'>HOLD / WAIT</span>", unsafe_allow_html=True)
            
        st.write(strategy.get("reasoning", "No detailed reasoning generated."))
        
    with col_risk:
        st.subheader("🛡️ Risk & Execution Parameters")
        r_c1, r_c2, r_c3 = st.columns(3)
        r_c1.metric("Stop Loss", f"${stop_loss:,.2f}" if stop_loss else "N/A")
        r_c2.metric("Take Profit", f"${take_profit:,.2f}" if take_profit else "N/A")
        r_c3.metric("R:R Ratio", risk_reward)

    st.markdown("---")

    # Candlestick Chart View
    st.subheader("📊 Interactive Price & Smart Money Chart")
    candles = market_data.get("recent_candles", [])
    if candles:
        chart_fig = render_market_chart(
            candles,
            market_data.get("bos", []),
            market_data.get("order_blocks", []),
            market_data.get("fvgs", [])
        )
        if chart_fig:
            st.plotly_chart(chart_fig, use_container_width=True)
    else:
        st.info("Price data loaded.")

    # Agent Breakdown Tabs
    st.subheader("🔍 Deep Agent Inspection")
    tab_market, tab_news, tab_technical, tab_raw = st.tabs([
        "📈 Market Structure Agent",
        "📰 News & Sentiment Agent",
        "📐 Indicators & SMC Signals",
        "⚙️ Full State JSON"
    ])

    with tab_market:
        c_m1, c_m2 = st.columns(2)
        with c_m1:
            st.markdown("#### Break of Structure (BOS)")
            bos_data = market_data.get("bos", [])
            if bos_data:
                st.dataframe(pd.DataFrame(bos_data), use_container_width=True)
            else:
                st.info("No recent BOS detected.")
                
        with c_m2:
            st.markdown("#### Order Blocks (OB)")
            ob_data = market_data.get("order_blocks", [])
            if ob_data:
                st.dataframe(pd.DataFrame(ob_data), use_container_width=True)
            else:
                st.info("No recent Order Blocks detected.")

        st.markdown("#### Fair Value Gaps (FVG)")
        fvg_data = market_data.get("fvgs", [])
        if fvg_data:
            st.dataframe(pd.DataFrame(fvg_data), use_container_width=True)
        else:
            st.info("No recent Fair Value Gaps detected.")

    with tab_news:
        st.markdown(f"**Sentiment Analysis Mode:** `{news_analysis.get('mode', 'LLaMA-3.3-70B')}`")
        n1, n2, n3 = st.columns(3)
        n1.metric("Sentiment", news_analysis.get("sentiment", "Neutral").upper())
        n2.metric("News Signal", news_analysis.get("signal", "HOLD"))
        n3.metric("Importance Rating", f"{news_analysis.get('importance', 0)} / 10")

        st.markdown("#### Synthesis Summary")
        st.write(news_analysis.get("summary", "N/A"))
        st.write(f"**Market Impact:** {news_analysis.get('market_impact', 'N/A')}")
        
        risks = news_analysis.get("risks", [])
        if risks:
            st.markdown("#### Identified Risks")
            for r in risks:
                st.markdown(f"- ⚠️ {r}")

        st.markdown("#### Live Feeds Used")
        if news:
            for item in news[:5]:
                with st.expander(f"📰 {item.get('title')}"):
                    st.write(item.get("summary", ""))
                    st.caption(f"Source: {item.get('source')} | Published: {item.get('published')}")
                    if item.get("link"):
                        st.markdown(f"[Read Article]({item.get('link')})")

    with tab_technical:
        st.markdown("#### Technical Indicators")
        t1, t2, t3, t4 = st.columns(4)
        t1.metric("RSI (14)", indicators.get("rsi_14", "N/A"))
        t2.metric("SMA 20", f"${indicators.get('sma_20', 0):,.2f}" if indicators.get('sma_20') else "N/A")
        t3.metric("SMA 50", f"${indicators.get('sma_50', 0):,.2f}" if indicators.get('sma_50') else "N/A")
        t4.metric("Trend Classification", indicators.get("trend", "N/A"))

    with tab_raw:
        clean_result = {
            "symbol": result.get("symbol"),
            "interval": result.get("interval"),
            "signal": result.get("signal"),
            "strategy_decision": result.get("strategy_decision"),
            "news_analysis": result.get("news_analysis")
        }
        st.json(clean_result)

else:
    st.info("👈 Select your desired trading pair and timeframe from the sidebar, then click **Run Multi-Agent Analysis**.")
