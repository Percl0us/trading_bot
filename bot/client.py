import time
import hmac
import hashlib
import requests
import logging

class BinanceFuturesClient:
    def __init__(self, api_key, api_secret, base_url="https://testnet.binancefuture.com"):
        self.api_key = api_key
        self.api_secret = api_secret
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({
            "X-MBX-APIKEY": self.api_key,
            "Content-Type": "application/x-www-form-urlencoded"
        })

    def _generate_signature(self, params):
        query_string = "&".join([f"{k}={v}" for k, v in params.items()])
        signature = hmac.new(
            self.api_secret.encode("utf-8"),
            query_string.encode("utf-8"),
            hashlib.sha256
        ).hexdigest()
        return signature

    def check_balance(self):
        """Return latest futures wallet balances (deduplicated by updateTime)."""
        params = {"timestamp": int(time.time() * 1000)}
        params["signature"] = self._generate_signature(params)
        response = self.session.get(f"{self.base_url}/fapi/v2/balance", params=params)
        response.raise_for_status()
        data = response.json()
        # Deduplicate: keep only the most recent entry per asset
        latest = {}
        for item in data:
            asset = item['asset']
            if asset not in latest or int(item['updateTime']) > int(latest[asset]['updateTime']):
                latest[asset] = item
        return list(latest.values())

    def place_order(self, symbol, side, order_type, quantity, price=None):
        endpoint = "/fapi/v1/order"
        url = self.base_url + endpoint

        params = {
            "symbol": symbol,
            "side": side,
            "type": order_type,
            "quantity": quantity,
            "timestamp": int(time.time() * 1000)
        }

        if order_type == "LIMIT":
            if price is None:
                raise ValueError("Price required for LIMIT order")
            params["price"] = price
            params["timeInForce"] = "GTC"

        params["signature"] = self._generate_signature(params)

        logging.info(f"Order request: {params}")

        try:
            response = self.session.post(url, params=params)
            response.raise_for_status()
            data = response.json()
            logging.info(f"Order response: {data}")
            return data
        except Exception as e:
            logging.error(f"Order error: {e}")
            raise