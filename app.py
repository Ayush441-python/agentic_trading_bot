import streamlit as st
from graph.workflow import graph

# -------------------------------
# Page Config
# -------------------------------

st.set_page_config(
    page_title="Agentic Trading Bot",
    page_icon="📈",
    layout="wide"
)

# -------------------------------
# Header
# -------------------------------

st.title("📈 Agentic Trading Bot")
st.caption("Market Agent + News Agent + Strategy Agent")

# -------------------------------
# Sidebar
# -------------------------------

with st.sidebar:
    st.header("Settings")

    symbol = st.selectbox(
        "Trading Pair",
        ["BTCUSDT", "ETHUSDT", "SOLUSDT"]
    )

    interval = st.selectbox(
        "Timeframe",
        ["15m", "1h", "4h", "1d"]
    )

    analyze_btn = st.button(
        "Generate Signal",
        use_container_width=True
    )

# -------------------------------
# Analysis
# -------------------------------

if analyze_btn:

    with st.spinner("Running agents..."):

        state = {
            "symbol": symbol,
            "interval": interval,

            "market_data": {},
            "signal": "",

            "news": [],
            "news_analysis": {},

            "strategy_decision": {}
        }

        result = graph.invoke(state)

    st.success("Analysis Complete")

    # ==========================
    # Top Metrics
    # ==========================

    market_data = result.get("market_data", {})
    signal = result.get("signal", "N/A")
    strategy = result.get("strategy_decision", {})
    news_analysis = result.get("news_analysis", {})

    latest_price = market_data.get(
        "latest_price",
        "N/A"
    )

    confidence = strategy.get(
        "confidence",
        "N/A"
    )

    action = strategy.get(
        "action",
        "N/A"
    )

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Symbol",
        symbol
    )

    col2.metric(
        "Price",
        latest_price
    )

    col3.metric(
        "Market Signal",
        signal
    )

    col4.metric(
        "Strategy Action",
        action
    )

    # ==========================
    # Strategy Decision
    # ==========================

    st.divider()

    st.subheader("Strategy Decision")

    if action == "BUY":
        st.success(f"BUY • Confidence: {confidence}%")

    elif action == "SELL":
        st.error(f"SELL • Confidence: {confidence}%")

    else:
        st.warning(f"HOLD • Confidence: {confidence}%")

    st.json(strategy)

    # ==========================
    # Agent Outputs
    # ==========================

    st.divider()

    tab1, tab2 = st.tabs([
        "Market Agent",
        "News Agent"
    ])

    with tab1:
        st.subheader("Market Analysis")
        st.json(market_data)

    with tab2:
        st.subheader("News Analysis")
        st.json(news_analysis)

else:
    st.info(
        "Select a symbol and timeframe, then click Generate Signal."
    )

