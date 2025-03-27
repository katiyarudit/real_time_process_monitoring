import streamlit as st
import pandas as pd
import plotly.express as px
from utils import get_data
from styles import set_page_config

# Set Page Configuration
set_page_config()

# Sidebar Controls
st.sidebar.title("🔧 Control Panel")
if st.sidebar.button("🔄 Refresh Data"):
    st.rerun()  # Ensures smooth refresh

# Main Dashboard Title
st.title("🚀 Real-Time Process Monitoring Dashboard")

# Fetch Data from Backend
cpu_data = get_data("cpu")
memory_data = get_data("memory")
processes_data = get_data("processes")

# Handle Missing Data Gracefully
cpu = cpu_data.get("cpu", 0)
memory = memory_data.get("memory", 0)
processes = processes_data if isinstance(processes_data, list) else []

# Display Metrics
col1, col2 = st.columns(2)
col1.metric(label="🔥 CPU Usage", value=f"{cpu}%", delta=cpu - 50)
col2.metric(label="💾 Memory Usage", value=f"{memory}%", delta=memory - 50)

# Convert Process Data to DataFrame
if processes:
    df = pd.DataFrame(processes)
    df = df.sort_values(by="cpu_percent", ascending=False)

    # Visualization: CPU & Memory Usage per Process
    st.subheader("📊 CPU & Memory Analysis")
    fig = px.bar(df, x="name", y=["cpu_percent", "memory_percent"], title="Process Resource Usage")
    st.plotly_chart(fig, use_container_width=True)

    # Display Process Data
    st.subheader("📌 Running Processes")
    st.dataframe(df, use_container_width=True)
else:
    st.warning("⚠️ No process data available.")
