import pandas as pd
import streamlit as st

# GitHub raw CSV link
CSV_URL = "https://raw.githubusercontent.com/quenker4545-dot/homework/refs/heads/master/dht22_data.csv"

st.set_page_config(page_title="🌡️ DHT22 Live Monitor", layout="wide")

st.title("🌡️ DHT22 Live Temperature & Humidity Monitor")

# Sidebar settings
refresh_rate = st.sidebar.slider("Auto-refresh every (seconds):", 5, 60, 30)
zoom_window = st.sidebar.slider("Show last N readings:", 10, 500, 100, step=10)

# 🔁 Auto-refresh every N seconds
st_autorefresh = st.experimental_rerun  # old fallback if you use Streamlit < 1.33
count = st.experimental_rerun if False else None  # compatibility shim
st_autorefresh = st.autorefresh = getattr(st, "autorefresh", None)
if st_autorefresh:
    st_autorefresh(interval=refresh_rate * 1000, key="data_refresh")

# Load CSV
try:
    df = pd.read_csv(CSV_URL, header=0, names=["timestamp", "temperature", "humidity"], parse_dates=["timestamp"])
    df_zoomed = df.tail(zoom_window)
except Exception as e:
    st.error(f"Error reading CSV: {e}")
    st.stop()

# Display metrics
latest = df_zoomed.iloc[-1]
col1, col2 = st.columns(2)
col1.metric("🌡️ Temperature (°C)", f"{latest['temperature']:.1f}")
col2.metric("💧 Humidity (%)", f"{latest['humidity']:.1f}")

# Chart
st.line_chart(
    df_zoomed.set_index("timestamp")[["temperature", "humidity"]],
    use_container_width=True,
    height=400,
)

st.caption(f"Chart refreshes automatically every {refresh_rate} seconds.")
