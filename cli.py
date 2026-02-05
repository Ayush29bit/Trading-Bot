
"""
CLI entry point for the trading bot.
Provides command-line interface for placing orders on Binance Futures Testnet.
"""
import typer
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from typing import Optional
import sys

from bot.logging_config import setup_logging, get_logger
from bot.client import BinanceClient
from bot.orders import OrderManager
from bot.validators import validate_order_params, ValidationError

# Initialize Typer app and Rich console
app = typer.Typer(
    name="trading-bot",
    help="Simplified Trading Bot for Binance Futures Testnet",
    add_completion=False
)
console = Console()

# Setup logging
_, log_file = setup_logging()
logger = get_logger(__name__)

@app.command()
def order(
    symbol: str = typer.Option(..., "--symbol", "-s", help="Trading pair symbol (e.g., BTCUSDT)"),
    side: str = typer.Option(..., "--side", help="Order side: BUY or SELL"),
    order_type: str = typer.Option(..., "--type", "-t", help="Order type: MARKET or LIMIT"),
    quantity: str = typer.Option(..., "--quantity", "-q", help="Order quantity"),
    price: Optional[str] = typer.Option(None, "--price", "-p", help="Price (required for LIMIT orders)"),
):
    """
    Place an order on Binance Futures Testnet.
    Examples:
        # Market Order
        python cli.py order -s BTCUSDT --side BUY -t MARKET -q 0.001
        # Limit Order
        python cli.py order -s BTCUSDT --side SELL -t LIMIT -q 0.001 -p 45000
    """
    console.print()
    console.print(Panel.fit(
        "[bold cyan]🤖 Binance Futures Trading Bot[/bold cyan]\n"
        "[dim]Testnet Environment[/dim]",
        border_style="cyan"
    ))
    console.print()

    logger.info("=" * 60)
    logger.info("NEW ORDER REQUEST")
    logger.info("=" * 60)
    
    try:
        # Validate inputs
        console.print("[yellow]⚙️  Validating inputs...[/yellow]")
        validated_symbol, validated_side, validated_type, validated_quantity, validated_price = \
            validate_order_params(symbol, side, order_type, quantity, price)
        console.print("[green]✓[/green] Inputs validated successfully\n")
        
        # Display order summary
        table = Table(title="Order Summary", show_header=True, header_style="bold magenta")
        table.add_column("Parameter", style="cyan")
        table.add_column("Value", style="yellow")
        
        table.add_row("Symbol", validated_symbol)
        table.add_row("Side", validated_side)
        table.add_row("Type", validated_type)
        table.add_row("Quantity", str(validated_quantity))
        if validated_price:
            table.add_row("Price", str(validated_price))
        
        console.print(table)
        console.print()
        
        # Initialize client
        console.print("[yellow]🔌 Connecting to Binance Futures Testnet...[/yellow]")
        client = BinanceClient()
        console.print("[green]✓[/green] Connected successfully\n")
        
        # Initialize order manager
        order_manager = OrderManager(client)
        
        # Place order
        console.print(f"[yellow]📤 Placing {validated_type} {validated_side} order...[/yellow]")
        
        response = order_manager.place_order(
            symbol=validated_symbol,
            side=validated_side,
            order_type=validated_type,
            quantity=validated_quantity,
            price=validated_price
        )
        
        # Display success
        console.print()
        console.print(Panel.fit(
            f"[bold green]✓ Order Placed Successfully![/bold green]\n\n"
            f"Order ID: [cyan]{response.get('orderId')}[/cyan]\n"
            f"Status: [cyan]{response.get('status')}[/cyan]\n"
            f"Executed Qty: [cyan]{response.get('executedQty', 'N/A')}[/cyan]",
            border_style="green"
        ))
        console.print()
        
        # Show log file location
        console.print(f"[dim]📝 Detailed logs saved to: {log_file}[/dim]")
        console.print()
        
        logger.info("Order completed successfully")
        
    except ValidationError as e:
        console.print()
        console.print(Panel.fit(
            f"[bold red]✗ Validation Error[/bold red]\n\n{str(e)}",
            border_style="red"
        ))
        console.print()
        logger.error(f"Validation error: {e}")
        sys.exit(1)
        
    except ValueError as e:
        console.print()
        console.print(Panel.fit(
            f"[bold red]✗ Configuration Error[/bold red]\n\n{str(e)}",
            border_style="red"
        ))
        console.print()
        logger.error(f"Configuration error: {e}")
        sys.exit(1)
        
    except Exception as e:
        console.print()
        console.print(Panel.fit(
            f"[bold red]✗ Error[/bold red]\n\n{str(e)}",
            border_style="red"
        ))
        console.print()
        logger.error(f"Unexpected error: {e}", exc_info=True)
        sys.exit(1)


@app.command()
def balance():
    """Check account balance on Binance Futures Testnet."""
    console.print()
    console.print(Panel.fit(
        "[bold cyan]💰 Account Balance Check[/bold cyan]",
        border_style="cyan"
    ))
    console.print()
    
    try:
        console.print("[yellow]🔌 Connecting to Binance...[/yellow]")
        client = BinanceClient()
        console.print("[green]✓[/green] Connected\n")
        
        console.print("[yellow]📊 Fetching balance...[/yellow]")
        account = client.get_account_balance()
        
        console.print()
        console.print(Panel.fit(
            f"[bold green]Total Wallet Balance[/bold green]\n\n"
            f"[cyan]{account.get('totalWalletBalance', 'N/A')} USDT[/cyan]",
            border_style="green"
        ))
        console.print()
        
    except Exception as e:
        console.print()
        console.print(Panel.fit(
            f"[bold red]✗ Error[/bold red]\n\n{str(e)}",
            border_style="red"
        ))
        console.print()
        sys.exit(1)

@app.command()
def version():
    """Show version information."""
    from bot import __version__
    console.print(f"\n[cyan]Trading Bot v{__version__}[/cyan]\n")

if __name__ == "__main__":
    app()