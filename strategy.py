import numpy as np
from config import POSITION_SIZE
from ml_predictor import add_ml_predictions

def trading_strategy(data):
    """Implement the trading strategy."""
    data = add_ml_predictions(data)  # Add ML predictions to our dataset
    data['Signal'] = 0  # Initialize signal column

    # Calculate additional indicators
    data['SMA50'] = data['Close'].rolling(window=50).mean()
    data['Volatility'] = data['Close'].rolling(window=20).std()
    data['ATR'] = data['Volatility']  # Use volatility as a proxy for ATR
    data['Volume_MA'] = data['Volume'].rolling(window=20).mean()

    # Buy signal
    buy_condition = (
        (data['ML_Prediction'] > data['Close'] * 1.001) &  # ML predicts at least 0.1% price increase
        (data['RSI'] < 70) &  # RSI not overbought
        (data['Close'] > data['SMA50'] * 0.98)  # Price close to or above long-term average
    )
    data.loc[buy_condition, 'Signal'] = 1

    # Sell signal
    sell_condition = (
        (data['ML_Prediction'] < data['Close'] * 0.999) &  # ML predicts at least 0.1% price decrease
        (data['RSI'] > 30) &  # RSI not oversold
        (data['Close'] < data['SMA50'] * 1.02)  # Price close to or below long-term average
    )
    data.loc[sell_condition, 'Signal'] = -1

    # Implement trailing stop-loss
    data['TrailingStop'] = 0.0
    in_position = False
    entry_price = 0.0
    trailing_stop = 0.0

    for i in range(1, len(data)):
        if data['Signal'].iloc[i] == 1 and not in_position:
            in_position = True
            entry_price = data['Close'].iloc[i]
            trailing_stop = entry_price - 1.5 * data['ATR'].iloc[i]
        elif in_position:
            trailing_stop = max(trailing_stop, data['Close'].iloc[i] - 1.5 * data['ATR'].iloc[i])
            if data['Close'].iloc[i] <= trailing_stop:
                data.loc[data.index[i], 'Signal'] = -1
                in_position = False
            data.loc[data.index[i], 'TrailingStop'] = trailing_stop

    # Print debug information
    print(f"Total data points: {len(data)}")
    print(f"Buy signals: {len(data[data['Signal'] == 1])}")
    print(f"Sell signals: {len(data[data['Signal'] == -1])}")
    
    # Print the first few rows where we have a signal
    print("\nFirst few buy signals:")
    print(data[data['Signal'] == 1].head())
    print("\nFirst few sell signals:")
    print(data[data['Signal'] == -1].head())

    return data

def calculate_position_size(capital, price, volatility):
    """Calculate position size based on volatility and ensure a minimum position."""
    risk_per_trade = capital * POSITION_SIZE
    shares = max(1, int(risk_per_trade / (1.5 * volatility)))  # Ensure at least 1 share
    max_shares = int(capital * POSITION_SIZE / price)
    return min(shares, max_shares)  # Respect the maximum position size
