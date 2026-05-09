def validate_quantity(quantity):
    if quantity <= 0:
        raise ValueError("Quantity must be positive")
    return True

def validate_limit_price(order_type, price):
    if order_type == "LIMIT" and price is None:
        raise ValueError("Price is required for LIMIT orders")

def validate_symbol(symbol):
    if not isinstance(symbol, str) or len(symbol) == 0:
        raise ValueError("Symbol must be a non-empty string")
    return True