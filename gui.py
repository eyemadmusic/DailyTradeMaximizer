import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from trading_algorithm import run_trading_algorithm
from config import TICKERS, INITIAL_CAPITAL, PERIOD, INTERVAL, PROFIT_TARGET, MAX_DAILY_LOSS, POSITION_SIZE

def run_gui():
    st.title("Day Trading Algorithm GUI")

    st.sidebar.header("Configuration")
    selected_tickers = st.sidebar.multiselect("Select Tickers", TICKERS, default=TICKERS)
    initial_capital = st.sidebar.number_input("Initial Capital", value=INITIAL_CAPITAL, step=1000)
    period = st.sidebar.text_input("Time Period", value=PERIOD)
    interval = st.sidebar.text_input("Time Interval", value=INTERVAL)
    profit_target = st.sidebar.number_input("Profit Target", value=PROFIT_TARGET, step=10)
    max_daily_loss = st.sidebar.number_input("Max Daily Loss", value=MAX_DAILY_LOSS, step=10)
    position_size = st.sidebar.slider("Position Size", min_value=0.01, max_value=0.1, value=POSITION_SIZE, step=0.01)

    if st.sidebar.button("Run Algorithm"):
        with st.spinner("Running trading algorithm..."):
            metrics, equity_curve = run_trading_algorithm()

        st.header("Performance Metrics")
        for metric, value in metrics.items():
            st.metric(metric, f"{value:.2f}")

        st.header("Equity Curve")
        fig, ax = plt.subplots()
        ax.plot(equity_curve)
        ax.set_title("Equity Curve")
        ax.set_xlabel("Time")
        ax.set_ylabel("Portfolio Value")
        st.pyplot(fig)

if __name__ == "__main__":
    run_gui()
