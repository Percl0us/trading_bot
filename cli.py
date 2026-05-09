from dotenv import load_dotenv
load_dotenv()

#!/usr/bin/env python3
import argparse
import sys
import logging
import os
from bot.logging_config import setup_logging
from bot.validators import validate_quantity, validate_limit_price, validate_symbol
from bot.client import BinanceFuturesClient

API_KEY = os.getenv("BINANCE_TESTNET_API_KEY")
SECRET_KEY = os.getenv("BINANCE_TESTNET_SECRET_KEY")

def main():
    setup_logging()

    parser = argparse.ArgumentParser(description="Trading Bot - Binance Futures Testnet")
    parser.add_argument("--symbol", help="Trading pair, e.g., BTCUSDT")
    parser.add_argument("--side", choices=["BUY", "SELL"])
    parser.add_argument("--type", choices=["MARKET", "LIMIT"])
    parser.add_argument("--quantity", type=float)
    parser.add_argument("--price", type=float, help="Required for LIMIT orders")
    parser.add_argument("--balance", action="store_true", help="Check account balance")

    args = parser.parse_args()

    # If --balance is provided, just show balance and exit
    if args.balance:
        if not API_KEY or not SECRET_KEY:
            print("ERROR: API keys not set in environment variables.")
            sys.exit(1)
        client = BinanceFuturesClient(API_KEY, SECRET_KEY)
        try:
            balance = client.check_balance()
            print("\n*** ACCOUNT BALANCE ***")
            for asset in balance:
                if float(asset.get('balance', 0)) > 0:
                    print(f"{asset['asset']}: {asset['balance']}")
            print("***********************\n")
        except Exception as e:
            print(f"Failed to fetch balance: {e}")
        sys.exit(0)

    # Otherwise, require all order arguments
    if not all([args.symbol, args.side, args.type, args.quantity]):
        parser.error("--symbol, --side, --type, and --quantity are required for placing orders")

    try:
        validate_symbol(args.symbol)
        validate_quantity(args.quantity)
        validate_limit_price(args.type, args.price)
    except ValueError as e:
        logging.error(f"Validation failed: {e}")
        print(f"\nERROR: {e}")
        sys.exit(1)

    if not API_KEY or not SECRET_KEY:
        logging.error("Environment variables BINANCE_TESTNET_API_KEY and BINANCE_TESTNET_SECRET_KEY are not set")
        print("\nERROR: API keys not found in environment variables.")
        print("Please set them in a .env file or export them.")
        sys.exit(1)

    client = BinanceFuturesClient(API_KEY, SECRET_KEY)

    print("\n*** ORDER SUMMARY ***")
    print(f"Symbol   : {args.symbol}")
    print(f"Side     : {args.side}")
    print(f"Type     : {args.type}")
    print(f"Quantity : {args.quantity}")
    if args.price:
        print(f"Price    : {args.price}")
    print("********************\n")

    try:
        result = client.place_order(
            symbol=args.symbol,
            side=args.side,
            order_type=args.type,
            quantity=args.quantity,
            price=args.price
        )

        print("\n*** ORDER RESPONSE ***")
        print(f"Order ID      : {result.get('orderId')}")
        print(f"Status        : {result.get('status')}")
        print(f"Executed Qty  : {result.get('executedQty')}")
        print(f"Avg price     : {result.get('avgPrice', 'N/A')}")
        if result.get('status') == 'NEW' and args.type == 'LIMIT':
            print("Info: Limit order placed, waiting to fill.")
        print("**********************")
        logging.info("Order placed successfully")

    except Exception as e:
        print(f"\nFAILED: {e}")
        logging.error(f"Order placement failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()