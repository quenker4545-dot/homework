import pandas as pd
import streamlit as st
import time

# URL of raw CSV file in your GitHub repo
CSV_URL = "https://raw.githubusercontent.com/quenker4545-dot/homework/refs/heads/master/dht22_data.csv"

st.set_page_config(page_title="🌡️ DHT22 Live Monitor", layout="wide")

st.title("🌡️ DHT22 Live Temperature & Humidity Monitor")

# Sidebar settings
refresh_rate = st.sidebar.slider("Refresh every (seconds):", 1, 30, 5)
zoom_window = st.sidebar.slider("Show last N readings:", 10, 500, 100, step=10)

placeholder = st.empty()

# Live update loop
while True:
    try:
        # Read CSV (handle header properly)
        df = pd.read_csv(CSV_URL, header=0, names=["timestamp", "temperature", "humidity"], parse_dates=["timestamp"])

        if df.empty:
            st.warning("No data available yet.")
            time.sleep(refresh_rate)
            continue

        # Show only the latest N readings for zoomed-in view
        df_zoomed = df.tail(zoom_window)

        with placeholder.container():
            st.subheader(f"📅 Last Updated: {df_zoomed['timestamp'].iloc[-1]}")
            col1, col2 = st.columns(2)
            col1.metric("🌡️ Temperature (°C)", f"{df_zoomed['temperature'].iloc[-1]:.1f}")
            col2.metric("💧 Humidity (%)", f"{df_zoomed['humidity'].iloc[-1]:.1f}")

            st.line_chart(
                df_zoomed.set_index("timestamp")[["temperature", "humidity"]],
                use_container_width=True,
                height=400
            )

            st.caption(f"Showing last {zoom_window} readings. Auto-refreshing every {refresh_rate} seconds.")
        
        time.sleep(refresh_rate)

    except Exception as e:
        st.error(f"Error loading data: {e}")
        time.sleep(refresh_rate)
