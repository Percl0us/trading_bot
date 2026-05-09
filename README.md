# Trading Bot for Binance Futures Testnet

A Python application that places **MARKET** and **LIMIT** orders on the Binance Futures Testnet (USDT-M) via CLI.
Live Link --https://percybinancetradingbot.streamlit.app/

## Setup

1. **Clone or download** this repository.
2. **Install Python 3.8+** and run `pip install -r requirements.txt`
3. **Get Testnet API keys** from [Binance Futures Testnet](https://testnet.binancefuture.com/):
   - Register / login
   - Go to "API Management" → Create new API key
   - Copy **API Key** and **Secret Key**
4. **Edit `cli.py`** and replace `YOUR_TESTNET_API_KEY` and `YOUR_TESTNET_SECRET_KEY` with your keys.
   - For security, you may use environment variables instead (not required for the assignment).

## How to Run

Open a terminal in the `trading_bot/` folder.

### MARKET order (BUY)
```bash
python cli.py --symbol BTCUSDT --side BUY --type MARKET --quantity 0.001# trading_bot
