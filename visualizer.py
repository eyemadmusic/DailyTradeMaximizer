import matplotlib.pyplot as plt
import pandas as pd

def plot_results(data, trades, equity_curve):
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10), sharex=True)
    
    # Plot price and indicators
    ax1.plot(data.index, data['Close'], label='Close Price')
    ax1.plot(data.index, data['EMA9'], label='EMA9')
    ax1.plot(data.index, data['EMA21'], label='EMA21')
    
    # Plot buy and sell signals
    buy_signals = trades[trades['Action'] == 'Buy']
    sell_signals = trades[trades['Action'] == 'Sell']
    ax1.scatter(buy_signals['Timestamp'], buy_signals['Price'], marker='^', color='g', label='Buy')
    ax1.scatter(sell_signals['Timestamp'], sell_signals['Price'], marker='v', color='r', label='Sell')
    
    ax1.set_title('Trading Signals')
    ax1.legend()
    
    # Plot equity curve
    equity_series = pd.Series(equity_curve, index=data.index[-len(equity_curve):])
    ax2.plot(equity_series.index, equity_series.values)
    ax2.set_title('Equity Curve')
    
    plt.tight_layout()
    plt.show()
