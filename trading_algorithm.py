from data_fetcher import get_intraday_data
from strategy import trading_strategy
from backtester import backtest
from performance_metrics import calculate_performance_metrics
from visualizer import plot_results
from config import TICKERS, INITIAL_CAPITAL
import pandas as pd
import numpy as np

def optimize_portfolio(returns):
    """Simple portfolio optimization using equal-weight strategy."""
    return np.ones(len(returns.columns)) / len(returns.columns)

def run_trading_algorithm():
    """Run the trading algorithm for all tickers."""
    all_data = {}
    all_trades = {}
    all_equity_curves = {}
    
    # Fetch data and run backtests for each ticker
    for ticker in TICKERS:
        print(f"Running algorithm for {ticker}")
        
        # Fetch and prepare data
        data = get_intraday_data(ticker)
        data = trading_strategy(data)
        
        # Perform backtesting
        trades, equity_curve = backtest(data, INITIAL_CAPITAL / len(TICKERS))
        
        all_data[ticker] = data
        all_trades[ticker] = trades
        all_equity_curves[ticker] = pd.Series(equity_curve, index=data.index[:len(equity_curve)])
    
    # Combine all data
    combined_data = pd.concat(all_data.values())
    combined_data = combined_data.sort_index()
    
    # Resample and interpolate equity curves to match combined data index
    resampled_equity_curves = {}
    for ticker, equity_curve in all_equity_curves.items():
        resampled = equity_curve.reindex(combined_data.index)
        resampled_equity_curves[ticker] = resampled.interpolate()
    
    # Calculate returns for portfolio optimization
    returns = pd.DataFrame({ticker: curve.pct_change().dropna() for ticker, curve in resampled_equity_curves.items()})
    
    # Optimize portfolio
    weights = optimize_portfolio(returns)
    
    # Calculate combined equity curve
    combined_equity_curve = pd.DataFrame(resampled_equity_curves).dot(weights)
    
    # Calculate combined trades
    combined_trades = pd.concat(all_trades.values())
    combined_trades = combined_trades.sort_values('Timestamp').reset_index(drop=True)
    
    # Calculate performance metrics for the portfolio
    metrics = calculate_performance_metrics(combined_trades, combined_equity_curve.values)
    
    # Print results
    print(f"Performance metrics for the portfolio:")
    for metric, value in metrics.items():
        print(f"{metric}: {value:.2f}")
    
    # Visualize results
    plot_results(combined_data, combined_trades, combined_equity_curve.values)
    
    print("\n" + "="*50 + "\n")

    return metrics, combined_equity_curve.values
