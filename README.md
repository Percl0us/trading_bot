# Trading Bot for Binance Futures Testnet

A Python application that places **MARKET** and **LIMIT** orders on the Binance Futures Testnet (USDT-M) via CLI, plus an optional web UI built with Streamlit.

🔗 **Live Demo**: [percybinancetradingbot.streamlit.app](https://percybinancetradingbot.streamlit.app/)

---

## Features

- Place **MARKET** and **LIMIT** orders (BUY/SELL)
- CLI with argument validation (`argparse`)
- Web UI (Streamlit) – check balance and place orders interactively
- Full logging to file (`trading_bot.log`)
- Environment variables for API keys (`.env` file or Streamlit secrets)
- Error handling for network issues, invalid inputs, and API errors

---

# Setup (Local Development)

## 1. Clone the repository

```bash
git clone https://github.com/your-username/trading_bot.git
cd trading_bot
```

---

## 2. Install dependencies

```bash
pip install -r requirements.txt
```

---

## 3. Get Binance Futures Testnet API keys

1. Go to Binance Futures Testnet  
2. Register / login  
3. Navigate to **API Management → Create API Key**
4. Copy the API Key and Secret Key
5. Fund your testnet account using the Faucet (you need USDT to place orders)

---

## 4. Set up environment variables

Create a `.env` file in the project root:

```ini
BINANCE_TESTNET_API_KEY=your_api_key_here
BINANCE_TESTNET_SECRET_KEY=your_secret_key_here
BINANCE_FUTURES_BASE_URL=https://testnet.binancefuture.com
```

> ⚠️ Never commit the `.env` file — it's already included in `.gitignore`.

---

# CLI Usage (Command Line Interface)

All commands are run from the project root.

---

## Check account balance

```bash
python cli.py --balance
```

---

## Place a MARKET order (BUY)

```bash
python cli.py --symbol BTCUSDT --side BUY --type MARKET --quantity 0.001
```

---

## Place a MARKET order (SELL)

```bash
python cli.py --symbol BTCUSDT --side SELL --type MARKET --quantity 0.001
```

---

## Place a LIMIT order (BUY)

```bash
python cli.py --symbol BTCUSDT --side BUY --type LIMIT --quantity 0.001 --price 60000
```

---

## Place a LIMIT order (SELL)

```bash
python cli.py --symbol BTCUSDT --side SELL --type LIMIT --quantity 0.001 --price 80000
```

---

## View all CLI options

```bash
python cli.py --help
```

---

# Web UI (Streamlit)

Run the interactive web interface:

```bash
streamlit run ui.py
```

Then open your browser to:

```text
http://localhost:8501
```

---

## Features

- View real-time account balance (with totals and per-asset breakdown)
- Place MARKET / LIMIT orders via a simple form
- See order response as JSON
- Refresh balance after each order

The UI uses the same `.env` credentials and logs all activity to `trading_bot.log`.

---

# Deployment (Streamlit Cloud)

The bot is live at:

🔗 **https://percybinancetradingbot.streamlit.app**

---

## Deploy your own instance

### 1. Push your code to GitHub

Push the project to a public GitHub repository.

---

### 2. Open Streamlit Cloud

Go to Streamlit Cloud and sign in with GitHub.

---

### 3. Create a new app

Click:

```text
New app → Select repo → Select branch → Main file: ui.py
```

---

### 4. Add Streamlit secrets

In app settings, add the following secrets in **TOML** format:

```toml
BINANCE_TESTNET_API_KEY = "your_api_key"
BINANCE_TESTNET_SECRET_KEY = "your_secret"
BINANCE_FUTURES_BASE_URL = "https://testnet.binancefuture.com"
```

---

### 5. Deploy

Click **Deploy**.

Your app will be available at:

```text
https://your-app-name.streamlit.app
```

---

# Logging

All API requests, responses, and errors are logged to:

```text
trading_bot.log
```

Example log entry:

```text
2026-05-09 16:45:48,298 - INFO - Order request: {'symbol': 'BTCUSDT', ...}
2026-05-09 16:45:49,034 - INFO - Order response: {'orderId': 13123508662, 'status': 'NEW', ...}
```

---

# Project Structure

```text
trading_bot/
├── bot/
│   ├── __init__.py
│   ├── client.py           # Binance API wrapper (signatures, requests)
│   ├── validators.py       # Input validation (quantity, price, symbol)
│   └── logging_config.py   # Logging setup (file + console)
├── cli.py                  # CLI entry point (argparse)
├── ui.py                   # Streamlit web UI
├── requirements.txt        # Dependencies
├── .env                    # API keys (ignored by git) – local only
├── .gitignore
├── trading_bot.log         # Auto-generated log file
└── README.md
```

---

# Troubleshooting

| Error | Solution |
|---|---|
| Margin is insufficient | Fund your testnet account using the Faucet on the testnet dashboard. |
| Limit price can't be lower than X | Choose a limit price above the current market price. |
| Invalid API key | Regenerate API keys on the testnet and update your `.env` / secrets. |
| 451 Client Error | Your IP or cloud region is blocked. Switch to the global testnet (`testnet.binancefuture.com`) and use keys from there. |
| ModuleNotFoundError | Run `pip install -r requirements.txt` again. |

---

# License

This project was created as a coding assignment for Primetrade.ai.

---

# Author

**Aryan / Percy**

🔗 Live Demo: [percybinancetradingbot.streamlit.app](https://percybinancetradingbot.streamlit.app/)
