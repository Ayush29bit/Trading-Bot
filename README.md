# Binance Futures Trading Bot

**A professional Python CLI trading bot for Binance Futures Testnet**

##  Table of Contents

- [Overview](#-overview)
- [Features](#-features)
- [Demo](#-demo)
- [Installation](#-installation)
- [Configuration](#-configuration)
- [Usage](#-usage)
- [Project Structure](#-project-structure)
- [How It Works](#-how-it-works)
- [Examples](#-examples)
- [Logging](#-logging)
- [Error Handling](#-error-handling)
---

##  Overview

This is a simplified trading bot built for Binance Futures Testnet (USDT-M). It provides a clean, professional command-line interface for placing MARKET and LIMIT orders with comprehensive validation, error handling, and logging.

---

##  Features

### Core Functionality
-  **Order Types**: MARKET and LIMIT orders
-  **Order Sides**: BUY and SELL support
-  **Input Validation**: Comprehensive validation before API calls
-  **Error Handling**: Multi-level error handling with clear messages
-  **Logging**: Detailed file logging + console output
-  **Balance Checking**: View account balance

### Technical Highlights
-  **Modular Architecture**: Separated concerns (client, orders, validation, CLI)
-  **Rich CLI**: Beautiful terminal interface with colors and tables
-  **Security**: Environment variables for API credentials
-  **Comprehensive Logging**: Timestamped logs for debugging and auditing
-  **Robust Validation**: Type checking, range validation, business rules
-  **Exception Handling**: Graceful handling of API, network, and user errors

### User Experience
-  Colored, formatted terminal output
-  Clear order summaries before execution
-  Success/failure indicators
-  Detailed log file references
-  User-friendly error messages

---
### Entire Flow
┌─────────────────────────────────────────────────────────────────┐
│                         USER TYPES COMMAND                       │
│  python cli.py order -s BTCUSDT --side BUY -t MARKET -q 0.001  │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                     CLI.PY (Entry Point)                         │
│  1. Typer parses command line arguments                         │
│  2. Sets up logging system                                      │
│  3. Calls order() function with parsed arguments                │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                    VALIDATORS.PY (Input Check)                   │
│  1. validate_symbol("BTCUSDT") → "BTCUSDT" ✓                   │
│  2. validate_side("BUY") → "BUY" ✓                             │
│  3. validate_order_type("MARKET") → "MARKET" ✓                 │
│  4. validate_quantity("0.001") → 0.001 (float) ✓               │
│  5. validate_price(None) → None (not needed for MARKET) ✓      │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                     CLIENT.PY (API Connection)                   │
│  1. Load API_KEY and API_SECRET from .env file                  │
│  2. Create Binance Client object                                │
│  3. Set testnet URL: https://testnet.binancefuture.com         │
│  4. Test connection by calling futures_account()                │
│  5. Return authenticated client ready for trading                │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                    ORDERS.PY (Order Execution)                   │
│  1. Create OrderManager with BinanceClient                       │
│  2. Log order request details                                    │
│  3. Call Binance API: futures_create_order()                    │
│  4. Binance processes the order                                  │
│  5. Receive response with order details                          │
│  6. Log response details                                         │
│  7. Return response to CLI                                       │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│              BINANCE FUTURES TESTNET API                         │
│  1. Receives authenticated API request                           │
│  2. Validates signature using API_SECRET                         │
│  3. Checks order parameters                                      │
│  4. Executes trade (MARKET) or places order (LIMIT)             │
│  5. Returns JSON response with order details                     │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                    BACK TO CLI.PY (Display)                      │
│  1. Receive order response                                       │
│  2. Display success message with Rich formatting                 │
│  3. Show order ID, status, executed quantity                     │
│  4. Point user to log file                                       │
│  5. Exit with success code (0)                                   │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│               LOGGING_CONFIG.PY (Throughout)                     │
│  Every step above is logged to:                                  │
│  - Console (INFO level - user sees this)                        │
│  - Log file (DEBUG level - everything recorded)                 │
└─────────────────────────────────────────────────────────────────┘

##  Installation

### 1️⃣ Clone the Repository

git clone https://github.com/your-username/trading-bot.git
cd trading-bot

### 2️⃣ Create a Virtual Environment

python -m venv venv
Mac: source venv/bin/activate      
Windows: venv\Scripts\activate

### 3️⃣ Install Dependencies
pip install -r requirements.txt

## Configuration

Binance Futures Testnet API Keys

Go to Binance → Futures → Demo Trading

Create API keys

Create a .env file in the project root:

BINANCE_API_KEY=your_testnet_api_key
BINANCE_API_SECRET=your_testnet_api_secret

▶️ Usage

All interactions happen via the terminal.

Place a Market Order
python cli.py order \
  --symbol BTCUSDT \
  --side BUY \
  --type MARKET \
  --quantity 0.001

Place a Limit Order
python cli.py order \
  --symbol BTCUSDT \
  --side SELL \
  --type LIMIT \
  --quantity 0.001 \
  --price 45000

Check Account Balance
python cli.py balance

📤 Example Output
✔ Inputs validated successfully

┌──────── Order Summary ────────┐
│ Symbol     BTCUSDT             │
│ Side       BUY                 │
│ Type       MARKET              │
│ Quantity   0.001               │
└───────────────────────────────┘

✔ Order Placed Successfully!

Order ID: 12345678
Status: FILLED
Executed Qty: 0.001

Detailed logs saved to: logs/trading_bot_20240210_143512.log

## Logging

Logs are written to the logs/ directory

Each run generates a timestamped log file

Includes:

Input parameters

API requests

API responses

Errors & stack traces

Example log file:

logs/trading_bot_20240210_143512.log

## Error Handling

The application handles errors gracefully:

ValidationError → Invalid user input

API errors → Binance API issues

Network errors → Connectivity problems

Unexpected errors → Logged with stack trace

Errors are:

Shown clearly in the terminal

Logged in detail to file

Cause a clean program exit

