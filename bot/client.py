import time
import hmac
import hashlib
import requests
import logging
from urllib.parse import urlencode


class BinanceFuturesClient:
    def __init__(self, api_key, api_secret, base_url="https://testnet.binancefuture.com"):
        if not api_key or not api_secret:
            raise ValueError("API key and API secret are required")
        
        self.api_key = api_key
        self.api_secret = api_secret
        self.base_url = base_url.rstrip('/')  # Remove trailing slash
        self.session = requests.Session()
        self.session.headers.update({
            "X-MBX-APIKEY": self.api_key,
            "Content-Type": "application/x-www-form-urlencoded"
        })

    def _generate_signature(self, params):
        """Generate HMAC SHA256 signature for request."""
        query_string = urlencode(params, doseq=True)
        signature = hmac.new(
            self.api_secret.encode("utf-8"),
            query_string.encode("utf-8"),
            hashlib.sha256
        ).hexdigest()
        return signature

    def check_balance(self):
        """Return latest futures wallet balances."""
        params = {"timestamp": int(time.time() * 1000)}
        params["signature"] = self._generate_signature(params)
        
        try:
            response = self.session.get(
                f"{self.base_url}/fapi/v2/balance", 
                params=params,
                timeout=10
            )
            response.raise_for_status()
            data = response.json()
            
            if not isinstance(data, list):
                raise ValueError(f"Unexpected response format: {type(data)}")
            
            # Deduplicate: keep only the most recent entry per asset
            latest = {}
            for item in data:
                asset = item.get('asset')
                if not asset:
                    continue
                if asset not in latest or int(item.get('updateTime', 0)) > int(latest[asset].get('updateTime', 0)):
                    latest[asset] = item
            
            return list(latest.values())
        except requests.exceptions.Timeout:
            logging.error("Balance request timed out after 10s")
            raise
        except requests.exceptions.ConnectionError as e:
            logging.error(f"Connection error: {e}")
            raise
        except requests.exceptions.RequestException as e:
            logging.error(f"Balance request failed: {e}")
            if hasattr(e, 'response') and e.response is not None:
                try:
                    logging.error(f"Response: {e.response.text}")
                except Exception:
                    pass
            raise
        except Exception as e:
            logging.error(f"Unexpected error in check_balance: {e}")
            raise

    def place_order(self, symbol, side, order_type, quantity, price=None):
        """Place an order on Binance Futures."""
        # Validate inputs
        if not symbol or not side or not order_type or quantity is None:
            raise ValueError("Missing required parameters")
        
        if quantity <= 0:
            raise ValueError("Quantity must be positive")
        
        if side not in ["BUY", "SELL"]:
            raise ValueError("Side must be BUY or SELL")
        
        if order_type not in ["MARKET", "LIMIT"]:
            raise ValueError("Order type must be MARKET or LIMIT")

        url = f"{self.base_url}/fapi/v1/order"

        params = {
            "symbol": symbol,
            "side": side,
            "type": order_type,
            "quantity": quantity,
            "timestamp": int(time.time() * 1000)
        }

        if order_type == "LIMIT":
            if price is None or price <= 0:
                raise ValueError("Price required and must be positive for LIMIT order")
            params["price"] = price
            params["timeInForce"] = "GTC"

        params["signature"] = self._generate_signature(params)

        # Don't log signature
        safe_params = {k: v for k, v in params.items() if k != "signature"}
        logging.info(f"Order request: {safe_params}")

        try:
            response = self.session.post(url, data=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            logging.info(f"Order response: {data}")
            return data
        except requests.exceptions.Timeout:
            logging.error("Order request timed out after 10s")
            raise
        except requests.exceptions.ConnectionError as e:
            logging.error(f"Connection error: {e}")
            raise
        except requests.exceptions.RequestException as e:
            logging.error(f"Order request failed: {e}")
            if hasattr(e, 'response') and e.response is not None:
                try:
                    logging.error(f"Response: {e.response.text}")
                except Exception:
                    pass
            raise
        except Exception as e:
            logging.error(f"Unexpected error in place_order: {e}")
            raise