import streamlit as st
import pandas as pd
import requests
from datetime import datetime
import plotly.express as px
from prophet import Prophet
st.set_page_config(page_title="Weather Forecast Station", layout="wide")
# ----------------------------------------
# CONFIG
# ----------------------------------------
LOCAL_CSV = "dht22_data.csv"  # Your Pi sensor data
API_KEY = "f89a93ee0f3f4e01bb5142407250510"  # 🔑 Replace this
CITIES = ["Taoyuan", "Taipei", "Tokyo", "New York", "Kaohsiung"]

st.set_page_config(page_title="🌦️ Smart Weather Station", layout="wide")
st.title("🌦️ Smart Weather Station Dashboard (WeatherAPI)")

# Sidebar
location = st.sidebar.selectbox("Select location", ["Local Pi"] + CITIES)
forecast_days = st.sidebar.slider("Forecast horizon (days)", 7, 365, 30)
zoom_window = st.sidebar.slider("Show last N readings", 10, 500, 100, step=10)

# ----------------------------------------
# HELPERS
# ----------------------------------------

def load_local_data():
    """Load DHT22 CSV data"""
    try:
        df = pd.read_csv(LOCAL_CSV, parse_dates=["timestamp"])
        df = df.tail(zoom_window)
        return df
    except Exception as e:
        st.warning(f"Could not load local data: {e}")
        return pd.DataFrame(columns=["timestamp", "temperature", "humidity"])

def fetch_weatherapi_city(city):
    """Fetch current weather data from WeatherAPI"""
    url = f"http://api.weatherapi.com/v1/current.json?key={API_KEY}&q={city}&aqi=no"
    try:
        r = requests.get(url).json()
        data = {
            "timestamp": datetime.now(),
            "temperature": r["current"]["temp_c"],
            "humidity": r["current"]["humidity"]
        }
        return pd.DataFrame([data])
    except Exception as e:
        st.error(f"Error fetching data for {city}: {e}")
        return pd.DataFrame(columns=["timestamp", "temperature", "humidity"])

def create_forecast(df, column="temperature", periods=365):
    """Forecast with Prophet"""
    if df.empty:
        return pd.DataFrame(columns=["ds", "yhat"])
    forecast_df = df[["timestamp", column]].rename(columns={"timestamp": "ds", column: "y"})
    model = Prophet(yearly_seasonality=True, daily_seasonality=False)
    model.fit(forecast_df)
    future = model.make_future_dataframe(periods=periods)
    forecast = model.predict(future)
    return forecast[["ds", "yhat"]]

# ----------------------------------------
# MAIN APP
# ----------------------------------------

if location == "Local Pi":
    df = load_local_data()
else:
    df = fetch_weatherapi_city(location)

# 1️⃣ LATEST METRICS
st.subheader("📊 Latest Reading")
if not df.empty:
    latest = df.iloc[-1]
    col1, col2 = st.columns(2)
    col1.metric("🌡️ Temperature (°C)", f"{latest['temperature']:.1f}")
    col2.metric("💧 Humidity (%)", f"{latest['humidity']:.1f}")
else:
    st.warning("No data available for this location yet.")

# 2️⃣ HISTORICAL CHART
if location == "Local Pi" and not df.empty:
    st.subheader("📈 Historical Data")
    fig = px.line(df, x="timestamp", y=["temperature", "humidity"], labels={"value": "Value", "timestamp": "Time"})
    st.plotly_chart(fig, use_container_width=True)

# 3️⃣ FORECAST SECTION
st.subheader(f"🔮 Forecast for Next {forecast_days} Days")
if not df.empty:
    forecast_temp = create_forecast(df, "temperature", forecast_days)
    forecast_hum = create_forecast(df, "humidity", forecast_days)
    
    fig_temp = px.line(forecast_temp, x="ds", y="yhat", labels={"ds": "Date", "yhat": "Temperature (°C)"}, title="Temperature Forecast")
    st.plotly_chart(fig_temp, use_container_width=True)
    
    fig_hum = px.line(forecast_hum, x="ds", y="yhat", labels={"ds": "Date", "yhat": "Humidity (%)"}, title="Humidity Forecast")
    st.plotly_chart(fig_hum, use_container_width=True)

st.caption("🔁 Refresh the page periodically to fetch updated WeatherAPI data. Local Pi data updates continuously from your sensor.")
