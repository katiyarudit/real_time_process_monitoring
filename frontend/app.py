import streamlit as st
import requests
import pandas as pd
import plotly.express as px
from utils import get_data
from styles import set_page_config

set_page_config()

with open("styles.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

st.markdown(
    """
    <div class='header'>
        <h1>🚀 Real-Time Process Monitoring Dashboard</h1>
    </div>
    """,
    unsafe_allow_html=True
)

st.sidebar.markdown("<h2>🔧 Control Panel</h2>", unsafe_allow_html=True)
if st.sidebar.button("Refresh Data"):
    st.rerun()

theme = st.sidebar.radio("Select Theme:", ["🌙 Dark Mode", "☀️ Light Mode"])
theme_class = "dark-mode" if theme == "🌙 Dark Mode" else "light-mode"

cpu = get_data("cpu")["cpu"]
memory = get_data("memory")["memory"]
processes = get_data("processes")

st.markdown(f"<div class='{theme_class}'>", unsafe_allow_html=True)
col1, col2 = st.columns(2)
col1.metric(label="🔥 CPU Usage", value=f"{cpu}%")
col2.metric(label="💾 Memory Usage", value=f"{memory}%")

df = pd.DataFrame(processes).sort_values(by="cpu_percent", ascending=False)

tab1, tab2, tab3, tab4, tab5 = st.tabs(["📊 Process Analysis", "📈 CPU History", "⚙️ Memory Trends", "📌 Summary", "👨‍👩‍👧‍👦 About Us"])

# **Tab 1: Process Resource Usage**
with tab1:
    st.subheader("📊 Process Resource Usage")
    fig = px.bar(df, x="name", y=["cpu_percent", "memory_percent"], title="CPU & Memory Usage",
                 color_discrete_sequence=["#1e88e5", "#ff4081"], height=500)
    fig.update_traces(marker=dict(line=dict(width=2)))  # **Increased Bar Size**
    st.plotly_chart(fig, use_container_width=True)

    # **Running Processes Table**
    st.subheader("📋 Running Processes")
    st.dataframe(df[["pid", "name", "cpu_percent", "memory_percent"]].rename(columns={
        "pid": "Process ID", "name": "Process Name", "cpu_percent": "CPU Usage (%)", "memory_percent": "Memory Usage (%)"
    }))

# **Tab 2: CPU History**
with tab2:
    st.subheader("📈 CPU Usage Over Time")
    history_df = pd.DataFrame({"time": range(1, 21), "cpu_usage": [cpu + i for i in range(20)]})
    fig2 = px.line(history_df, x="time", y="cpu_usage", title="CPU Usage Trend",
                   line_shape="spline", markers=True, color_discrete_sequence=["#1e88e5"])
    st.plotly_chart(fig2, use_container_width=True)

# **Tab 3: Memory Trends**
with tab3:
    st.subheader("⚙️ Memory Usage Trend")
    memory_df = pd.DataFrame({"time": range(1, 21), "memory_usage": [memory - i for i in range(20)]})
    fig3 = px.area(memory_df, x="time", y="memory_usage", title="Memory Consumption Trend",
                   color_discrete_sequence=["#ff4081"])
    st.plotly_chart(fig3, use_container_width=True)

# **Tab 4: Summary**
with tab4:
    st.subheader("📌 System Summary")
    avg_cpu = df["cpu_percent"].mean()
    avg_memory = df["memory_percent"].mean()
    st.markdown(f"✅ **Average CPU Usage:** {avg_cpu:.2f}%")
    st.markdown(f"✅ **Average Memory Usage:** {avg_memory:.2f}%")
    st.markdown(f"🔍 **Highest CPU Consuming Process:** {df.iloc[0]['name']} ({df.iloc[0]['cpu_percent']}%)")
    st.markdown(f"🔍 **Highest Memory Consuming Process:** {df.iloc[0]['name']} ({df.iloc[0]['memory_percent']}%)")

# **Tab 5: About Us**
with tab5:
    st.subheader("👨‍👩‍👧‍👦 Meet the Team")
    
    friends = [
        {"name": "Shubham", "role": "Full Stack Developer", "bio": "Passionate about backend systems."},
        {"name": "Arshia", "role": "UI/UX Designer", "bio": "Loves creating beautiful user experiences."},
        {"name": "Udit Katiyar", "role": "Project Lead", "bio": "Specialist in real-time monitoring and AI."}
    ]
    
    for friend in friends:
        st.markdown(f"""
        <div class='team-member'>
            <h3>{friend['name']}</h3>
            <p><strong>Role:</strong> {friend['role']}</p>
            <p><em>{friend['bio']}</em></p>
        </div>
        <hr>
        """, unsafe_allow_html=True)

# **Footer**
st.markdown(
    """
    <div class='footer'>
        <h4>👨‍💻 About Me: Udit Katiyar</h4>
        <p>Passionate about building real-time monitoring systems & AI solutions.</p>
    </div>
    """,
    unsafe_allow_html=True
)
