"""
Binance Futures Testnet client wrapper.
Handles API communication.
"""
import os
from binance.client import Client
from binance.exceptions import BinanceAPIException
from dotenv import load_dotenv
from bot.logging_config import get_logger

logger = get_logger(__name__)
load_dotenv()

class BinanceClient:
    """
    Wrapper for Binance Futures Testnet client.
    Handles connection, authentication, and provides methods for trading operations.
    """    
    def __init__(self, api_key: str = None, api_secret: str = None):
        """
        Initialize Binance client.
        
        Args:
            api_key: Binance API key (optional, defaults to env variable)
            api_secret: Binance API secret (optional, defaults to env variable)
        """
        self.api_key = api_key or os.getenv("BINANCE_API_KEY")
        self.api_secret = api_secret or os.getenv("BINANCE_API_SECRET")

        
        if not self.api_key or not self.api_secret:
            raise ValueError(
                "API credentials not found. Please set BINANCE_API_KEY and "
                "BINANCE_API_SECRET in .env file"
            )
        
        logger.info("Initializing Binance Futures Testnet client...")
        
        try:
            # Initialize client with testnet URL
            self.client = Client(
                api_key=self.api_key,
                api_secret=self.api_secret,
                testnet=True
            )            
            # Set testnet URL for futures
            self.client.FUTURES_URL = 'https://testnet.binancefuture.com'
            
            logger.info("Binance client initialized successfully")
            
            # Test connection
            self._test_connection()
            
        except Exception as e:
            logger.error(f"Failed to initialize Binance client: {e}")
            raise
    
    def _test_connection(self):
        """Test connection to Binance API."""
        try:
            account = self.client.futures_account()
            logger.info(f"✓ Connection test successful. Account balance: {account.get('totalWalletBalance', 'N/A')} USDT")
        except BinanceAPIException as e:
            logger.error(f"API Error during connection test: {e.message}")
            raise
        except Exception as e:
            logger.error(f"Connection test failed: {e}")
            raise
    
    def get_client(self):
        """
        Get Binance client instance.        
        Returns:
            Binance Client instance
        """
        return self.client
    
    def get_symbol_info(self, symbol: str):
        """
        Get information about a trading symbol.        
        Args:
            symbol: Trading pair symbol            
        Returns:
            Symbol information dictionary
        """
        try:
            logger.debug(f"Fetching symbol info for {symbol}")
            exchange_info = self.client.futures_exchange_info()
            
            for s in exchange_info['symbols']:
                if s['symbol'] == symbol:
                    logger.debug(f"Symbol info retrieved for {symbol}")
                    return s
            
            logger.warning(f"Symbol {symbol} not found in exchange info")
            return None
            
        except BinanceAPIException as e:
            logger.error(f"API Error fetching symbol info: {e.message}")
            raise
        except Exception as e:
            logger.error(f"Error fetching symbol info: {e}")
            raise
    
    def get_account_balance(self):
        """
        Get account balance information.        
        Returns:
            Account balance dictionary
        """
        try:
            logger.debug("Fetching account balance")
            account = self.client.futures_account()
            balance = account.get('totalWalletBalance', 'N/A')
            logger.info(f"Account balance: {balance} USDT")
            return account
        except BinanceAPIException as e:
            logger.error(f"API Error fetching account balance: {e.message}")
            raise
        except Exception as e:
            logger.error(f"Error fetching account balance: {e}")
            raise