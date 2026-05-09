import os
from datetime import datetime

import streamlit as st
from dotenv import load_dotenv

from bot.client import BinanceFuturesClient
from bot.logging_config import setup_logging
from bot.validators import validate_limit_price, validate_quantity, validate_symbol

load_dotenv()
setup_logging()

st.set_page_config(page_title="Trading Bot UI", layout="centered")

st.markdown(
    """
    <style>
    [data-testid="stHeaderActionElements"] {display: none;}
    </style>
    """, unsafe_allow_html=True)

st.title("Binance Futures Testnet Bot")

# Load from secrets.toml first, fallback to .env
API_KEY = None
SECRET_KEY = None
BASE_URL = "https://demo-fapi.binance.com"

# Try Streamlit secrets first
try:
    API_KEY = st.secrets.get("BINANCE_TESTNET_API_KEY")
    SECRET_KEY = st.secrets.get("BINANCE_TESTNET_SECRET_KEY")
    BASE_URL = st.secrets.get("BINANCE_FUTURES_BASE_URL", BASE_URL)
except Exception:
    pass

# Fallback to environment variables
if not API_KEY:
    API_KEY = os.getenv("BINANCE_TESTNET_API_KEY")
if not SECRET_KEY:
    SECRET_KEY = os.getenv("BINANCE_TESTNET_SECRET_KEY")
if not BASE_URL or BASE_URL == "https://demo-fapi.binance.com":
    BASE_URL = os.getenv("BINANCE_FUTURES_BASE_URL", BASE_URL)

if not API_KEY or not SECRET_KEY:
    st.error("❌ API keys not found. Please configure them:")
    st.code(
        """
BINANCE_TESTNET_API_KEY="your_key_here"
BINANCE_TESTNET_SECRET_KEY="your_secret_here"
BINANCE_FUTURES_BASE_URL="https://demo-fapi.binance.com"
        """)
    st.stop()

try:
    client = BinanceFuturesClient(API_KEY, SECRET_KEY, BASE_URL)
except Exception as e:
    st.error(f"Failed to initialize client: {e}")
    st.stop()


def fetch_balance():
    return client.check_balance()


def render_balance():
    st.write("### Account Balance")

    if st.button("Refresh Balance"):
        st.session_state["refresh_balance"] = True

    try:
        balance = fetch_balance()

        if not balance:
            st.info("No balance data returned from the API.")
            return

        rows = []
        total_wallet = 0.0
        total_available = 0.0
        total_unrealized = 0.0

        for asset in balance:
            bal = float(asset.get("balance", 0) or 0)
            available = float(asset.get("availableBalance", 0) or 0)
            wallet = float(asset.get("crossWalletBalance", 0) or 0)
            unrealized = float(asset.get("crossUnPnl", 0) or 0)

            total_wallet += wallet
            total_available += available
            total_unrealized += unrealized

            if bal > 0 or available > 0 or wallet > 0 or unrealized != 0:
                rows.append({
                    "Asset": asset.get("asset", ""),
                    "Balance": bal,
                    "Available": available,
                    "Wallet": wallet,
                    "Unrealized PnL": unrealized,
                    "Max Withdraw": float(asset.get("maxWithdrawAmount", 0) or 0),
                })

        c1, c2, c3 = st.columns(3)
        c1.metric("Wallet", f"{total_wallet:.8f}")
        c2.metric("Available", f"{total_available:.8f}")
        c3.metric("Unrealized PnL", f"{total_unrealized:.8f}")

        st.caption(f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

        if rows:
            st.dataframe(rows, use_container_width=True, hide_index=True)
        else:
            st.info("No positive balances found.")
    except Exception as e:
        st.error(f"Failed to fetch balance: {e}")


render_balance()

st.divider()

st.write("### Place Order")
with st.form("order_form"):
    col1, col2 = st.columns(2)

    with col1:
        symbol = st.text_input("Symbol", value="BTCUSDT")
        side = st.selectbox("Side", ["BUY", "SELL"])

    with col2:
        order_type = st.selectbox("Order Type", ["MARKET", "LIMIT"])
        quantity = st.number_input(
            "Quantity",
            min_value=0.0001,
            value=0.001,
            step=0.0001,
            format="%.4f",
        )

    price = None
    if order_type == "LIMIT":
        price = st.number_input(
            "Price (USDT)",
            min_value=0.0,
            value=77000.0,
            step=100.0,
            format="%.2f",
        )

    submitted = st.form_submit_button("Place Order")

    if submitted:
        try:
            validate_symbol(symbol)
            validate_quantity(quantity)
            validate_limit_price(order_type, price)
        except ValueError as e:
            st.error(f"Validation error: {e}")
            st.stop()

        st.write("### Order Summary")
        st.write(f"**Symbol:** {symbol}")
        st.write(f"**Side:** {side}")
        st.write(f"**Type:** {order_type}")
        st.write(f"**Quantity:** {quantity}")
        if price is not None:
            st.write(f"**Price:** {price}")

        try:
            result = client.place_order(symbol, side, order_type, quantity, price)
            st.success("Order placed successfully!")
            st.json(result)
        except Exception as e:
            st.error(f"Order failed: {e}")