import streamlit as st
import json
import time
from datetime import datetime
from agents import run_agents
from timeline import render_timeline
from export_utils import export_pdf, export_png

st.set_page_config(page_title="Agent Collaboration Timeline", layout="wide")

st.title("🤖 Visual Timeline of Agent Collaboration")
st.markdown("Run multiple AI agents and visualize their collaboration over time.")

# Sidebar controls
with st.sidebar:
    st.header("⚙️ Configuration")
    model = st.selectbox("Ollama Model", ["llama3.2", "mistral", "phi3", "gemma2"])
    topic = st.text_input("Topic / Task", value="Explain the impact of AI on healthcare")
    agents_config = st.multiselect(
        "Select Agents",
        ["Researcher", "Analyst", "Critic", "Summarizer"],
        default=["Researcher", "Analyst", "Summarizer"]
    )
    run_btn = st.button("▶ Run Agents", type="primary", use_container_width=True)

    st.markdown("---")
    st.header("📤 Export")
    col1, col2 = st.columns(2)
    with col1:
        pdf_btn = st.button("Export PDF", use_container_width=True)
    with col2:
        png_btn = st.button("Export PNG", use_container_width=True)

# Session state for logs
if "agent_logs" not in st.session_state:
    st.session_state.agent_logs = []

if run_btn:
    if not agents_config:
        st.error("Please select at least one agent.")
    else:
        st.session_state.agent_logs = []
        with st.spinner("Running agents..."):
            logs = run_agents(topic, agents_config, model)
            st.session_state.agent_logs = logs

# Render timeline
if st.session_state.agent_logs:
    render_timeline(st.session_state.agent_logs)

    # Export buttons
    if pdf_btn:
        pdf_path = export_pdf(st.session_state.agent_logs)
        with open(pdf_path, "rb") as f:
            st.sidebar.download_button(
                "⬇ Download PDF", f, file_name="agent_timeline.pdf", mime="application/pdf"
            )

    if png_btn:
        png_path = export_png(st.session_state.agent_logs)
        with open(png_path, "rb") as f:
            st.sidebar.download_button(
                "⬇ Download PNG", f, file_name="agent_timeline.png", mime="image/png"
            )

    # Raw JSON log viewer
    with st.expander("📋 Raw Agent Logs (JSON)"):
        st.json(st.session_state.agent_logs)
else:
    st.info("Configure agents in the sidebar and click **▶ Run Agents** to get started.")
