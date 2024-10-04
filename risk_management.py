from config import MAX_DAILY_LOSS

def apply_risk_management(data, position, entry_price, current_price, daily_pnl):
    """Apply risk management rules."""
    
    # Stop loss: 2 * ATR
    stop_loss = entry_price - (2 * data['ATR'].iloc[-1])
    
    # Take profit: 3 * ATR
    take_profit = entry_price + (3 * data['ATR'].iloc[-1])
    
    # Check for stop loss or take profit
    if current_price <= stop_loss or current_price >= take_profit:
        return -position  # Close the position
    
    # Check daily loss limit
    if daily_pnl <= -MAX_DAILY_LOSS:
        return -position  # Close all positions if daily loss limit is reached
    
    return 0  # No action needed
