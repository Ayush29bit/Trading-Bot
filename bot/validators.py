"""
Input validation functions for trading bot parameters.
"""
from typing import Tuple
from bot.logging_config import get_logger

logger = get_logger(__name__)


class ValidationError(Exception):
    """Custom exception for validation errors."""
    pass

def validate_symbol(symbol: str) -> str:
    """
    Validate trading symbol format.
    
    Args:
        symbol: Trading pair symbol (e.g., BTCUSDT)        
    Returns:
        Uppercase symbol        
    Raises:
        ValidationError: If symbol format is invalid
    """
    if not symbol:
        raise ValidationError("Symbol cannot be empty")
    
    symbol = symbol.upper().strip()
    
    if not symbol.endswith("USDT"):
        logger.warning(f"Symbol {symbol} doesn't end with USDT. This might fail on Binance Futures.")
    
    logger.debug(f"Validated symbol: {symbol}")
    return symbol


def validate_side(side: str) -> str:
    """
    Validate order side.    
    Args:
        side: Order side (BUY or SELL)       
    Returns:
        Uppercase side       
    Raises:
        ValidationError: If side is invalid
    """
    valid_sides = ["BUY", "SELL"]
    side = side.upper().strip()
    
    if side not in valid_sides:
        raise ValidationError(f"Invalid side: {side}. Must be one of {valid_sides}")
    
    logger.debug(f"Validated side: {side}")
    return side

def validate_order_type(order_type: str) -> str:
    """
    Validate order type.
    Args:
        order_type: Type of order (MARKET or LIMIT)       
    Returns:
        Uppercase order type        
    Raises:
        ValidationError: If order type is invalid
    """
    valid_types = ["MARKET", "LIMIT"]
    order_type = order_type.upper().strip()
    
    if order_type not in valid_types:
        raise ValidationError(f"Invalid order type: {order_type}. Must be one of {valid_types}")
    
    logger.debug(f"Validated order type: {order_type}")
    return order_type


def validate_quantity(quantity: str) -> float:
    """
    Validate order quantity.
    
    Args:
        quantity: Order quantity as string
        
    Returns:
        Quantity as float
        
    Raises:
        ValidationError: If quantity is invalid
    """
    try:
        qty = float(quantity)
    except ValueError:
        raise ValidationError(f"Invalid quantity: {quantity}. Must be a number")
    
    if qty <= 0:
        raise ValidationError(f"Quantity must be positive. Got: {qty}")
    
    logger.debug(f"Validated quantity: {qty}")
    return qty


def validate_price(price: str) -> float:
    """
    Validate order price.
    
    Args:
        price: Order price as string
        
    Returns:
        Price as float
        
    Raises:
        ValidationError: If price is invalid
    """
    try:
        prc = float(price)
    except ValueError:
        raise ValidationError(f"Invalid price: {price}. Must be a number")
    
    if prc <= 0:
        raise ValidationError(f"Price must be positive. Got: {prc}")
    
    logger.debug(f"Validated price: {prc}")
    return prc


def validate_order_params(
    symbol: str,
    side: str,
    order_type: str,
    quantity: str,
    price: str = None
) -> Tuple[str, str, str, float, float]:
    """
    Validate all order parameters together.
    
    Args:
        symbol: Trading pair symbol
        side: Order side (BUY/SELL)
        order_type: Order type (MARKET/LIMIT)
        quantity: Order quantity
        price: Order price (required for LIMIT orders)
        
    Returns:
        Tuple of validated parameters
        
    Raises:
        ValidationError: If any parameter is invalid
    """
    validated_symbol = validate_symbol(symbol)
    validated_side = validate_side(side)
    validated_type = validate_order_type(order_type)
    validated_quantity = validate_quantity(quantity)
    
    # Price is required for LIMIT orders
    if validated_type == "LIMIT":
        if price is None or price == "":
            raise ValidationError("Price is required for LIMIT orders")
        validated_price = validate_price(price)
    else:
        validated_price = None
    
    logger.info(f"All parameters validated successfully")
    return (
        validated_symbol,
        validated_side,
        validated_type,
        validated_quantity,
        validated_price
    )