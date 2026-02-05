"""
Order placement logic for Binance Futures.
Handles MARKET and LIMIT orders with proper error handling.
"""
from binance.exceptions import BinanceAPIException, BinanceRequestException
from bot.logging_config import get_logger
from bot.client import BinanceClient

logger = get_logger(__name__)

class OrderManager:
    """
    Manages order placement and tracking for Binance Futures.
    """
    
    def __init__(self, client: BinanceClient):
        self.client = client
        self.binance_client = client.get_client()
        logger.info("OrderManager initialized")
    
    def _log_order_request(self, symbol: str, side: str, order_type: str, 
                          quantity: float, price: float = None):
        logger.info("=" * 60)
        logger.info("ORDER REQUEST SUMMARY")
        logger.info("=" * 60)
        logger.info(f"Symbol:       {symbol}")
        logger.info(f"Side:         {side}")
        logger.info(f"Order Type:   {order_type}")
        logger.info(f"Quantity:     {quantity}")
        if price:
            logger.info(f"Price:        {price}")
        logger.info("=" * 60)
    
    def _log_order_response(self, response: dict):
        logger.info("=" * 60)
        logger.info("ORDER RESPONSE DETAILS")
        logger.info("=" * 60)
        logger.info(f"Order ID:{response.get('orderId', 'N/A')}")
        logger.info(f"Status:{response.get('status', 'N/A')}")
        logger.info(f"Symbol:{response.get('symbol', 'N/A')}")
        logger.info(f"Side: {response.get('side', 'N/A')}")
        logger.info(f"Type: {response.get('type', 'N/A')}")
        logger.info(f"Quantity: {response.get('origQty', 'N/A')}")
        
        if 'executedQty' in response:
            logger.info(f"Executed Qty: {response.get('executedQty', 'N/A')}")
        
        if 'avgPrice' in response and response.get('avgPrice') != '0':
            logger.info(f"Avg Price:    {response.get('avgPrice', 'N/A')}")
        elif 'price' in response:
            logger.info(f"Price:        {response.get('price', 'N/A')}")   
        if 'cumQuote' in response:
            logger.info(f"Cum Quote:    {response.get('cumQuote', 'N/A')}")
        
        logger.info(f"Time:         {response.get('updateTime', response.get('transactTime', 'N/A'))}")
        logger.info("=" * 60)
    
    def place_market_order(self, symbol: str, side: str, quantity: float) -> dict:
        self._log_order_request(symbol, side, "MARKET", quantity)
        
        try:
            logger.info(f"Placing MARKET {side} order for {quantity} {symbol}...")
            
            # Place market order
            if side == "BUY":
                response = self.binance_client.futures_create_order(
                    symbol=symbol,
                    side="BUY",
                    type="MARKET",
                    quantity=quantity
                )
            else:  # SELL
                response = self.binance_client.futures_create_order(
                    symbol=symbol,
                    side="SELL",
                    type="MARKET",
                    quantity=quantity
                )
            
            self._log_order_response(response)
            logger.info("MARKET order placed successfully!")
            
            return response
            
        except BinanceAPIException as e:
            logger.error(f"Binance API Error: {e.status_code} - {e.message}")
            logger.error(f"Full error: {e}")
            raise
        except BinanceRequestException as e:
            logger.error(f"Binance Request Error: {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error placing MARKET order: {e}")
            raise
    
    def place_limit_order(self, symbol: str, side: str, quantity: float, price: float) -> dict:
        self._log_order_request(symbol, side, "LIMIT", quantity, price)
        
        try:
            logger.info(f"Placing LIMIT {side} order for {quantity} {symbol} at {price}...")
            
            # Place limit order 
            if side == "BUY":
                response = self.binance_client.futures_create_order(
                    symbol=symbol,
                    side="BUY",
                    type="LIMIT",
                    timeInForce="GTC",
                    quantity=quantity,
                    price=price
                )
            else: 
                response = self.binance_client.futures_create_order(
                    symbol=symbol,
                    side="SELL",
                    type="LIMIT",
                    timeInForce="GTC",
                    quantity=quantity,
                    price=price
                )
            
            self._log_order_response(response)
            logger.info("LIMIT order placed successfully!")
            
            return response
            
        except BinanceAPIException as e:
            logger.error(f"Binance API Error: {e.status_code} - {e.message}")
            logger.error(f"Full error: {e}")
            raise
        except BinanceRequestException as e:
            logger.error(f" Binance Request Error: {e}")
            raise
        except Exception as e:
            logger.error(f" Unexpected error placing LIMIT order: {e}")
            raise
    
    def place_order(self, symbol: str, side: str, order_type: str, 
                   quantity: float, price: float = None) -> dict:
        if order_type == "MARKET":
            return self.place_market_order(symbol, side, quantity)
        elif order_type == "LIMIT":
            if price is None:
                raise ValueError("Price is required for LIMIT orders")
            return self.place_limit_order(symbol, side, quantity, price)
        else:
            raise ValueError(f"Unsupported order type: {order_type}")