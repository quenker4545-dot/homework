import pandas as pd
import streamlit as st

# URL of raw CSV file in your GitHub repo
CSV_URL = "https://raw.githubusercontent.com/quenker4545-dot/homework/refs/heads/master/dht22_data.csv"

st.title("🌡️ DHT22 Monitor")

df = pd.read_csv(CSV_URL, header=None, names=["timestamp", "temperature", "humidity"], parse_dates=["timestamp"])


st.subheader("Latest Reading")
latest = df.iloc[-1]
st.metric("Temperature (°C)", f"{latest['temperature']:.1f}")
st.metric("Humidity (%)", f"{latest['humidity']:.1f}")

st.subheader("Trend Over Time")
st.line_chart(df.set_index("timestamp")[["temperature", "humidity"]])
