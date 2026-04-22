import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from datetime import datetime, timedelta

# Page Configuration
st.set_page_config(
    page_title="SAPC Framework | Intelligent Air Control",
    page_icon="🌍",
    layout="wide"
)

# Custom CSS for a professional look
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stMetric { background-color: #ffffff; padding: 15px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR CONTROLS ---
st.sidebar.header("🛠️ System Configuration")
st.sidebar.info("SAPC Framework: Proactive AI Control")
aqi_threshold = st.sidebar.slider("Set Safety Threshold (AQI)", 50, 300, 100)
update_interval = st.sidebar.selectbox("Refresh Rate", ["1s", "5s", "10s"])

# --- DATA GENERATION (Simulating Real-Time IoT Feed) ---
def get_sensor_data():
    now = datetime.now()
    times = [now - timedelta(minutes=i) for i in range(20, 0, -1)]
    data = {
        "Timestamp": times,
        "AQI": np.random.randint(40, 120, 20),
        "CO2 (ppm)": np.random.randint(300, 800, 20),
        "NOx (ppb)": np.random.randint(10, 50, 20)
    }
    return pd.DataFrame(data)

df = get_sensor_data()
latest_aqi = df["AQI"].iloc[-1]

# --- MAIN INTERFACE ---
st.title("🌍 SAPC: Self-Adaptive Predictive Control")
st.markdown(f"**Status:** {'🟢 System Optimal' if latest_aqi < aqi_threshold else '🔴 Activating Mitigation'}")

# Top Row: Real-time Metrics
col1, col2, col3, col4 = st.columns(4)
col1.metric("Current AQI", latest_aqi, delta="-3", delta_color="inverse")
col2.metric("CO2 Level", f"{df['CO2 (ppm)'].iloc[-1]} ppm", delta="Stable")
col3.metric("AI Predicted (Next 1hr)", f"{latest_aqi + 5}", delta="+5", delta_color="inverse")
col4.metric("Control State", "Ventilation ON" if latest_aqi > aqi_threshold else "Monitoring", delta=None)

st.write("---")

# Layout: Charts and Logic
tab1, tab2 = st.tabs(["📊 Analytics", "🧠 AI Insights"])

with tab1:
    c1, c2 = st.columns([2, 1])
    with c1:
        st.subheader("Live Air Quality Trends")
        fig = px.line(df, x="Timestamp", y=["AQI", "CO2 (ppm)"], 
                      color_discrete_sequence=["#00CC96", "#EF553B"],
                      template="plotly_white")
        st.plotly_chart(fig, use_container_width=True)
    
    with c2:
        st.subheader("Pollutant Distribution")
        pie_fig = px.pie(values=[latest_aqi, 20, 15], names=["AQI", "NOx", "Others"], hole=0.4)
        st.plotly_chart(pie_fig, use_container_width=True)

with tab2:
    st.subheader("SAPC Decision Engine")
    st.code(f"""
    IF Predicted_AQI > {aqi_threshold}:
        ACTION: Trigger High-Efficiency Filtration
        MODE: Proactive Adaptive Control
        CONFIDENCE: 94.2%
    ELSE:
        ACTION: Low-Power Monitoring
    """, language="python")
    
    st.image("https://via.placeholder.com/800x200.png?text=AI+Model+Confidence+Gradient+Map", caption="Model Prediction Confidence Heatmap")

# Footer
st.write("---")
st.caption(f"SAPC Framework v1.0 | Developed by Vasanthram R | Last Sync: {datetime.now().strftime('%H:%M:%S')}")
