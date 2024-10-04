import pandas as pd
from strategy import trading_strategy, calculate_position_size
from risk_management import apply_risk_management

TRANSACTION_COST = 0.001  # 0.1% transaction cost

def backtest(data, initial_capital):
    """Perform backtesting on the given data."""
    capital = initial_capital
    position = 0
    entry_price = 0
    daily_pnl = 0
    trades = []
    equity_curve = [initial_capital]

    for i in range(1, len(data)):
        current_price = data['Close'].iloc[i]
        signal = data['Signal'].iloc[i]
        
        # Apply risk management
        risk_action = apply_risk_management(data.iloc[:i], position, entry_price, current_price, daily_pnl)
        if risk_action != 0:
            exit_price = current_price * (1 - TRANSACTION_COST)  # Account for transaction costs
            capital += position * exit_price
            trades.append((data.index[i], 'Exit (Risk)', exit_price, -position, capital))
            print(f"Risk management exit at {data.index[i]}: Price: {exit_price:.2f}, Position: {-position}, Capital: {capital:.2f}")
            position = 0
            entry_price = 0

        # Execute trading signal
        if signal == 1 and position == 0:  # Buy signal
            position_size = calculate_position_size(capital, current_price, data['Volatility'].iloc[i])
            if position_size > 0:
                position = position_size
                entry_price = current_price * (1 + TRANSACTION_COST)  # Account for transaction costs
                capital -= position * entry_price
                trades.append((data.index[i], 'Buy', entry_price, position, capital))
                print(f"Buy at {data.index[i]}: Price: {entry_price:.2f}, Position: {position}, Capital: {capital:.2f}")
        elif signal == -1 and position > 0:  # Sell signal
            exit_price = current_price * (1 - TRANSACTION_COST)  # Account for transaction costs
            capital += position * exit_price
            daily_pnl += (exit_price - entry_price) * position
            trades.append((data.index[i], 'Sell', exit_price, -position, capital))
            print(f"Sell at {data.index[i]}: Price: {exit_price:.2f}, Position: {-position}, Capital: {capital:.2f}")
            position = 0
            entry_price = 0

        # Update equity curve
        equity_curve.append(capital + (position * current_price))

        # Reset daily P&L at the end of the day
        if i < len(data) - 1 and data.index[i].date() != data.index[i+1].date():
            daily_pnl = 0

    # Close any remaining position at the end
    if position != 0:
        final_price = data['Close'].iloc[-1] * (1 - TRANSACTION_COST)
        capital += position * final_price
        trades.append((data.index[-1], 'Close', final_price, -position, capital))
        print(f"Close final position at {data.index[-1]}: Price: {final_price:.2f}, Position: {-position}, Capital: {capital:.2f}")

    print(f"Final capital: {capital:.2f}")
    print(f"Total trades: {len(trades)}")
    
    # Add more detailed debugging information
    print("\nFirst few trades:")
    for trade in trades[:5]:
        print(trade)
    
    return pd.DataFrame(trades, columns=['Timestamp', 'Action', 'Price', 'Shares', 'Capital']), equity_curve
