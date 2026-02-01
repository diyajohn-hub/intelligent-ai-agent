import streamlit as st
import os
import json
import pandas as pd
from agent import IncidentResponseAgent

# --- Page Config for Terminal Vibe ---
st.set_page_config(
    page_title="SYSTEM_ERROR_LOG_V1.0",
    page_icon="💻",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- Custom CSS for Terminal Appearance ---
st.markdown("""
<style>
    .stApp {
        background-color: #0c0c0c;
        color: #00ff41;
        font-family: 'Courier New', Courier, monospace;
    }
    .terminal-box {
        background-color: #000;
        border: 1px solid #333;
        padding: 20px;
        border-radius: 5px;
        box-shadow: 0 0 10px rgba(0, 255, 65, 0.2);
        margin-bottom: 20px;
    }
    .stHeader, h1, h2, h3 {
        color: #00ff41 !important;
        font-family: 'Courier New', Courier, monospace;
    }
    .stDataFrame {
        border: 1px solid #333;
    }
    div[data-testid="stMetricValue"] {
        color: #00ff41;
    }
</style>
""", unsafe_allow_html=True)

st.title(">_ SYSTEM_ERROR_LOG_V1.0")

# Initialize agent
agent = IncidentResponseAgent()

# File Uploader
uploaded_file = st.file_uploader("UPLOAD_TELEMETRY_DATA", type=['json', 'txt', 'log'])

if uploaded_file is not None:
    try:
        # Read content
        content = uploaded_file.read().decode("utf-8")
        
        # Determine format
        try:
            telemetry_data = json.loads(content)
            st.toast("Protocol: JSON Detected", icon="ℹ️")
        except json.JSONDecodeError:
            telemetry_data = content
            st.toast("Protocol: RAW TEXT Detected", icon="ℹ️")

        with st.spinner("EXECUTING_ANALYSIS_SEQUENCE..."):
            report = agent.run_cycle(telemetry_data)

        # --- SEVERITY RANKING LOGIC ---
        # Map detected severity to a score for visualization
        severity_map = {"CRITICAL": 100, "HIGH": 75, "MEDIUM": 50, "LOW": 25}
        current_severity = report['decision']['severity']
        severity_score = severity_map.get(current_severity, 10)
        
        # --- TERMINAL DASHBOARD ---
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown('<div class="terminal-box">', unsafe_allow_html=True)
            st.subheader(">> INCIDENT_REPORT")
            st.write(f"**TYPE:** {report['incident_type']}")
            st.write(f"**ROOT CAUSE:** {report['explanation']}")
            st.write(f"**ACTION:** {report['decision']['action']}")
            
            if "evidence" in report and report["evidence"] != "N/A":
                 st.write("**EVIDENCE trace:**")
                 st.code(report["evidence"], language="bash")
            st.markdown('</div>', unsafe_allow_html=True)

        with col2:
            st.markdown('<div class="terminal-box">', unsafe_allow_html=True)
            st.subheader(">> THREAT_LEVEL")
            st.progress(severity_score / 100)
            st.metric("SEVERITY", current_severity)
            st.metric("CONFIDENCE", f"{report['confidence']*100:.1f}%")
            st.markdown('</div>', unsafe_allow_html=True)

        # Ranked List (Real Data from DB)
        st.markdown('<div class="terminal-box">', unsafe_allow_html=True)
        st.subheader(">> INCIDENT_HISTORY_RANKING")
        
        try:
            from database.db import fetch_history
            history = fetch_history()
            
            if history:
                df = pd.DataFrame(history)
                # Map severity text to numeric for charting
                sev_map = {"CRITICAL": 100, "HIGH": 75, "MEDIUM": 50, "LOW": 25, "UNKNOWN": 10}
                df["severity_score"] = df["severity"].map(sev_map).fillna(10)
                
                # Chart
                st.bar_chart(df.set_index("incident_type")["severity_score"], color="#ef4444")
                
                # Table
                st.dataframe(
                    df[["timestamp", "incident_type", "severity", "status", "action"]],
                    use_container_width=True
                )
            else:
                st.info("NO_HISTORY_FOUND")
                
        except Exception as e:
            st.error(f"DB_CONNECTION_ERROR: {e}")
            
        st.markdown('</div>', unsafe_allow_html=True)

    except Exception as e:
        st.error(f"SYSTEM_FAILURE: {e}")
else:
    st.info("WAITING_FOR_INPUT_STREAM...")
