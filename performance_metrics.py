import numpy as np
import pandas as pd

def calculate_performance_metrics(trades, equity_curve):
    """Calculate various performance metrics."""
    initial_capital = equity_curve[0]
    final_capital = equity_curve[-1]
    
    total_return = (final_capital - initial_capital) / initial_capital if initial_capital != 0 else 0
    
    # Calculate Sharpe ratio only if there's variation in equity curve
    equity_returns = np.diff(equity_curve)
    if len(equity_returns) > 1 and np.std(equity_returns) != 0:
        sharpe_ratio = np.sqrt(252) * np.mean(equity_returns) / np.std(equity_returns)
    else:
        sharpe_ratio = 0
    
    trades_df = pd.DataFrame(trades, columns=['Timestamp', 'Action', 'Price', 'Shares', 'Capital'])
    trades_df['PnL'] = trades_df['Capital'].diff()
    
    winning_trades = trades_df[trades_df['PnL'] > 0]
    losing_trades = trades_df[trades_df['PnL'] < 0]
    
    win_rate = len(winning_trades) / len(trades_df) if len(trades_df) > 0 else 0
    average_win = winning_trades['PnL'].mean() if len(winning_trades) > 0 else 0
    average_loss = abs(losing_trades['PnL'].mean()) if len(losing_trades) > 0 else 0
    profit_factor = average_win / average_loss if average_loss != 0 else 0
    
    # Calculate max drawdown
    peak = equity_curve[0]
    max_drawdown = 0
    for value in equity_curve[1:]:
        if value > peak:
            peak = value
        drawdown = (peak - value) / peak
        if drawdown > max_drawdown:
            max_drawdown = drawdown
    
    return {
        'Total Return': total_return,
        'Sharpe Ratio': sharpe_ratio,
        'Win Rate': win_rate,
        'Profit Factor': profit_factor,
        'Max Drawdown': max_drawdown
    }
