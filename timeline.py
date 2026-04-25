import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from collections import defaultdict


def render_timeline(logs: list):
    """Render the full timeline UI: chart + grouped cards."""

    st.markdown("---")
    st.subheader("📅 Agent Collaboration Timeline")

    _render_gantt_chart(logs)
    _render_cards(logs)
    _render_stats(logs)


def _render_gantt_chart(logs: list):
    """Render a Plotly horizontal bar chart showing agent timing."""
    if not logs:
        return

    fig = go.Figure()

    base_time = pd.Timestamp(logs[0]["timestamp"])

    for i, entry in enumerate(logs):
        start = pd.Timestamp(entry["timestamp"])
        duration = entry["duration_sec"]
        offset_sec = (start - base_time).total_seconds()

        fig.add_trace(go.Bar(
            name=f"{entry['icon']} {entry['agent']}",
            x=[duration],
            y=[f"{entry['icon']} {entry['agent']}"],
            orientation="h",
            base=offset_sec,
            marker_color=entry["color"],
            hovertemplate=(
                f"<b>{entry['agent']}</b><br>"
                f"Start: {entry['timestamp_display']}<br>"
                f"Duration: {duration}s<br>"
                "<extra></extra>"
            ),
        ))

    fig.update_layout(
        title="Agent Execution Timeline (seconds from start)",
        xaxis_title="Elapsed Time (seconds)",
        yaxis_title="Agent",
        barmode="overlay",
        height=300,
        showlegend=False,
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(gridcolor="rgba(200,200,200,0.3)"),
    )

    st.plotly_chart(fig, use_container_width=True)


def _render_cards(logs: list):
    """Render timeline cards grouped by agent."""
    st.subheader("🗂️ Agent Responses (Chronological)")

    # Group by topic for multi-topic support
    by_topic = defaultdict(list)
    for entry in logs:
        by_topic[entry["topic"]].append(entry)

    for topic, entries in by_topic.items():
        st.markdown(f"**📌 Topic:** `{topic}`")

        for entry in entries:
            color = entry["color"]
            icon = entry["icon"]
            agent = entry["agent"]
            ts = entry["timestamp_display"]
            date = entry["date_display"]
            duration = entry["duration_sec"]
            output = entry["output"]

            st.markdown(
                f"""
                <div style="
                    border-left: 5px solid {color};
                    padding: 12px 16px;
                    margin: 10px 0;
                    background: rgba(0,0,0,0.03);
                    border-radius: 0 8px 8px 0;
                ">
                    <div style="display:flex; justify-content:space-between; align-items:center;">
                        <span style="font-size:1.1em; font-weight:bold; color:{color};">
                            {icon} {agent}
                        </span>
                        <span style="font-size:0.8em; color:#888;">
                            🕐 {date} {ts} &nbsp;|&nbsp; ⏱ {duration}s
                        </span>
                    </div>
                    <div style="margin-top:8px; line-height:1.6;">
                        {output}
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )


def _render_stats(logs: list):
    """Render summary statistics."""
    st.subheader("📊 Session Statistics")

    total_time = sum(e["duration_sec"] for e in logs)
    num_agents = len(set(e["agent"] for e in logs))
    num_interactions = len(logs)

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total Agents", num_agents)
    c2.metric("Total Interactions", num_interactions)
    c3.metric("Total Time (s)", f"{total_time:.1f}")
    c4.metric("Avg Time / Agent (s)", f"{total_time / num_interactions:.1f}" if num_interactions else "—")

    # Per-agent breakdown table
    rows = []
    for entry in logs:
        rows.append({
            "Agent": f"{entry['icon']} {entry['agent']}",
            "Timestamp": entry["timestamp_display"],
            "Duration (s)": entry["duration_sec"],
            "Output Length (chars)": len(entry["output"]),
        })

    df = __import__("pandas").DataFrame(rows)
    st.dataframe(df, use_container_width=True, hide_index=True)
