# Day Trading Algorithm

## Overview
This day trading algorithm is designed to generate profits through high-frequency trading using technical analysis and machine learning predictions. It supports multiple assets, portfolio optimization, and includes a simple GUI for easier interaction and monitoring.

## Requirements
- Python 3.7+
- yfinance
- pandas
- numpy
- scikit-learn
- matplotlib
- streamlit

## Installation
1. Clone the repository
2. Install the required packages:
   ```
   pip install yfinance pandas numpy scikit-learn matplotlib streamlit
   ```

## Configuration
You can configure the algorithm by modifying the `config.py` file. The main parameters include:
- Tickers: List of stock symbols to trade
- Initial capital: Starting amount for trading
- Time period and interval: Data fetching parameters
- Profit target and maximum daily loss: Risk management settings
- Position size: Maximum position size as a fraction of capital per asset

## Usage
To run the algorithm without GUI:
```
python main.py
```

To run the algorithm with GUI:
```
python main.py --gui
```

## Components
1. Data fetching: Uses yfinance to fetch intraday data
2. Trading strategy: Combines technical indicators and machine learning predictions
3. Machine learning predictions: Uses RandomForestRegressor for price predictions
4. Backtesting: Simulates trading based on historical data
5. Performance metrics: Calculates various metrics like Sharpe ratio, win rate, etc.
6. Visualization: Plots equity curves and trading signals
7. GUI: Provides an interactive interface for configuring and running the algorithm

## Output
The algorithm outputs performance metrics, including total return, Sharpe ratio, win rate, profit factor, and maximum drawdown. It also generates visualizations of the equity curve and trading signals.

## Customization
You can customize the algorithm by:
1. Modifying the trading strategy in `strategy.py`
2. Adjusting risk management parameters in `config.py`
3. Implementing new technical indicators or machine learning models
4. Extending the GUI functionality in `gui.py`

## Disclaimer
This algorithmic trading system is for educational and research purposes only. It is not intended to be used as financial advice or a recommendation to trade real money. Algorithmic trading carries a high level of risk, and there is always the potential for significant financial loss. Always consult with a qualified financial advisor before making any investment decisions.
