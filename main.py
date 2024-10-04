import sys
from trading_algorithm import run_trading_algorithm
from config import INITIAL_CAPITAL

def run_algorithm():
    metrics, final_equity_curve = run_trading_algorithm()
    
    # Calculate and print the total return
    total_return = (final_equity_curve[-1] - INITIAL_CAPITAL) / INITIAL_CAPITAL * 100
    print(f"Total portfolio return: {total_return:.2f}%")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--gui":
        from gui import run_gui
        run_gui()
    else:
        run_algorithm()
