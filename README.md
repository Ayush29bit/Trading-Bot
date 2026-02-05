
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
- [Testing](#-testing)
- [Troubleshooting](#-troubleshooting)
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

