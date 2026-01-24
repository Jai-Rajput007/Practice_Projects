class PaymentProcessor:
    """Handles payment processing using coins."""
    
    COINS = {
        "penny": 0.01,
        "dime": 0.10,
        "nickel": 0.05,
        "quarter": 0.25
    }
    
    @staticmethod
    def get_coin_value(coin_name: str) -> float:
        """Get the value of a coin."""
        return PaymentProcessor.COINS.get(coin_name.lower(), 0.0)
    
    @staticmethod
    def display_coin_options():
        """Display available coins for payment."""
        print("\nYou can pay with:")
        for coin, value in PaymentProcessor.COINS.items():
            print(f"  {coin.capitalize()} (${value:.2f})")
    
    @staticmethod
    def process_payment(required_amount: float) -> bool:
        """Process coin-based payment."""
        PaymentProcessor.display_coin_options()
        
        try:
            pennies = int(input("How many pennies?   → ") or 0)
            dimes = int(input("How many dimes?     → ") or 0)
            nickels = int(input("How many nickels?   → ") or 0)
            quarters = int(input("How many quarters?  → ") or 0)
        except ValueError:
            print("Invalid input — payment cancelled.")
            return False
        
        total_paid = (
            pennies * 0.01 +
            dimes * 0.10 +
            nickels * 0.05 +
            quarters * 0.25
        )
        
        if total_paid < required_amount:
            shortfall = required_amount - total_paid
            print(f"\nYou paid ${total_paid:.2f} — ${shortfall:.2f} short.")
            print("Payment rejected.")
            return False
        
        if total_paid > required_amount:
            change = total_paid - required_amount
            print(f"\nHere is your change: ${change:.2f}")
        
        print("Payment accepted!")
        return True
