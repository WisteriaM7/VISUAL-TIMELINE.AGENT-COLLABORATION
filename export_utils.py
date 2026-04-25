import os
import tempfile
from datetime import datetime


def export_pdf(logs: list) -> str:
    """
    Export agent logs as a formatted PDF.
    Returns the path to the generated PDF file.
    Requires: fpdf2  (pip install fpdf2)
    """
    try:
        from fpdf import FPDF
    except ImportError:
        raise ImportError("fpdf2 is required for PDF export. Run: pip install fpdf2")

    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    # Title
    pdf.set_font("Helvetica", "B", 18)
    pdf.cell(0, 12, "Agent Collaboration Timeline", ln=True, align="C")
    pdf.set_font("Helvetica", "", 10)
    pdf.cell(0, 8, f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", ln=True, align="C")
    pdf.ln(6)

    if logs:
        pdf.set_font("Helvetica", "B", 11)
        pdf.cell(0, 8, f"Topic: {logs[0]['topic']}", ln=True)
        pdf.ln(4)

    for entry in logs:
        # Agent header
        pdf.set_font("Helvetica", "B", 12)
        header = f"{entry['icon']} {entry['agent']}  |  {entry['date_display']} {entry['timestamp_display']}  |  {entry['duration_sec']}s"
        pdf.cell(0, 9, header, ln=True)

        # Output text
        pdf.set_font("Helvetica", "", 10)
        # Clean up non-latin characters for basic FPDF compatibility
        safe_output = entry["output"].encode("latin-1", errors="replace").decode("latin-1")
        pdf.multi_cell(0, 6, safe_output)
        pdf.ln(4)
        pdf.line(10, pdf.get_y(), 200, pdf.get_y())
        pdf.ln(4)

    # Stats summary
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 14)
    pdf.cell(0, 10, "Session Statistics", ln=True)
    pdf.set_font("Helvetica", "", 11)
    total_time = sum(e["duration_sec"] for e in logs)
    pdf.cell(0, 8, f"Total Agents: {len(set(e['agent'] for e in logs))}", ln=True)
    pdf.cell(0, 8, f"Total Interactions: {len(logs)}", ln=True)
    pdf.cell(0, 8, f"Total Duration: {total_time:.1f}s", ln=True)

    out_path = os.path.join(tempfile.gettempdir(), "agent_timeline.pdf")
    pdf.output(out_path)
    return out_path


def export_png(logs: list) -> str:
    """
    Export a timeline chart as PNG using matplotlib.
    Returns path to the generated PNG file.
    Requires: matplotlib (pip install matplotlib)
    """
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        import matplotlib.patches as mpatches
        from datetime import datetime as dt
    except ImportError:
        raise ImportError("matplotlib is required for PNG export. Run: pip install matplotlib")

    fig, axes = plt.subplots(2, 1, figsize=(14, 10))
    fig.suptitle("Agent Collaboration Timeline", fontsize=16, fontweight="bold")

    # --- Chart 1: Gantt bar chart ---
    ax = axes[0]
    base = dt.fromisoformat(logs[0]["timestamp"])
    colors = [e["color"] for e in logs]
    agents = [f"{e['icon']} {e['agent']}" for e in logs]
    offsets = [(dt.fromisoformat(e["timestamp"]) - base).total_seconds() for e in logs]
    durations = [e["duration_sec"] for e in logs]

    y_pos = range(len(logs))
    bars = ax.barh(y_pos, durations, left=offsets, color=colors, edgecolor="white", height=0.5)
    ax.set_yticks(list(y_pos))
    ax.set_yticklabels(agents, fontsize=10)
    ax.set_xlabel("Elapsed Time (seconds)")
    ax.set_title("Execution Timeline")
    ax.invert_yaxis()

    for bar, entry in zip(bars, logs):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_y() + bar.get_height() / 2,
            f"{entry['duration_sec']}s",
            va="center", ha="center", color="white", fontsize=9, fontweight="bold"
        )

    # --- Chart 2: Output length bar chart ---
    ax2 = axes[1]
    lengths = [len(e["output"]) for e in logs]
    bars2 = ax2.bar(agents, lengths, color=colors, edgecolor="white")
    ax2.set_ylabel("Output Length (characters)")
    ax2.set_title("Output Size per Agent")
    ax2.tick_params(axis="x", rotation=15)

    for bar, length in zip(bars2, lengths):
        ax2.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + 5,
            str(length),
            ha="center", va="bottom", fontsize=9
        )

    plt.tight_layout(rect=[0, 0, 1, 0.95])

    out_path = os.path.join(tempfile.gettempdir(), "agent_timeline.png")
    plt.savefig(out_path, dpi=150, bbox_inches="tight")
    plt.close()
    return out_path
